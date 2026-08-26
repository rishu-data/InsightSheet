import reflex as rx

from app.components.legal import related_policies
from app.components.security_readiness import security_readiness_report
from app.components.sidebar import page_shell


def security_readiness_page() -> rx.Component:
    return page_shell(
        "security",
        "Security Readiness",
        "What the app can verify, and what still needs a human on deployment",
        rx.el.div(
            security_readiness_report(),
            related_policies(),
            class_name="flex flex-col gap-6 w-full",
        ),
    )
