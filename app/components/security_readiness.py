import reflex as rx

from app.components.icon import app_icon
from app.states.security_state import (
    ManualAction,
    SecurityCheck,
    SecurityReadinessState,
)

_PASS_BADGE = "flex items-center gap-1.5 w-fit shrink-0 rounded-full bg-green-100 px-2.5 py-1 text-xs font-semibold text-green-700"
_WARN_BADGE = "flex items-center gap-1.5 w-fit shrink-0 rounded-full bg-yellow-100 px-2.5 py-1 text-xs font-semibold text-yellow-700"
_UNKNOWN_BADGE = "flex items-center gap-1.5 w-fit shrink-0 rounded-full bg-blue-100 px-2.5 py-1 text-xs font-semibold text-blue-700"


def _status_badge(check: SecurityCheck) -> rx.Component:
    return rx.el.span(
        rx.cond(
            check["state"] == "pass",
            rx.icon("circle-check", class_name="h-3.5 w-3.5"),
            rx.cond(
                check["state"] == "warn",
                rx.icon("triangle-alert", class_name="h-3.5 w-3.5"),
                rx.icon("circle-help", class_name="h-3.5 w-3.5"),
            ),
        ),
        rx.el.span(check["status_label"]),
        class_name=rx.cond(
            check["state"] == "pass",
            _PASS_BADGE,
            rx.cond(check["state"] == "warn", _WARN_BADGE, _UNKNOWN_BADGE),
        ),
    )


def _check_card(check: SecurityCheck) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            app_icon(check["icon"], "h-4 w-4 text-blue-600"),
            class_name="flex items-center justify-center h-9 w-9 rounded-lg bg-blue-50 shrink-0",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    check["title"],
                    class_name="text-sm font-semibold text-gray-900",
                ),
                _status_badge(check),
                class_name="flex flex-wrap items-center justify-between gap-2",
            ),
            rx.el.p(
                check["detail"],
                class_name="text-sm font-medium text-gray-500 mt-1",
            ),
            class_name="min-w-0 flex-1",
        ),
        class_name="flex items-start gap-3 rounded-2xl border border-gray-200 bg-white p-5 shadow-sm w-full",
    )


def _secret_row(check: SecurityCheck) -> rx.Component:
    return rx.el.div(
        app_icon(
            check["icon"],
            "h-3.5 w-3.5 text-indigo-600 mt-0.5 shrink-0",
        ),
        rx.el.div(
            rx.el.p(
                check["title"],
                class_name="text-sm font-semibold text-gray-900 break-all",
            ),
            rx.el.p(
                check["detail"],
                class_name="text-xs font-medium text-gray-500 mt-0.5",
            ),
            class_name="min-w-0 flex-1",
        ),
        _status_badge(check),
        class_name="flex items-start gap-3 rounded-xl border border-gray-200 bg-gray-50 p-4 w-full",
    )


def _manual_step(step: str) -> rx.Component:
    return rx.el.li(
        step,
        class_name="text-sm font-medium text-gray-600 leading-relaxed",
    )


def _manual_card(action: ManualAction) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                app_icon(action["icon"], "h-4 w-4 text-yellow-700"),
                class_name="flex items-center justify-center h-9 w-9 rounded-lg bg-yellow-100 shrink-0",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        action["title"],
                        class_name="text-sm font-semibold text-gray-900",
                    ),
                    rx.el.span(
                        rx.icon("user-cog", class_name="h-3.5 w-3.5"),
                        rx.el.span("Manual action required"),
                        class_name="flex items-center gap-1.5 w-fit shrink-0 rounded-full bg-yellow-100 px-2.5 py-1 text-xs font-semibold text-yellow-800",
                    ),
                    class_name="flex flex-wrap items-center justify-between gap-2",
                ),
                rx.el.p(
                    action["detail"],
                    class_name="text-sm font-medium text-gray-500 mt-1",
                ),
                class_name="min-w-0 flex-1",
            ),
            class_name="flex items-start gap-3",
        ),
        rx.el.ul(
            rx.foreach(action["steps"], _manual_step),
            class_name="flex flex-col gap-1.5 mt-3 list-disc pl-5",
        ),
        class_name="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm w-full",
    )


def _summary_tile(
    icon: str, label: str, value: rx.Component | str, tone: str
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name="h-4 w-4"),
            class_name=tone,
        ),
        rx.el.div(
            rx.el.p(value, class_name="text-xl font-semibold text-gray-900"),
            rx.el.p(label, class_name="text-xs font-medium text-gray-500"),
            class_name="min-w-0",
        ),
        class_name="flex items-center gap-3 w-full rounded-2xl border border-gray-200 bg-white p-4 shadow-sm",
    )


def _summary() -> rx.Component:
    return rx.el.div(
        _summary_tile(
            "circle-check",
            "Checks verified in code",
            f"{SecurityReadinessState.passing_count} / {SecurityReadinessState.total_count}",
            "flex items-center justify-center h-9 w-9 rounded-lg bg-green-100 text-green-700 shrink-0",
        ),
        _summary_tile(
            "triangle-alert",
            "Automated checks needing attention",
            SecurityReadinessState.attention_count.to_string(),
            "flex items-center justify-center h-9 w-9 rounded-lg bg-yellow-100 text-yellow-700 shrink-0",
        ),
        _summary_tile(
            "user-cog",
            "Manual deployment actions",
            SecurityReadinessState.manual_count.to_string(),
            "flex items-center justify-center h-9 w-9 rounded-lg bg-indigo-100 text-indigo-700 shrink-0",
        ),
        _summary_tile(
            "clock",
            "Report generated",
            rx.cond(
                SecurityReadinessState.last_checked,
                SecurityReadinessState.last_checked,
                "Running checks…",
            ),
            "flex items-center justify-center h-9 w-9 rounded-lg bg-blue-100 text-blue-700 shrink-0",
        ),
        class_name="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4 w-full",
    )


