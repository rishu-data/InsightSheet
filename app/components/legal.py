import reflex as rx

from app.components.icon import app_icon

REVIEW_NOTE = (
    "This page is written in plain, general-purpose language for transparency. "
    "It is not legal advice and the wording has not been reviewed by a lawyer, "
    "accountant or compliance professional. Before relying on it commercially, "
    "have a qualified professional review it against the laws that apply to you."
)

SUPPORT_EMAIL = "support@insightsheet.app"


def legal_intro(icon: str, title: str, summary: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name="h-5 w-5 text-blue-600"),
            class_name="flex items-center justify-center h-11 w-11 rounded-xl bg-blue-50 shrink-0",
        ),
        rx.el.div(
            rx.el.h2(
                title,
                class_name="text-2xl font-semibold tracking-tight text-gray-900",
            ),
            rx.el.p(
                summary,
                class_name="text-sm font-medium text-gray-500 mt-1 max-w-3xl",
            ),
            class_name="min-w-0",
        ),
        class_name="flex items-start gap-3 rounded-2xl border border-gray-200 bg-white p-6 shadow-sm w-full",
    )


def legal_card(icon: str, title: str, body: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name="h-4 w-4 text-blue-600"),
            class_name="flex items-center justify-center h-9 w-9 rounded-lg bg-blue-50 shrink-0",
        ),
        rx.el.div(
            rx.el.p(title, class_name="text-sm font-semibold text-gray-900"),
            rx.el.p(body, class_name="text-sm font-medium text-gray-500 mt-1"),
            class_name="min-w-0",
        ),
        class_name="flex items-start gap-3 rounded-2xl border border-gray-200 bg-white p-5 shadow-sm w-full",
    )


def legal_grid(*cards: rx.Component) -> rx.Component:
    return rx.el.div(
        *cards,
        class_name="grid grid-cols-1 md:grid-cols-2 gap-4 w-full",
    )


def bullet(text: str) -> rx.Component:
    return rx.el.li(
        text, class_name="text-sm font-medium text-gray-600 leading-relaxed"
    )


def bullet_card(icon: str, title: str, *items: rx.Component) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name="h-4 w-4 text-indigo-600"),
            rx.el.h3(title, class_name="text-lg font-semibold text-gray-900"),
            class_name="flex items-center gap-2",
        ),
        rx.el.ul(*items, class_name="flex flex-col gap-2 mt-3 list-disc pl-5"),
        class_name="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm w-full",
    )


def review_notice() -> rx.Component:
    return rx.el.div(
        rx.icon("scale", class_name="h-4 w-4 text-yellow-600 shrink-0 mt-0.5"),
        rx.el.div(
            rx.el.p(
                "Professional review required",
                class_name="text-sm font-semibold text-yellow-800",
            ),
            rx.el.p(
                REVIEW_NOTE,
                class_name="text-sm font-medium text-yellow-700 mt-1",
            ),
            class_name="min-w-0",
        ),
        class_name="flex items-start gap-2 rounded-2xl border border-yellow-200 bg-yellow-50 p-5 w-full",
    )


_LEGAL_LINKS: list[tuple[str, str, str]] = [
    ("shield", "Privacy Policy", "/privacy"),
    ("file-text", "Terms of Service", "/terms"),
    ("receipt", "Refund & Cancellation", "/refund-policy"),
    ("credit-card", "Payment & Subscription Terms", "/payment-terms"),
    ("life-buoy", "Contact / Support", "/support"),
    ("shield-check", "Security Readiness", "/security-readiness"),
]


def _related_link(item: tuple[str, str, str]) -> rx.Component:
    return rx.el.a(
        app_icon(item[0], class_name="h-3.5 w-3.5 shrink-0"),
        rx.el.span(item[1]),
        href=item[2],
        class_name="flex items-center gap-2 w-fit rounded-full border border-gray-200 bg-white px-3.5 py-1.5 text-xs font-medium text-gray-600 hover:border-blue-300 hover:text-blue-700 transition-colors",
    )


def related_policies() -> rx.Component:
    return rx.el.div(
        rx.el.p(
            "Related policies and support",
            class_name="text-sm font-semibold text-gray-900",
        ),
        rx.el.div(
            _related_link(_LEGAL_LINKS[0]),
            _related_link(_LEGAL_LINKS[1]),
            _related_link(_LEGAL_LINKS[2]),
            _related_link(_LEGAL_LINKS[3]),
            _related_link(_LEGAL_LINKS[4]),
            _related_link(_LEGAL_LINKS[5]),
            class_name="flex flex-wrap items-center gap-2 mt-3",
        ),
        class_name="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm w-full",
    )
