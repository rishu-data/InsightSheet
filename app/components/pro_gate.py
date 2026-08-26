import reflex as rx

from app.states.subscription_state import (
    PRO_LOCK_BODY,
    PRO_LOCK_TITLE,
    SubscriptionState,
)


def _pro_pill() -> rx.Component:
    return rx.el.span(
        rx.icon("sparkles", class_name="h-3.5 w-3.5"),
        "Pro",
        class_name="flex items-center gap-1.5 w-fit shrink-0 rounded-full bg-indigo-600 px-3 py-1 text-xs font-semibold text-white",
    )


def pro_locked_card(title: str, detail: str) -> rx.Component:
    """The standard locked placeholder shown in place of a Pro section."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("lock", class_name="h-5 w-5 text-indigo-600"),
                    class_name="flex items-center justify-center h-11 w-11 rounded-xl bg-indigo-50 shrink-0",
                ),
                rx.el.div(
                    rx.el.h2(
                        title,
                        class_name="text-lg font-semibold text-gray-900",
                    ),
                    rx.el.p(
                        detail,
                        class_name="text-sm font-medium text-gray-500 mt-0.5",
                    ),
                    class_name="min-w-0",
                ),
                class_name="flex items-start gap-3 min-w-0",
            ),
            _pro_pill(),
            class_name="flex flex-wrap items-start justify-between gap-3",
        ),
        rx.el.div(
            rx.icon(
                "info", class_name="h-4 w-4 text-indigo-600 shrink-0 mt-0.5"
            ),
            rx.el.div(
                rx.el.p(
                    SubscriptionState.status_message,
                    class_name="text-sm font-medium text-gray-600",
                ),
                rx.el.p(
                    f"Current plan status: {SubscriptionState.status_label}",
                    class_name="text-xs font-medium text-gray-500 mt-0.5",
                ),
                class_name="min-w-0",
            ),
            class_name="flex items-start gap-2 rounded-xl border border-indigo-100 bg-indigo-50/50 p-4 mt-4",
        ),
        rx.el.div(
            rx.el.a(
                rx.icon("credit-card", class_name="h-4 w-4"),
                rx.cond(
                    SubscriptionState.show_try_again,
                    "Try again \u2014 \u20b9199/month",
                    "Upgrade to Pro \u2014 \u20b9199/month",
                ),
                href="/pricing",
                class_name="flex items-center gap-2 w-fit rounded-xl bg-indigo-600 px-4 py-2.5 text-sm font-semibold text-white hover:bg-indigo-700 transition-colors",
            ),
            rx.cond(
                SubscriptionState.is_signed_in,
                rx.el.button(
                    rx.cond(
                        SubscriptionState.is_refreshing,
                        rx.el.div(
                            class_name="h-4 w-4 rounded-full border-2 border-indigo-300/50 border-t-indigo-700 animate-spin"
                        ),
                        rx.icon("refresh-cw", class_name="h-4 w-4"),
                    ),
                    rx.cond(
                        SubscriptionState.is_refreshing,
                        "Refreshing",
                        "Refresh status",
                    ),
                    on_click=SubscriptionState.refresh_status,
                    disabled=SubscriptionState.is_refreshing,
                    class_name="flex items-center gap-2 w-fit rounded-xl border border-indigo-200 bg-indigo-50 px-4 py-2.5 text-sm font-semibold text-indigo-700 hover:bg-indigo-100 disabled:opacity-60 transition-colors",
                ),
                rx.el.a(
                    rx.icon("log-in", class_name="h-4 w-4"),
                    "Sign in",
                    href="/login",
                    class_name="flex items-center gap-2 w-fit rounded-xl border border-indigo-200 bg-indigo-50 px-4 py-2.5 text-sm font-semibold text-indigo-700 hover:bg-indigo-100 transition-colors",
                ),
            ),
            rx.cond(
                SubscriptionState.refresh_error,
                rx.el.p(
                    SubscriptionState.refresh_error,
                    class_name="w-full text-xs font-medium text-red-600",
                ),
            ),
            class_name="flex flex-wrap items-center gap-3 mt-4",
        ),
        class_name="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm w-full",
    )


def pro_gate(
    content: rx.Component,
    title: str = PRO_LOCK_TITLE,
    detail: str = PRO_LOCK_BODY,
) -> rx.Component:
    """Render an existing Pro section only when the database says ACTIVE."""
    return rx.cond(
        SubscriptionState.is_pro,
        content,
        pro_locked_card(title, detail),
    )
