import reflex as rx

from app.components.feedback_form import (
    feedback_form_card,
    feedback_history_card,
)
from app.components.sidebar import page_shell
from app.states.account_state import (
    NOT_AVAILABLE,
    AccountState,
    ActivityRow,
    BillingRow,
    UntrackedRow,
)
from app.states.auth_state import AuthState

ACCOUNT_TITLE = "My Account — InsightSheet"

_CARD = "rounded-2xl border border-gray-200 bg-white p-6 shadow-sm w-full"
_LABEL = "text-xs font-semibold uppercase tracking-wide text-gray-500"
_VALUE = "text-sm font-semibold text-gray-900 mt-1 break-words"
_MUTED = "text-sm font-medium text-gray-400 mt-1"

_TONES: dict[str, str] = {
    "good": "bg-green-100 text-green-600",
    "bad": "bg-red-100 text-red-500",
    "warn": "bg-yellow-100 text-yellow-600",
    "info": "bg-blue-100 text-blue-500",
    "neutral": "bg-gray-100 text-gray-600",
}


def _tone_class(tone: rx.Var) -> rx.Var:
    return rx.match(
        tone,
        (
            "good",
            f"w-fit rounded-full px-2.5 py-0.5 text-xs font-semibold {_TONES['good']}",
        ),
        (
            "bad",
            f"w-fit rounded-full px-2.5 py-0.5 text-xs font-semibold {_TONES['bad']}",
        ),
        (
            "warn",
            f"w-fit rounded-full px-2.5 py-0.5 text-xs font-semibold {_TONES['warn']}",
        ),
        (
            "info",
            f"w-fit rounded-full px-2.5 py-0.5 text-xs font-semibold {_TONES['info']}",
        ),
        f"w-fit rounded-full px-2.5 py-0.5 text-xs font-semibold {_TONES['neutral']}",
    )


def _dot_class(tone: rx.Var) -> rx.Var:
    return rx.match(
        tone,
        (
            "good",
            "flex items-center justify-center h-8 w-8 rounded-full bg-green-100 text-green-600 shrink-0",
        ),
        (
            "bad",
            "flex items-center justify-center h-8 w-8 rounded-full bg-red-100 text-red-500 shrink-0",
        ),
        (
            "warn",
            "flex items-center justify-center h-8 w-8 rounded-full bg-yellow-100 text-yellow-600 shrink-0",
        ),
        "flex items-center justify-center h-8 w-8 rounded-full bg-blue-100 text-blue-500 shrink-0",
    )


def _field(label: str, value: rx.Var | str) -> rx.Component:
    return rx.el.div(
        rx.el.p(label, class_name=_LABEL),
        rx.el.p(
            value,
            class_name=rx.cond(value == NOT_AVAILABLE, _MUTED, _VALUE),
        ),
        class_name="w-full min-w-0",
    )


def _section_header(
    icon: str, title: str, subtitle: str, badge: rx.Component
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(icon, class_name="h-4 w-4 text-blue-600"),
                class_name="flex items-center justify-center h-9 w-9 rounded-xl bg-blue-50 shrink-0",
            ),
            rx.el.div(
                rx.el.h2(
                    title, class_name="text-base font-semibold text-gray-900"
                ),
                rx.el.p(
                    subtitle,
                    class_name="text-xs font-medium text-gray-500 mt-0.5",
                ),
                class_name="min-w-0",
            ),
            class_name="flex items-start gap-3 min-w-0",
        ),
        badge,
        class_name="flex flex-wrap items-start justify-between gap-3 mb-5",
    )


