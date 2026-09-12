"""Admin Control Center state.

Security rules enforced here:
  * Authorization is resolved server-side on EVERY event, by reading
    `app_user.is_admin` and `app_user.is_active` from the database for the
    exact user id behind the existing secure session (`current_user`).
  * Nothing trusts a client var, URL, plan, subscription, email domain or a
    client-supplied user id. On denial every dataset is cleared and the
    visitor is redirected.
  * Only explicitly named safe columns are selected. Password hashes,
    password algorithm, session token hashes, rate-limit rows, cookies,
    tokens, webhook signatures, raw payloads and environment values are never
    read into state or UI.
  * All SQL is parameterized raw SQL through `rx.asession()`.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timedelta, timezone
from typing import TypedDict

import reflex as rx
from sqlalchemy import text

PAGE_SIZE = 20
# Successful purchase signals — kept identical for Overview, Purchases,
# Revenue and user detail so every count agrees.
PURCHASE_EVENTS: tuple[str, ...] = ("payment.captured", "subscription.charged")
SUCCESS_EVENTS: tuple[str, ...] = PURCHASE_EVENTS
FAILED_EVENTS: tuple[str, ...] = ("payment.failed",)
PENDING_EVENTS: tuple[str, ...] = (
    "payment.authorized",
    "subscription.pending",
    "subscription.authenticated",
)
REFUND_EVENTS: tuple[str, ...] = ("payment.refunded",)
ALL_PAYMENT_EVENTS: tuple[str, ...] = (
    SUCCESS_EVENTS + FAILED_EVENTS + PENDING_EVENTS + REFUND_EVENTS
)
REVENUE_SCAN_LIMIT = 5000
DETAIL_LIMIT = 10
RECENT_LIMIT = 10
NOT_STORED = "Not stored"

FEEDBACK_FILTERS: list[str] = ["All", "New", "Reviewed", "Resolved"]
FEEDBACK_STATUS_VALUES: dict[str, str] = {
    "New": "NEW",
    "Reviewed": "REVIEWED",
    "Resolved": "RESOLVED",
}
ALLOWED_FEEDBACK_UPDATES: tuple[str, ...] = ("REVIEWED", "RESOLVED")

PURCHASE_FILTERS: list[str] = [
    "All",
    "Successful",
    "Failed",
    "Pending",
    "Refunded",
]
PURCHASE_FILTER_EVENTS: dict[str, tuple[str, ...]] = {
    "All": ALL_PAYMENT_EVENTS,
    "Successful": SUCCESS_EVENTS,
    "Failed": FAILED_EVENTS,
    "Pending": PENDING_EVENTS,
    "Refunded": REFUND_EVENTS,
}

SUBSCRIPTION_FILTERS: list[str] = [
    "All",
    "Active",
    "Pending",
    "Failed",
    "Cancelled",
    "Expired",
]
SUBSCRIPTION_FILTER_STATUS: dict[str, str] = {
    "Active": "ACTIVE",
    "Pending": "PENDING",
    "Failed": "PAYMENT_FAILED",
    "Cancelled": "CANCELLED",
    "Expired": "EXPIRED",
}

DB_ERROR = "We couldn't load this data right now. Please try again."
DENIED = "You don't have access to the admin control center."

FILTERS: list[str] = ["All", "Free", "Pro", "Active", "Expired/Cancelled"]

TABS: list[str] = [
    "Overview",
    "Users",
    "Feedback",
    "Purchases",
    "Subscriptions",
    "Revenue",
    "Usage",
]


CURRENCY_SYMBOLS: dict[str, str] = {
    "INR": "\u20b9",
    "USD": "$",
    "EUR": "\u20ac",
}


class AdminUserRow(TypedDict):
    id: int
    name: str
    email: str
    signup: str
    plan: str
    status: str
    last_activity: str


class AdminUserDetail(TypedDict):
    id: int
    name: str
    email: str
    signup: str
    last_activity: str
    plan: str
    status: str
    activated_at: str
    cancelled_at: str
    expires_at: str
    subscription_ref: str
    plan_ref: str
    feedback_count: int
    purchase_count: int


class AdminFeedbackRow(TypedDict):
    id: int
    name: str
    email: str
    rating: int
    category: str
    message: str
    submitted: str
    status: str


class AdminPurchaseRow(TypedDict):
    id: int
    customer: str
    plan: str
    amount: str
    currency: str
    status: str
    date: str
    payment_ref: str
    subscription_ref: str


class AdminSubscriptionRow(TypedDict):
    id: int
    name: str
    email: str
    identifier: str
    plan: str
    status: str
    started: str
    ended: str
    subscription_ref: str
    payment_ref: str


class RevenueCurrencyRow(TypedDict):
    currency: str
    total: str
    count: int


class RevenuePlanRow(TypedDict):
    plan: str
    total: str
    count: int
    share_label: str


class RevenueTxnRow(TypedDict):
    id: int
    date: str
    amount: str
    plan: str
    payment_ref: str


class DetailPurchaseRow(TypedDict):
    id: int
    date: str
    amount: str
    plan: str
    payment_ref: str


class DetailFeedbackRow(TypedDict):
    id: int
    submitted: str
    category: str
    rating: int
    status: str
    message: str


EMPTY_DETAIL: AdminUserDetail = {
    "id": 0,
    "name": "",
    "email": "",
    "signup": "",
    "last_activity": "",
    "plan": "",
    "status": "",
    "activated_at": "",
    "cancelled_at": "",
    "expires_at": "",
    "subscription_ref": "",
    "plan_ref": "",
    "feedback_count": 0,
    "purchase_count": 0,
}


def _now() -> datetime:
    return datetime.now(tz=timezone.utc)


def _fmt(value: object) -> str:
    if isinstance(value, datetime):
        return value.strftime("%d %b %Y, %H:%M")
    return ""


def _latest(*values: object) -> str:
    stamps = [v for v in values if isinstance(v, datetime)]
    if not stamps:
        return ""
    aware = [
        v if v.tzinfo is not None else v.replace(tzinfo=timezone.utc)
        for v in stamps
    ]
    return _fmt(max(aware))


def _plan_of(status: str) -> str:
    return "Pro" if status == "ACTIVE" else "Free"


def _in_clause(
    prefix: str, names: tuple[str, ...]
) -> tuple[str, dict[str, str]]:
    """Build a parameterized IN (...) fragment from a fixed name tuple."""
    keys = [f"{prefix}{index}" for index in range(len(names))]
    fragment = "(" + ", ".join(f":{key}" for key in keys) + ")"
    return fragment, {key: name for key, name in zip(keys, names)}


def _short(ref: str) -> str:
    value = str(ref or "").strip()
    if not value:
        return NOT_STORED
    if len(value) <= 20:
        return value
    return f"{value[:12]}\u2026{value[-4:]}"


def _meta(raw: object) -> dict[str, str | int]:
    """Parse the stored safe metadata note. Never raw payloads or signatures."""
    try:
        data = json.loads(str(raw or "") or "{}")
    except Exception:
        logging.exception("Unexpected error")
        return {}
    if not isinstance(data, dict):
        return {}
    clean: dict[str, str | int] = {}
    for key in ("plan_id", "currency", "payment_status", "subscription_id"):
        value = data.get(key)
        if isinstance(value, str) and value:
            clean[key] = value[:64]
    amount = data.get("amount_minor_units")
    if isinstance(amount, int) and amount >= 0:
        clean["amount_minor_units"] = amount
    return clean


def _money(minor: int, currency: str) -> str:
    code = str(currency or "").upper()[:8]
    symbol = CURRENCY_SYMBOLS.get(code, "")
    label = code if code and code != "UNKNOWN" else ""
    return f"{symbol}{minor / 100:,.2f} {label}".strip()


def _purchase_status(event_name: str) -> str:
    name = str(event_name or "")
    if name in SUCCESS_EVENTS:
        return "Successful"
    if name in FAILED_EVENTS:
        return "Failed"
    if name in PENDING_EVENTS:
        return "Pending"
    if name in REFUND_EVENTS:
        return "Refunded"
    return "Recorded"


def _pages(total: int) -> int:
    if total <= 0:
        return 1
    return (total + PAGE_SIZE - 1) // PAGE_SIZE


def _range_label(page: int, total: int, noun: str) -> str:
    if total <= 0:
        return f"No matching {noun}"
    start = (page - 1) * PAGE_SIZE + 1
    end = min(page * PAGE_SIZE, total)
    return f"Showing {start}\u2013{end} of {total} {noun}"


_SUCCESS_IN, _SUCCESS_PARAMS = _in_clause("sx", SUCCESS_EVENTS)

# Successful purchases are deduplicated by non-empty payment id: only the
# earliest successful event for a payment id counts.
_DEDUP = f"""
(e.razorpay_payment_id IS NULL
 OR e.razorpay_payment_id = ''
 OR e.event_name NOT IN {_SUCCESS_IN}
 OR NOT EXISTS (
     SELECT 1 FROM razorpay_webhook_event d
      WHERE d.razorpay_payment_id = e.razorpay_payment_id
        AND d.event_name IN {_SUCCESS_IN}
        AND d.id < e.id))
