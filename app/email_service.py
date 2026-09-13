"""Server-only transactional email delivery via Resend.

Security notes:
  * Credentials are read from the environment only (`RESEND_API_KEY`) and are
    never hard-coded, echoed or logged.
  * Verification tokens and links are passed straight to the provider and are
    NEVER logged, printed or returned to the caller.
  * Only a boolean success flag is returned. Provider message ids stay inside
    this module so they can never reach frontend state.
  * Every log line is a static string.
  * The blocking Resend SDK call runs in a worker thread via
    `asyncio.to_thread`, so Reflex event handlers never block the event loop.
"""

from __future__ import annotations

import asyncio
import logging
import os
from urllib.parse import quote

import reflex as rx

APP_NAME = "InsightSheet"
FALLBACK_PUBLIC_URL = "https://reflex-build-generation-silver-apple.reflex.run"


def _fallback_public_url() -> str:
    """The configured deploy URL, used as a safe Preview fallback."""
    try:
        configured = str(rx.config.get_config().deploy_url or "").strip()
    except Exception:
        logging.exception("Unexpected error")
        logging.error("Could not read the configured deploy URL")
        configured = ""
    return (configured or FALLBACK_PUBLIC_URL).rstrip("/")


def public_url() -> str:
    """Origin used to build emailed links (never a secret)."""
    configured = str(
        os.environ.get("INSIGHTSHEET_PUBLIC_URL", "") or ""
    ).strip()
    return configured.rstrip("/") or _fallback_public_url()


def email_is_configured() -> bool:
    """True only when both the API key and verified sender are present."""
    return bool(
        str(os.environ.get("RESEND_API_KEY", "") or "").strip()
        and str(os.environ.get("INSIGHTSHEET_EMAIL_FROM", "") or "").strip()
    )


def verification_link(token: str) -> str:
    """Absolute verification URL for a freshly issued token."""
    return f"{public_url()}/verify-email?token={quote(token, safe='')}"


def password_reset_link(token: str) -> str:
    """Absolute password-reset URL for a freshly issued token."""
    return f"{public_url()}/reset-password?token={quote(token, safe='')}"


def _send_blocking(
    from_address: str,
    to_address: str,
    subject: str,
    html: str,
    text: str,
    idempotency_key: str,
) -> str:
    """Blocking provider call. Runs in a worker thread; returns the message id."""
    import resend

    resend.api_key = os.environ["RESEND_API_KEY"]
    params = {
        "from": from_address,
        "to": [to_address],
        "subject": subject,
        "html": html,
        "text": text,
    }
    response = resend.Emails.send(params, {"idempotency_key": idempotency_key})
    return str(response.get("id", "") or "")


async def send_email(
    to_address: str,
    subject: str,
    html: str,
    text: str,
    idempotency_key: str,
) -> bool:
    """Send one transactional email. Returns True only on provider success."""
    if not email_is_configured():
        logging.error("Email not sent: email delivery is not configured")
        return False
    recipient = str(to_address or "").strip()
    if not recipient or "@" not in recipient:
        logging.error("Email not sent: recipient address is not usable")
        return False
    from_address = str(os.environ["INSIGHTSHEET_EMAIL_FROM"]).strip()
    try:
        message_id = await asyncio.to_thread(
            _send_blocking,
            from_address,
            recipient,
            subject,
            html,
            text,
            str(idempotency_key)[:256],
        )
    except Exception:
        logging.exception("Unexpected error")
        logging.error("Transactional email delivery failed")
        return False
    if not message_id:
        logging.error("Transactional email delivery returned no confirmation")
        return False
    logging.info("Transactional email accepted by the provider")
    return True


def _wrapper(heading: str, body_html: str) -> str:
    return (
        '<div style="font-family:Inter,Helvetica,Arial,sans-serif;'
        'background:#f9fafb;padding:24px">'
        '<div style="max-width:520px;margin:0 auto;background:#ffffff;'
        'border:1px solid #e5e7eb;border-radius:16px;padding:24px">'
        f'<p style="font-size:14px;font-weight:600;color:#2563eb;margin:0 0 12px">{APP_NAME}</p>'
        f'<h1 style="font-size:18px;font-weight:600;color:#111827;margin:0 0 12px">{heading}</h1>'
        f"{body_html}"
        '<p style="font-size:12px;color:#6b7280;margin:20px 0 0">'
        "You are receiving this transactional message because this address is "
        f"associated with an {APP_NAME} account or account request."
        "</p></div></div>"
    )


