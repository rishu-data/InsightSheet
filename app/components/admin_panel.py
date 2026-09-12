"""Admin Control Center UI — shell, overview and users views.

Only safe, already-sanitised state values are rendered here. Nothing in this
module can widen access: every dataset it displays was loaded by an event that
re-verified `app_user.is_admin` server-side.
"""

import reflex as rx

from app.states.admin_state import (
    FEEDBACK_FILTERS,
    FILTERS,
    PURCHASE_FILTERS,
    SUBSCRIPTION_FILTERS,
    AdminFeedbackRow,
    AdminPurchaseRow,
    AdminState,
    AdminSubscriptionRow,
    AdminUserRow,
    DetailFeedbackRow,
    DetailPurchaseRow,
    RevenueCurrencyRow,
    RevenuePlanRow,
    RevenueTxnRow,
)

_NAV: list[tuple[str, str, bool]] = [
    ("layout-dashboard", "Overview", True),
    ("users-round", "Users", True),
    ("message-square-heart", "Feedback", True),
    ("receipt", "Purchases", True),
    ("credit-card", "Subscriptions", True),
    ("indian-rupee", "Revenue", True),
    ("activity", "Usage", True),
]

_CARD = "rounded-2xl border border-gray-200 bg-white shadow-sm"


def _brand() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("shield-check", class_name="h-4 w-4 text-white"),
            class_name="flex items-center justify-center h-8 w-8 rounded-lg bg-blue-600 shrink-0",
        ),
        rx.el.div(
            rx.el.p(
                "Admin Control Center",
                class_name="text-sm font-semibold text-gray-900",
            ),
            rx.el.p(
                "InsightSheet operations",
                class_name="text-xs font-medium text-gray-500",
            ),
            class_name="min-w-0",
        ),
        class_name="flex items-center gap-2.5 min-w-0",
    )


def _nav_item(icon: str, label: str, ready: bool) -> rx.Component:
    return rx.cond(
        ready,
        rx.el.button(
            rx.icon(icon, class_name="h-4 w-4 shrink-0"),
            rx.el.span(label, class_name="truncate"),
            on_click=lambda: AdminState.select_tab(label),
            class_name=rx.cond(
                AdminState.active_tab == label,
                "flex items-center gap-3 w-full rounded-xl bg-blue-50 px-3 py-2.5 text-sm font-semibold text-blue-700 transition-colors",
                "flex items-center gap-3 w-full rounded-xl px-3 py-2.5 text-sm font-medium text-gray-600 hover:bg-gray-100 hover:text-gray-900 transition-colors",
            ),
        ),
        rx.el.div(
            rx.icon(icon, class_name="h-4 w-4 shrink-0 text-gray-300"),
            rx.el.span(label, class_name="truncate"),
            rx.el.span(
                "Soon",
                class_name="ml-auto w-fit rounded-full border border-gray-200 bg-gray-50 px-2 py-0.5 text-[10px] font-semibold text-gray-400",
            ),
            class_name="flex items-center gap-3 w-full rounded-xl px-3 py-2.5 text-sm font-medium text-gray-400 cursor-not-allowed",
        ),
    )


def _pill(icon: str, label: str, ready: bool) -> rx.Component:
    return rx.cond(
        ready,
        rx.el.button(
            rx.icon(icon, class_name="h-3.5 w-3.5 shrink-0"),
            rx.el.span(label),
            on_click=lambda: AdminState.select_tab(label),
            class_name=rx.cond(
                AdminState.active_tab == label,
                "flex items-center gap-2 shrink-0 w-fit rounded-full bg-blue-600 px-3.5 py-1.5 text-xs font-semibold text-white",
                "flex items-center gap-2 shrink-0 w-fit rounded-full border border-gray-200 bg-white px-3.5 py-1.5 text-xs font-medium text-gray-600 hover:border-blue-300 hover:text-blue-700 transition-colors",
            ),
        ),
        rx.el.div(
            rx.icon(icon, class_name="h-3.5 w-3.5 shrink-0"),
            rx.el.span(label),
            class_name="flex items-center gap-2 shrink-0 w-fit rounded-full border border-dashed border-gray-200 bg-gray-50 px-3.5 py-1.5 text-xs font-medium text-gray-400",
        ),
    )


def _sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            _brand(),
            class_name="flex items-center h-16 px-5 border-b border-gray-200 shrink-0",
        ),
        rx.el.nav(
            _nav_item(_NAV[0][0], _NAV[0][1], _NAV[0][2]),
            _nav_item(_NAV[1][0], _NAV[1][1], _NAV[1][2]),
            _nav_item(_NAV[2][0], _NAV[2][1], _NAV[2][2]),
            _nav_item(_NAV[3][0], _NAV[3][1], _NAV[3][2]),
            _nav_item(_NAV[4][0], _NAV[4][1], _NAV[4][2]),
            _nav_item(_NAV[5][0], _NAV[5][1], _NAV[5][2]),
            _nav_item(_NAV[6][0], _NAV[6][1], _NAV[6][2]),
            class_name="flex min-h-0 w-full min-w-0 flex-1 flex-col gap-1 overflow-y-auto p-4",
        ),
        rx.el.div(
            rx.el.div(
                rx.icon(
                    "lock",
                    class_name="h-3.5 w-3.5 text-gray-400 mt-0.5 shrink-0",
                ),
                rx.el.p(
                    "Admin access is verified on the server for every action. "
                    "Credentials and payment secrets are never loaded here.",
                    class_name="text-xs font-medium text-gray-500",
                ),
                class_name="flex items-start gap-2 rounded-xl border border-gray-200 bg-gray-50 p-3",
            ),
            rx.el.a(
                rx.icon("arrow-left", class_name="h-3.5 w-3.5"),
                "Back to app",
                href="/dashboard",
                class_name="flex items-center justify-center gap-2 w-full rounded-xl border border-gray-200 bg-white px-3 py-2 text-xs font-semibold text-gray-600 hover:border-blue-300 hover:text-blue-700 transition-colors mt-3",
            ),
            class_name="p-4 shrink-0",
        ),
        class_name="hidden lg:flex h-full w-64 shrink-0 flex-col border-r border-gray-200 bg-white",
    )


