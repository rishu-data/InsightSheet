"""Read-only account dashboard state for the signed-in user.

Everything here is derived server-side from `current_user(self)`. No event
handler accepts a user id, and no query is ever run for an identifier supplied
by the browser. Only non-sensitive columns are read: password hashes, session
token hashes, raw webhook payloads and signatures are never selected or
exposed.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from typing import TypedDict

import reflex as rx
from sqlalchemy import func, select

from app.models import (
    Feedback,
    Subscription,
    SubscriptionStatus,
    User,
    UserSession,
    WebhookEvent,
)
from app.states.auth_state import current_user

NOT_AVAILABLE = "Not available"
NOT_TRACKED = "Not tracked"

BILLING_LIMIT = 50
TIMELINE_LIMIT = 60
FEEDBACK_LIMIT = 20

# Verified webhook events that represent a purchase / payment attempt.
BILLING_EVENTS: tuple[str, ...] = (
    "payment.captured",
    "payment.authorized",
    "payment.failed",
    "subscription.charged",
    "subscription.activated",
    "subscription.cancelled",
    "subscription.completed",
    "subscription.expired",
    "subscription.halted",
    "subscription.pending",
    "subscription.authenticated",
)

PLAN_STATUS_LABELS: dict[str, str] = {
    "FREE": "No paid subscription",
    "PENDING": "Payment pending confirmation",
    "ACTIVE": "Active",
    "PAYMENT_FAILED": "Payment failed",
    "CANCELLED": "Cancelled",
    "EXPIRED": "Expired",
}

PLAN_STATUS_NOTES: dict[str, str] = {
    "FREE": "You're on the Free plan. Pro features stay locked until a payment is confirmed.",
    "PENDING": "A payment is being confirmed. Pro unlocks automatically once the webhook confirms it.",
    "ACTIVE": "Every Pro feature is unlocked on this account.",
    "PAYMENT_FAILED": "The last payment failed, so Pro was not activated on this account.",
    "CANCELLED": "The subscription was cancelled, so Pro is not active on this account.",
    "EXPIRED": "Pro access ended because the subscription expired.",
}


class ProfileInfo(TypedDict):
    name: str
    email: str
    created_at: str
    status: str
    is_active: bool
    email_verified: str
    is_verified: bool
    account_reference: str


class PlanInfo(TypedDict):
    name: str
    status: str
    status_code: str
    note: str
    started_at: str
    ends_at: str
    cancelled_at: str
    plan_reference: str
    subscription_reference: str
    is_pro: bool


class BillingRow(TypedDict):
    id: str
    event: str
    label: str
    amount: str
    currency: str
    method: str
    status: str
    occurred_at: str
    reference: str
    tone: str


class ActivityRow(TypedDict):
    id: str
    icon: str
    title: str
    detail: str
    occurred_at: str
    tone: str


class UntrackedRow(TypedDict):
    icon: str
    title: str
    reason: str


EMPTY_PROFILE: ProfileInfo = {
    "name": NOT_AVAILABLE,
    "email": NOT_AVAILABLE,
    "created_at": NOT_AVAILABLE,
    "status": NOT_AVAILABLE,
    "is_active": False,
    "email_verified": "Pending verification",
    "is_verified": False,
    "account_reference": NOT_AVAILABLE,
}

EMPTY_PLAN: PlanInfo = {
    "name": "Free",
    "status": NOT_AVAILABLE,
    "status_code": "FREE",
    "note": PLAN_STATUS_NOTES["FREE"],
    "started_at": NOT_AVAILABLE,
    "ends_at": NOT_AVAILABLE,
    "cancelled_at": NOT_AVAILABLE,
    "plan_reference": NOT_AVAILABLE,
    "subscription_reference": NOT_AVAILABLE,
    "is_pro": False,
}

UNTRACKED_ROWS: list[UntrackedRow] = [
    {
        "icon": "cloud-upload",
        "title": "File uploads",
        "reason": "Not tracked — uploads are processed in memory and no upload history table exists.",
    },
    {
        "icon": "chart-line",
        "title": "Analysis runs",
        "reason": "Not tracked — dashboard analysis is computed on demand and never persisted.",
    },
    {
        "icon": "file-text",
        "title": "Report generation",
        "reason": "Not tracked — reports are generated for download only and no report log is stored.",
    },
]


def _stamp(value: datetime | None) -> str:
    if value is None:
        return NOT_AVAILABLE
    return value.strftime("%b %d, %Y at %H:%M")


def _sort_key(value: datetime | None) -> datetime:
    if value is None:
        return datetime.min.replace(tzinfo=timezone.utc)
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value


def _short_reference(value: str | None) -> str:
    text = str(value or "").strip()
    if not text:
        return NOT_AVAILABLE
    if len(text) <= 10:
        return text
    return f"{text[:6]}\u2026{text[-4:]}"


def _status_value(value: object) -> str:
    if isinstance(value, SubscriptionStatus):
        return str(value.value)
    return str(value or "FREE")


def _safe_note(raw: str | None) -> dict[str, str]:
    """Parse the stored safe metadata note into plain short strings."""
    try:
        parsed = json.loads(str(raw or "") or "{}")
    except Exception:
        logging.exception("Unexpected error")
        return {}
    if not isinstance(parsed, dict):
        return {}
    out: dict[str, str] = {}
    for key, value in parsed.items():
        if isinstance(value, (str, int, float)) and not isinstance(value, bool):
            out[str(key)[:40]] = str(value)[:80]
    return out


def _amount_text(note: dict[str, str]) -> tuple[str, str]:
    minor = note.get("amount_minor_units", "")
    currency = note.get("currency", "").upper()
    if not minor:
        return (NOT_AVAILABLE, currency or NOT_AVAILABLE)
    try:
        major = int(float(minor)) / 100.0
    except (TypeError, ValueError):
        return (NOT_AVAILABLE, currency or NOT_AVAILABLE)
    symbol = "\u20b9" if currency in ("", "INR") else f"{currency} "
    return (f"{symbol}{major:,.2f}", currency or "INR")


def _event_tone(event_name: str) -> str:
    if event_name in (
        "payment.captured",
        "subscription.charged",
        "subscription.activated",
    ):
        return "good"
    if event_name in ("payment.failed", "subscription.halted"):
        return "bad"
    if event_name in (
        "subscription.cancelled",
        "subscription.expired",
        "subscription.completed",
    ):
        return "warn"
    return "info"


def _event_label(event_name: str) -> str:
    labels = {
        "payment.captured": "Payment captured",
        "payment.authorized": "Payment authorised",
        "payment.failed": "Payment failed",
        "subscription.charged": "Subscription charged",
        "subscription.activated": "Subscription activated",
        "subscription.authenticated": "Subscription authenticated",
        "subscription.pending": "Subscription pending",
        "subscription.cancelled": "Subscription cancelled",
        "subscription.completed": "Subscription completed",
        "subscription.expired": "Subscription expired",
        "subscription.halted": "Subscription halted",
    }
    return labels.get(event_name, event_name.replace(".", " ").capitalize())


class AccountState(rx.State):
    """Loads the authenticated account's own persisted record."""

    is_loading: bool = False
    loaded: bool = False
    load_error: str = ""
    signed_in: bool = False

    profile: ProfileInfo = EMPTY_PROFILE
    plan: PlanInfo = EMPTY_PLAN
    billing: list[BillingRow] = []
    activity: list[ActivityRow] = []
    untracked: list[UntrackedRow] = UNTRACKED_ROWS

    has_subscription_record: bool = False
    feedback_count: int = 0
    active_session_count: int = 0
    latest_login: str = NOT_AVAILABLE

    @rx.var
    def has_error(self) -> bool:
        return bool(self.load_error)

    @rx.var
    def has_billing(self) -> bool:
        return len(self.billing) > 0

    @rx.var
    def has_activity(self) -> bool:
        return len(self.activity) > 0

    @rx.var
    def billing_count(self) -> int:
        return len(self.billing)

    @rx.var
    def activity_count(self) -> int:
        return len(self.activity)

    def _reset(self) -> None:
        self.profile = EMPTY_PROFILE
        self.plan = EMPTY_PLAN
        self.billing = []
        self.activity = []
        self.has_subscription_record = False
        self.feedback_count = 0
        self.active_session_count = 0
        self.latest_login = NOT_AVAILABLE

    @rx.event
    async def load_account(self):
        """Protected loader: waits for session restoration, then loads own data."""
        # `current_user` restores the session first when it hasn't been checked,
        # so a page refresh never bounces an authenticated visitor.
        try:
            user_id, _email = await current_user(self)
        except Exception as e:
            logging.exception(f"Account session resolution failed: {e}")
            self.signed_in = False
            self.loaded = True
            self.load_error = (
                "We couldn't confirm your session just now. Please try again."
            )
            return

        if not user_id:
            self.signed_in = False
            self.loaded = True
            self._reset()
            yield rx.redirect("/login")
            return

        self.signed_in = True
        self.load_error = ""
        self.is_loading = True
        yield
        try:
            await self._load_for(int(user_id))
            await self._load_feedback_history(int(user_id))
        except Exception as e:
            logging.exception(f"Account dashboard load failed: {e}")
            self._reset()
            self.load_error = (
                "We couldn't load your account details just now. "
                "Please refresh and try again."
            )
        finally:
            self.is_loading = False
            self.loaded = True

    async def _load_feedback_history(self, user_id: int) -> None:
        """Reuse the existing FeedbackState loader for this account only."""
        from app.states.feedback_state import FeedbackState

        feedback = await self.get_state(FeedbackState)
        await feedback._load_history_for(int(user_id))

    async def _load_for(self, user_id: int) -> None:
        """Read only this account's row plus records it verifiably owns."""
        async with rx.asession() as session:
            user = (
                await session.scalars(select(User).where(User.id == user_id))
            ).first()
            if user is None:
                self._reset()
                self.load_error = (
                    "We couldn't load your account details just now. "
                    "Please refresh and try again."
                )
                return

            email_normalized = str(user.email_normalized or "").strip().lower()
            verified_at = user.email_verified_at
            is_verified = verified_at is not None
            verification_label = (
                f"Verified on {_stamp(verified_at)}"
                if is_verified
                else "Pending verification"
            )
            self.profile = ProfileInfo(
                name=str(user.display_name or "") or NOT_AVAILABLE,
                email=str(user.email or "") or NOT_AVAILABLE,
                created_at=_stamp(user.created_at),
                status="Active" if user.is_active else "Inactive",
                is_active=bool(user.is_active),
                email_verified=verification_label,
                is_verified=is_verified,
                account_reference=f"Account #{int(user.id)}",
            )
            self.latest_login = _stamp(user.last_login_at)

            subscription = await self._owned_subscription(
                session, user_id, email_normalized
            )
            self.has_subscription_record = subscription is not None
            self.plan = self._plan_from(subscription)

            events = await self._owned_events(session, subscription)
            self.billing = [self._billing_row(row) for row in events]

            feedback_rows = (
                await session.scalars(
                    select(Feedback)
                    .where(Feedback.user_id == user_id)
                    .order_by(Feedback.submitted_at.desc(), Feedback.id.desc())
                    .limit(FEEDBACK_LIMIT)
                )
            ).all()
            self.feedback_count = int(
                (
                    await session.scalar(
                        select(func.count(Feedback.id)).where(
                            Feedback.user_id == user_id
                        )
                    )
                )
                or 0
            )
            self.active_session_count = int(
                (
                    await session.scalar(
                        select(func.count(UserSession.id)).where(
                            UserSession.user_id == user_id,
                            UserSession.revoked_at.is_(None),
                            UserSession.expires_at
                            > datetime.now(tz=timezone.utc),
                        )
                    )
                )
                or 0
            )

            self.activity = self._build_activity(user, feedback_rows, events)

    async def _owned_subscription(
        self, session, user_id: int, email_normalized: str
    ) -> Subscription | None:
        """The subscription row this account provably owns, or None.

        Ownership is either the existing `app_user_id` link, or an *unlinked*
        row whose `user_identifier` exactly matches this account's normalised
        email. A row linked to a different app user is never read.
        """
        row = (
            await session.scalars(
                select(Subscription)
                .where(Subscription.app_user_id == user_id)
                .order_by(Subscription.id)
            )
        ).first()
        if row is not None:
            return row
        if not email_normalized:
            return None
        candidate = (
            await session.scalars(
                select(Subscription).where(
                    func.lower(Subscription.user_identifier) == email_normalized
                )
            )
        ).first()
        if candidate is None:
            return None
        owner = candidate.app_user_id
        if owner is None or int(owner) == user_id:
            return candidate
        return None

    async def _owned_events(
        self, session, subscription: Subscription | None
    ) -> list[WebhookEvent]:
        """Verified webhook events attributable to this account's subscription."""
        if subscription is None:
            return []
        subscription_id = str(subscription.razorpay_subscription_id or "")
        payment_id = str(subscription.razorpay_payment_id or "")
        if not subscription_id and not payment_id:
            return []
        conditions = []
        if subscription_id:
            conditions.append(
                WebhookEvent.razorpay_subscription_id == subscription_id
            )
        if payment_id:
            conditions.append(WebhookEvent.razorpay_payment_id == payment_id)
        clause = conditions[0]
        for extra in conditions[1:]:
            clause = clause | extra
        rows = (
            await session.scalars(
                select(WebhookEvent)
                .where(clause, WebhookEvent.event_name.in_(BILLING_EVENTS))
                .order_by(
                    WebhookEvent.processed_at.desc(), WebhookEvent.id.desc()
                )
                .limit(BILLING_LIMIT)
            )
        ).all()
        return list(rows)

    def _plan_from(self, subscription: Subscription | None) -> PlanInfo:
        if subscription is None:
            return EMPTY_PLAN
        status = _status_value(subscription.status)
        plan_id = str(subscription.razorpay_plan_id or "")
        name = "Free"
        if status == "ACTIVE":
            # "Business" is only claimed when the stored plan id says so.
            name = "Business" if "business" in plan_id.lower() else "Pro"
        return PlanInfo(
            name=name,
            status=PLAN_STATUS_LABELS.get(status, NOT_AVAILABLE),
            status_code=status,
            note=PLAN_STATUS_NOTES.get(status, PLAN_STATUS_NOTES["FREE"]),
            started_at=_stamp(subscription.activated_at),
            ends_at=_stamp(subscription.expires_at),
            cancelled_at=_stamp(subscription.cancelled_at),
            plan_reference=_short_reference(subscription.razorpay_plan_id),
            subscription_reference=_short_reference(
                subscription.razorpay_subscription_id
            ),
            is_pro=status == "ACTIVE",
        )

    def _billing_row(self, row: WebhookEvent) -> BillingRow:
        note = _safe_note(row.safe_metadata)
        amount, currency = _amount_text(note)
        event_name = str(row.event_name or "")
        status = note.get("payment_status") or note.get("subscription_status")
        if not status and row.resulting_status is not None:
            status = _status_value(row.resulting_status)
        reference = _short_reference(
            row.razorpay_payment_id or row.razorpay_subscription_id
        )
        return BillingRow(
            id=f"billing-{int(row.id)}",
            event=event_name,
            label=_event_label(event_name),
            amount=amount,
            currency=currency,
            method=str(note.get("method", "") or NOT_AVAILABLE),
            status=str(status or NOT_AVAILABLE).replace("_", " ").title(),
            occurred_at=_stamp(row.processed_at),
            reference=reference,
            tone=_event_tone(event_name),
        )

    def _build_activity(
        self,
        user: User,
        feedback_rows: list[Feedback],
        events: list[WebhookEvent],
    ) -> list[ActivityRow]:
        items: list[tuple[datetime, ActivityRow]] = []

        items.append(
            (
                _sort_key(user.created_at),
                ActivityRow(
                    id="activity-signup",
                    icon="user-plus",
                    title="Account created",
                    detail="Signed up for InsightSheet with this email address.",
                    occurred_at=_stamp(user.created_at),
                    tone="info",
                ),
            )
        )
        if user.last_login_at is not None:
            items.append(
                (
                    _sort_key(user.last_login_at),
                    ActivityRow(
                        id="activity-login",
                        icon="log-in",
                        title="Most recent sign in",
                        detail="Latest successful sign in recorded for this account.",
                        occurred_at=_stamp(user.last_login_at),
                        tone="info",
                    ),
                )
            )
        if user.password_updated_at is not None:
            items.append(
                (
                    _sort_key(user.password_updated_at),
                    ActivityRow(
                        id="activity-password",
                        icon="key-round",
                        title="Password set",
                        detail="The stored password hash was last written at this time.",
                        occurred_at=_stamp(user.password_updated_at),
                        tone="info",
                    ),
                )
            )
        for row in feedback_rows:
            items.append(
                (
                    _sort_key(row.submitted_at),
                    ActivityRow(
                        id=f"activity-feedback-{int(row.id)}",
                        icon="message-square-heart",
                        title="Feedback submitted",
                        detail=f"{int(row.rating or 0)} of 5 \u2014 {str(row.category or 'Feedback')}",
                        occurred_at=_stamp(row.submitted_at),
                        tone="good",
                    ),
                )
            )
        for row in events:
            note = _safe_note(row.safe_metadata)
            amount, _currency = _amount_text(note)
            event_name = str(row.event_name or "")
            detail = _event_label(event_name)
            if amount != NOT_AVAILABLE:
                detail = f"{detail} \u2014 {amount}"
            items.append(
                (
                    _sort_key(row.processed_at),
                    ActivityRow(
                        id=f"activity-event-{int(row.id)}",
                        icon="credit-card",
                        title="Subscription event",
                        detail=detail,
                        occurred_at=_stamp(row.processed_at),
                        tone=_event_tone(event_name),
                    ),
                )
            )

        items.sort(key=lambda pair: pair[0], reverse=True)
        return [row for _stamp_value, row in items[:TIMELINE_LIMIT]]
