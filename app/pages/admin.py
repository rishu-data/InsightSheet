import reflex as rx

from app.components.admin_panel import admin_shell

ADMIN_TITLE = "Admin Control Center | InsightSheet"


def admin_page() -> rx.Component:
    return admin_shell()