"""

# Safe customer identity for a webhook event: only via a stored subscription
# row matched on subscription id or payment id, preferring the linked account.
_EVENT_IDENTITY = """
(SELECT COALESCE(au.email, s.user_identifier, '')
   FROM razorpay_subscription s
   LEFT JOIN app_user au ON au.id = s.app_user_id
  WHERE (e.razorpay_subscription_id IS NOT NULL
         AND e.razorpay_subscription_id <> ''
         AND s.razorpay_subscription_id = e.razorpay_subscription_id)
     OR (e.razorpay_payment_id IS NOT NULL
         AND e.razorpay_payment_id <> ''
         AND s.razorpay_payment_id = e.razorpay_payment_id)
  ORDER BY s.id
  LIMIT 1)
"""

_EVENT_PLAN = """
(SELECT COALESCE(s.razorpay_plan_id, '')
   FROM razorpay_subscription s
  WHERE (e.razorpay_subscription_id IS NOT NULL
         AND e.razorpay_subscription_id <> ''
         AND s.razorpay_subscription_id = e.razorpay_subscription_id)
     OR (e.razorpay_payment_id IS NOT NULL
         AND e.razorpay_payment_id <> ''
         AND s.razorpay_payment_id = e.razorpay_payment_id)
  ORDER BY s.id
  LIMIT 1)
"""

_USER_SUBSCRIPTION_IDS = """
(SELECT s.razorpay_subscription_id
   FROM razorpay_subscription s
   LEFT JOIN app_user ou ON ou.id = :uid
  WHERE (s.app_user_id = :uid
         OR LOWER(s.user_identifier) = LOWER(ou.email_normalized))
    AND s.razorpay_subscription_id IS NOT NULL
    AND s.razorpay_subscription_id <> '')
"""


# Consistent with existing behaviour: a user is Pro only when an ACTIVE
# subscription row is linked to their account id, or carries their exact
# normalised email as its identifier.
_SUB_JOIN = """
LEFT JOIN razorpay_subscription s
       ON (s.app_user_id = u.id
           OR LOWER(s.user_identifier) = LOWER(u.email_normalized))
"""

_ACTIVE_EXISTS = """
EXISTS (
    SELECT 1 FROM razorpay_subscription sa
     WHERE (sa.app_user_id = u.id
            OR LOWER(sa.user_identifier) = LOWER(u.email_normalized))
       AND sa.status = 'ACTIVE'
)
"""


async def admin_user_id(state: rx.State) -> int:
    """Return the signed-in admin's user id, or 0. Fails closed."""
    from app.states.auth_state import current_user

    try:
        user_id, _email = await current_user(state)
    except Exception as e:
        logging.exception(f"Admin session lookup failed: {e}")
        return 0
    if not user_id or int(user_id) <= 0:
        return 0
    try:
        async with rx.asession() as session:
            row = (
                await session.execute(
                    text(
                        "SELECT is_admin, is_active FROM app_user "
                        "WHERE id = :uid"
                    ),
                    {"uid": int(user_id)},
                )
            ).first()
    except Exception as e:
        logging.exception(f"Admin authorization lookup failed: {e}")
        return 0
    if row is None or not bool(row[0]) or not bool(row[1]):
        return 0
    return int(user_id)


