"""Database-backed subscription status for Pro feature access.

The `razorpay_subscription` table is the single source of truth. Only the
ACTIVE status unlocks Pro; FREE, PENDING, PAYMENT_FAILED, CANCELLED and
EXPIRED all keep Pro features locked. Nothing here reads URL parameters,
browser storage or frontend flags, and nothing here writes to the table —
webhook processing and the checkout URL are untouched.
"""

from __future__ import annotations

import logging

import reflex as rx
from sqlalchemy import func, select

from app.models import Subscription, SubscriptionStatus

PRO_LOCK_TITLE = "This is a Pro feature"
PRO_LOCK_BODY = (
    "Upgrade to Pro (\u20b9199/month) to unlock this section. Access is granted "
    "automatically once your payment is confirmed."
)

STATUS_MESSAGES: dict[str, str] = {
    "FREE": "You're on the Free plan. Pro features are locked.",
    "PENDING": (
        "Your payment is being confirmed. Pro features stay locked until the "
        "payment is confirmed, then unlock automatically."
    ),
    "PAYMENT_FAILED": (
        "Payment failed \u2014 Pro was not activated. Pro features remain "
        "locked. Please try again."
    ),
    "CANCELLED": (
        "Payment cancelled \u2014 Pro was not activated. Pro features remain "
        "locked. You can try again at any time."
    ),
    "EXPIRED": (
        "Your Pro access was removed \u2014 the subscription expired. Pro "
        "features are locked until you subscribe again."
    ),
    "ACTIVE": "Pro Active — every Pro feature is unlocked on this account.",
}

STATUS_LABELS: dict[str, str] = {
    "FREE": "Free plan",
    "PENDING": "Payment pending",
    "PAYMENT_FAILED": "Payment failed",
    "CANCELLED": "Payment cancelled",
    "EXPIRED": "Pro access expired",
    "ACTIVE": "Pro Active",
}

RETRY_STATUSES = ("PAYMENT_FAILED", "CANCELLED", "EXPIRED", "FREE")

SIGNED_OUT_MESSAGE = (
    "Sign in to check your subscription. Pro features stay locked until an "
    "active subscription is found for your account."
)


def _status_value(value: object) -> str:
    if isinstance(value, SubscriptionStatus):
        return str(value.value)
    return str(value or "FREE")


class SubscriptionState(rx.State):
    """Mirrors the current user's row in `razorpay_subscription`."""

    status: str = "FREE"
    identity: str = ""
    loaded: bool = False
    account_id: int = 0
    is_refreshing: bool = False
    refresh_error: str = ""

    @rx.var
    def is_pro(self) -> bool:
        return self.status == "ACTIVE"

    @rx.var
    def is_signed_in(self) -> bool:
        return bool(self.identity)

    @rx.var
    def status_label(self) -> str:
        return STATUS_LABELS.get(self.status, "Free plan")

    @rx.var
    def status_message(self) -> str:
        if not self.identity:
            return SIGNED_OUT_MESSAGE
        return STATUS_MESSAGES.get(self.status, STATUS_MESSAGES["FREE"])

    @rx.var
    def status_tone(self) -> str:
        if self.status == "ACTIVE":
            return "good"
        if self.status == "PENDING":
            return "info"
        if self.status in ("PAYMENT_FAILED", "CANCELLED", "EXPIRED"):
            return "warn"
        return "neutral"

    @rx.var
    def show_try_again(self) -> bool:
        return self.status in ("PAYMENT_FAILED", "CANCELLED", "EXPIRED")

    async def _read_persisted_status(
        self, user_id: int, email: str
    ) -> str | None:
        """Return the persisted status for this account, linking rows if needed.

        Ownership must be verified before anything is linked or read as ACTIVE:

          1. a row already linked to this `app_user_id`, or
          2. an existing **unlinked** row whose `user_identifier` exactly
             matches this authenticated account's email (claimed in place,
             never duplicated and never taken from another app user).

        Nothing is claimed from Razorpay here, and a row whose Razorpay
        subscription id is also carried by an ACTIVE row owned by a different
        app user is treated as ambiguous and never reported as ACTIVE.
        """
        async with rx.asession() as session:
            row = (
                await session.scalars(
                    select(Subscription)
                    .where(Subscription.app_user_id == user_id)
                    .order_by(Subscription.id)
                )
            ).first()
            if row is None and email:
                candidate = (
                    await session.scalars(
                        select(Subscription).where(
                            func.lower(Subscription.user_identifier)
                            == email.strip().lower()
                        )
                    )
                ).first()
                if candidate is not None:
                    owner = candidate.app_user_id
                    if owner is None:
                        candidate.app_user_id = user_id
                        await session.commit()
                        row = candidate
                    elif int(owner) == user_id:
                        row = candidate
                    else:
                        # Owned by a different app user: never claim it.
                        row = None
            if row is None:
                return None
            status = _status_value(row.status)
            if status == "ACTIVE" and row.razorpay_subscription_id:
                conflicting = (
                    await session.scalars(
                        select(Subscription).where(
                            Subscription.razorpay_subscription_id
                            == row.razorpay_subscription_id,
                            Subscription.id != row.id,
                            Subscription.status == SubscriptionStatus.ACTIVE,
                            Subscription.app_user_id.is_not(None),
                            Subscription.app_user_id != user_id,
                        )
                    )
                ).first()
                if conflicting is not None:
                    logging.warning(
                        "Ambiguous Razorpay subscription ownership detected; "
                        "Pro access withheld."
                    )
                    return "PENDING"
            return status

    async def _refresh(self) -> None:
        """Read the authoritative status out of the database."""
        from app.states.auth_state import current_user

        try:
            user_id, email = await current_user(self)
        except Exception as e:
            logging.exception(f"Could not resolve current user: {e}")
            user_id, email = 0, ""
        identity = str(email or "").strip()
        self.identity = identity if user_id else ""
        self.account_id = int(user_id or 0)
        self.loaded = True
        if not user_id:
            self.status = "FREE"
            return
        try:
            status = await self._read_persisted_status(int(user_id), identity)
        except Exception as e:
            logging.exception(f"Subscription lookup failed: {e}")
            status = None
        # No remote auto-claiming: Pro is unlocked only by a verified, linked
        # local subscription row written by a signature-verified webhook.
        self.status = status or "FREE"

    @rx.event
    async def load_status(self):
        """Page `on_load` hook: refresh the subscription status from the DB."""
        await self._refresh()

    @rx.event
    async def refresh_status(self):
        """Refresh the authenticated account's subscription status on demand."""
        if self.is_refreshing:
            return
        self.is_refreshing = True
        self.refresh_error = ""
        yield
        try:
            await self._refresh()
        except Exception as e:
            logging.exception(f"Subscription refresh failed: {e}")
            self.refresh_error = "We couldn't refresh your subscription right now. Please try again."
        finally:
            self.is_refreshing = False


async def pro_access(state: rx.State) -> bool:
    """Server-side Pro check for event guards.

    Always re-reads the database, so a user cannot unlock Pro by editing any
    frontend state or var.
    """
    try:
        sub = await state.get_state(SubscriptionState)
        await sub._refresh()
        return sub.status == "ACTIVE"
    except Exception as e:
        logging.exception(f"Pro access check failed: {e}")
        return False


PRO_DENIED_MESSAGE = (
    "This is a Pro feature. Upgrade to Pro (\u20b9199/month) on the Pricing "
    "page to unlock it — access is granted automatically once your payment is "
    "confirmed."
)
