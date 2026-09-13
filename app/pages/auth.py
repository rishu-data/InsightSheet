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


def _notice() -> rx.Component:
    return rx.cond(
        AuthState.has_notice,
        rx.el.div(
            rx.icon(
                "mail-check",
                class_name="h-4 w-4 text-blue-500 shrink-0 mt-0.5",
            ),
            rx.el.p(
                AuthState.notice,
                class_name="text-sm font-medium text-blue-600",
            ),
            class_name="flex items-start gap-2 rounded-xl border border-blue-200 bg-blue-100 px-4 py-3",
        ),
    )


def _resend_block() -> rx.Component:
    """Shown only after correct credentials on an unverified account."""
    return rx.cond(
        AuthState.verification_required,
        rx.el.form(
            rx.el.div(
                rx.icon(
                    "shield-alert",
                    class_name="h-4 w-4 text-gray-500 shrink-0 mt-0.5",
                ),
                rx.el.p(
                    "Verification links expire after 24 hours and can be used "
                    "once. Send a fresh link to your email address.",
                    class_name="text-xs font-medium text-gray-500",
                ),
                class_name="flex items-start gap-2",
            ),
            rx.el.input(
                type="email",
                name="email",
                required=True,
                placeholder="you@company.com",
                default_value=AuthState.pending_email,
                key=AuthState.pending_email,
                class_name=_INPUT,
            ),
            rx.el.button(
                rx.cond(
                    AuthState.resend_busy,
                    rx.el.div(
                        class_name="h-4 w-4 rounded-full border-2 border-blue-200 border-t-blue-600 animate-spin"
                    ),
                    rx.icon("send", class_name="h-4 w-4"),
                ),
                rx.el.span("Resend verification email"),
                type="submit",
                disabled=AuthState.resend_busy,
                class_name=(
                    "flex items-center justify-center gap-2 w-full rounded-xl "
                    "border border-blue-200 bg-white px-4 py-2.5 text-sm "
                    "font-semibold text-blue-600 hover:bg-blue-50 "
                    "disabled:opacity-60 transition-colors"
                ),
            ),
            on_submit=AuthState.resend_verification,
            class_name="flex flex-col gap-3 mt-4 w-full rounded-xl border border-gray-200 bg-gray-50 p-4",
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
            rx.el.a(
                rx.icon("key-round", class_name="h-3.5 w-3.5"),
                rx.el.span("Forgot password?"),
                href="/forgot-password",
                class_name="flex items-center gap-1.5 w-fit self-end text-xs font-semibold text-blue-600 hover:text-blue-700",
            ),
            _notice(),
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
        rx.fragment(
            _resend_block(),
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
            rx.el.div(
                rx.icon(
                    "mail", class_name="h-4 w-4 text-gray-500 shrink-0 mt-0.5"
                ),
                rx.el.p(
                    "We'll email you a verification link. Confirm your address "
                    "within 24 hours before signing in.",
                    class_name="text-xs font-medium text-gray-500",
                ),
                class_name="flex items-start gap-2 rounded-xl border border-gray-200 bg-gray-50 p-3",
            ),
            _notice(),
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


def _verify_result() -> rx.Component:
    return rx.cond(
        AuthState.verify_is_checking,
        rx.el.div(
            rx.el.div(
                class_name="h-5 w-5 rounded-full border-2 border-blue-200 border-t-blue-600 animate-spin"
            ),
            rx.el.p(
                "Checking your verification link...",
                class_name="text-sm font-medium text-gray-500",
            ),
            class_name="flex items-center gap-3 rounded-xl border border-gray-200 bg-gray-50 px-4 py-4",
        ),
        rx.cond(
            AuthState.verify_succeeded,
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "shield-check",
                        class_name="h-4 w-4 text-green-500 shrink-0 mt-0.5",
                    ),
                    rx.el.p(
                        "Your email address is verified. You can sign in now.",
                        class_name="text-sm font-medium text-green-500",
                    ),
                    class_name="flex items-start gap-2 rounded-xl border border-green-200 bg-green-100 px-4 py-3",
                ),
                rx.el.a(
                    rx.icon("log-in", class_name="h-4 w-4"),
                    rx.el.span("Go to sign in"),
                    href="/login",
                    class_name=_SUBMIT + " mt-4",
                ),
                class_name="w-full",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "circle-alert",
                        class_name="h-4 w-4 text-red-500 shrink-0 mt-0.5",
                    ),
                    rx.el.p(
                        "This verification link is invalid, has expired, or has "
                        "already been used. Sign in with your email and password "
                        "to request a new link.",
                        class_name="text-sm font-medium text-red-500",
                    ),
                    class_name="flex items-start gap-2 rounded-xl border border-red-200 bg-red-100 px-4 py-3",
                ),
                rx.el.a(
                    rx.icon("log-in", class_name="h-4 w-4"),
                    rx.el.span("Back to sign in"),
                    href="/login",
                    class_name=_SUBMIT + " mt-4",
                ),
                class_name="w-full",
            ),
        ),
    )