def _top_bar() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    AdminState.active_tab,
                    class_name="text-lg font-semibold text-gray-900 truncate",
                ),
                rx.el.p(
                    "Operational data read live from the InsightSheet database",
                    class_name="text-xs font-medium text-gray-500 truncate",
                ),
                class_name="min-w-0",
            ),
            rx.el.div(_brand(), class_name="lg:hidden"),
            rx.el.button(
                rx.icon("refresh-cw", class_name="h-3.5 w-3.5"),
                rx.el.span("Refresh", class_name="hidden sm:inline"),
                on_click=AdminState.refresh,
                disabled=AdminState.is_loading,
                class_name="flex items-center gap-2 shrink-0 w-fit rounded-full border border-gray-200 bg-white px-3.5 py-1.5 text-xs font-semibold text-gray-600 hover:border-blue-300 hover:text-blue-700 disabled:opacity-60 transition-colors",
            ),
            class_name="flex items-center justify-between gap-4 px-4 sm:px-6 lg:px-8 h-16",
        ),
        rx.el.div(
            _pill(_NAV[0][0], _NAV[0][1], _NAV[0][2]),
            _pill(_NAV[1][0], _NAV[1][1], _NAV[1][2]),
            _pill(_NAV[2][0], _NAV[2][1], _NAV[2][2]),
            _pill(_NAV[3][0], _NAV[3][1], _NAV[3][2]),
            _pill(_NAV[4][0], _NAV[4][1], _NAV[4][2]),
            _pill(_NAV[5][0], _NAV[5][1], _NAV[5][2]),
            _pill(_NAV[6][0], _NAV[6][1], _NAV[6][2]),
            class_name="lg:hidden flex items-center gap-2 overflow-x-auto px-4 sm:px-6 pb-3",
        ),
        class_name="w-full shrink-0 border-b border-gray-200 bg-white/85 backdrop-blur-sm",
    )


def _kpi(icon: str, label: str, value: rx.Var | str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name="h-3.5 w-3.5 text-blue-600"),
            rx.el.p(label, class_name="text-xs font-medium text-gray-500"),
            class_name="flex items-center gap-2",
        ),
        rx.el.p(
            value,
            class_name="text-2xl font-semibold tracking-tight text-gray-900 mt-2",
        ),
        class_name=f"{_CARD} w-full p-4",
    )


def _error_banner(message: rx.Var) -> rx.Component:
    return rx.el.div(
        rx.icon("triangle-alert", class_name="h-4 w-4 text-red-500 shrink-0"),
        rx.el.p(message, class_name="text-sm font-medium text-red-600"),
        class_name="flex items-start gap-2 rounded-xl border border-red-200 bg-red-50 p-4 w-full",
    )


def _skeleton() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            class_name="animate-pulse rounded-2xl bg-gray-200 h-24 w-full"
        ),
        rx.el.div(
            class_name="animate-pulse rounded-2xl bg-gray-200 h-24 w-full"
        ),
        rx.el.div(
            class_name="animate-pulse rounded-2xl bg-gray-200 h-24 w-full"
        ),
        rx.el.div(
            class_name="animate-pulse rounded-2xl bg-gray-200 h-24 w-full"
        ),
        class_name="grid grid-cols-2 lg:grid-cols-4 gap-4 w-full",
    )


def _activity_counter(label: str, value: rx.Var) -> rx.Component:
    return rx.el.div(
        rx.el.p(
            value,
            class_name="text-xl font-semibold tracking-tight text-gray-900",
        ),
        rx.el.p(label, class_name="text-xs font-medium text-gray-500 mt-0.5"),
        class_name="rounded-xl border border-gray-200 bg-gray-50 p-3 w-full",
    )


def _overview() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        AdminState.period_label,
                        class_name="w-fit rounded-full bg-blue-50 px-2.5 py-1 text-[11px] font-semibold text-blue-700",
                    ),
                    rx.el.h2(
                        "Operational overview",
                        class_name="text-xl font-semibold tracking-tight text-gray-900 mt-2",
                    ),
                    rx.el.p(
                        "Live counts from accounts, subscriptions, verified "
                        "payment webhooks and feedback.",
                        class_name="text-sm font-medium text-gray-500",
                    ),
                    class_name="min-w-0",
                ),
                rx.el.div(
                    _activity_counter(
                        "New users (7d)", AdminState.new_users_7d
                    ),
                    _activity_counter(
                        "New purchases (7d)", AdminState.new_purchases_7d
                    ),
                    _activity_counter(
                        "New feedback (7d)", AdminState.new_feedback_7d
                    ),
                    class_name="grid grid-cols-3 gap-3 w-full lg:w-auto lg:min-w-[420px]",
                ),
                class_name="flex flex-col lg:flex-row lg:items-end lg:justify-between gap-5 w-full",
            ),
            rx.el.div(
                rx.icon(
                    "database",
                    class_name="h-3.5 w-3.5 text-gray-400 mt-0.5 shrink-0",
                ),
                rx.el.p(
                    "Source: app accounts, subscription records and verified "
                    "Razorpay webhook events. No plan-price estimates, no "
                    "sample data, no credentials.",
                    class_name="text-xs font-medium text-gray-500",
                ),
                class_name="flex items-start gap-2 rounded-xl border border-gray-200 bg-gray-50 p-3 mt-5",
            ),
            class_name=f"{_CARD} w-full p-5",
        ),
        rx.el.div(
            _kpi("users-round", "Total users", AdminState.total_users),
            _kpi("user", "Free users", AdminState.free_users),
            _kpi("crown", "Pro users", AdminState.pro_users),
            _kpi(
                "credit-card",
                "Active subscriptions",
                AdminState.active_subscriptions,
            ),
            class_name="grid grid-cols-2 lg:grid-cols-4 gap-4 w-full",
        ),
        rx.el.div(
            _kpi(
                "circle-slash",
                "Expired / cancelled",
                AdminState.ended_subscriptions,
            ),
            _kpi("receipt", "Purchase events", AdminState.purchase_events),
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "indian-rupee", class_name="h-3.5 w-3.5 text-blue-600"
                    ),
                    rx.el.p(
                        "Total revenue",
                        class_name="text-xs font-medium text-gray-500",
                    ),
                    class_name="flex items-center gap-2",
                ),
                rx.el.p(
                    AdminState.revenue_display,
                    class_name=rx.cond(
                        AdminState.revenue_available,
                        "text-2xl font-semibold tracking-tight text-gray-900 mt-2",
                        "text-xl font-semibold tracking-tight text-amber-600 mt-2",
                    ),
                ),
                rx.el.p(
                    AdminState.revenue_note,
                    class_name="text-xs font-medium text-gray-500 mt-2",
                ),
                class_name=f"{_CARD} w-full p-4 col-span-2",
            ),
            class_name="grid grid-cols-2 lg:grid-cols-4 gap-4 w-full",
        ),
        class_name="flex flex-col gap-5 w-full",
    )


def _filter_button(label: str) -> rx.Component:
    return rx.el.button(
        label,
        on_click=lambda: AdminState.set_filter(label),
        class_name=rx.cond(
            AdminState.plan_filter == label,
            "w-fit shrink-0 rounded-full bg-blue-600 px-3.5 py-1.5 text-xs font-semibold text-white",
            "w-fit shrink-0 rounded-full border border-gray-200 bg-white px-3.5 py-1.5 text-xs font-medium text-gray-600 hover:border-blue-300 hover:text-blue-700 transition-colors",
        ),
    )