def _snapshot() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    AuthState.account_initial,
                    class_name="text-lg font-semibold text-white",
                ),
                class_name="flex items-center justify-center h-14 w-14 rounded-2xl bg-blue-600 shrink-0",
            ),
            rx.el.div(
                rx.el.p(
                    AccountState.profile["name"],
                    class_name="text-xl font-semibold tracking-tight text-gray-900 truncate",
                ),
                rx.el.p(
                    AccountState.profile["email"],
                    class_name="text-sm font-medium text-gray-500 truncate",
                ),
                class_name="min-w-0",
            ),
            class_name="flex items-center gap-4 min-w-0",
        ),
        rx.el.div(
            rx.el.span(
                rx.icon("badge-check", class_name="h-3.5 w-3.5"),
                AccountState.plan["name"],
                class_name=rx.cond(
                    AccountState.plan["is_pro"],
                    "flex items-center gap-1.5 w-fit rounded-full bg-blue-600 px-3 py-1 text-xs font-semibold text-white",
                    "flex items-center gap-1.5 w-fit rounded-full bg-gray-100 px-3 py-1 text-xs font-semibold text-gray-700",
                ),
            ),
            rx.el.span(
                rx.icon("circle-dot", class_name="h-3.5 w-3.5"),
                AccountState.profile["status"],
                class_name=rx.cond(
                    AccountState.profile["is_active"],
                    "flex items-center gap-1.5 w-fit rounded-full bg-green-100 px-3 py-1 text-xs font-semibold text-green-600",
                    "flex items-center gap-1.5 w-fit rounded-full bg-red-100 px-3 py-1 text-xs font-semibold text-red-500",
                ),
            ),
            rx.el.span(
                rx.icon("shield", class_name="h-3.5 w-3.5"),
                f"{AccountState.active_session_count} active session(s)",
                class_name="flex items-center gap-1.5 w-fit rounded-full border border-gray-200 bg-white px-3 py-1 text-xs font-medium text-gray-600",
            ),
            rx.el.span(
                rx.icon("message-square-heart", class_name="h-3.5 w-3.5"),
                f"{AccountState.feedback_count} feedback saved",
                class_name="flex items-center gap-1.5 w-fit rounded-full border border-gray-200 bg-white px-3 py-1 text-xs font-medium text-gray-600",
            ),
            class_name="flex flex-wrap items-center gap-2",
        ),
        class_name="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-5 rounded-2xl border border-gray-200 bg-white p-6 shadow-sm w-full",
    )


def _profile_card() -> rx.Component:
    return rx.el.div(
        _section_header(
            "user",
            "Profile",
            "Read directly from your account record — nothing here is editable on this page.",
            rx.el.span(
                AccountState.profile["account_reference"],
                class_name="w-fit rounded-full bg-gray-100 px-3 py-1 text-xs font-medium text-gray-600",
            ),
        ),
        rx.el.div(
            _field("Name", AccountState.profile["name"]),
            _field("Email", AccountState.profile["email"]),
            _field("Account created", AccountState.profile["created_at"]),
            _field("Account status", AccountState.profile["status"]),
            _field(
                "Email verification", AccountState.profile["email_verified"]
            ),
            _field("Latest sign in", AccountState.latest_login),
            class_name="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-5 w-full",
        ),
        rx.el.div(
            rx.icon(
                "info", class_name="h-3.5 w-3.5 text-blue-600 shrink-0 mt-0.5"
            ),
            rx.el.p(
                "Email verification shows as “Not available” because InsightSheet does not store an "
                "email verification field. Passwords are kept only as irreversible hashes and are "
                "never shown here.",
                class_name="text-xs font-medium text-gray-600",
            ),
            class_name="flex items-start gap-2 rounded-xl border border-blue-100 bg-blue-50/60 px-4 py-3 mt-5",
        ),
        class_name=_CARD,
    )


