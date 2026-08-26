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

from app.models import AuthAction, User, UserSession
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
                    last_login_at=_now(),
                )
                session.add(user)
                await session.commit()
                await session.refresh(user)
                user_id = int(user.id)
                user_email = str(user.email)
                user_name = str(user.display_name or "")
            token = await self._start_session(user_id)
            await register_success(email, AuthAction.SIGN_UP)
        except Exception:
            logging.exception("Sign up failed")
            self.is_busy = False
            await register_failure(email, AuthAction.SIGN_UP)
            self.error = (
                "We couldn't create that account just now. Please try again."
            )
            return
        self.is_busy = False
        self.session_token = token
        self.legacy_session_token = ""
        self.user_id = user_id
        self.user_email = user_email
        self.display_name = user_name
        self.session_checked = True
        yield rx.toast(
            "Account created — you're signed in.",
            duration=4000,
            close_button=True,
        )
        yield rx.redirect("/")

    @rx.event
    async def log_in(self, form_data: dict[str, Any]):
        email = normalize_email(form_data.get("email", ""))
        password = str(form_data.get("password", "") or "")
        self.error = ""
        self.notice = ""
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