def _plan_badge(plan: rx.Var) -> rx.Component:
    return rx.el.span(
        plan,
        class_name=rx.cond(
            plan == "Pro",
            "w-fit rounded-full bg-blue-100 px-2 py-0.5 text-[11px] font-semibold text-blue-700",
            "w-fit rounded-full bg-gray-100 px-2 py-0.5 text-[11px] font-semibold text-gray-600",
        ),
    )


def _user_row(row: AdminUserRow) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            row["id"],
            class_name="px-4 py-3 text-xs font-medium text-gray-500 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.p(
                row["name"],
                class_name="text-sm font-semibold text-gray-900 truncate",
            ),
            rx.el.p(
                row["email"],
                class_name="text-xs font-medium text-gray-500 truncate",
            ),
            class_name="px-4 py-3 max-w-[240px]",
        ),
        rx.el.td(
            row["signup"],
            class_name="px-4 py-3 text-xs font-medium text-gray-600 whitespace-nowrap hidden md:table-cell",
        ),
        rx.el.td(_plan_badge(row["plan"]), class_name="px-4 py-3"),
        rx.el.td(
            row["status"],
            class_name="px-4 py-3 text-xs font-medium text-gray-600 whitespace-nowrap hidden lg:table-cell",
        ),
        rx.el.td(
            row["last_activity"],
            class_name="px-4 py-3 text-xs font-medium text-gray-600 whitespace-nowrap hidden lg:table-cell",
        ),
        rx.el.td(
            rx.el.button(
                "View",
                on_click=lambda: AdminState.select_user(row["id"]),
                class_name="w-fit rounded-lg border border-gray-200 bg-white px-2.5 py-1 text-xs font-semibold text-blue-700 hover:border-blue-300 transition-colors",
            ),
            class_name="px-4 py-3 text-right",
        ),
        class_name="border-t border-gray-100 hover:bg-gray-50 transition-colors",
    )


def _users_table() -> rx.Component:
    return rx.el.div(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    rx.el.th(
                        "ID",
                        class_name="px-4 py-2.5 text-left text-xs font-semibold text-gray-500",
                    ),
                    rx.el.th(
                        "Account",
                        class_name="px-4 py-2.5 text-left text-xs font-semibold text-gray-500",
                    ),
                    rx.el.th(
                        "Signed up",
                        class_name="px-4 py-2.5 text-left text-xs font-semibold text-gray-500 hidden md:table-cell",
                    ),
                    rx.el.th(
                        "Plan",
                        class_name="px-4 py-2.5 text-left text-xs font-semibold text-gray-500",
                    ),
                    rx.el.th(
                        "Subscription",
                        class_name="px-4 py-2.5 text-left text-xs font-semibold text-gray-500 hidden lg:table-cell",
                    ),
                    rx.el.th(
                        "Last activity",
                        class_name="px-4 py-2.5 text-left text-xs font-semibold text-gray-500 hidden lg:table-cell",
                    ),
                    rx.el.th("", class_name="px-4 py-2.5"),
                    class_name="bg-gray-50",
                ),
            ),
            rx.el.tbody(rx.foreach(AdminState.users, _user_row)),
            class_name="table-auto w-full min-w-[640px]",
        ),
        class_name="w-full overflow-x-auto",
    )


def _empty_users() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("user-round-search", class_name="h-5 w-5 text-blue-600"),
            class_name="flex items-center justify-center h-10 w-10 rounded-xl bg-blue-50 mb-3",
        ),
        rx.el.p(
            "No accounts match this search or filter",
            class_name="text-sm font-semibold text-gray-900",
        ),
        rx.el.p(
            "Try a different name, email or account id.",
            class_name="text-xs font-medium text-gray-500 mt-1",
        ),
        class_name="flex flex-col items-center justify-center px-6 py-14 w-full",
    )


def _pagination() -> rx.Component:
    return rx.el.div(
        rx.el.p(
            AdminState.range_label,
            class_name="text-xs font-medium text-gray-500",
        ),
        rx.el.div(
            rx.el.button(
                rx.icon("chevron-left", class_name="h-3.5 w-3.5"),
                "Previous",
                on_click=AdminState.prev_page,
                disabled=~AdminState.can_prev,
                class_name="flex items-center gap-1.5 w-fit rounded-xl border border-gray-200 bg-white px-3 py-1.5 text-xs font-semibold text-gray-600 hover:border-blue-300 hover:text-blue-700 disabled:opacity-50 transition-colors",
            ),
            rx.el.p(
                f"Page {AdminState.page} of {AdminState.total_pages}",
                class_name="text-xs font-medium text-gray-500 px-1",
            ),
            rx.el.button(
                "Next",
                rx.icon("chevron-right", class_name="h-3.5 w-3.5"),
                on_click=AdminState.next_page,
                disabled=~AdminState.can_next,
                class_name="flex items-center gap-1.5 w-fit rounded-xl border border-gray-200 bg-white px-3 py-1.5 text-xs font-semibold text-gray-600 hover:border-blue-300 hover:text-blue-700 disabled:opacity-50 transition-colors",
            ),
            class_name="flex items-center gap-2",
        ),
        class_name="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 border-t border-gray-100 px-4 py-3",
    )


def _th(label: str, extra: str = "") -> rx.Component:
    return rx.el.th(
        label,
        class_name=f"px-4 py-2.5 text-left text-xs font-semibold text-gray-500 {extra}",
    )


def _table_shell(*children: rx.Component) -> rx.Component:
    return rx.el.div(*children, class_name="w-full overflow-x-auto")


def _empty_state(icon: str, title: str, body: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name="h-5 w-5 text-blue-600"),
            class_name="flex items-center justify-center h-10 w-10 rounded-xl bg-blue-50 mb-3",
        ),
        rx.el.p(title, class_name="text-sm font-semibold text-gray-900"),
        rx.el.p(
            body,
            class_name="text-xs font-medium text-gray-500 mt-1 text-center max-w-md",
        ),
        class_name="flex flex-col items-center justify-center px-6 py-14 w-full",
    )


