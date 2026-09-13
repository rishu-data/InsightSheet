"""Secure accounts and server-side sessions for InsightSheet.

Security notes:
  * Passwords are never stored. Only a PBKDF2-HMAC-SHA256 digest with a random
    per-user salt is persisted, in the format
    `pbkdf2_sha256$iterations$salt_hex$digest_hex`.
  * Session tokens are random 32-byte URL-safe strings kept in a same-site,
    secure browser cookie (`SameSite=Strict`, `Secure`, scoped to `/`), not in
    localStorage. The database stores nothing but a SHA-256 hash of the token,
    so a leaked row cannot be replayed.
  * Every comparison of secrets uses `hmac.compare_digest`.
  * No raw token, password, cookie value or payment credential is ever logged;
    log messages are static and never interpolate secret material.
  * Nothing in this module touches Razorpay, the payment URL or pricing.
"""

from __future__ import annotations

import hashlib
import hmac
import logging
import secrets
from datetime import datetime, timedelta, timezone
from typing import Any

import reflex as rx
from sqlalchemy import select

from app.email_service import (
    email_is_configured,
    send_password_changed_email,
    send_password_reset_email,
    send_verification_email,
    send_welcome_email,
)
from app.models import (
    AuthAction,
    AuthToken,
    AuthTokenPurpose,
    User,
    UserSession,
)
from app.states.auth_rate_limit import (
    check_and_register_attempt,
    register_failure,
    register_success,
    throttle_message,
)

PBKDF2_ITERATIONS = 260_000
PBKDF2_ALGORITHM = "pbkdf2_sha256"
SALT_BYTES = 16
TOKEN_BYTES = 32
SESSION_DAYS = 14
SESSION_MAX_AGE = SESSION_DAYS * 24 * 60 * 60
MIN_PASSWORD_LENGTH = 8
SESSION_COOKIE_NAME = "insightsheet_session"
LEGACY_STORAGE_NAME = "insightsheet_session"

GENERIC_LOGIN_ERROR = (
    "That email and password combination doesn't match an account."
)

VERIFICATION_TOKEN_HOURS = 24

VERIFICATION_REQUIRED_ERROR = (
    "Your email address hasn't been verified yet. Use the verification link we "
    "emailed you, or send a new one below."
)
GENERIC_RESEND_NOTICE = (
    "If that address belongs to an account that still needs verifying, a new "
    "verification email is on its way. The link expires in 24 hours."
)
RESET_TOKEN_HOURS = 1

GENERIC_RESET_NOTICE = (
    "If that address belongs to an active account and email delivery is "
    "available, you'll receive a single-use password reset link. It expires in "
    "1 hour."
)
RESET_SERVICE_NOTICE = (
    "Password reset emails can't be sent right now because our email service "
    "is unavailable. Please try again later or contact support."
)
RESET_LINK_INVALID_ERROR = (
    "This password reset link is invalid, has expired, or has already been "
    "used. Request a new one to continue."
)
RESET_SUCCESS_NOTICE = (
    "Your password has been changed and every existing session was signed out. "
    "Sign in with your new password."
)
RESET_CONFIRMATION_UNSENT = (
    "Your password was changed successfully, but we could not send the "
    "confirmation email just now."
)

EMAIL_UNAVAILABLE_NOTICE = (
    "Your account was created, but we could not send the verification email "
    "just now. Please use the resend option below, or contact support if it "
    "keeps failing."
)


def hash_password(password: str) -> str:
    """Return an irreversible PBKDF2-HMAC-SHA256 digest of a password."""
    salt = secrets.token_bytes(SALT_BYTES)
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, PBKDF2_ITERATIONS
    )
    return f"{PBKDF2_ALGORITHM}${PBKDF2_ITERATIONS}${salt.hex()}${digest.hex()}"


def verify_password(password: str, stored: str) -> bool:
    """Constant-time verification of a password against a stored digest."""
    try:
        algorithm, iterations, salt_hex, digest_hex = stored.split("$", 3)
        if algorithm != PBKDF2_ALGORITHM:
            return False
        digest = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            bytes.fromhex(salt_hex),
            int(iterations),
        )
        return hmac.compare_digest(digest.hex(), digest_hex)
    except Exception:
        logging.exception("Password verification failed")
        return False


