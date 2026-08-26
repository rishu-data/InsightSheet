"""Backend rate limiting for sign-in and sign-up attempts.

Only non-sensitive counters are persisted: a normalised-email throttle key,
the action (SIGN_IN / SIGN_UP), attempt tallies and window/block timestamps.
Passwords, tokens and payment data never reach this module, and log messages
are static so no email or secret is ever interpolated into the logs.

Behaviour:
  * A rolling window (``WINDOW_SECONDS``) counts attempts per email + action.
  * Crossing the per-action threshold opens a short block whose duration
    escalates with each repeat block, capped at ``MAX_BLOCK_SECONDS``.
  * A successful sign-in or sign-up clears the window counters and softens
    the escalation so honest users are never punished for a typo streak.
  * Callers receive only a generic, user-safe message — never internal
    thresholds, counts or timings beyond a coarse "try again in ..." hint.
"""

from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone

import reflex as rx
from sqlalchemy import select

from app.models import AuthAction, AuthRateLimit

WINDOW_SECONDS = 15 * 60
MAX_ATTEMPTS = {AuthAction.SIGN_IN: 8, AuthAction.SIGN_UP: 5}
BASE_BLOCK_SECONDS = 60
MAX_BLOCK_SECONDS = 15 * 60
MAX_BLOCK_COUNT = 6

GENERIC_THROTTLE_MESSAGE = (
    "Too many attempts from this account. Please wait a moment and try again."
)


def _now() -> datetime:
    return datetime.now(tz=timezone.utc)


def _aware(value: datetime | None) -> datetime | None:
    if value is None:
        return None
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value


def _throttle_key(email: str) -> str:
    return f"email:{str(email or '').strip().lower()}"[:255]


def _block_seconds(block_count: int) -> int:
    steps = max(0, min(int(block_count), MAX_BLOCK_COUNT) - 1)
    return min(BASE_BLOCK_SECONDS * (2**steps), MAX_BLOCK_SECONDS)


def throttle_message(retry_after_seconds: int) -> str:
    """Generic, user-safe wait message with a coarse retry hint."""
    if retry_after_seconds <= 0:
        return GENERIC_THROTTLE_MESSAGE
    if retry_after_seconds < 60:
        wait = f"{max(5, retry_after_seconds)} seconds"
    else:
        minutes = (retry_after_seconds + 59) // 60
        wait = "1 minute" if minutes == 1 else f"{minutes} minutes"
    return (
        "Too many attempts from this account. "
        f"Please try again in about {wait}."
    )


async def check_and_register_attempt(email: str, action: AuthAction) -> int:
    """Record an attempt; return seconds to wait, or 0 when allowed.

    Fails open (returns 0) if the counter store is unavailable so a database
    hiccup can never lock legitimate users out of the product.
    """
    key = _throttle_key(email)
    if not key or key == "email:":
        return 0
    limit = MAX_ATTEMPTS.get(action, 8)
    now = _now()
    try:
        async with rx.asession() as session:
            row = (
                await session.scalars(
                    select(AuthRateLimit).where(
                        AuthRateLimit.throttle_key == key,
                        AuthRateLimit.action == action,
                    )
                )
            ).first()
            if row is None:
                row = AuthRateLimit(throttle_key=key, action=action)
                row.attempt_count = 1
                row.window_started_at = now
                row.window_expires_at = now + timedelta(seconds=WINDOW_SECONDS)
                row.last_attempt_at = now
                session.add(row)
                await session.commit()
                return 0

            blocked_until = _aware(row.blocked_until)
            if blocked_until is not None and blocked_until > now:
                row.last_attempt_at = now
                await session.commit()
                return max(1, int((blocked_until - now).total_seconds()))

            window_expires = _aware(row.window_expires_at)
            if window_expires is None or window_expires <= now:
                row.attempt_count = 1
                row.window_started_at = now
                row.window_expires_at = now + timedelta(seconds=WINDOW_SECONDS)
                row.blocked_until = None
                row.last_attempt_at = now
                await session.commit()
                return 0

            row.attempt_count = int(row.attempt_count or 0) + 1
            row.last_attempt_at = now
            if row.attempt_count > limit:
                row.block_count = int(row.block_count or 0) + 1
                wait = _block_seconds(row.block_count)
                row.blocked_until = now + timedelta(seconds=wait)
                row.attempt_count = 0
                row.window_started_at = now
                row.window_expires_at = now + timedelta(seconds=WINDOW_SECONDS)
                await session.commit()
                logging.warning("Authentication attempt throttled")
                return wait
            await session.commit()
            return 0
    except Exception:
        logging.exception("Auth rate-limit check failed")
        return 0


async def register_failure(email: str, action: AuthAction) -> None:
    """Bump the lifetime failure tally for a rejected attempt."""
    key = _throttle_key(email)
    if not key or key == "email:":
        return
    try:
        async with rx.asession() as session:
            row = (
                await session.scalars(
                    select(AuthRateLimit).where(
                        AuthRateLimit.throttle_key == key,
                        AuthRateLimit.action == action,
                    )
                )
            ).first()
            if row is None:
                return
            row.failure_count = int(row.failure_count or 0) + 1
            await session.commit()
    except Exception:
        logging.exception("Auth rate-limit failure update failed")


async def register_success(email: str, action: AuthAction) -> None:
    """Clear the window and soften escalation after a successful auth."""
    key = _throttle_key(email)
    if not key or key == "email:":
        return
    now = _now()
    try:
        async with rx.asession() as session:
            row = (
                await session.scalars(
                    select(AuthRateLimit).where(
                        AuthRateLimit.throttle_key == key,
                        AuthRateLimit.action == action,
                    )
                )
            ).first()
            if row is None:
                return
            row.attempt_count = 0
            row.window_started_at = None
            row.window_expires_at = None
            row.blocked_until = None
            row.block_count = max(0, int(row.block_count or 0) - 1)
            row.last_success_at = now
            await session.commit()
    except Exception:
        logging.exception("Auth rate-limit success reset failed")