def _pager(
    label: rx.Var,
    page: rx.Var,
    pages: rx.Var,
    can_prev: rx.Var,
    can_next: rx.Var,
    on_prev: rx.event.EventType,
    on_next: rx.event.EventType,
) -> rx.Component:
    return rx.el.div(
        rx.el.p(label, class_name="text-xs font-medium text-gray-500"),
        rx.el.div(
            rx.el.button(
                rx.icon("chevron-left", class_name="h-3.5 w-3.5"),
                "Previous",
                on_click=on_prev,
                disabled=~can_prev,
                class_name="flex items-center gap-1.5 w-fit rounded-xl border border-gray-200 bg-white px-3 py-1.5 text-xs font-semibold text-gray-600 hover:border-blue-300 hover:text-blue-700 disabled:opacity-50 transition-colors",
            ),
            rx.el.p(
                f"Page {page} of {pages}",
                class_name="text-xs font-medium text-gray-500 px-1",
            ),
            rx.el.button(
                "Next",
                rx.icon("chevron-right", class_name="h-3.5 w-3.5"),
                on_click=on_next,
                disabled=~can_next,
                class_name="flex items-center gap-1.5 w-fit rounded-xl border border-gray-200 bg-white px-3 py-1.5 text-xs font-semibold text-gray-600 hover:border-blue-300 hover:text-blue-700 disabled:opacity-50 transition-colors",
            ),
            class_name="flex items-center gap-2",
        ),
        class_name="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 border-t border-gray-100 px-4 py-3",
    )


def _search_box(
    placeholder: str, value: rx.Var, on_change: rx.event.EventType
) -> rx.Component:
    return rx.el.div(
        rx.icon(
            "search",
            class_name="h-4 w-4 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2",
        ),
        rx.el.input(
            placeholder=placeholder,
            default_value=value,
            on_change=on_change,
            class_name="w-full rounded-xl border border-gray-300 bg-white pl-9 pr-4 py-2 text-sm font-medium text-gray-900 focus:border-blue-500 focus:ring-2 focus:ring-blue-500 outline-hidden",
        ),
        class_name="relative w-full sm:max-w-sm",
    )


def _chip(
    label: str, active: rx.Var, on_click: rx.event.EventType
) -> rx.Component:
    return rx.el.button(
        label,
        on_click=on_click,
        class_name=rx.cond(
            active,
            "w-fit shrink-0 rounded-full bg-blue-600 px-3.5 py-1.5 text-xs font-semibold text-white",
            "w-fit shrink-0 rounded-full border border-gray-200 bg-white px-3.5 py-1.5 text-xs font-medium text-gray-600 hover:border-blue-300 hover:text-blue-700 transition-colors",
        ),
    )


def _status_badge(value: rx.Var) -> rx.Component:
    return rx.el.span(
        value,
        class_name=rx.match(
            value,
            (
                "ACTIVE",
                "w-fit rounded-full bg-emerald-100 px-2 py-0.5 text-[11px] font-semibold text-emerald-700",
            ),
            (
                "Successful",
                "w-fit rounded-full bg-emerald-100 px-2 py-0.5 text-[11px] font-semibold text-emerald-700",
            ),
            (
                "RESOLVED",
                "w-fit rounded-full bg-emerald-100 px-2 py-0.5 text-[11px] font-semibold text-emerald-700",
            ),
            (
                "PENDING",
                "w-fit rounded-full bg-amber-100 px-2 py-0.5 text-[11px] font-semibold text-amber-700",
            ),
            (
                "Pending",
                "w-fit rounded-full bg-amber-100 px-2 py-0.5 text-[11px] font-semibold text-amber-700",
            ),
            (
                "REVIEWED",
                "w-fit rounded-full bg-blue-100 px-2 py-0.5 text-[11px] font-semibold text-blue-700",
            ),
            (
                "NEW",
                "w-fit rounded-full bg-amber-100 px-2 py-0.5 text-[11px] font-semibold text-amber-700",
            ),
            (
                "Refunded",
                "w-fit rounded-full bg-amber-100 px-2 py-0.5 text-[11px] font-semibold text-amber-700",
            ),
            (
                "Failed",
                "w-fit rounded-full bg-red-100 px-2 py-0.5 text-[11px] font-semibold text-red-700",
            ),
            (
                "PAYMENT_FAILED",
                "w-fit rounded-full bg-red-100 px-2 py-0.5 text-[11px] font-semibold text-red-700",
            ),
            (
                "CANCELLED",
                "w-fit rounded-full bg-red-100 px-2 py-0.5 text-[11px] font-semibold text-red-700",
            ),
            (
                "EXPIRED",
                "w-fit rounded-full bg-gray-100 px-2 py-0.5 text-[11px] font-semibold text-gray-600",
            ),
            "w-fit rounded-full bg-gray-100 px-2 py-0.5 text-[11px] font-semibold text-gray-600",
        ),
    )


# ------------------------------------------------------------------ feedback


def _feedback_filter(label: str) -> rx.Component:
    return _chip(
        label,
        AdminState.feedback_filter == label,
        AdminState.set_feedback_filter(label),
    )


def _feedback_actions(row: AdminFeedbackRow) -> rx.Component:
    return rx.el.div(
        rx.el.button(
            "Reviewed",
            on_click=lambda: AdminState.mark_feedback(row["id"], "REVIEWED"),
            disabled=AdminState.feedback_busy_id == row["id"],
            class_name="w-fit rounded-lg border border-gray-200 bg-white px-2.5 py-1 text-xs font-semibold text-blue-700 hover:border-blue-300 disabled:opacity-50 transition-colors",
        ),
        rx.el.button(
            "Resolved",
            on_click=lambda: AdminState.mark_feedback(row["id"], "RESOLVED"),
            disabled=AdminState.feedback_busy_id == row["id"],
            class_name="w-fit rounded-lg border border-gray-200 bg-white px-2.5 py-1 text-xs font-semibold text-emerald-700 hover:border-emerald-300 disabled:opacity-50 transition-colors",
        ),
        class_name="flex items-center justify-end gap-2",
    )


def _feedback_row(row: AdminFeedbackRow) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            f"#{row['id']}",
            class_name="px-4 py-3 text-xs font-medium text-gray-500 whitespace-nowrap align-top",
        ),
        rx.el.td(
            rx.el.p(
                row["name"],
                class_name="text-sm font-semibold text-gray-900 truncate",
            ),
            rx.el.p(
                row["email"],
                class_name="text-xs font-medium text-gray-500 truncate",
            ),
            class_name="px-4 py-3 max-w-[220px] align-top",
        ),
        rx.el.td(
            rx.el.p(
                row["category"],
                class_name="text-xs font-semibold text-gray-700",
            ),
            rx.el.p(
                f"{row['rating']} / 5",
                class_name="text-xs font-medium text-gray-500",
            ),
            class_name="px-4 py-3 whitespace-nowrap align-top hidden md:table-cell",
        ),
        rx.el.td(
            rx.el.p(
                row["message"],
                class_name="text-xs font-medium text-gray-700 break-words",
            ),
            class_name="px-4 py-3 max-w-[420px] align-top",
        ),
        rx.el.td(
            row["submitted"],
            class_name="px-4 py-3 text-xs font-medium text-gray-600 whitespace-nowrap align-top hidden lg:table-cell",
        ),
        rx.el.td(
            _status_badge(row["status"]),
            class_name="px-4 py-3 align-top",
        ),
        rx.el.td(_feedback_actions(row), class_name="px-4 py-3 align-top"),
        class_name="border-t border-gray-100 hover:bg-gray-50 transition-colors",
    )