def forgot_password_page() -> rx.Component:
    return _shell(
        "Reset your password",
        "We'll email a single-use link to the address on your account.",
        rx.el.form(
            _field("Email", "email", "email", "you@company.com", "mail"),
            rx.el.div(
                rx.icon(
                    "shield",
                    class_name="h-4 w-4 text-gray-500 shrink-0 mt-0.5",
                ),
                rx.el.p(
                    "Reset links expire after 1 hour and can be used once. "
                    "For your security we always show the same confirmation, "
                    "whether or not an account exists for that address.",
                    class_name="text-xs font-medium text-gray-500",
                ),
                class_name="flex items-start gap-2 rounded-xl border border-gray-200 bg-gray-50 p-3",
            ),
            _notice(),
            _error(),
            rx.el.button(
                rx.cond(
                    AuthState.forgot_busy,
                    rx.el.div(
                        class_name="h-4 w-4 rounded-full border-2 border-white/40 border-t-white animate-spin"
                    ),
                    rx.icon("send", class_name="h-4 w-4"),
                ),
                rx.el.span("Send reset link"),
                type="submit",
                disabled=AuthState.forgot_busy,
                class_name=_SUBMIT,
            ),
            on_submit=AuthState.request_password_reset,
            reset_on_submit=True,
            class_name="flex flex-col gap-4 mt-6 w-full",
        ),
        rx.el.p(
            rx.el.span(
                "Remembered it? ",
                class_name="text-sm font-medium text-gray-500",
            ),
            rx.el.a(
                "Back to sign in",
                href="/login",
                class_name="text-sm font-semibold text-blue-600 hover:text-blue-700",
            ),
            class_name="mt-5 text-center",
        ),
    )


def _reset_form() -> rx.Component:
    return rx.el.form(
        _field(
            "New password",
            "new_password",
            "password",
            "At least 8 characters",
            "lock",
        ),
        _field(
            "Confirm new password",
            "confirm_password",
            "password",
            "Repeat your new password",
            "shield-check",
        ),
        _error(),
        rx.el.button(
            rx.cond(
                AuthState.reset_busy,
                rx.el.div(
                    class_name="h-4 w-4 rounded-full border-2 border-white/40 border-t-white animate-spin"
                ),
                rx.icon("key-round", class_name="h-4 w-4"),
            ),
            rx.el.span("Set new password"),
            type="submit",
            disabled=AuthState.reset_busy,
            class_name=_SUBMIT,
        ),
        on_submit=AuthState.submit_password_reset,
        reset_on_submit=True,
        class_name="flex flex-col gap-4 w-full",
    )


def _reset_done() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(
                "shield-check",
                class_name="h-4 w-4 text-green-500 shrink-0 mt-0.5",
            ),
            rx.el.p(
                AuthState.notice,
                class_name="text-sm font-medium text-green-500",
            ),
            class_name="flex items-start gap-2 rounded-xl border border-green-200 bg-green-100 px-4 py-3",
        ),
        rx.cond(
            AuthState.reset_confirmation_sent,
            rx.fragment(),
            rx.el.div(
                rx.icon(
                    "mail",
                    class_name="h-4 w-4 text-yellow-600 shrink-0 mt-0.5",
                ),
                rx.el.p(
                    "Your password was changed successfully, but the "
                    "confirmation email could not be sent just now.",
                    class_name="text-sm font-medium text-yellow-600",
                ),
                class_name="flex items-start gap-2 rounded-xl border border-yellow-200 bg-yellow-100 px-4 py-3 mt-3",
            ),
        ),
        rx.el.a(
            rx.icon("log-in", class_name="h-4 w-4"),
            rx.el.span("Go to sign in"),
            href="/login",
            class_name=_SUBMIT + " mt-4",
        ),
        class_name="w-full",
    )


def _reset_invalid() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(
                "circle-alert",
                class_name="h-4 w-4 text-red-500 shrink-0 mt-0.5",
            ),
            rx.el.p(
                "This password reset link is invalid, has expired, or has "
                "already been used. Request a new one to continue.",
                class_name="text-sm font-medium text-red-500",
            ),
            class_name="flex items-start gap-2 rounded-xl border border-red-200 bg-red-100 px-4 py-3",
        ),
        rx.el.a(
            rx.icon("send", class_name="h-4 w-4"),
            rx.el.span("Request a new link"),
            href="/forgot-password",
            class_name=_SUBMIT + " mt-4",
        ),
        class_name="w-full",
    )


def _reset_body() -> rx.Component:
    return rx.cond(
        AuthState.reset_is_checking,
        rx.el.div(
            rx.el.div(
                class_name="h-5 w-5 rounded-full border-2 border-blue-200 border-t-blue-600 animate-spin"
            ),
            rx.el.p(
                "Checking your reset link...",
                class_name="text-sm font-medium text-gray-500",
            ),
            class_name="flex items-center gap-3 rounded-xl border border-gray-200 bg-gray-50 px-4 py-4",
        ),
        rx.cond(
            AuthState.reset_is_ready,
            _reset_form(),
            rx.cond(AuthState.reset_is_done, _reset_done(), _reset_invalid()),
        ),
    )


def reset_password_page() -> rx.Component:
    return _shell(
        "Choose a new password",
        "Setting a new password signs out every existing session.",
        rx.el.div(_reset_body(), class_name="mt-6 w-full"),
        rx.el.p(
            rx.el.span(
                "Need a new link? ",
                class_name="text-sm font-medium text-gray-500",
            ),
            rx.el.a(
                "Start again",
                href="/forgot-password",
                class_name="text-sm font-semibold text-blue-600 hover:text-blue-700",
            ),
            class_name="mt-5 text-center",
        ),
    )


def verify_email_page() -> rx.Component:
    return _shell(
        "Email verification",
        "Confirming your address keeps your uploads and reports tied to you.",
        rx.el.div(_verify_result(), class_name="mt-6 w-full"),
        rx.el.p(
            rx.el.span(
                "Need a new link? ",
                class_name="text-sm font-medium text-gray-500",
            ),
            rx.el.a(
                "Sign in to resend it",
                href="/login",
                class_name="text-sm font-semibold text-blue-600 hover:text-blue-700",
            ),
            class_name="mt-5 text-center",
        ),
    )