class AdminState(rx.State):
    """Server-authorized admin datasets. Holds only safe aggregate data."""

    active_tab: str = "Overview"
    authorized: bool = False
    checked: bool = False
    is_loading: bool = False
    error: str = ""

    period_label: str = "Last 7 days"

    total_users: int = 0
    free_users: int = 0
    pro_users: int = 0
    active_subscriptions: int = 0
    ended_subscriptions: int = 0
    purchase_events: int = 0

    revenue_display: str = "Unavailable"
    revenue_note: str = (
        "Revenue is read only from verified webhook amount metadata."
    )
    revenue_available: bool = False

    new_users_7d: int = 0
    new_purchases_7d: int = 0
    new_feedback_7d: int = 0

    search: str = ""
    plan_filter: str = "All"
    page: int = 1
    total_matches: int = 0
    users: list[AdminUserRow] = []
    users_loaded: bool = False

    selected: AdminUserDetail = EMPTY_DETAIL
    detail_error: str = ""
    detail_loading: bool = False
    selected_purchases: list[DetailPurchaseRow] = []
    selected_feedback: list[DetailFeedbackRow] = []

    feedback_search: str = ""
    feedback_filter: str = "All"
    feedback_page: int = 1
    feedback_total: int = 0
    feedback_rows: list[AdminFeedbackRow] = []
    feedback_loaded: bool = False
    feedback_notice: str = ""
    feedback_busy_id: int = 0

    purchase_filter: str = "All"
    purchase_page: int = 1
    purchase_total: int = 0
    purchase_rows: list[AdminPurchaseRow] = []
    purchases_loaded: bool = False

    subscription_search: str = ""
    subscription_filter: str = "All"
    subscription_page: int = 1
    subscription_total: int = 0
    subscription_rows: list[AdminSubscriptionRow] = []
    subscriptions_loaded: bool = False

    revenue_currencies: list[RevenueCurrencyRow] = []
    revenue_plans: list[RevenuePlanRow] = []
    revenue_recent: list[RevenueTxnRow] = []
    revenue_success_count: int = 0
    revenue_missing_amount: int = 0
    revenue_loaded: bool = False

    @rx.var
    def has_feedback(self) -> bool:
        return len(self.feedback_rows) > 0

    @rx.var
    def feedback_pages(self) -> int:
        return _pages(self.feedback_total)

    @rx.var
    def feedback_can_prev(self) -> bool:
        return self.feedback_page > 1

    @rx.var
    def feedback_can_next(self) -> bool:
        return self.feedback_page < self.feedback_pages

    @rx.var
    def feedback_range_label(self) -> str:
        return _range_label(
            self.feedback_page, self.feedback_total, "feedback entries"
        )

    @rx.var
    def has_purchases(self) -> bool:
        return len(self.purchase_rows) > 0

    @rx.var
    def purchase_pages(self) -> int:
        return _pages(self.purchase_total)

    @rx.var
    def purchase_can_prev(self) -> bool:
        return self.purchase_page > 1

    @rx.var
    def purchase_can_next(self) -> bool:
        return self.purchase_page < self.purchase_pages

    @rx.var
    def purchase_range_label(self) -> str:
        return _range_label(
            self.purchase_page, self.purchase_total, "payment records"
        )

    @rx.var
    def has_subscriptions(self) -> bool:
        return len(self.subscription_rows) > 0

    @rx.var
    def subscription_pages(self) -> int:
        return _pages(self.subscription_total)

    @rx.var
    def subscription_can_prev(self) -> bool:
        return self.subscription_page > 1

    @rx.var
    def subscription_can_next(self) -> bool:
        return self.subscription_page < self.subscription_pages

    @rx.var
    def subscription_range_label(self) -> str:
        return _range_label(
            self.subscription_page, self.subscription_total, "subscriptions"
        )

    @rx.var
    def has_revenue(self) -> bool:
        return len(self.revenue_currencies) > 0

    @rx.var
    def has_detail_purchases(self) -> bool:
        return len(self.selected_purchases) > 0

    @rx.var
    def has_detail_feedback(self) -> bool:
        return len(self.selected_feedback) > 0

    @rx.var
    def has_users(self) -> bool:
        return len(self.users) > 0

    @rx.var
    def has_selection(self) -> bool:
        return self.selected["id"] > 0

    @rx.var
    def total_pages(self) -> int:
        if self.total_matches <= 0:
            return 1
        return (self.total_matches + PAGE_SIZE - 1) // PAGE_SIZE

    @rx.var
    def can_prev(self) -> bool:
        return self.page > 1

    @rx.var
    def can_next(self) -> bool:
        return self.page < self.total_pages

    @rx.var
    def range_label(self) -> str:
        if self.total_matches <= 0:
            return "No matching users"
        start = (self.page - 1) * PAGE_SIZE + 1
        end = min(self.page * PAGE_SIZE, self.total_matches)
        return f"Showing {start}–{end} of {self.total_matches} users"

    def _clear_data(self) -> None:
        self.total_users = 0
        self.free_users = 0
        self.pro_users = 0
        self.active_subscriptions = 0
        self.ended_subscriptions = 0
        self.purchase_events = 0
        self.revenue_display = "Unavailable"
        self.revenue_available = False
        self.new_users_7d = 0
        self.new_purchases_7d = 0
        self.new_feedback_7d = 0
        self.users = []
        self.users_loaded = False
        self.total_matches = 0
        self.page = 1
        self.search = ""
        self.plan_filter = "All"
        self.selected = EMPTY_DETAIL
        self.detail_error = ""
        self.selected_purchases = []
        self.selected_feedback = []
        self.feedback_rows = []
        self.feedback_loaded = False
        self.feedback_total = 0
        self.feedback_page = 1
        self.feedback_search = ""
        self.feedback_filter = "All"
        self.feedback_notice = ""
        self.feedback_busy_id = 0
        self.purchase_rows = []
        self.purchases_loaded = False
        self.purchase_total = 0
        self.purchase_page = 1
        self.purchase_filter = "All"
        self.subscription_rows = []
        self.subscriptions_loaded = False
        self.subscription_total = 0
        self.subscription_page = 1
        self.subscription_search = ""
        self.subscription_filter = "All"
        self.revenue_currencies = []
        self.revenue_plans = []
        self.revenue_recent = []
        self.revenue_success_count = 0
        self.revenue_missing_amount = 0
        self.revenue_loaded = False
        self.error = ""

    async def _authorize(self) -> int:
        user_id = await admin_user_id(self)
        self.checked = True
        self.authorized = user_id > 0
        if not user_id:
            self._clear_data()
        return user_id

    # ---------------------------------------------------------------- events

    @rx.event
    async def load_admin(self):
        """`/admin` on-load guard: authorize first, then load data."""
        from app.states.auth_state import current_user

        user_id, _email = await current_user(self)
        if not user_id:
            self.checked = True
            self.authorized = False
            self._clear_data()
            yield rx.redirect("/login")
            return
        if not await self._authorize():
            yield rx.redirect("/dashboard")
            return
        async for update in self._load_active():
            yield update

    @rx.event
    async def refresh(self):
        if not await self._authorize():
            yield rx.redirect("/dashboard")
            return
        async for update in self._load_active():
            yield update

    @rx.event
    async def select_tab(self, tab: str):
        if tab not in TABS:
            return
        if not await self._authorize():
            yield rx.redirect("/dashboard")
            return
        self.active_tab = tab
        self.error = ""
        async for update in self._load_active():
            yield update

    @rx.event
    async def set_search(self, value: str):
        if not await self._authorize():
            yield rx.redirect("/dashboard")
            return
        self.search = str(value or "")[:200]
        self.page = 1
        async for update in self._load_users():
            yield update

    @rx.event
    async def set_filter(self, value: str):
        if value not in FILTERS:
            return
        if not await self._authorize():
            yield rx.redirect("/dashboard")
            return
        self.plan_filter = value
        self.page = 1
        async for update in self._load_users():
            yield update

    @rx.event
    async def prev_page(self):
        if not await self._authorize():
            yield rx.redirect("/dashboard")
            return
        if self.page <= 1:
            return
        self.page -= 1
        async for update in self._load_users():
            yield update

    @rx.event
    async def next_page(self):
        if not await self._authorize():
            yield rx.redirect("/dashboard")
            return
        if self.page >= self.total_pages:
            return
        self.page += 1
        async for update in self._load_users():
            yield update

    # ------------------------------------------------------- feedback events

    @rx.event
    async def set_feedback_search(self, value: str):
        if not await self._authorize():
            yield rx.redirect("/dashboard")
            return
        self.feedback_search = str(value or "")[:200]
        self.feedback_page = 1
        async for update in self._load_feedback():
            yield update

    @rx.event
    async def set_feedback_filter(self, value: str):
        if value not in FEEDBACK_FILTERS:
            return
        if not await self._authorize():
            yield rx.redirect("/dashboard")
            return
        self.feedback_filter = value
        self.feedback_page = 1
        async for update in self._load_feedback():
            yield update

    @rx.event
    async def feedback_prev(self):
        if not await self._authorize():
            yield rx.redirect("/dashboard")
            return
        if self.feedback_page <= 1:
            return
        self.feedback_page -= 1
        async for update in self._load_feedback():
            yield update

    @rx.event
    async def feedback_next(self):
        if not await self._authorize():
            yield rx.redirect("/dashboard")
            return
        if self.feedback_page >= self.feedback_pages:
            return
        self.feedback_page += 1
        async for update in self._load_feedback():
            yield update

    @rx.event
    async def mark_feedback(self, feedback_id: int, status: str):
        """Admin-only review action: update ONLY `app_feedback.status`."""
        if not await self._authorize():
            yield rx.redirect("/dashboard")
            return
        target_status = str(status or "").strip().upper()
        if target_status not in ALLOWED_FEEDBACK_UPDATES:
            self.feedback_notice = "That review status isn't allowed."
            return
        try:
            target = int(feedback_id)
        except (TypeError, ValueError):
            self.feedback_notice = "That feedback entry could not be found."
            return
        if target <= 0:
            self.feedback_notice = "That feedback entry could not be found."
            return
        self.feedback_busy_id = target
        self.feedback_notice = ""
        yield
        # Re-verify admin authorization immediately before the update.
        if not await self._authorize():
            yield rx.redirect("/dashboard")
            return
        try:
            async with rx.asession() as session:
                result = await session.execute(
                    text(
                        "UPDATE app_feedback SET status = :status "
                        "WHERE id = :fid"
                    ),
                    {"status": target_status, "fid": target},
                )
                changed = int(result.rowcount or 0)
                if changed == 1:
                    await session.commit()
                else:
                    await session.rollback()
        except Exception as e:
            logging.exception(f"Admin feedback status update failed: {e}")
            self.feedback_busy_id = 0
            self.feedback_notice = DB_ERROR
            return
        self.feedback_busy_id = 0
        if changed != 1:
            self.feedback_notice = "That feedback entry no longer exists."
        else:
            self.feedback_notice = (
                f"Feedback #{target} marked {target_status.title()}."
            )
        async for update in self._load_feedback():
            yield update
        async for update in self._load_overview():
            yield update

    # ------------------------------------------------------ purchase events

    @rx.event
    async def set_purchase_filter(self, value: str):
        if value not in PURCHASE_FILTERS:
            return
        if not await self._authorize():
            yield rx.redirect("/dashboard")
            return
        self.purchase_filter = value
        self.purchase_page = 1
        async for update in self._load_purchases():
            yield update

    @rx.event
    async def purchase_prev(self):
        if not await self._authorize():
            yield rx.redirect("/dashboard")
            return
        if self.purchase_page <= 1:
            return
        self.purchase_page -= 1
        async for update in self._load_purchases():
            yield update

    @rx.event
    async def purchase_next(self):
        if not await self._authorize():
            yield rx.redirect("/dashboard")
            return
        if self.purchase_page >= self.purchase_pages:
            return
        self.purchase_page += 1
        async for update in self._load_purchases():
            yield update

    # -------------------------------------------------- subscription events

    @rx.event
    async def set_subscription_search(self, value: str):
        if not await self._authorize():
            yield rx.redirect("/dashboard")
            return
        self.subscription_search = str(value or "")[:200]
        self.subscription_page = 1
        async for update in self._load_subscriptions():
            yield update

    @rx.event
    async def set_subscription_filter(self, value: str):
        if value not in SUBSCRIPTION_FILTERS:
            return
        if not await self._authorize():
            yield rx.redirect("/dashboard")
            return
        self.subscription_filter = value
        self.subscription_page = 1
        async for update in self._load_subscriptions():
            yield update

    @rx.event
    async def subscription_prev(self):
        if not await self._authorize():
            yield rx.redirect("/dashboard")
            return
        if self.subscription_page <= 1:
            return
        self.subscription_page -= 1
        async for update in self._load_subscriptions():
            yield update

    @rx.event
    async def subscription_next(self):
        if not await self._authorize():
            yield rx.redirect("/dashboard")
            return
        if self.subscription_page >= self.subscription_pages:
            return
        self.subscription_page += 1
        async for update in self._load_subscriptions():
            yield update

    @rx.event
    async def clear_selection(self):
        self.selected = EMPTY_DETAIL
        self.detail_error = ""
        self.selected_purchases = []
        self.selected_feedback = []

    @rx.event
    async def select_user(self, user_id: int):
        if not await self._authorize():
            yield rx.redirect("/dashboard")
            return
        try:
            target = int(user_id)
        except (TypeError, ValueError):
            self.detail_error = "That account could not be found."
            return
        if target <= 0:
            self.detail_error = "That account could not be found."
            return
        self.detail_loading = True
        self.detail_error = ""
        self.selected_purchases = []
        self.selected_feedback = []
        yield
        try:
            detail = await self._read_detail(target)
        except Exception as e:
            logging.exception(f"Admin user detail query failed: {e}")
            self.detail_loading = False
            self.selected = EMPTY_DETAIL
            self.detail_error = DB_ERROR
            return
        if detail is None:
            self.detail_loading = False
            self.selected = EMPTY_DETAIL
            self.detail_error = "That account no longer exists."
            return
        self.selected = detail
        # Bounded child histories, re-authorized and scoped to this user.
        if not await self._authorize():
            yield rx.redirect("/dashboard")
            return
        try:
            purchases, feedback = await self._read_detail_history(target)
        except Exception as e:
            logging.exception(f"Admin user history query failed: {e}")
            self.detail_loading = False
            self.detail_error = DB_ERROR
            return
        self.selected_purchases = purchases
        self.selected_feedback = feedback
        self.detail_loading = False

    # --------------------------------------------------------------- loaders

    async def _load_active(self):
        if self.active_tab == "Users":
            async for update in self._load_users():
                yield update
            return
        if self.active_tab == "Overview":
            async for update in self._load_overview():
                yield update
            return
        if self.active_tab == "Feedback":
            async for update in self._load_feedback():
                yield update
            return
        if self.active_tab == "Purchases":
            async for update in self._load_purchases():
                yield update
            return
        if self.active_tab == "Subscriptions":
            async for update in self._load_subscriptions():
                yield update
            return
        if self.active_tab == "Revenue":
            async for update in self._load_revenue():
                yield update
            return
        # Usage: the stored schema keeps no upload, report, analytics or
        # activity records, so nothing is queried and nothing is invented.
        self.is_loading = False
        self.error = ""
        yield

    async def _load_overview(self):
        self.is_loading = True
        self.error = ""
        yield
        cutoff = _now() - timedelta(days=7)
        try:
            async with rx.asession() as session:
                counts = (
                    await session.execute(
                        text(
                            f"""
                            SELECT COUNT(*) AS total,
                                   SUM(CASE WHEN {_ACTIVE_EXISTS}
                                            THEN 1 ELSE 0 END) AS pro,
                                   SUM(CASE WHEN u.created_at >= :cutoff
                                            THEN 1 ELSE 0 END) AS recent
                              FROM app_user u
                            """
                        ),
                        {"cutoff": cutoff},
                    )
                ).first()
                subs = (
                    await session.execute(
                        text(
                            """
                            SELECT
                              SUM(CASE WHEN status = 'ACTIVE'
                                       THEN 1 ELSE 0 END) AS active,
                              SUM(CASE WHEN status IN ('EXPIRED','CANCELLED')
                                       THEN 1 ELSE 0 END) AS ended
                            FROM razorpay_subscription
                            """
                        )
                    )
                ).first()
                feedback = (
                    await session.execute(
                        text(
                            "SELECT COUNT(*) FROM app_feedback "
                            "WHERE submitted_at >= :cutoff"
                        ),
                        {"cutoff": cutoff},
                    )
                ).first()
                purchases = (
                    await session.execute(
                        text(
                            """
                            SELECT COUNT(DISTINCT COALESCE(
                                       razorpay_payment_id,
                                       'event:' || razorpay_event_id)) AS total,
                                   COUNT(DISTINCT CASE
                                       WHEN processed_at >= :cutoff
                                       THEN COALESCE(
                                           razorpay_payment_id,
                                           'event:' || razorpay_event_id)
                                       END) AS recent
                              FROM razorpay_webhook_event
                             WHERE event_name IN (:e1, :e2)
                            """
                        ),
                        {
                            "cutoff": cutoff,
                            "e1": PURCHASE_EVENTS[0],
                            "e2": PURCHASE_EVENTS[1],
                        },
                    )
                ).first()
                revenue_rows = (
                    await session.execute(
                        text(
                            """
                            SELECT razorpay_payment_id,
                                   razorpay_event_id,
                                   safe_metadata
                              FROM razorpay_webhook_event
                             WHERE event_name IN (:e1, :e2)
                             ORDER BY id DESC
                             LIMIT :cap
                            """
                        ),
                        {
                            "e1": PURCHASE_EVENTS[0],
                            "e2": PURCHASE_EVENTS[1],
                            "cap": REVENUE_SCAN_LIMIT,
                        },
                    )
                ).all()
        except Exception as e:
            logging.exception(f"Admin overview query failed: {e}")
            self.is_loading = False
            self._clear_data()
            self.error = DB_ERROR
            return

        total = int(counts[0] or 0) if counts else 0
        pro = int(counts[1] or 0) if counts else 0
        self.total_users = total
        self.pro_users = pro
        self.free_users = max(total - pro, 0)
        self.new_users_7d = int(counts[2] or 0) if counts else 0
        self.active_subscriptions = int(subs[0] or 0) if subs else 0
        self.ended_subscriptions = int(subs[1] or 0) if subs else 0
        self.new_feedback_7d = int(feedback[0] or 0) if feedback else 0
        self.purchase_events = int(purchases[0] or 0) if purchases else 0
        self.new_purchases_7d = int(purchases[1] or 0) if purchases else 0
        self._apply_revenue(revenue_rows)
        self.is_loading = False

    def _apply_revenue(self, rows: list) -> None:
        """Total revenue from safe `amount_minor_units` metadata only."""
        seen: set[str] = set()
        currencies: set[str] = set()
        minor_total = 0
        with_amount = 0
        for row in rows:
            key = str(row[0] or "") or f"event:{row[1]}"
            if key in seen:
                continue
            seen.add(key)
            try:
                data = json.loads(str(row[2] or "") or "{}")
            except Exception:
                logging.exception("Unexpected error")
                continue
            if not isinstance(data, dict):
                continue
            amount = data.get("amount_minor_units")
            if not isinstance(amount, int) or amount < 0:
                continue
            currency = str(data.get("currency") or "").upper()[:8]
            currencies.add(currency or "UNKNOWN")
            minor_total += amount
            with_amount += 1
        if with_amount == 0:
            self.revenue_available = False
            self.revenue_display = "Unavailable"
            self.revenue_note = (
                "No verified payment event carries safe amount metadata, so "
                "revenue cannot be reported. Purchase counts are unaffected."
            )
            return
        if len(currencies) > 1:
            self.revenue_available = False
            self.revenue_display = "Multi-currency"
            self.revenue_note = (
                "Verified payment amounts span more than one currency "
                f"({', '.join(sorted(currencies))}); totals are not combined."
            )
            return
        currency = next(iter(currencies))
        symbol = CURRENCY_SYMBOLS.get(currency, "")
        major = minor_total / 100
        label = currency if currency != "UNKNOWN" else ""
        self.revenue_available = True
        self.revenue_display = f"{symbol}{major:,.2f} {label}".strip()
        self.revenue_note = (
            f"Parsed from safe amount metadata on {with_amount} verified "
            "payment events — never from plan prices."
        )

    def _user_where(self) -> tuple[str, dict[str, str]]:
        clauses: list[str] = ["u.id IS NOT NULL"]
        params: dict[str, str] = {}
        term = self.search.strip()
        if term:
            clauses.append(
                "(LOWER(COALESCE(u.display_name, '')) LIKE :term"
                " OR LOWER(u.email) LIKE :term"
                " OR CAST(u.id AS VARCHAR(20)) LIKE :term)"
            )
            params["term"] = f"%{term.lower()}%"
        if self.plan_filter == "Pro" or self.plan_filter == "Active":
            clauses.append(_ACTIVE_EXISTS)
        elif self.plan_filter == "Free":
            clauses.append(f"NOT {_ACTIVE_EXISTS}")
        elif self.plan_filter == "Expired/Cancelled":
            clauses.append(
                """
                EXISTS (
                    SELECT 1 FROM razorpay_subscription se
                     WHERE (se.app_user_id = u.id
                            OR LOWER(se.user_identifier)
                               = LOWER(u.email_normalized))
                       AND se.status IN ('EXPIRED','CANCELLED')
                )
                """
            )
        return " AND ".join(clauses), params

    async def _load_users(self):
        self.is_loading = True
        self.error = ""
        yield
        where, params = self._user_where()
        page = max(int(self.page), 1)
        try:
            async with rx.asession() as session:
                total_row = (
                    await session.execute(
                        text(f"SELECT COUNT(*) FROM app_user u WHERE {where}"),
                        params,
                    )
                ).first()
                total = int(total_row[0] or 0) if total_row else 0
                pages = max((total + PAGE_SIZE - 1) // PAGE_SIZE, 1)
                page = min(page, pages)
                rows = (
                    await session.execute(
                        text(
                            f"""
                            SELECT u.id,
                                   COALESCE(u.display_name, '') AS name,
                                   u.email,
                                   u.created_at,
                                   u.last_login_at,
                                   (SELECT MAX(x.last_seen_at)
                                      FROM app_user_session x
                                     WHERE x.user_id = u.id) AS seen,
                                   (SELECT sp.status
                                      FROM razorpay_subscription sp
                                     WHERE (sp.app_user_id = u.id
                                            OR LOWER(sp.user_identifier)
                                               = LOWER(u.email_normalized))
                                     ORDER BY CASE WHEN sp.status = 'ACTIVE'
                                                   THEN 0 ELSE 1 END, sp.id
                                     LIMIT 1) AS status
                              FROM app_user u
                             WHERE {where}
                             ORDER BY u.created_at DESC, u.id DESC
                             LIMIT :lim OFFSET :off
                            """
                        ),
                        {
                            **params,
                            "lim": PAGE_SIZE,
                            "off": (page - 1) * PAGE_SIZE,
                        },
                    )
                ).all()
        except Exception as e:
            logging.exception(f"Admin users query failed: {e}")
            self.is_loading = False
            self.users = []
            self.users_loaded = True
            self.total_matches = 0
            self.error = DB_ERROR
            return
        self.total_matches = total
        self.page = page
        self.users = [
            {
                "id": int(row[0]),
                "name": str(row[1] or "") or "—",
                "email": str(row[2] or ""),
                "signup": _fmt(row[3]),
                "plan": _plan_of(str(row[6] or "")),
                "status": str(row[6] or "FREE"),
                "last_activity": _latest(row[4], row[5]) or "No activity yet",
            }
            for row in rows
        ]
        self.users_loaded = True
        self.is_loading = False

    async def _read_detail(self, target: int) -> AdminUserDetail | None:
        async with rx.asession() as session:
            row = (
                await session.execute(
                    text(
                        """
                        SELECT u.id,
                               COALESCE(u.display_name, '') AS name,
                               u.email,
                               u.created_at,
                               u.last_login_at,
                               (SELECT MAX(x.last_seen_at)
                                  FROM app_user_session x
                                 WHERE x.user_id = u.id) AS seen
                          FROM app_user u
                         WHERE u.id = :uid
                        """
                    ),
                    {"uid": target},
                )
            ).first()
            if row is None:
                return None
            sub = (
                await session.execute(
                    text(
                        """
                        SELECT s.status,
                               s.activated_at,
                               s.cancelled_at,
                               s.expires_at,
                               COALESCE(s.razorpay_subscription_id, ''),
                               COALESCE(s.razorpay_plan_id, '')
                          FROM razorpay_subscription s
                          LEFT JOIN app_user u ON u.id = :uid
                         WHERE s.app_user_id = :uid
                            OR LOWER(s.user_identifier)
                               = LOWER(u.email_normalized)
                         ORDER BY CASE WHEN s.status = 'ACTIVE'
                                       THEN 0 ELSE 1 END, s.id
                         LIMIT 1
                        """
                    ),
                    {"uid": target},
                )
            ).first()
            feedback = (
                await session.execute(
                    text(
                        "SELECT COUNT(*) FROM app_feedback WHERE user_id = :uid"
                    ),
                    {"uid": target},
                )
            ).first()
            purchases = (
                await session.execute(
                    text(
                        """
                        SELECT COUNT(DISTINCT COALESCE(
                                   e.razorpay_payment_id,
                                   'event:' || e.razorpay_event_id))
                          FROM razorpay_webhook_event e
                         WHERE e.event_name IN (:e1, :e2)
                           AND e.razorpay_subscription_id IS NOT NULL
                           AND e.razorpay_subscription_id IN (
                               SELECT s.razorpay_subscription_id
                                 FROM razorpay_subscription s
                                 LEFT JOIN app_user u ON u.id = :uid
                                WHERE (s.app_user_id = :uid
                                       OR LOWER(s.user_identifier)
                                          = LOWER(u.email_normalized))
                                  AND s.razorpay_subscription_id IS NOT NULL)
                        """
                    ),
                    {
                        "uid": target,
                        "e1": PURCHASE_EVENTS[0],
                        "e2": PURCHASE_EVENTS[1],
                    },
                )
            ).first()
        status = str(sub[0] or "") if sub is not None else ""
        return {
            "id": int(row[0]),
            "name": str(row[1] or "") or "—",
            "email": str(row[2] or ""),
            "signup": _fmt(row[3]),
            "last_activity": _latest(row[4], row[5]) or "No activity yet",
            "plan": _plan_of(status),
            "status": status or "FREE",
            "activated_at": _fmt(sub[1]) if sub is not None else "",
            "cancelled_at": _fmt(sub[2]) if sub is not None else "",
            "expires_at": _fmt(sub[3]) if sub is not None else "",
            "subscription_ref": str(sub[4] or "") if sub is not None else "",
            "plan_ref": str(sub[5] or "") if sub is not None else "",
            "feedback_count": int(feedback[0] or 0) if feedback else 0,
            "purchase_count": int(purchases[0] or 0) if purchases else 0,
        }

    async def _read_detail_history(
        self, target: int
    ) -> tuple[list[DetailPurchaseRow], list[DetailFeedbackRow]]:
        """Bounded safe purchase and feedback history for ONE account."""
        async with rx.asession() as session:
            purchase_rows = (
                await session.execute(
                    text(
                        f"""
                        SELECT e.id,
                               e.processed_at,
                               COALESCE(e.razorpay_payment_id, ''),
                               COALESCE(e.safe_metadata, ''),
                               {_EVENT_PLAN} AS plan_ref
                          FROM razorpay_webhook_event e
                         WHERE e.event_name IN {_SUCCESS_IN}
                           AND {_DEDUP}
                           AND e.razorpay_subscription_id IS NOT NULL
                           AND e.razorpay_subscription_id <> ''
                           AND e.razorpay_subscription_id IN
                               {_USER_SUBSCRIPTION_IDS}
                         ORDER BY e.processed_at DESC, e.id DESC
                         LIMIT :lim
                        """
                    ),
                    {**_SUCCESS_PARAMS, "uid": target, "lim": DETAIL_LIMIT},
                )
            ).all()
            feedback_rows = (
                await session.execute(
                    text(
                        """
                        SELECT f.id,
                               f.submitted_at,
                               f.category,
                               f.rating,
                               f.status,
                               f.message
                          FROM app_feedback f
                         WHERE f.user_id = :uid
                         ORDER BY f.submitted_at DESC, f.id DESC
                         LIMIT :lim
                        """
                    ),
                    {"uid": target, "lim": DETAIL_LIMIT},
                )
            ).all()
        purchases: list[DetailPurchaseRow] = []
        for row in purchase_rows:
            data = _meta(row[3])
            amount = data.get("amount_minor_units")
            currency = str(data.get("currency") or "")
            plan = str(data.get("plan_id") or "") or str(row[4] or "")
            purchases.append(
                {
                    "id": int(row[0]),
                    "date": _fmt(row[1]) or NOT_STORED,
                    "amount": (
                        _money(int(amount), currency)
                        if isinstance(amount, int)
                        else NOT_STORED
                    ),
                    "plan": plan or "Plan not stored",
                    "payment_ref": _short(str(row[2] or "")),
                }
            )
        feedback: list[DetailFeedbackRow] = []
        for row in feedback_rows:
            feedback.append(
                {
                    "id": int(row[0]),
                    "submitted": _fmt(row[1]) or NOT_STORED,
                    "category": str(row[2] or ""),
                    "rating": int(row[3] or 0),
                    "status": str(row[4] or "NEW"),
                    "message": str(row[5] or "")[:400],
                }
            )
        return purchases, feedback

    # ------------------------------------------------------ feedback loader

    def _feedback_where(self) -> tuple[str, dict[str, str]]:
        clauses: list[str] = ["f.id IS NOT NULL"]
        params: dict[str, str] = {}
        term = self.feedback_search.strip()
        if term:
            clauses.append(
                "(LOWER(COALESCE(u.display_name, '')) LIKE :fterm"
                " OR LOWER(COALESCE(u.email, '')) LIKE :fterm"
                " OR LOWER(f.message) LIKE :fterm"
                " OR LOWER(f.category) LIKE :fterm"
                " OR CAST(f.id AS VARCHAR(20)) LIKE :fterm)"
            )
            params["fterm"] = f"%{term.lower()}%"
        status = FEEDBACK_STATUS_VALUES.get(self.feedback_filter, "")
        if status:
            clauses.append("f.status = :fstatus")
            params["fstatus"] = status
        return " AND ".join(clauses), params

    async def _load_feedback(self):
        self.is_loading = True
        self.error = ""
        yield
        where, params = self._feedback_where()
        page = max(int(self.feedback_page), 1)
        try:
            async with rx.asession() as session:
                total_row = (
                    await session.execute(
                        text(
                            f"""
                            SELECT COUNT(*)
                              FROM app_feedback f
                              LEFT JOIN app_user u ON u.id = f.user_id
                             WHERE {where}
                            """
                        ),
                        params,
                    )
                ).first()
                total = int(total_row[0] or 0) if total_row else 0
                page = min(page, _pages(total))
                rows = (
                    await session.execute(
                        text(
                            f"""
                            SELECT f.id,
                                   COALESCE(u.display_name, ''),
                                   COALESCE(u.email, ''),
                                   f.rating,
                                   f.category,
                                   f.message,
                                   f.submitted_at,
                                   f.status
                              FROM app_feedback f
                              LEFT JOIN app_user u ON u.id = f.user_id
                             WHERE {where}
                             ORDER BY f.submitted_at DESC, f.id DESC
                             LIMIT :lim OFFSET :off
                            """
                        ),
                        {
                            **params,
                            "lim": PAGE_SIZE,
                            "off": (page - 1) * PAGE_SIZE,
                        },
                    )
                ).all()
        except Exception as e:
            logging.exception(f"Admin feedback query failed: {e}")
            self.is_loading = False
            self.feedback_rows = []
            self.feedback_loaded = True
            self.feedback_total = 0
            self.error = DB_ERROR
            return
        self.feedback_total = total
        self.feedback_page = page
        self.feedback_rows = [
            {
                "id": int(row[0]),
                "name": str(row[1] or "") or NOT_STORED,
                "email": str(row[2] or "") or NOT_STORED,
                "rating": int(row[3] or 0),
                "category": str(row[4] or ""),
                "message": str(row[5] or "")[:600],
                "submitted": _fmt(row[6]) or NOT_STORED,
                "status": str(row[7] or "NEW"),
            }
            for row in rows
        ]
        self.feedback_loaded = True
        self.is_loading = False

    # ----------------------------------------------------- purchases loader

    async def _load_purchases(self):
        self.is_loading = True
        self.error = ""
        yield
        names = PURCHASE_FILTER_EVENTS.get(
            self.purchase_filter, ALL_PAYMENT_EVENTS
        )
        event_in, event_params = _in_clause("pe", names)
        params: dict[str, str] = {**event_params, **_SUCCESS_PARAMS}
        where = f"e.event_name IN {event_in} AND {_DEDUP}"
        page = max(int(self.purchase_page), 1)
        try:
            async with rx.asession() as session:
                total_row = (
                    await session.execute(
                        text(
                            f"""
                            SELECT COUNT(*)
                              FROM razorpay_webhook_event e
                             WHERE {where}
                            """
                        ),
                        params,
                    )
                ).first()
                total = int(total_row[0] or 0) if total_row else 0
                page = min(page, _pages(total))
                rows = (
                    await session.execute(
                        text(
                            f"""
                            SELECT e.id,
                                   e.event_name,
                                   e.processed_at,
                                   COALESCE(e.razorpay_payment_id, ''),
                                   COALESCE(e.razorpay_subscription_id, ''),
                                   COALESCE(e.safe_metadata, ''),
                                   {_EVENT_IDENTITY} AS identity,
                                   {_EVENT_PLAN} AS plan_ref
                              FROM razorpay_webhook_event e
                             WHERE {where}
                             ORDER BY e.processed_at DESC, e.id DESC
                             LIMIT :lim OFFSET :off
                            """
                        ),
                        {
                            **params,
                            "lim": PAGE_SIZE,
                            "off": (page - 1) * PAGE_SIZE,
                        },
                    )
                ).all()
        except Exception as e:
            logging.exception(f"Admin purchases query failed: {e}")
            self.is_loading = False
            self.purchase_rows = []
            self.purchases_loaded = True
            self.purchase_total = 0
            self.error = DB_ERROR
            return
        self.purchase_total = total
        self.purchase_page = page
        records: list[AdminPurchaseRow] = []
        for row in rows:
            data = _meta(row[5])
            amount = data.get("amount_minor_units")
            currency = str(data.get("currency") or "")
            plan = str(data.get("plan_id") or "") or str(row[7] or "")
            records.append(
                {
                    "id": int(row[0]),
                    "customer": str(row[6] or "") or NOT_STORED,
                    "plan": plan or "Plan not stored",
                    "amount": (
                        _money(int(amount), currency)
                        if isinstance(amount, int)
                        else NOT_STORED
                    ),
                    "currency": currency.upper() or NOT_STORED,
                    "status": _purchase_status(str(row[1] or "")),
                    "date": _fmt(row[2]) or NOT_STORED,
                    "payment_ref": _short(str(row[3] or "")),
                    "subscription_ref": _short(str(row[4] or "")),
                }
            )
        self.purchase_rows = records
        self.purchases_loaded = True
        self.is_loading = False

    # ------------------------------------------------- subscriptions loader

    def _subscription_where(self) -> tuple[str, dict[str, str]]:
        clauses: list[str] = ["s.id IS NOT NULL"]
        params: dict[str, str] = {}
        term = self.subscription_search.strip()
        if term:
            clauses.append(
                "(LOWER(COALESCE(u.display_name, '')) LIKE :sterm"
                " OR LOWER(COALESCE(u.email, '')) LIKE :sterm"
                " OR LOWER(s.user_identifier) LIKE :sterm)"
            )
            params["sterm"] = f"%{term.lower()}%"
        status = SUBSCRIPTION_FILTER_STATUS.get(self.subscription_filter, "")
        if status:
            clauses.append("s.status = :sstatus")
            params["sstatus"] = status
        return " AND ".join(clauses), params

    async def _load_subscriptions(self):
        self.is_loading = True
        self.error = ""
        yield
        where, params = self._subscription_where()
        page = max(int(self.subscription_page), 1)
        try:
            async with rx.asession() as session:
                total_row = (
                    await session.execute(
                        text(
                            f"""
                            SELECT COUNT(*)
                              FROM razorpay_subscription s
                              LEFT JOIN app_user u ON u.id = s.app_user_id
                             WHERE {where}
                            """
                        ),
                        params,
                    )
                ).first()
                total = int(total_row[0] or 0) if total_row else 0
                page = min(page, _pages(total))
                rows = (
                    await session.execute(
                        text(
                            f"""
                            SELECT s.id,
                                   COALESCE(u.display_name, ''),
                                   COALESCE(u.email, ''),
                                   COALESCE(s.user_identifier, ''),
                                   s.status,
                                   s.activated_at,
                                   s.cancelled_at,
                                   s.expires_at,
                                   COALESCE(s.razorpay_subscription_id, ''),
                                   COALESCE(s.razorpay_payment_id, ''),
                                   s.created_at
                              FROM razorpay_subscription s
                              LEFT JOIN app_user u ON u.id = s.app_user_id
                             WHERE {where}
                             ORDER BY s.created_at DESC, s.id DESC
                             LIMIT :lim OFFSET :off
                            """
                        ),
                        {
                            **params,
                            "lim": PAGE_SIZE,
                            "off": (page - 1) * PAGE_SIZE,
                        },
                    )
                ).all()
        except Exception as e:
            logging.exception(f"Admin subscriptions query failed: {e}")
            self.is_loading = False
            self.subscription_rows = []
            self.subscriptions_loaded = True
            self.subscription_total = 0
            self.error = DB_ERROR
            return
        self.subscription_total = total
        self.subscription_page = page
        records: list[AdminSubscriptionRow] = []
        for row in rows:
            status = str(row[4] or "FREE")
            started = _fmt(row[5]) or _fmt(row[10])
            ended = _fmt(row[6]) or _fmt(row[7])
            records.append(
                {
                    "id": int(row[0]),
                    "name": str(row[1] or "") or NOT_STORED,
                    "email": str(row[2] or "") or NOT_STORED,
                    "identifier": str(row[3] or "") or NOT_STORED,
                    "plan": _plan_of(status),
                    "status": status,
                    "started": started or NOT_STORED,
                    "ended": ended or NOT_STORED,
                    "subscription_ref": _short(str(row[8] or "")),
                    "payment_ref": _short(str(row[9] or "")),
                }
            )
        self.subscription_rows = records
        self.subscriptions_loaded = True
        self.is_loading = False

    # -------------------------------------------------------- revenue loader

    async def _load_revenue(self):
        self.is_loading = True
        self.error = ""
        yield
        try:
            async with rx.asession() as session:
                rows = (
                    await session.execute(
                        text(
                            f"""
                            SELECT e.id,
                                   e.processed_at,
                                   COALESCE(e.razorpay_payment_id, ''),
                                   COALESCE(e.safe_metadata, ''),
                                   {_EVENT_PLAN} AS plan_ref
                              FROM razorpay_webhook_event e
                             WHERE e.event_name IN {_SUCCESS_IN}
                               AND {_DEDUP}
                             ORDER BY e.processed_at DESC, e.id DESC
                             LIMIT :cap
                            """
                        ),
                        {**_SUCCESS_PARAMS, "cap": REVENUE_SCAN_LIMIT},
                    )
                ).all()
        except Exception as e:
            logging.exception(f"Admin revenue query failed: {e}")
            self.is_loading = False
            self.revenue_currencies = []
            self.revenue_plans = []
            self.revenue_recent = []
            self.revenue_success_count = 0
            self.revenue_missing_amount = 0
            self.revenue_loaded = True
            self.error = DB_ERROR
            return

        currency_totals: dict[str, int] = {}
        currency_counts: dict[str, int] = {}
        plan_totals: dict[tuple[str, str], int] = {}
        plan_counts: dict[tuple[str, str], int] = {}
        recent: list[RevenueTxnRow] = []
        success_count = 0
        missing_amount = 0

        for row in rows:
            success_count += 1
            data = _meta(row[3])
            amount = data.get("amount_minor_units")
            currency = str(data.get("currency") or "").upper() or "UNKNOWN"
            plan = (
                str(data.get("plan_id") or "")
                or str(row[4] or "")
                or "Plan not stored"
            )
            if not isinstance(amount, int):
                missing_amount += 1
                if len(recent) < RECENT_LIMIT:
                    recent.append(
                        {
                            "id": int(row[0]),
                            "date": _fmt(row[1]) or NOT_STORED,
                            "amount": NOT_STORED,
                            "plan": plan,
                            "payment_ref": _short(str(row[2] or "")),
                        }
                    )
                continue
            currency_totals[currency] = (
                currency_totals.get(currency, 0) + amount
            )
            currency_counts[currency] = currency_counts.get(currency, 0) + 1
            key = (currency, plan)
            plan_totals[key] = plan_totals.get(key, 0) + amount
            plan_counts[key] = plan_counts.get(key, 0) + 1
            if len(recent) < RECENT_LIMIT:
                recent.append(
                    {
                        "id": int(row[0]),
                        "date": _fmt(row[1]) or NOT_STORED,
                        "amount": _money(amount, currency),
                        "plan": plan,
                        "payment_ref": _short(str(row[2] or "")),
                    }
                )

        self.revenue_currencies = [
            {
                "currency": code,
                "total": _money(total, code),
                "count": currency_counts.get(code, 0),
            }
            for code, total in sorted(
                currency_totals.items(), key=lambda item: -item[1]
            )
        ]
        plans: list[RevenuePlanRow] = []
        for (code, plan), total in sorted(
            plan_totals.items(), key=lambda item: -item[1]
        ):
            base = currency_totals.get(code, 0)
            share = int(round(total * 100 / base)) if base > 0 else 0
            plans.append(
                {
                    "plan": plan,
                    "total": _money(total, code),
                    "count": plan_counts.get((code, plan), 0),
                    "share_label": f"{max(min(share, 100), 2)}%",
                }
            )
        self.revenue_plans = plans
        self.revenue_recent = recent
        self.revenue_success_count = success_count
        self.revenue_missing_amount = missing_amount
        self.revenue_loaded = True
        self.is_loading = False