def _feedback() -> rx.Component:
    return rx.el.div(
        rx.cond(
            AdminState.feedback_notice != "",
            rx.el.div(
                rx.icon(
                    "info", class_name="h-3.5 w-3.5 text-blue-600 shrink-0"
                ),
                rx.el.p(
                    AdminState.feedback_notice,
                    class_name="text-xs font-medium text-blue-700",
                ),
                class_name="flex items-start gap-2 rounded-xl border border-blue-200 bg-blue-50 p-3 w-full",
            ),
        ),
        rx.el.div(
            rx.el.div(
                _search_box(
                    "Search user, email, message or category",
                    AdminState.feedback_search,
                    AdminState.set_feedback_search.debounce(500),
                ),
                rx.el.div(
                    rx.foreach(FEEDBACK_FILTERS, _feedback_filter),
                    class_name="flex items-center gap-2 overflow-x-auto",
                ),
                class_name="flex flex-col sm:flex-row sm:items-center gap-3 p-4 border-b border-gray-100",
            ),
            rx.cond(
                AdminState.has_feedback,
                rx.el.div(
                    _table_shell(
                        rx.el.table(
                            rx.el.thead(
                                rx.el.tr(
                                    _th("ID"),
                                    _th("User"),
                                    _th("Category", "hidden md:table-cell"),
                                    _th("Message"),
                                    _th("Submitted", "hidden lg:table-cell"),
                                    _th("Status"),
                                    _th("Review"),
                                    class_name="bg-gray-50",
                                ),
                            ),
                            rx.el.tbody(
                                rx.foreach(
                                    AdminState.feedback_rows, _feedback_row
                                )
                            ),
                            class_name="table-auto w-full min-w-[860px]",
                        )
                    ),
                    _pager(
                        AdminState.feedback_range_label,
                        AdminState.feedback_page,
                        AdminState.feedback_pages,
                        AdminState.feedback_can_prev,
                        AdminState.feedback_can_next,
                        AdminState.feedback_prev,
                        AdminState.feedback_next,
                    ),
                    class_name="w-full",
                ),
                _empty_state(
                    "message-square-heart",
                    "No feedback matches this search or status",
                    "Feedback appears here as soon as a signed-in user submits it. New submissions start with the New status.",
                ),
            ),
            class_name=f"{_CARD} w-full min-w-0 overflow-hidden",
        ),
        class_name="flex flex-col gap-4 w-full",
    )


# ----------------------------------------------------------------- purchases


def _purchase_filter(label: str) -> rx.Component:
    return _chip(
        label,
        AdminState.purchase_filter == label,
        AdminState.set_purchase_filter(label),
    )


def _purchase_row(row: AdminPurchaseRow) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.p(
                row["customer"],
                class_name="text-sm font-semibold text-gray-900 truncate",
            ),
            rx.el.p(
                row["payment_ref"],
                class_name="text-xs font-medium text-gray-500 truncate",
            ),
            class_name="px-4 py-3 max-w-[240px]",
        ),
        rx.el.td(
            row["plan"],
            class_name="px-4 py-3 text-xs font-medium text-gray-600 whitespace-nowrap hidden md:table-cell",
        ),
        rx.el.td(
            rx.el.p(
                row["amount"],
                class_name="text-sm font-semibold text-gray-900 whitespace-nowrap",
            ),
            class_name="px-4 py-3",
        ),
        rx.el.td(_status_badge(row["status"]), class_name="px-4 py-3"),
        rx.el.td(
            row["date"],
            class_name="px-4 py-3 text-xs font-medium text-gray-600 whitespace-nowrap hidden lg:table-cell",
        ),
        rx.el.td(
            row["subscription_ref"],
            class_name="px-4 py-3 text-xs font-medium text-gray-500 whitespace-nowrap hidden lg:table-cell",
        ),
        class_name="border-t border-gray-100 hover:bg-gray-50 transition-colors",
    )


def _purchases() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(
                "shield-check",
                class_name="h-3.5 w-3.5 text-gray-400 mt-0.5 shrink-0",
            ),
            rx.el.p(
                "Every record below comes from a signature-verified Razorpay "
                "webhook event and its stored safe metadata. Successful "
                "payments are deduplicated by payment id; nothing is inferred "
                "from plan prices.",
                class_name="text-xs font-medium text-gray-500",
            ),
            class_name="flex items-start gap-2 rounded-xl border border-gray-200 bg-gray-50 p-3 w-full",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "Payment records",
                    class_name="text-sm font-semibold text-gray-900",
                ),
                rx.el.div(
                    rx.foreach(PURCHASE_FILTERS, _purchase_filter),
                    class_name="flex items-center gap-2 overflow-x-auto",
                ),
                class_name="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 p-4 border-b border-gray-100",
            ),
            rx.cond(
                AdminState.has_purchases,
                rx.el.div(
                    _table_shell(
                        rx.el.table(
                            rx.el.thead(
                                rx.el.tr(
                                    _th("Customer"),
                                    _th("Plan", "hidden md:table-cell"),
                                    _th("Amount"),
                                    _th("Status"),
                                    _th("Date", "hidden lg:table-cell"),
                                    _th(
                                        "Subscription",
                                        "hidden lg:table-cell",
                                    ),
                                    class_name="bg-gray-50",
                                ),
                            ),
                            rx.el.tbody(
                                rx.foreach(
                                    AdminState.purchase_rows, _purchase_row
                                )
                            ),
                            class_name="table-auto w-full min-w-[760px]",
                        )
                    ),
                    _pager(
                        AdminState.purchase_range_label,
                        AdminState.purchase_page,
                        AdminState.purchase_pages,
                        AdminState.purchase_can_prev,
                        AdminState.purchase_can_next,
                        AdminState.purchase_prev,
                        AdminState.purchase_next,
                    ),
                    class_name="w-full",
                ),
                _empty_state(
                    "receipt",
                    "No verified payment events stored yet",
                    "Purchases appear here only when Razorpay delivers a signature-verified payment or charge event.",
                ),
            ),
            class_name=f"{_CARD} w-full min-w-0 overflow-hidden",
        ),
        class_name="flex flex-col gap-4 w-full",
    )


# ------------------------------------------------------------- subscriptions


def _subscription_filter(label: str) -> rx.Component:
    return _chip(
        label,
        AdminState.subscription_filter == label,
        AdminState.set_subscription_filter(label),
    )