def _plan_card() -> rx.Component:
    return rx.el.div(
        _section_header(
            "credit-card",
            "Current plan",
            "Resolved from your stored subscription record only.",
            rx.el.span(
                AccountState.plan["status"],
                class_name=rx.cond(
                    AccountState.plan["is_pro"],
                    "w-fit rounded-full bg-green-100 px-3 py-1 text-xs font-semibold text-green-600",
                    "w-fit rounded-full bg-gray-100 px-3 py-1 text-xs font-semibold text-gray-600",
                ),
            ),
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p("Plan", class_name=_LABEL),
                rx.el.p(
                    AccountState.plan["name"],
                    class_name="text-2xl font-semibold tracking-tight text-gray-900 mt-1",
                ),
                rx.el.p(
                    AccountState.plan["note"],
                    class_name="text-sm font-medium text-gray-600 mt-2",
                ),
                class_name="min-w-0 flex-1",
            ),
            rx.el.a(
                rx.icon("arrow-up-right", class_name="h-3.5 w-3.5"),
                rx.cond(
                    AccountState.plan["is_pro"],
                    "View plan details",
                    "See Pro pricing",
                ),
                href="/pricing",
                class_name="flex items-center gap-1.5 w-fit shrink-0 rounded-xl border border-gray-200 bg-white px-4 py-2 text-xs font-semibold text-gray-700 hover:border-blue-300 hover:text-blue-700 transition-colors",
            ),
            class_name="flex flex-wrap items-start justify-between gap-4 rounded-xl border border-gray-200 bg-gray-50 p-5",
        ),
        rx.el.div(
            _field("Status", AccountState.plan["status"]),
            _field("Started", AccountState.plan["started_at"]),
            _field("Ends / renews", AccountState.plan["ends_at"]),
            _field("Cancelled", AccountState.plan["cancelled_at"]),
            _field("Plan reference", AccountState.plan["plan_reference"]),
            _field(
                "Subscription reference",
                AccountState.plan["subscription_reference"],
            ),
            class_name="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-5 w-full mt-5",
        ),
        rx.cond(
            AccountState.has_subscription_record,
            rx.fragment(),
            rx.el.p(
                "No subscription record is stored for this account yet, so plan dates show as “Not available”.",
                class_name="text-xs font-medium text-gray-500 mt-4",
            ),
        ),
        class_name=_CARD,
    )


def _billing_row(row: BillingRow) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("receipt", class_name="h-4 w-4"),
                class_name=_dot_class(row["tone"]),
            ),
            rx.el.div(
                rx.el.p(
                    row["label"],
                    class_name="text-sm font-semibold text-gray-900",
                ),
                rx.el.p(
                    row["occurred_at"],
                    class_name="text-xs font-medium text-gray-500 mt-0.5",
                ),
                class_name="min-w-0",
            ),
            class_name="flex items-center gap-3 min-w-0 flex-1",
        ),
        rx.el.div(
            rx.el.p(
                row["amount"],
                class_name="text-sm font-semibold text-gray-900 text-right",
            ),
            rx.el.p(
                row["method"],
                class_name="text-xs font-medium text-gray-500 text-right mt-0.5",
            ),
            class_name="shrink-0",
        ),
        rx.el.div(
            rx.el.span(row["status"], class_name=_tone_class(row["tone"])),
            rx.el.span(
                row["reference"],
                class_name="text-xs font-medium text-gray-400",
            ),
            class_name="flex items-center gap-2 shrink-0",
        ),
        class_name="flex flex-wrap items-center justify-between gap-4 rounded-xl border border-gray-200 bg-white px-4 py-3 hover:border-blue-200 transition-colors w-full",
    )


def _billing_card() -> rx.Component:
    return rx.el.div(
        _section_header(
            "wallet",
            "Billing & purchases",
            "Only signature-verified webhook events linked to your own subscription.",
            rx.el.span(
                f"{AccountState.billing_count} recorded",
                class_name="w-fit rounded-full bg-gray-100 px-3 py-1 text-xs font-medium text-gray-600",
            ),
        ),
        rx.cond(
            AccountState.has_billing,
            rx.el.div(
                rx.foreach(
                    AccountState.billing,
                    lambda row: _billing_row(row),
                ),
                class_name="flex flex-col gap-3 w-full",
            ),
            rx.el.div(
                rx.icon("receipt", class_name="h-5 w-5 text-gray-400"),
                rx.el.p(
                    "No verified purchase or payment events are stored for this account yet. "
                    "Confirmed payments appear here automatically.",
                    class_name="text-sm font-medium text-gray-500 max-w-md text-center",
                ),
                class_name="flex flex-col items-center justify-center gap-2 rounded-xl border border-dashed border-gray-300 bg-gray-50/60 px-6 py-12 w-full",
            ),
        ),
        rx.el.p(
            "Amounts, dates and short references are shown only where they were stored by a verified "
            "webhook. Card numbers, UPI details and payment credentials are never stored or shown.",
            class_name="text-xs font-medium text-gray-500 mt-4",
        ),
        class_name=_CARD,
    )


