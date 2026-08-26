import reflex as rx

from app.states.auth_state import AuthState

_LABEL = "text-sm font-medium text-gray-700"
_INPUT = (
    "w-full rounded-xl border border-gray-300 bg-white px-4 py-2.5 text-sm "
    "font-medium text-gray-900 placeholder:text-gray-400 focus:border-blue-500 "
    "focus:ring-2 focus:ring-blue-500 outline-hidden transition-colors"
)
_SUBMIT = (
    "flex items-center justify-center gap-2 w-full rounded-xl bg-blue-600 px-4 "
    "py-2.5 text-sm font-semibold text-white hover:bg-blue-700 "
    "disabled:opacity-60 transition-colors"
)


def _brand() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("sheet", class_name="h-4 w-4 text-white"),
            class_name="flex items-center justify-center h-9 w-9 rounded-lg bg-blue-600 shrink-0",
        ),
        rx.el.div(
            rx.el.p(
                "InsightSheet",
                class_name="text-base font-semibold text-gray-900",
            ),
            rx.el.p(
                "Spreadsheet analytics",
                class_name="text-xs font-medium text-gray-500",
            ),
            class_name="min-w-0",
        ),
        class_name="flex items-center gap-2.5",
    )


def _field(
    label: str, name: str, kind: str, placeholder: str, icon: str
) -> rx.Component:
    return rx.el.div(
        rx.el.label(label, html_for=name, class_name=_LABEL),
        rx.el.div(
            rx.icon(
                icon,
                class_name="h-4 w-4 text-gray-400 absolute left-3.5 top-1/2 -translate-y-1/2",
            ),
            rx.el.input(
                id=name,
                name=name,
                type=kind,
                placeholder=placeholder,
                required=True,
                auto_complete="off",
                class_name=f"{_INPUT} pl-10",
            ),
            class_name="relative mt-1.5",
        ),
        class_name="w-full",
    )


def _error() -> rx.Component:
    return rx.cond(
        AuthState.has_error,
        rx.el.div(
            rx.icon(
                "circle-alert",
                class_name="h-4 w-4 text-red-500 shrink-0 mt-0.5",
            ),
            rx.el.p(
                AuthState.error, class_name="text-sm font-medium text-red-500"
            ),
            class_name="flex items-start gap-2 rounded-xl border border-red-200 bg-red-100 px-4 py-3",
        ),
    )


def _shell(
    title: str, subtitle: str, body: rx.Component, footer: rx.Component
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            _brand(),
            rx.el.div(
                rx.el.h1(
                    title,
                    class_name="text-xl font-semibold tracking-tight text-gray-900",
                ),
                rx.el.p(
                    subtitle,
                    class_name="text-sm font-medium text-gray-500 mt-0.5",
                ),
                class_name="mt-6",
            ),
            body,
            footer,
            rx.el.div(
                rx.icon(
                    "lock", class_name="h-3.5 w-3.5 text-gray-400 shrink-0"
                ),
                rx.el.p(
                    "Passwords are stored only as irreversible hashes — never in plain text. "
                    "Repeated failed attempts are briefly slowed down to protect your account.",
                    class_name="text-xs font-medium text-gray-500",
                ),
                class_name="flex items-start gap-2 rounded-xl border border-gray-200 bg-gray-50 p-3 mt-6",
            ),
            rx.el.div(
                rx.el.a(
                    "Privacy Policy",
                    href="/privacy",
                    class_name="text-xs font-medium text-gray-500 hover:text-blue-700 transition-colors",
                ),
                rx.el.a(
                    "Terms of Service",
                    href="/terms",
                    class_name="text-xs font-medium text-gray-500 hover:text-blue-700 transition-colors",
                ),
                rx.el.a(
                    "Contact / Support",
                    href="/support",
                    class_name="text-xs font-medium text-gray-500 hover:text-blue-700 transition-colors",
                ),
                class_name="flex flex-wrap items-center justify-center gap-x-4 gap-y-2 mt-4",
            ),
            class_name="w-full max-w-md rounded-2xl border border-gray-200 bg-white p-6 sm:p-8 shadow-sm",
        ),
        class_name="font-['Inter'] flex min-h-screen w-full items-center justify-center bg-gray-50 px-4 py-10",
    )


def login_page() -> rx.Component:
    return _shell(
        "Sign in to InsightSheet",
        "Your uploads, reports and feedback stay tied to your account.",
        rx.el.form(
            _field("Email", "email", "email", "you@company.com", "mail"),
            _field("Password", "password", "password", "Your password", "lock"),
            _error(),
            rx.el.button(
                rx.cond(
                    AuthState.is_busy,
                    rx.el.div(
                        class_name="h-4 w-4 rounded-full border-2 border-white/40 border-t-white animate-spin"
                    ),
                    rx.icon("log-in", class_name="h-4 w-4"),
                ),
                rx.el.span("Sign in"),
                type="submit",
                disabled=AuthState.is_busy,
                class_name=_SUBMIT,
            ),
            on_submit=AuthState.log_in,
            reset_on_submit=True,
            class_name="flex flex-col gap-4 mt-6 w-full",
        ),
        rx.el.p(
            rx.el.span(
                "New to InsightSheet? ",
                class_name="text-sm font-medium text-gray-500",
            ),
            rx.el.a(
                "Create an account",
                href="/signup",
                class_name="text-sm font-semibold text-blue-600 hover:text-blue-700",
            ),
            class_name="mt-5 text-center",
        ),
    )


def signup_page() -> rx.Component:
    return _shell(
        "Create your account",
        "One account keeps your cleaned data, reports and plan together.",
        rx.el.form(
            _field(
                "Name (optional)", "display_name", "text", "Your name", "user"
            ),
            _field("Email", "email", "email", "you@company.com", "mail"),
            _field(
                "Password",
                "password",
                "password",
                "At least 8 characters",
                "lock",
            ),
            _field(
                "Confirm password",
                "confirm_password",
                "password",
                "Repeat your password",
                "shield-check",
            ),
            _error(),
            rx.el.button(
                rx.cond(
                    AuthState.is_busy,
                    rx.el.div(
                        class_name="h-4 w-4 rounded-full border-2 border-white/40 border-t-white animate-spin"
                    ),
                    rx.icon("user-plus", class_name="h-4 w-4"),
                ),
                rx.el.span("Create account"),
                type="submit",
                disabled=AuthState.is_busy,
                class_name=_SUBMIT,
            ),
            on_submit=AuthState.sign_up,
            reset_on_submit=True,
            class_name="flex flex-col gap-4 mt-6 w-full",
        ),
        rx.el.p(
            rx.el.span(
                "Already registered? ",
                class_name="text-sm font-medium text-gray-500",
            ),
            rx.el.a(
                "Sign in",
                href="/login",
                class_name="text-sm font-semibold text-blue-600 hover:text-blue-700",
            ),
            class_name="mt-5 text-center",
        ),
    )