def _subscription_row(row: AdminSubscriptionRow) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.p(
                row["name"],
                class_name="text-sm font-semibold text-gray-900 truncate",
            ),
            rx.el.p(
                row["identifier"],
                class_name="text-xs font-medium text-gray-500 truncate",
            ),
            class_name="px-4 py-3 max-w-[240px]",
        ),
        rx.el.td(_plan_badge(row["plan"]), class_name="px-4 py-3"),
        rx.el.td(_status_badge(row["status"]), class_name="px-4 py-3"),
        rx.el.td(
            row["started"],
            class_name="px-4 py-3 text-xs font-medium text-gray-600 whitespace-nowrap hidden md:table-cell",
        ),
        rx.el.td(
            row["ended"],
            class_name="px-4 py-3 text-xs font-medium text-gray-600 whitespace-nowrap hidden lg:table-cell",
        ),
        rx.el.td(
            row["subscription_ref"],
            class_name="px-4 py-3 text-xs font-medium text-gray-500 whitespace-nowrap hidden lg:table-cell",
        ),
        class_name="border-t border-gray-100 hover:bg-gray-50 transition-colors",
    )


def _subscriptions() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(
                "lock",
                class_name="h-3.5 w-3.5 text-gray-400 mt-0.5 shrink-0",
            ),
            rx.el.p(
                "Read-only: verified webhook processing remains the single "
                "source of subscription truth, so there are no edit controls "
                "here.",
                class_name="text-xs font-medium text-gray-500",
            ),
            class_name="flex items-start gap-2 rounded-xl border border-gray-200 bg-gray-50 p-3 w-full",
        ),
        rx.el.div(
            rx.el.div(
                _search_box(
                    "Search user, email or identifier",
                    AdminState.subscription_search,
                    AdminState.set_subscription_search.debounce(500),
                ),
                rx.el.div(
                    rx.foreach(SUBSCRIPTION_FILTERS, _subscription_filter),
                    class_name="flex items-center gap-2 overflow-x-auto",
                ),
                class_name="flex flex-col sm:flex-row sm:items-center gap-3 p-4 border-b border-gray-100",
            ),
            rx.cond(
                AdminState.has_subscriptions,
                rx.el.div(
                    _table_shell(
                        rx.el.table(
                            rx.el.thead(
                                rx.el.tr(
                                    _th("User"),
                                    _th("Plan"),
                                    _th("Status"),
                                    _th("Started", "hidden md:table-cell"),
                                    _th(
                                        "Ended / expires",
                                        "hidden lg:table-cell",
                                    ),
                                    _th(
                                        "Subscription",
                                        "hidden lg:table-cell",
                                    ),
                                    class_name="bg-gray-50",
                                ),
                            ),
                            rx.el.tbody(
                                rx.foreach(
                                    AdminState.subscription_rows,
                                    _subscription_row,
                                )
                            ),
                            class_name="table-auto w-full min-w-[760px]",
                        )
                    ),
                    _pager(
                        AdminState.subscription_range_label,
                        AdminState.subscription_page,
                        AdminState.subscription_pages,
                        AdminState.subscription_can_prev,
                        AdminState.subscription_can_next,
                        AdminState.subscription_prev,
                        AdminState.subscription_next,
                    ),
                    class_name="w-full",
                ),
                _empty_state(
                    "credit-card",
                    "No subscription records match",
                    "Subscription rows are created only by verified Razorpay webhook processing.",
                ),
            ),
            class_name=f"{_CARD} w-full min-w-0 overflow-hidden",
        ),
        class_name="flex flex-col gap-4 w-full",
    )


# -------------------------------------------------------------------- revenue


def _revenue_currency(row: RevenueCurrencyRow) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("wallet", class_name="h-3.5 w-3.5 text-blue-600"),
            rx.el.p(
                f"Total revenue ({row['currency']})",
                class_name="text-xs font-medium text-gray-500",
            ),
            class_name="flex items-center gap-2",
        ),
        rx.el.p(
            row["total"],
            class_name="text-2xl font-semibold tracking-tight text-gray-900 mt-2",
        ),
        rx.el.p(
            f"{row['count']} successful payments with stored amounts",
            class_name="text-xs font-medium text-gray-500 mt-1",
        ),
        class_name=f"{_CARD} w-full p-4",
    )


def _revenue_plan(row: RevenuePlanRow) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                row["plan"],
                class_name="text-xs font-semibold text-gray-900 truncate",
            ),
            rx.el.p(
                row["total"],
                class_name="text-xs font-semibold text-gray-700 shrink-0",
            ),
            class_name="flex items-center justify-between gap-3",
        ),
        rx.el.div(
            rx.el.div(
                class_name="h-1.5 rounded-full bg-blue-600",
                style={"width": row["share_label"]},
            ),
            class_name="h-1.5 w-full rounded-full bg-gray-100 mt-2",
        ),
        rx.el.p(
            f"{row['count']} payments · {row['share_label']} of this currency",
            class_name="text-xs font-medium text-gray-500 mt-1.5",
        ),
        class_name="w-full rounded-xl border border-gray-200 bg-white p-3",
    )


def _revenue_txn(row: RevenueTxnRow) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            row["date"],
            class_name="px-4 py-3 text-xs font-medium text-gray-600 whitespace-nowrap",
        ),
        rx.el.td(
            row["amount"],
            class_name="px-4 py-3 text-sm font-semibold text-gray-900 whitespace-nowrap",
        ),
        rx.el.td(
            row["plan"],
            class_name="px-4 py-3 text-xs font-medium text-gray-600 whitespace-nowrap hidden md:table-cell",
        ),
        rx.el.td(
            row["payment_ref"],
            class_name="px-4 py-3 text-xs font-medium text-gray-500 whitespace-nowrap",
        ),
        class_name="border-t border-gray-100 hover:bg-gray-50 transition-colors",
    )