def _activity_item(row: ActivityRow) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(row["icon"], class_name="h-4 w-4"),
                class_name=_dot_class(row["tone"]),
            ),
            rx.el.div(class_name="w-px flex-1 bg-gray-200 mt-1"),
            class_name="flex flex-col items-center self-stretch shrink-0",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    row["title"],
                    class_name="text-sm font-semibold text-gray-900",
                ),
                rx.el.span(
                    row["occurred_at"],
                    class_name="text-xs font-medium text-gray-400",
                ),
                class_name="flex flex-wrap items-center justify-between gap-2",
            ),
            rx.el.p(
                row["detail"],
                class_name="text-sm font-medium text-gray-600 mt-0.5",
            ),
            class_name="min-w-0 flex-1 pb-5",
        ),
        class_name="flex items-start gap-3 w-full",
    )


def _untracked_item(row: UntrackedRow) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(row["icon"], class_name="h-4 w-4 text-gray-400"),
            class_name="flex items-center justify-center h-8 w-8 rounded-full bg-gray-100 shrink-0",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    row["title"],
                    class_name="text-sm font-semibold text-gray-700",
                ),
                rx.el.span(
                    "Not tracked",
                    class_name="w-fit rounded-full bg-gray-100 px-2.5 py-0.5 text-xs font-semibold text-gray-500",
                ),
                class_name="flex flex-wrap items-center gap-2",
            ),
            rx.el.p(
                row["reason"],
                class_name="text-xs font-medium text-gray-500 mt-0.5",
            ),
            class_name="min-w-0 flex-1",
        ),
        class_name="flex items-start gap-3 rounded-xl border border-gray-200 bg-gray-50/70 px-4 py-3 w-full",
    )


def _activity_card() -> rx.Component:
    return rx.el.div(
        _section_header(
            "history",
            "Account activity",
            "Chronological, based only on events InsightSheet actually persists.",
            rx.el.span(
                f"{AccountState.activity_count} events",
                class_name="w-fit rounded-full bg-gray-100 px-3 py-1 text-xs font-medium text-gray-600",
            ),
        ),
        rx.cond(
            AccountState.has_activity,
            rx.el.div(
                rx.foreach(
                    AccountState.activity,
                    lambda row: _activity_item(row),
                ),
                class_name="flex flex-col w-full",
            ),
            rx.el.div(
                rx.icon("history", class_name="h-5 w-5 text-gray-400"),
                rx.el.p(
                    "No persisted activity is recorded for this account yet.",
                    class_name="text-sm font-medium text-gray-500",
                ),
                class_name="flex flex-col items-center justify-center gap-2 rounded-xl border border-dashed border-gray-300 bg-gray-50/60 px-6 py-12 w-full",
            ),
        ),
        rx.el.div(
            rx.el.p(
                "Not tracked by InsightSheet",
                class_name="text-xs font-semibold uppercase tracking-wide text-gray-500 mb-3",
            ),
            rx.el.div(
                rx.foreach(
                    AccountState.untracked,
                    lambda row: _untracked_item(row),
                ),
                class_name="flex flex-col gap-2 w-full",
            ),
            class_name="w-full pt-5 mt-1 border-t border-gray-100",
        ),
        class_name=_CARD,
    )


def _feedback_section() -> rx.Component:
    return rx.el.div(
        _section_header(
            "message-square-heart",
            "Feedback",
            "Saved against this account only — the same form and history as the Feedback page.",
            rx.el.a(
                rx.icon("arrow-up-right", class_name="h-3.5 w-3.5"),
                "Open Feedback page",
                href="/feedback",
                class_name="flex items-center gap-1.5 w-fit shrink-0 rounded-xl border border-gray-200 bg-white px-4 py-2 text-xs font-semibold text-gray-700 hover:border-blue-300 hover:text-blue-700 transition-colors",
            ),
        ),
        rx.el.div(
            feedback_form_card(),
            feedback_history_card(),
            class_name="flex flex-col gap-6 w-full",
        ),
        class_name=_CARD,
    )