async def send_welcome_email(
    to_address: str, display_name: str, user_id: int
) -> bool:
    """Account-created email that states verification is still required."""
    greeting = f"Hi {display_name}," if display_name else "Hi,"
    html = _wrapper(
        f"Your {APP_NAME} account has been created",
        f'<p style="font-size:14px;color:#374151;margin:0 0 12px">{greeting}</p>'
        '<p style="font-size:14px;color:#374151;margin:0 0 12px">'
        f"Your {APP_NAME} account is set up. <strong>Your email address still needs "
        "to be verified</strong> before you can sign in and use your account."
        "</p>"
        '<p style="font-size:14px;color:#374151;margin:0">'
        "We sent a separate verification email with your confirmation link. "
        "It expires in 24 hours."
        "</p>",
    )
    text = (
        f"{greeting}\n\n"
        f"Your {APP_NAME} account has been created.\n\n"
        "Your email address still needs to be verified before you can sign in.\n"
        "We sent a separate verification email with your confirmation link, "
        "which expires in 24 hours.\n"
    )
    return await send_email(
        to_address,
        f"Your {APP_NAME} account was created — verification required",
        html,
        text,
        f"welcome-email/user-{int(user_id)}",
    )


async def send_verification_email(
    to_address: str, token: str, user_id: int, token_id: int
) -> bool:
    """Verification email containing the single-use confirmation link."""
    link = verification_link(token)
    html = _wrapper(
        "Verify your email address",
        '<p style="font-size:14px;color:#374151;margin:0 0 16px">'
        "Confirm this email address to activate your account. "
        "This link can be used once and expires in 24 hours."
        "</p>"
        f'<p style="margin:0 0 16px"><a href="{link}" '
        'style="display:inline-block;background:#2563eb;color:#ffffff;'
        "font-size:14px;font-weight:600;text-decoration:none;padding:10px 18px;"
        'border-radius:12px">Verify email address</a></p>'
        '<p style="font-size:12px;color:#6b7280;margin:0">'
        f"If the button does not work, open this link:<br>{link}</p>",
    )
    text = (
        "Verify your email address\n\n"
        "Confirm this email address to activate your account. This link can be "
        "used once and expires in 24 hours.\n\n"
        f"{link}\n"
    )
    return await send_email(
        to_address,
        f"Verify your email for {APP_NAME}",
        html,
        text,
        f"verify-email/token-{int(token_id)}-user-{int(user_id)}",
    )


async def send_password_reset_email(
    to_address: str, token: str, user_id: int, token_id: int
) -> bool:
    """Password-reset email containing the single-use, 1 hour reset link."""
    link = password_reset_link(token)
    html = _wrapper(
        "Reset your password",
        '<p style="font-size:14px;color:#374151;margin:0 0 16px">'
        "Use the button below to choose a new password. This link can be used "
        "once and expires in 1 hour. If you did not request it, you can ignore "
        "this email — your current password stays unchanged."
        "</p>"
        f'<p style="margin:0 0 16px"><a href="{link}" '
        'style="display:inline-block;background:#2563eb;color:#ffffff;'
        "font-size:14px;font-weight:600;text-decoration:none;padding:10px 18px;"
        'border-radius:12px">Reset password</a></p>'
        '<p style="font-size:12px;color:#6b7280;margin:0">'
        f"If the button does not work, open this link:<br>{link}</p>",
    )
    text = (
        "Reset your password\n\n"
        "Use the link below to choose a new password. It can be used once and "
        "expires in 1 hour. If you did not request it, ignore this email.\n\n"
        f"{link}\n"
    )
    return await send_email(
        to_address,
        f"Reset your {APP_NAME} password",
        html,
        text,
        f"password-reset/token-{int(token_id)}-user-{int(user_id)}",
    )


async def send_password_changed_email(
    to_address: str, user_id: int, token_id: int
) -> bool:
    """Confirmation that the password changed. Never contains a password."""
    html = _wrapper(
        "Your password was changed",
        '<p style="font-size:14px;color:#374151;margin:0 0 12px">'
        f"The password for your {APP_NAME} account was just changed using a "
        "password-reset link. All existing sessions were signed out."
        "</p>"
        '<p style="font-size:14px;color:#374151;margin:0">'
        "If this was not you, contact support immediately. This email never "
        "contains your password or a reset link."
        "</p>",
    )
    text = (
        f"The password for your {APP_NAME} account was just changed using a "
        "password-reset link. All existing sessions were signed out.\n\n"
        "If this was not you, contact support immediately.\n"
    )
    return await send_email(
        to_address,
        f"Your {APP_NAME} password was changed",
        html,
        text,
        f"password-changed/token-{int(token_id)}-user-{int(user_id)}",
    )