def _revenue() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "Revenue from verified payments",
                    class_name="text-xl font-semibold tracking-tight text-gray-900",
                ),
                rx.el.p(
                    "Calculated only from stored amount metadata on "
                    "signature-verified successful payment events, "
                    "deduplicated by payment id. Currencies are never "
                    "combined.",
                    class_name="text-sm font-medium text-gray-500 mt-1",
                ),
                class_name="min-w-0",
            ),
            rx.el.div(
                _activity_counter(
                    "Successful purchases", AdminState.revenue_success_count
                ),
                _activity_counter(
                    "Without stored amount", AdminState.revenue_missing_amount
                ),
                class_name="grid grid-cols-2 gap-3 w-full lg:w-auto lg:min-w-[300px]",
            ),
            class_name=f"{_CARD} flex flex-col lg:flex-row lg:items-end lg:justify-between gap-5 w-full p-5",
        ),
        rx.cond(
            AdminState.has_revenue,
            rx.el.div(
                rx.el.div(
                    rx.foreach(
                        AdminState.revenue_currencies, _revenue_currency
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 w-full",
                ),
                rx.el.div(
                    rx.el.p(
                        "Revenue by stored plan",
                        class_name="text-sm font-semibold text-gray-900 mb-3",
                    ),
                    rx.el.div(
                        rx.foreach(AdminState.revenue_plans, _revenue_plan),
                        class_name="flex flex-col gap-3 w-full",
                    ),
                    class_name=f"{_CARD} w-full p-4",
                ),
                rx.el.div(
                    rx.el.p(
                        "Recent verified transactions",
                        class_name="text-sm font-semibold text-gray-900 p-4 border-b border-gray-100",
                    ),
                    _table_shell(
                        rx.el.table(
                            rx.el.thead(
                                rx.el.tr(
                                    _th("Date"),
                                    _th("Amount"),
                                    _th("Plan", "hidden md:table-cell"),
                                    _th("Payment"),
                                    class_name="bg-gray-50",
                                ),
                            ),
                            rx.el.tbody(
                                rx.foreach(
                                    AdminState.revenue_recent, _revenue_txn
                                )
                            ),
                            class_name="table-auto w-full min-w-[560px]",
                        )
                    ),
                    class_name=f"{_CARD} w-full min-w-0 overflow-hidden",
                ),
                class_name="flex flex-col gap-5 w-full",
            ),
            rx.el.div(
                _empty_state(
                    "indian-rupee",
                    "No stored payment amounts to report",
                    "Revenue is only shown when a verified successful payment event carries safe amount metadata. Nothing is estimated from plan prices.",
                ),
                class_name=f"{_CARD} w-full",
            ),
        ),
        class_name="flex flex-col gap-5 w-full",
    )


def _detail_line(label: str, value: rx.Var) -> rx.Component:
    return rx.el.div(
        rx.el.p(label, class_name="text-xs font-medium text-gray-500"),
        rx.el.p(
            value,
            class_name="text-sm font-semibold text-gray-900 break-words",
        ),
        class_name="flex flex-col gap-0.5",
    )


def _detail_purchase(row: DetailPurchaseRow) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                row["amount"],
                class_name="text-xs font-semibold text-gray-900",
            ),
            rx.el.p(
                row["date"],
                class_name="text-xs font-medium text-gray-500",
            ),
            class_name="flex items-center justify-between gap-2",
        ),
        rx.el.p(
            row["plan"],
            class_name="text-xs font-medium text-gray-600 truncate",
        ),
        rx.el.p(
            row["payment_ref"],
            class_name="text-[11px] font-medium text-gray-400 truncate",
        ),
        class_name="rounded-xl border border-gray-200 bg-gray-50 p-2.5 w-full",
    )


def _detail_feedback(row: DetailFeedbackRow) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                f"#{row['id']} · {row['category']}",
                class_name="text-xs font-semibold text-gray-900 truncate",
            ),
            _status_badge(row["status"]),
            class_name="flex items-center justify-between gap-2",
        ),
        rx.el.p(
            row["message"],
            class_name="text-xs font-medium text-gray-600 break-words mt-1",
        ),
        rx.el.p(
            f"{row['rating']} / 5 · {row['submitted']}",
            class_name="text-[11px] font-medium text-gray-400 mt-1",
        ),
        class_name="rounded-xl border border-gray-200 bg-gray-50 p-2.5 w-full",
    )


def _detail_panel() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "Account summary",
                    class_name="text-sm font-semibold text-gray-900",
                ),
                rx.el.p(
                    "Safe fields only — no credentials or raw metadata.",
                    class_name="text-xs font-medium text-gray-500",
                ),
                class_name="min-w-0",
            ),
            rx.el.button(
                rx.icon("x", class_name="h-3.5 w-3.5"),
                on_click=AdminState.clear_selection,
                class_name="flex items-center justify-center h-7 w-7 shrink-0 rounded-lg border border-gray-200 bg-white text-gray-500 hover:text-gray-900 transition-colors",
            ),
            class_name="flex items-start justify-between gap-3 border-b border-gray-100 p-4",
        ),
        rx.cond(
            AdminState.detail_loading,
            rx.el.div(
                rx.el.div(
                    class_name="animate-pulse rounded-xl bg-gray-200 h-40 w-full"
                ),
                class_name="p-4",
            ),
            rx.el.div(
                _detail_line("Account id", AdminState.selected["id"]),
                _detail_line("Display name", AdminState.selected["name"]),
                _detail_line("Email", AdminState.selected["email"]),
                _detail_line("Signed up", AdminState.selected["signup"]),
                _detail_line(
                    "Last activity", AdminState.selected["last_activity"]
                ),
                _detail_line("Plan", AdminState.selected["plan"]),
                _detail_line(
                    "Subscription status", AdminState.selected["status"]
                ),
                rx.cond(
                    AdminState.selected["activated_at"] != "",
                    _detail_line(
                        "Activated", AdminState.selected["activated_at"]
                    ),
                ),
                rx.cond(
                    AdminState.selected["cancelled_at"] != "",
                    _detail_line(
                        "Cancelled", AdminState.selected["cancelled_at"]
                    ),
                ),
                rx.cond(
                    AdminState.selected["expires_at"] != "",
                    _detail_line("Expires", AdminState.selected["expires_at"]),
                ),
                rx.cond(
                    AdminState.selected["subscription_ref"] != "",
                    _detail_line(
                        "Subscription reference",
                        AdminState.selected["subscription_ref"],
                    ),
                ),
                rx.cond(
                    AdminState.selected["plan_ref"] != "",
                    _detail_line(
                        "Plan reference", AdminState.selected["plan_ref"]
                    ),
                ),
                _detail_line(
                    "Feedback submissions",
                    AdminState.selected["feedback_count"],
                ),
                _detail_line(
                    "Successful purchases",
                    AdminState.selected["purchase_count"],
                ),
                rx.el.div(
                    rx.el.p(
                        "Recent purchases (max 10)",
                        class_name="text-xs font-semibold text-gray-900",
                    ),
                    rx.cond(
                        AdminState.has_detail_purchases,
                        rx.el.div(
                            rx.foreach(
                                AdminState.selected_purchases,
                                _detail_purchase,
                            ),
                            class_name="flex flex-col gap-2 mt-2",
                        ),
                        rx.el.p(
                            "No verified purchase is reliably linked to this "
                            "account.",
                            class_name="text-xs font-medium text-gray-500 mt-1",
                        ),
                    ),
                    class_name="border-t border-gray-100 pt-3",
                ),
                rx.el.div(
                    rx.el.p(
                        "Recent feedback (max 10)",
                        class_name="text-xs font-semibold text-gray-900",
                    ),
                    rx.cond(
                        AdminState.has_detail_feedback,
                        rx.el.div(
                            rx.foreach(
                                AdminState.selected_feedback,
                                _detail_feedback,
                            ),
                            class_name="flex flex-col gap-2 mt-2",
                        ),
                        rx.el.p(
                            "This account hasn't submitted feedback yet.",
                            class_name="text-xs font-medium text-gray-500 mt-1",
                        ),
                    ),
                    class_name="border-t border-gray-100 pt-3",
                ),
                class_name="flex flex-col gap-3 p-4",
            ),
        ),
        class_name=f"{_CARD} w-full lg:w-80 shrink-0 h-fit",
    )