def _account_actions() -> rx.Component:
    return rx.el.div(
        _section_header(
            "settings",
            "Account actions",
            "Only actions this account system actually supports are shown here.",
            rx.el.span(
                AccountState.profile["account_reference"],
                class_name="w-fit rounded-full bg-gray-100 px-3 py-1 text-xs font-medium text-gray-600",
            ),
        ),
        rx.el.div(
            rx.el.a(
                rx.icon("layout-dashboard", class_name="h-4 w-4"),
                "Back to dashboard",
                href="/dashboard",
                class_name="flex items-center gap-2 w-fit rounded-xl border border-gray-200 bg-white px-4 py-2.5 text-sm font-semibold text-gray-700 hover:border-blue-300 hover:text-blue-700 transition-colors",
            ),
            rx.el.button(
                rx.icon("log-out", class_name="h-4 w-4"),
                "Sign out",
                on_click=AuthState.log_out,
                class_name="flex items-center gap-2 w-fit rounded-xl bg-blue-600 px-4 py-2.5 text-sm font-semibold text-white hover:bg-blue-700 transition-colors",
            ),
            class_name="flex flex-wrap items-center gap-3 w-full",
        ),
        rx.el.div(
            rx.icon(
                "info", class_name="h-3.5 w-3.5 text-blue-600 shrink-0 mt-0.5"
            ),
            rx.el.p(
                "Password reset and password change are not offered because InsightSheet's current "
                "auth system has no such flow — passwords are only ever written at sign-up as an "
                "irreversible hash. Signing out revokes this browser's server-side session.",
                class_name="text-xs font-medium text-gray-600",
            ),
            class_name="flex items-start gap-2 rounded-xl border border-blue-100 bg-blue-50/60 px-4 py-3 mt-5",
        ),
        class_name=_CARD,
    )


def _skeleton() -> rx.Component:
    return rx.el.div(
        rx.el.div(class_name="animate-pulse h-24 rounded-2xl bg-gray-200"),
        rx.el.div(class_name="animate-pulse h-56 rounded-2xl bg-gray-200"),
        rx.el.div(class_name="animate-pulse h-56 rounded-2xl bg-gray-200"),
        class_name="flex flex-col gap-6 w-full",
    )


def _error_banner() -> rx.Component:
    return rx.el.div(
        rx.icon(
            "circle-alert", class_name="h-4 w-4 text-red-500 shrink-0 mt-0.5"
        ),
        rx.el.div(
            rx.el.p(
                "We couldn't load your account",
                class_name="text-sm font-semibold text-gray-900",
            ),
            rx.el.p(
                AccountState.load_error,
                class_name="text-sm font-medium text-gray-600 mt-0.5",
            ),
            class_name="min-w-0 flex-1",
        ),
        rx.el.button(
            rx.icon("refresh-cw", class_name="h-3.5 w-3.5"),
            "Try again",
            on_click=AccountState.load_account,
            class_name="flex items-center gap-1.5 w-fit shrink-0 rounded-xl border border-gray-200 bg-white px-4 py-2 text-xs font-semibold text-gray-700 hover:border-blue-300 hover:text-blue-700 transition-colors",
        ),
        class_name="flex flex-wrap items-start gap-3 rounded-2xl border border-red-200 bg-red-100 px-4 py-3 w-full",
    )


def _signed_out() -> rx.Component:
    return rx.el.div(
        rx.icon("lock", class_name="h-5 w-5 text-gray-400"),
        rx.el.p(
            "Sign in to view your account.",
            class_name="text-sm font-medium text-gray-600",
        ),
        rx.el.a(
            "Go to sign in",
            href="/login",
            class_name="w-fit rounded-xl bg-blue-600 px-4 py-2 text-xs font-semibold text-white hover:bg-blue-700 transition-colors",
        ),
        class_name="flex flex-col items-center justify-center gap-3 rounded-2xl border border-dashed border-gray-300 bg-white px-6 py-16 w-full",
    )


def _loaded_body() -> rx.Component:
    return rx.el.div(
        _snapshot(),
        _profile_card(),
        rx.el.div(
            _plan_card(),
            _billing_card(),
            class_name="grid grid-cols-1 xl:grid-cols-2 gap-6 w-full items-start",
        ),
        _activity_card(),
        _feedback_section(),
        _account_actions(),
        class_name="flex flex-col gap-6 w-full",
    )


def _account_body() -> rx.Component:
    return rx.el.div(
        rx.cond(
            AccountState.is_loading | ~AccountState.loaded,
            _skeleton(),
            rx.cond(
                AccountState.has_error,
                _error_banner(),
                rx.cond(AccountState.signed_in, _loaded_body(), _signed_out()),
            ),
        ),
        class_name="flex flex-col gap-6 w-full",
    )


def account_page() -> rx.Component:
    return page_shell(
        "account",
        "My Account",
        "Your profile, plan, billing history and recorded account activity.",
        _account_body(),
    )
