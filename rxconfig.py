import os
from pathlib import Path

import reflex as rx
from reflex_base.plugins.base import Plugin


ROBOTS_DISALLOWED: tuple[str, ...] = (
    "/upload",
    "/dashboard",
    "/data-quality",
    "/feedback",
    "/security-readiness",
    "/login",
    "/signup",
    "/api/",
)


def robots_task(deploy_url: str) -> tuple[str, str]:
    lines = ["User-agent: *", "Allow: /"]
    lines.extend(f"Disallow: {path}" for path in ROBOTS_DISALLOWED)
    lines.append(f"Sitemap: {deploy_url.rstrip('/')}/sitemap.xml")
    return str(Path("public") / "robots.txt"), "\n".join(lines) + "\n"


class RobotsTxtPlugin(Plugin):
    def __init__(self, deploy_url: str):
        self.deploy_url = deploy_url.rstrip("/")

    def pre_compile(self, **context):
        context["add_save_task"](robots_task, self.deploy_url)


resolved_deploy_url = os.environ.get(
    "REFLEX_DEPLOY_URL", "http://localhost:3000"
)

config = rx.Config(
    app_name="app",
    deploy_url=resolved_deploy_url,
    show_reflex_badge=False,
    plugins=[
        rx.plugins.TailwindV4Plugin(),
        rx.plugins.RadixThemesPlugin(theme=rx.theme(appearance="light")),
        rx.plugins.SitemapPlugin(trailing_slash="preserve"),
        RobotsTxtPlugin(resolved_deploy_url),
    ],
)