def _intro() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("shield-check", class_name="h-5 w-5 text-blue-600"),
                class_name="flex items-center justify-center h-11 w-11 rounded-xl bg-blue-50 shrink-0",
            ),
            rx.el.div(
                rx.el.h2(
                    "Production security readiness",
                    class_name="text-2xl font-semibold tracking-tight text-gray-900",
                ),
                rx.el.p(
                    "This report is read-only. It lists the security controls "
                    "InsightSheet can verify from its own code and database, "
                    "and separates them from the deployment and infrastructure "
                    "actions only a human operator can complete. No secret "
                    "value, password, session token or payment credential is "
                    "shown here.",
                    class_name="text-sm font-medium text-gray-500 mt-1 max-w-3xl",
                ),
                class_name="min-w-0",
            ),
            class_name="flex items-start gap-3",
        ),
        rx.el.div(
            rx.el.button(
                rx.cond(
                    SecurityReadinessState.is_running,
                    rx.el.div(
                        class_name="h-3.5 w-3.5 rounded-full border-2 border-gray-300 border-t-blue-600 animate-spin"
                    ),
                    rx.icon("refresh-cw", class_name="h-3.5 w-3.5"),
                ),
                rx.cond(
                    SecurityReadinessState.is_running,
                    "Re-running checks…",
                    "Re-run checks",
                ),
                on_click=SecurityReadinessState.run_checks,
                disabled=SecurityReadinessState.is_running,
                class_name="flex items-center justify-center gap-2 w-fit shrink-0 rounded-xl border border-gray-200 bg-white px-3.5 py-2 text-xs font-semibold text-gray-600 hover:border-blue-300 hover:text-blue-700 disabled:opacity-60 transition-colors",
            ),
            rx.cond(
                SecurityReadinessState.run_error,
                rx.el.p(
                    SecurityReadinessState.run_error,
                    class_name="text-xs font-medium text-red-600 mt-2 max-w-xs",
                ),
            ),
            class_name="flex flex-col items-start lg:items-end shrink-0",
        ),
        class_name="flex flex-col lg:flex-row lg:items-start lg:justify-between gap-4 rounded-2xl border border-gray-200 bg-white p-6 shadow-sm w-full",
    )


def _section_heading(
    icon: str, title: str, subtitle: str, tone: str
) -> rx.Component:
    return rx.el.div(
        rx.icon(icon, class_name=tone),
        rx.el.div(
            rx.el.h3(title, class_name="text-lg font-semibold text-gray-900"),
            rx.el.p(
                subtitle, class_name="text-sm font-medium text-gray-500 mt-0.5"
            ),
            class_name="min-w-0",
        ),
        class_name="flex items-start gap-2 w-full",
    )


def _secrets_card() -> rx.Component:
    return rx.el.div(
        _section_heading(
            "key-round",
            "Production configuration — presence only",
            "InsightSheet checks that each item below is configured on the "
            "server. Variable names and values are never read into the "
            "frontend, never logged and never displayed on this page.",
            "h-4 w-4 text-indigo-600 mt-1 shrink-0",
        ),
        rx.el.div(
            rx.foreach(SecurityReadinessState.secret_names, _secret_row),
            class_name="grid grid-cols-1 md:grid-cols-2 gap-3 mt-4 w-full",
        ),
        class_name="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm w-full",
    )


def _manual_notice() -> rx.Component:
    return rx.el.div(
        rx.icon(
            "triangle-alert",
            class_name="h-4 w-4 text-yellow-600 shrink-0 mt-0.5",
        ),
        rx.el.div(
            rx.el.p(
                "These items are not complete",
                class_name="text-sm font-semibold text-yellow-800",
            ),
            rx.el.p(
                "The Builder cannot deploy, change hosting settings, rotate "
                "production secrets or configure infrastructure, so none of "
                "the actions below are claimed as done. Treat each one as an "
                "open task to confirm on the live environment.",
                class_name="text-sm font-medium text-yellow-700 mt-1",
            ),
            class_name="min-w-0",
        ),
        class_name="flex items-start gap-2 rounded-2xl border border-yellow-200 bg-yellow-50 p-5 w-full",
    )


def security_readiness_report() -> rx.Component:
    return rx.el.div(
        _intro(),
        _summary(),
        _section_heading(
            "circle-check",
            "Code-verifiable checks",
            "Verified directly from the application code and managed database.",
            "h-4 w-4 text-blue-600 mt-1 shrink-0",
        ),
        rx.el.div(
            rx.foreach(SecurityReadinessState.checks, _check_card),
            class_name="grid grid-cols-1 xl:grid-cols-2 gap-4 w-full",
        ),
        _secrets_card(),
        _section_heading(
            "user-cog",
            "Manual deployment & infrastructure actions",
            "Outside the application — a human operator must complete and "
            "confirm each of these.",
            "h-4 w-4 text-yellow-700 mt-1 shrink-0",
        ),
        _manual_notice(),
        rx.el.div(
            rx.foreach(SecurityReadinessState.manual_actions, _manual_card),
            class_name="grid grid-cols-1 xl:grid-cols-2 gap-4 w-full",
        ),
        class_name="flex flex-col gap-6 w-full",
    )