def hash_token(token: str) -> str:
    """SHA-256 hash of a session token — only this is ever persisted."""
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def normalize_email(email: str) -> str:
    return " ".join(str(email or "").strip().lower().split())


def _valid_email(email: str) -> bool:
    if not email or len(email) > 320 or " " in email:
        return False
    if email.count("@") != 1:
        return False
    local, _, domain = email.partition("@")
    return bool(local) and "." in domain and not domain.startswith(".")


def _now() -> datetime:
    return datetime.now(tz=timezone.utc)


class AuthState(rx.State):
    """Holds the signed-in identity and drives the login / sign-up forms."""

    # Browser-side session token in a secure, same-site cookie. The server
    # keeps only its SHA-256 hash; the cookie value itself is never logged.
    session_token: str = rx.Cookie(
        "",
        name=SESSION_COOKIE_NAME,
        path="/",
        max_age=SESSION_MAX_AGE,
        secure=True,
        same_site="strict",
    )

    # Read-only migration path for sessions issued before the cookie switch.
    legacy_session_token: str = rx.LocalStorage("", name=LEGACY_STORAGE_NAME)

    user_id: int = 0
    user_email: str = ""
    display_name: str = ""

    error: str = ""
    notice: str = ""
    is_busy: bool = False
    session_checked: bool = False

    # Set when correct credentials belong to an account that is not verified.
    # Only the account's own email is kept here - never a token.
    verification_required: bool = False
    pending_email: str = ""
    resend_busy: bool = False

    # "idle" | "checking" | "verified" | "invalid"
    verify_status: str = "idle"

    # Password reset UI state. "idle" | "checking" | "ready" | "invalid" | "done"
    reset_status: str = "idle"
    reset_busy: bool = False
    forgot_busy: bool = False
    reset_confirmation_sent: bool = True

    @rx.var
    def is_authenticated(self) -> bool:
        return self.user_id > 0

    @rx.var
    def account_label(self) -> str:
        return self.display_name or self.user_email

    @rx.var
    def account_initial(self) -> str:
        label = self.display_name or self.user_email
        return label[0].upper() if label else "?"

    @rx.var
    def scope_key(self) -> str:
        """Stable per-user key other states can use to separate data."""
        return f"user:{self.user_id}" if self.user_id > 0 else ""

    @rx.var
    def verify_is_checking(self) -> bool:
        return (self.verify_status == "idle") or (
            self.verify_status == "checking"
        )

    @rx.var
    def verify_succeeded(self) -> bool:
        return self.verify_status == "verified"

    @rx.var
    def reset_is_checking(self) -> bool:
        return (self.reset_status == "idle") or (
            self.reset_status == "checking"
        )

    @rx.var
    def reset_is_ready(self) -> bool:
        return self.reset_status == "ready"

    @rx.var
    def reset_is_done(self) -> bool:
        return self.reset_status == "done"

    @rx.var
    def has_error(self) -> bool:
        return bool(self.error)

    @rx.var
    def has_notice(self) -> bool:
        return bool(self.notice)

    def _clear_identity(self) -> None:
        self.user_id = 0
        self.user_email = ""
        self.display_name = ""

    def _forget_token(self) -> None:
        """Drop the browser-side token from the cookie and legacy storage."""
        self.session_token = ""
        self.legacy_session_token = ""

    @rx.event
    def clear_messages(self):
        self.error = ""
        self.notice = ""
        self.verification_required = False

    async def _issue_verification_token(self, user_id: int) -> tuple[str, int]:
        """Invalidate old verification tokens and mint a new one atomically.

        Only the SHA-256 hash of the random token is written. The plaintext
        token is returned for emailing and is never logged.
        """
        owner_id = int(user_id)
        token = secrets.token_urlsafe(TOKEN_BYTES)
        now = _now()
        async with rx.asession() as session:
            previous = (
                await session.scalars(
                    select(AuthToken).where(
                        AuthToken.user_id == owner_id,
                        AuthToken.purpose
                        == AuthTokenPurpose.EMAIL_VERIFICATION,
                        AuthToken.used_at.is_(None),
                    )
                )
            ).all()
            for stale in previous:
                stale.used_at = now
            row = AuthToken(
                user_id=owner_id,
                purpose=AuthTokenPurpose.EMAIL_VERIFICATION,
                token_hash=hash_token(token),
                expires_at=now + timedelta(hours=VERIFICATION_TOKEN_HOURS),
            )
            session.add(row)
            await session.flush()
            token_id = int(row.id)
            await session.commit()
        return (token, token_id)

    async def _send_verification_pair(
        self,
        email: str,
        display_name: str,
        user_id: int,
        include_welcome: bool,
    ) -> bool:
        """Issue a token and send the verification (plus optional welcome) mail."""
        if not email_is_configured():
            logging.error(
                "Verification email skipped: delivery is not configured"
            )
            return False
        try:
            token, token_id = await self._issue_verification_token(user_id)
        except Exception:
            logging.exception("Could not issue an email verification token")
            return False
        welcome_ok = True
        if include_welcome:
            welcome_ok = await send_welcome_email(email, display_name, user_id)
        verify_ok = await send_verification_email(
            email, token, user_id, token_id
        )
        return bool(verify_ok and welcome_ok)

    @rx.event
    async def check_session(self):
        """Resolve the stored token into the current user, if still valid."""
        await self._load_session()

    async def _load_session(self) -> None:
        """Look up the stored session token and refresh the identity vars."""
        token = str(self.session_token or "").strip()
        self.session_checked = True
        if not token:
            legacy = str(self.legacy_session_token or "").strip()
            if legacy:
                # Move a pre-existing session out of localStorage and into the
                # secure cookie without forcing the visitor to sign in again.
                self.session_token = legacy
                self.legacy_session_token = ""
                token = legacy
        if not token:
            self._clear_identity()
            return
        token_hash = hash_token(token)
        try:
            async with rx.asession() as session:
                row = (
                    await session.scalars(
                        select(UserSession).where(
                            UserSession.session_token_hash == token_hash
                        )
                    )
                ).first()
                if row is None or row.revoked_at is not None:
                    self._clear_identity()
                    self._forget_token()
                    return
                expires = row.expires_at
                if expires.tzinfo is None:
                    expires = expires.replace(tzinfo=timezone.utc)
                if expires <= _now():
                    row.revoked_at = _now()
                    await session.commit()
                    self._clear_identity()
                    self._forget_token()
                    return
                user = (
                    await session.scalars(
                        select(User).where(User.id == row.user_id)
                    )
                ).first()
                if user is None or not user.is_active:
                    self._clear_identity()
                    self._forget_token()
                    return
                row.last_seen_at = _now()
                await session.commit()
                self.user_id = int(user.id)
                self.user_email = str(user.email)
                self.display_name = str(user.display_name or "")
        except Exception:
            logging.exception("Session lookup failed")
            self._clear_identity()

    async def _start_session(self, user_id: int) -> str:
        """Create a server-side session row for a validated user id.

        Defensive by design: a missing, non-numeric or non-positive user id, or
        an id with no matching active account, never reaches an INSERT. Only the
        SHA-256 hash of the token is written; the token itself is never logged.
        """
        try:
            owner_id = int(user_id)
        except (TypeError, ValueError):
            logging.error(
                "Refusing to create a session: user id is not numeric"
            )
            raise ValueError("Invalid user id for session creation")
        if owner_id <= 0:
            logging.error("Refusing to create a session: missing user id")
            raise ValueError("Invalid user id for session creation")

        token = secrets.token_urlsafe(TOKEN_BYTES)
        async with rx.asession() as session:
            owner = (
                await session.scalars(select(User).where(User.id == owner_id))
            ).first()
            if owner is None or not owner.is_active:
                logging.error(
                    "Refusing to create a session: no active account for that id"
                )
                raise ValueError("Invalid user id for session creation")
            row = UserSession(
                user_id=owner_id,
                session_token_hash=hash_token(token),
                expires_at=_now() + timedelta(days=SESSION_DAYS),
                last_seen_at=_now(),
            )
            # Belt and braces: assert the FK survived construction before flush.
            if row.user_id != owner_id:
                row.user_id = owner_id
            session.add(row)
            await session.flush()
            if row.user_id is None or int(row.user_id) != owner_id:
                await session.rollback()
                logging.error(
                    "Session insert aborted: foreign key did not persist"
                )
                raise ValueError("Session creation failed validation")
            await session.commit()
        return token

    @rx.event
    async def sign_up(self, form_data: dict[str, Any]):
        email = normalize_email(form_data.get("email", ""))
        password = str(form_data.get("password", "") or "")
        confirm = str(form_data.get("confirm_password", "") or "")
        name = str(form_data.get("display_name", "") or "").strip()[:120]
        self.error = ""
        self.notice = ""

        if not _valid_email(email):
            self.error = "Enter a valid email address."
            return
        if len(password) < MIN_PASSWORD_LENGTH:
            self.error = (
                f"Use a password of at least {MIN_PASSWORD_LENGTH} characters."
            )
            return
        if password != confirm:
            self.error = "Both passwords must match."
            return

        wait = await check_and_register_attempt(email, AuthAction.SIGN_UP)
        if wait:
            self.error = throttle_message(wait)
            return

        self.is_busy = True
        yield
        try:
            async with rx.asession() as session:
                existing = (
                    await session.scalars(
                        select(User).where(User.email_normalized == email)
                    )
                ).first()
                if existing is not None:
                    self.is_busy = False
                    await register_failure(email, AuthAction.SIGN_UP)
                    self.error = "An account already exists for that email. Please sign in."
                    return
                user = User(
                    email=email,
                    email_normalized=email,
                    display_name=name or None,
                    password_hash=hash_password(password),
                    password_algorithm=PBKDF2_ALGORITHM,
                    password_updated_at=_now(),
                    email_verified_at=None,
                )
                session.add(user)
                await session.commit()
                await session.refresh(user)
                user_id = int(user.id)
                user_email = str(user.email)
                user_name = str(user.display_name or "")
            await register_success(email, AuthAction.SIGN_UP)
        except Exception:
            logging.exception("Sign up failed")
            self.is_busy = False
            await register_failure(email, AuthAction.SIGN_UP)
            self.error = (
                "We couldn't create that account just now. Please try again."
            )
            return

        delivered = await self._send_verification_pair(
            user_email, user_name, user_id, include_welcome=True
        )
        self.is_busy = False
        self.pending_email = user_email
        self.verification_required = True
        self._clear_identity()
        self.session_checked = True
        if not delivered:
            self.error = EMAIL_UNAVAILABLE_NOTICE
            self.notice = ""
            yield rx.toast(
                "Account created, but the verification email could not be sent.",
                duration=6000,
                close_button=True,
            )
            yield rx.redirect("/login")
            return
        self.error = ""
        self.notice = (
            f"Account created. We emailed a verification link to {user_email}. "
            "Confirm it within 24 hours, then sign in."
        )
        yield rx.toast(
            "Check your email to verify your address.",
            duration=5000,
            close_button=True,
        )
        yield rx.redirect("/login")

    @rx.event
    async def log_in(self, form_data: dict[str, Any]):
        email = normalize_email(form_data.get("email", ""))
        password = str(form_data.get("password", "") or "")
        self.error = ""
        self.notice = ""
        self.verification_required = False
        if not email or not password:
            self.error = "Enter your email and password."
            return

        wait = await check_and_register_attempt(email, AuthAction.SIGN_IN)
        if wait:
            self.error = throttle_message(wait)
            return

        self.is_busy = True
        yield
        try:
            async with rx.asession() as session:
                user = (
                    await session.scalars(
                        select(User).where(User.email_normalized == email)
                    )
                ).first()
                if (
                    user is None
                    or not user.is_active
                    or not verify_password(password, user.password_hash)
                ):
                    self.is_busy = False
                    await register_failure(email, AuthAction.SIGN_IN)
                    self.error = GENERIC_LOGIN_ERROR
                    return
                if user.email_verified_at is None:
                    # Correct credentials, but the address is unconfirmed: no
                    # session is created and no access is granted.
                    self.is_busy = False
                    self._clear_identity()
                    self.verification_required = True
                    self.pending_email = str(user.email)
                    self.error = VERIFICATION_REQUIRED_ERROR
                    return
                user.last_login_at = _now()
                await session.commit()
                user_id = int(user.id)
                user_email = str(user.email)
                user_name = str(user.display_name or "")
            token = await self._start_session(user_id)
            await register_success(email, AuthAction.SIGN_IN)
        except Exception:
            logging.exception("Login failed")
            self.is_busy = False
            await register_failure(email, AuthAction.SIGN_IN)
            self.error = "We couldn't sign you in just now. Please try again."
            return
        self.is_busy = False
        self.session_token = token
        self.legacy_session_token = ""
        self.user_id = user_id
        self.user_email = user_email
        self.display_name = user_name
        self.session_checked = True
        yield rx.toast(
            f"Signed in as {user_email}", duration=4000, close_button=True
        )
        yield rx.redirect("/")

    @rx.event
    async def resend_verification(self, form_data: dict[str, Any]):
        """Resend verification mail, with one generic reply for every case."""
        email = normalize_email(
            form_data.get("email", "") or self.pending_email
        )
        self.error = ""
        self.notice = ""
        if not _valid_email(email):
            self.error = "Enter a valid email address."
            return

        wait = await check_and_register_attempt(
            email, AuthAction.RESEND_VERIFICATION
        )
        if wait:
            self.error = throttle_message(wait)
            return

        self.resend_busy = True
        yield
        target_email = ""
        target_name = ""
        target_id = 0
        try:
            async with rx.asession() as session:
                user = (
                    await session.scalars(
                        select(User).where(User.email_normalized == email)
                    )
                ).first()
                # Never send to a verified or inactive account, and never
                # reveal which of those cases applies.
                if (
                    user is not None
                    and user.is_active
                    and user.email_verified_at is None
                ):
                    target_id = int(user.id)
                    target_email = str(user.email)
                    target_name = str(user.display_name or "")
        except Exception:
            logging.exception("Verification resend lookup failed")

        if target_id:
            await self._send_verification_pair(
                target_email, target_name, target_id, include_welcome=False
            )
        self.resend_busy = False
        self.pending_email = email
        self.verification_required = True
        self.notice = GENERIC_RESEND_NOTICE

    async def _redeem_verification_token(self, raw_token: str) -> bool:
        """Atomically redeem an email-verification token, server-side only.

        The raw token stays inside this helper: it is hashed immediately, never
        stored in state and never logged. The matching row is selected under a
        database row lock (`SELECT ... FOR UPDATE`), so two concurrent
        redemptions of the same link cannot both observe it as unused - the
        second attempt waits, then sees `used_at` already stamped and fails.
        """
        token = str(raw_token or "").strip()
        if not token or len(token) > 512:
            return False
        token_hash = hash_token(token)
        token = ""
        raw_token = ""
        try:
            async with rx.asession() as session:
                row = (
                    await session.scalars(
                        select(AuthToken)
                        .where(
                            AuthToken.token_hash == token_hash,
                            AuthToken.purpose
                            == AuthTokenPurpose.EMAIL_VERIFICATION,
                        )
                        .with_for_update()
                    )
                ).first()
                if row is None or row.used_at is not None:
                    await session.rollback()
                    return False
                expires = row.expires_at
                if expires.tzinfo is None:
                    expires = expires.replace(tzinfo=timezone.utc)
                if expires <= _now():
                    await session.rollback()
                    return False
                user = (
                    await session.scalars(
                        select(User).where(User.id == row.user_id)
                    )
                ).first()
                if user is None or not user.is_active:
                    await session.rollback()
                    return False
                now = _now()
                row.used_at = now
                if user.email_verified_at is None:
                    user.email_verified_at = now
                # One commit releases the row lock: the token is consumed and
                # the account is marked verified together, or neither lands.
                await session.commit()
        except Exception:
            logging.exception("Unexpected error")
            logging.error("Email verification could not be completed")
            return False
        return True

    @rx.event
    async def verify_email_from_link(self):
        """Redeem a verification link read straight from the router params.

        The raw token never enters public state, the UI or the logs: it is read
        server-side, handed to the redemption helper, hashed and discarded.
        """
        self.error = ""
        self.notice = ""
        self.verify_status = "checking"
        yield
        redeemed = await self._redeem_verification_token(
            str(self.router.url.query_parameters.get("token", "") or "")
        )
        if not redeemed:
            self.verify_status = "invalid"
            return
        self.verification_required = False
        self.verify_status = "verified"
        logging.info("An email address was verified successfully")

    async def _issue_reset_token(self, user_id: int) -> tuple[str, int]:
        """Invalidate old reset tokens and mint a new 1 hour one atomically.

        Only the SHA-256 hash of the random 32-byte URL-safe token is stored.
        The plaintext token is returned for emailing and is never logged.
        """
        owner_id = int(user_id)
        token = secrets.token_urlsafe(TOKEN_BYTES)
        now = _now()
        async with rx.asession() as session:
            previous = (
                await session.scalars(
                    select(AuthToken).where(
                        AuthToken.user_id == owner_id,
                        AuthToken.purpose == AuthTokenPurpose.PASSWORD_RESET,
                        AuthToken.used_at.is_(None),
                    )
                )
            ).all()
            for stale in previous:
                stale.used_at = now
            row = AuthToken(
                user_id=owner_id,
                purpose=AuthTokenPurpose.PASSWORD_RESET,
                token_hash=hash_token(token),
                expires_at=now + timedelta(hours=RESET_TOKEN_HOURS),
            )
            session.add(row)
            await session.flush()
            token_id = int(row.id)
            await session.commit()
        return (token, token_id)

    @rx.event
    async def request_password_reset(self, form_data: dict[str, Any]):
        """Generic forgot-password request: one neutral reply for every case."""
        email = normalize_email(form_data.get("email", ""))
        self.error = ""
        self.notice = ""
        if not _valid_email(email):
            self.error = "Enter a valid email address."
            return

        wait = await check_and_register_attempt(
            email, AuthAction.PASSWORD_RESET
        )
        if wait:
            self.error = throttle_message(wait)
            return

        self.forgot_busy = True
        yield

        if not email_is_configured():
            # Honest, non-account-specific service notice: nothing was sent.
            logging.error(
                "Password reset email skipped: delivery is not configured"
            )
            self.forgot_busy = False
            self.error = RESET_SERVICE_NOTICE
            return

        target_id = 0
        target_email = ""
        try:
            async with rx.asession() as session:
                user = (
                    await session.scalars(
                        select(User).where(User.email_normalized == email)
                    )
                ).first()
                # Never reveal whether the account exists, is inactive, or
                # whether its address has been verified.
                if user is not None and user.is_active:
                    target_id = int(user.id)
                    target_email = str(user.email)
        except Exception:
            logging.exception("Password reset lookup failed")

        if target_id:
            try:
                token, token_id = await self._issue_reset_token(target_id)
            except Exception:
                logging.exception("Unexpected error")
                logging.error("Could not issue a password reset token")
            else:
                sent = await send_password_reset_email(
                    target_email, token, target_id, token_id
                )
                if not sent:
                    # Never surface an account-specific delivery error here:
                    # it would reveal that the address has an account.
                    logging.error(
                        "Password reset email delivery was not confirmed"
                    )

        # One identical reply for unknown accounts, successful sends and
        # provider delivery failures.
        self.forgot_busy = False
        self.notice = GENERIC_RESET_NOTICE

    def _query_reset_token(self) -> str:
        """Read the reset token straight from the router, server-side only."""
        return str(
            self.router.url.query_parameters.get("token", "") or ""
        ).strip()

    async def _reset_token_is_valid(self, raw_token: str) -> bool:
        """True only when an unused, unexpired reset token exists for an account."""
        token = str(raw_token or "").strip()
        if not token or len(token) > 512:
            return False
        token_hash = hash_token(token)
        token = ""
        try:
            async with rx.asession() as session:
                row = (
                    await session.scalars(
                        select(AuthToken).where(
                            AuthToken.token_hash == token_hash,
                            AuthToken.purpose
                            == AuthTokenPurpose.PASSWORD_RESET,
                        )
                    )
                ).first()
                if row is None or row.used_at is not None:
                    return False
                expires = row.expires_at
                if expires.tzinfo is None:
                    expires = expires.replace(tzinfo=timezone.utc)
                if expires <= _now():
                    return False
                user = (
                    await session.scalars(
                        select(User).where(User.id == row.user_id)
                    )
                ).first()
                return user is not None and bool(user.is_active)
        except Exception:
            logging.exception("Unexpected error")
            logging.error("Password reset preflight could not be completed")
            return False

    @rx.event
    async def preflight_password_reset(self):
        """Server-only check of the emailed link before showing the form.

        The raw token is read from the router, hashed and discarded: it never
        enters public state, the UI or the logs.
        """
        self.error = ""
        self.notice = ""
        self.reset_confirmation_sent = True
        self.reset_status = "checking"
        yield
        ok = await self._reset_token_is_valid(self._query_reset_token())
        if not ok:
            self.reset_status = "invalid"
            self.error = RESET_LINK_INVALID_ERROR
            return
        self.reset_status = "ready"

    async def _redeem_reset_token(
        self, raw_token: str, new_password: str
    ) -> tuple[int, str, int]:
        """Atomically consume a reset token and rotate the password hash.

        Returns (user_id, email, token_id) on success, or (0, "", 0). Every
        security change lands in a single commit under `SELECT ... FOR UPDATE`.
        """
        token = str(raw_token or "").strip()
        if not token or len(token) > 512:
            return (0, "", 0)
        token_hash = hash_token(token)
        token = ""
        raw_token = ""
        try:
            async with rx.asession() as session:
                row = (
                    await session.scalars(
                        select(AuthToken)
                        .where(
                            AuthToken.token_hash == token_hash,
                            AuthToken.purpose
                            == AuthTokenPurpose.PASSWORD_RESET,
                        )
                        .with_for_update()
                    )
                ).first()
                if row is None or row.used_at is not None:
                    await session.rollback()
                    return (0, "", 0)
                expires = row.expires_at
                if expires.tzinfo is None:
                    expires = expires.replace(tzinfo=timezone.utc)
                if expires <= _now():
                    await session.rollback()
                    return (0, "", 0)
                user = (
                    await session.scalars(
                        select(User).where(User.id == row.user_id)
                    )
                ).first()
                if user is None or not user.is_active:
                    await session.rollback()
                    return (0, "", 0)

                now = _now()
                owner_id = int(user.id)
                owner_email = str(user.email)
                token_id = int(row.id)

                # Only the irreversible hash is written — never a plaintext.
                user.password_hash = hash_password(new_password)
                user.password_algorithm = PBKDF2_ALGORITHM
                user.password_updated_at = now
                if user.email_verified_at is None:
                    # Possession of the reset email proves the address.
                    user.email_verified_at = now

                row.used_at = now

                others = (
                    await session.scalars(
                        select(AuthToken).where(
                            AuthToken.user_id == owner_id,
                            AuthToken.purpose
                            == AuthTokenPurpose.PASSWORD_RESET,
                            AuthToken.used_at.is_(None),
                            AuthToken.id != token_id,
                        )
                    )
                ).all()
                for stale in others:
                    stale.used_at = now

                sessions = (
                    await session.scalars(
                        select(UserSession).where(
                            UserSession.user_id == owner_id,
                            UserSession.revoked_at.is_(None),
                        )
                    )
                ).all()
                for live in sessions:
                    live.revoked_at = now

                await session.commit()
        except Exception:
            logging.exception("Unexpected error")
            logging.error("Password reset could not be completed")
            return (0, "", 0)
        return (owner_id, owner_email, token_id)

    @rx.event
    async def submit_password_reset(self, form_data: dict[str, Any]):
        """Set a new password from a valid reset link. No automatic sign in."""
        password = str(form_data.get("new_password", "") or "")
        confirm = str(form_data.get("confirm_password", "") or "")
        self.error = ""
        self.notice = ""
        self.reset_confirmation_sent = True
        if len(password) < MIN_PASSWORD_LENGTH:
            self.error = (
                f"Use a password of at least {MIN_PASSWORD_LENGTH} characters."
            )
            return
        if password != confirm:
            self.error = "Both passwords must match."
            return

        self.reset_busy = True
        yield
        user_id, user_email, token_id = await self._redeem_reset_token(
            self._query_reset_token(), password
        )
        password = ""
        confirm = ""
        if not user_id:
            self.reset_busy = False
            self.reset_status = "invalid"
            self.error = RESET_LINK_INVALID_ERROR
            return

        # The password change already landed; only the notice depends on mail.
        confirmed = await send_password_changed_email(
            user_email, user_id, token_id
        )
        self.reset_busy = False
        self.reset_status = "done"
        self.reset_confirmation_sent = bool(confirmed)
        self.verification_required = False
        self._forget_token()
        self._clear_identity()
        self.notice = RESET_SUCCESS_NOTICE
        logging.info("A password was reset successfully")
        yield rx.toast(
            "Password changed. Sign in with your new password.",
            duration=5000,
            close_button=True,
        )

    @rx.event
    async def resend_verification_for_account(self):
        """Resend verification for the signed-in, server-resolved account only."""
        self.error = ""
        self.notice = ""
        user_id, user_email = await current_user(self)
        if not user_id or not user_email:
            self.error = "Sign in again to resend your verification email."
            return
        email = normalize_email(user_email)
        wait = await check_and_register_attempt(
            email, AuthAction.RESEND_VERIFICATION
        )
        if wait:
            self.error = throttle_message(wait)
            return
        self.resend_busy = True
        yield
        target_id = 0
        target_email = ""
        target_name = ""
        try:
            async with rx.asession() as session:
                user = (
                    await session.scalars(
                        select(User).where(User.id == int(user_id))
                    )
                ).first()
                if (
                    user is not None
                    and user.is_active
                    and user.email_verified_at is None
                ):
                    target_id = int(user.id)
                    target_email = str(user.email)
                    target_name = str(user.display_name or "")
        except Exception:
            logging.exception("Account verification resend lookup failed")
        delivered = False
        if target_id:
            delivered = await self._send_verification_pair(
                target_email, target_name, target_id, include_welcome=False
            )
        self.resend_busy = False
        if target_id and not delivered:
            self.error = (
                "We could not send the verification email just now. "
                "Please try again later."
            )
            return
        self.notice = GENERIC_RESEND_NOTICE

    @rx.event
    async def log_out(self):
        """Revoke the server-side session and forget the browser token."""
        token = (
            str(self.session_token or "").strip()
            or str(self.legacy_session_token or "").strip()
        )
        self._forget_token()
        self._clear_identity()
        self.error = ""
        self.notice = ""
        if token:
            try:
                async with rx.asession() as session:
                    row = (
                        await session.scalars(
                            select(UserSession).where(
                                UserSession.session_token_hash
                                == hash_token(token)
                            )
                        )
                    ).first()
                    if row is not None and row.revoked_at is None:
                        row.revoked_at = _now()
                        await session.commit()
            except Exception:
                logging.exception("Logout cleanup failed")
        yield rx.toast("Signed out.", duration=3000, close_button=True)
        yield rx.redirect("/login")


async def current_user(state: rx.State) -> tuple[int, str]:
    """Per-user separation helper: the signed-in user id and email, or (0, "").

    Any other state can call this inside an event handler to scope its work to
    the current account:

        user_id, email = await current_user(self)
        if not user_id:
            return
    """
    auth = await state.get_state(AuthState)
    if not auth.session_checked:
        await auth._load_session()
    return (int(auth.user_id), str(auth.user_email))


async def current_scope_key(state: rx.State) -> str:
    """Stable string key for namespacing per-user data (empty if signed out)."""
    user_id, _email = await current_user(state)
    return f"user:{user_id}" if user_id else ""