def _users() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "search",
                        class_name="h-4 w-4 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2",
                    ),
                    rx.el.input(
                        placeholder="Search name, email or account id",
                        default_value=AdminState.search,
                        on_change=AdminState.set_search.debounce(500),
                        class_name="w-full rounded-xl border border-gray-300 bg-white pl-9 pr-4 py-2 text-sm font-medium text-gray-900 focus:border-blue-500 focus:ring-2 focus:ring-blue-500 outline-hidden",
                    ),
                    class_name="relative w-full sm:max-w-sm",
                ),
                rx.el.div(
                    rx.foreach(FILTERS, _filter_button),
                    class_name="flex items-center gap-2 overflow-x-auto",
                ),
                class_name="flex flex-col sm:flex-row sm:items-center gap-3 p-4 border-b border-gray-100",
            ),
            rx.cond(
                AdminState.has_users,
                rx.el.div(_users_table(), _pagination(), class_name="w-full"),
                _empty_users(),
            ),
            class_name=f"{_CARD} flex-1 w-full min-w-0 overflow-hidden",
        ),
        rx.cond(
            AdminState.has_selection | AdminState.detail_loading,
            _detail_panel(),
        ),
        class_name="flex flex-col lg:flex-row gap-5 w-full items-start",
    )


def _usage_note(icon: str, title: str, body: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name="h-4 w-4 text-gray-500"),
            class_name="flex items-center justify-center h-8 w-8 rounded-lg bg-gray-100 shrink-0",
        ),
        rx.el.div(
            rx.el.p(
                title,
                class_name="text-sm font-semibold text-gray-900",
            ),
            rx.el.p(
                body,
                class_name="text-xs font-medium text-gray-500 mt-1",
            ),
            class_name="min-w-0",
        ),
        class_name="flex items-start gap-3 rounded-xl border border-gray-200 bg-white p-4 w-full",
    )


def _usage() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("activity", class_name="h-5 w-5 text-gray-500"),
                class_name="flex items-center justify-center h-10 w-10 rounded-xl bg-gray-100 mb-3",
            ),
            rx.el.p(
                "Usage tracking not available",
                class_name="text-base font-semibold text-gray-900",
            ),
            rx.el.p(
                "The InsightSheet database does not store uploads, generated "
                "reports, analytics feature usage or an activity log, so no "
                "usage figures can be shown without inventing them.",
                class_name="text-sm font-medium text-gray-600 mt-1.5 max-w-2xl",
            ),
            rx.el.span(
                "No data source",
                class_name="w-fit rounded-full border border-gray-200 bg-gray-50 px-2.5 py-1 text-[11px] font-semibold text-gray-500 mt-4",
            ),
            class_name=f"{_CARD} flex flex-col items-start px-6 py-8 w-full",
        ),
        rx.el.div(
            _usage_note(
                "clock",
                "What is available today",
                "Account last login and the latest session last-seen time are "
                "stored, and both are already shown per account in Users.",
            ),
            _usage_note(
                "file-x",
                "What cannot be shown",
                "Upload counts, report counts and analytics feature usage are "
                "never persisted, so per-account or aggregate counts cannot "
                "be reported from current stored data.",
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 gap-4 w-full",
        ),
        rx.el.div(
            rx.icon(
                "info",
                class_name="h-3.5 w-3.5 text-gray-400 mt-0.5 shrink-0",
            ),
            rx.el.p(
                "Enabling usage reporting would require new stored tracking "
                "data. Nothing is estimated, sampled or back-filled here.",
                class_name="text-xs font-medium text-gray-500",
            ),
            class_name="flex items-start gap-2 rounded-xl border border-gray-200 bg-gray-50 p-4 w-full",
        ),
        rx.el.button(
            rx.icon("users-round", class_name="h-3.5 w-3.5"),
            "Open Users for last login and session activity",
            on_click=lambda: AdminState.select_tab("Users"),
            class_name="flex items-center gap-2 w-fit rounded-xl border border-gray-200 bg-white px-4 py-2 text-xs font-semibold text-gray-600 hover:border-blue-300 hover:text-blue-700 transition-colors cursor-pointer",
        ),
        class_name="flex flex-col gap-4 w-full",
    )


def _unauthorized() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("shield-alert", class_name="h-5 w-5 text-red-500"),
            class_name="flex items-center justify-center h-10 w-10 rounded-xl bg-red-50 mb-3",
        ),
        rx.el.p(
            "Admin access required",
            class_name="text-sm font-semibold text-gray-900",
        ),
        rx.el.p(
            "This account isn't authorized for the control center.",
            class_name="text-xs font-medium text-gray-500 mt-1",
        ),
        rx.el.a(
            "Return to dashboard",
            href="/dashboard",
            class_name="w-fit rounded-xl bg-blue-600 px-4 py-2 text-xs font-semibold text-white hover:bg-blue-700 transition-colors mt-4",
        ),
        class_name=f"{_CARD} flex flex-col items-center justify-center px-6 py-16 w-full",
    )


def _content() -> rx.Component:
    return rx.cond(
        AdminState.error != "",
        rx.el.div(
            _error_banner(AdminState.error),
            class_name="flex flex-col gap-5 w-full",
        ),
        rx.cond(
            AdminState.is_loading,
            _skeleton(),
            rx.match(
                AdminState.active_tab,
                ("Overview", _overview()),
                ("Users", _users()),
                ("Feedback", _feedback()),
                ("Purchases", _purchases()),
                ("Subscriptions", _subscriptions()),
                ("Revenue", _revenue()),
                ("Usage", _usage()),
                _usage(),
            ),
        ),
    )


def _authorized_body() -> rx.Component:
    return rx.el.div(
        rx.cond(
            AdminState.detail_error != "",
            _error_banner(AdminState.detail_error),
        ),
        _content(),
        class_name="flex flex-col gap-5 w-full",
    )


def admin_shell() -> rx.Component:
    return rx.el.div(
        _sidebar(),
        rx.el.div(
            _top_bar(),
            rx.el.div(
                rx.cond(
                    AdminState.checked,
                    rx.cond(
                        AdminState.authorized,
                        _authorized_body(),
                        _unauthorized(),
                    ),
                    _skeleton(),
                ),
                class_name="w-full px-4 sm:px-6 lg:px-8 py-6",
            ),
            class_name="flex-1 w-full min-w-0 flex flex-col overflow-y-auto",
        ),
        class_name="font-['Inter'] flex h-dvh w-full overflow-hidden bg-gray-50",
    )
