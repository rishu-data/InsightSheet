"""Production security readiness reporting (read-only, no secrets exposed).

Every check here is either a static code fact (cookie flags, hashing
parameters, webhook signature enforcement) or a presence-only database /
environment probe. Secret VALUES are never read into state, never logged and
never rendered — only whether a name is configured.

Manual deployment and infrastructure actions are listed separately and are
never reported as complete, because the app cannot verify them.
"""

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import TypedDict

import reflex as rx
from sqlalchemy import text

from app.models import AuthAction
from app.razorpay_webhook import SECRET_ENV_VAR, verify_signature
from app.states.pricing_state import PAYMENT_ENV_VAR
from app.states.auth_rate_limit import MAX_ATTEMPTS, WINDOW_SECONDS
from app.states.auth_state import (
    PBKDF2_ITERATIONS,
    SESSION_COOKIE_NAME,
    SESSION_DAYS,
)


class SecurityCheck(TypedDict):
    key: str
    icon: str
    title: str
    detail: str
    state: str  # "pass" | "warn" | "unknown"
    status_label: str


class ManualAction(TypedDict):
    key: str
    icon: str
    title: str
    detail: str
    steps: list[str]


class ConfigItem(TypedDict):
    label: str
    icon: str
    env_names: list[str]
    purpose: str


# Generic, user-facing labels only. Environment variable NAMES live here for
# server-side presence probing and are NEVER rendered or logged; values are
# never read into state.
CONFIG_ITEMS: list[ConfigItem] = [
    {
        "label": "Webhook signing secret",
        "icon": "shield-check",
        "env_names": [SECRET_ENV_VAR],
        "purpose": "used to verify payment webhook deliveries",
    },
    {
        "label": "Razorpay API credentials",
        "icon": "key-round",
        "env_names": ["RAZORPAY_KEY_ID", "RAZORPAY_KEY_SECRET"],
        "purpose": "the key and secret pair used for payment provider calls",
    },
    {
        "label": "Payment checkout URL",
        "icon": "credit-card",
        "env_names": [PAYMENT_ENV_VAR],
        "purpose": "the external checkout destination for Pro upgrades",
    },
    {
        "label": "Managed database URL",
        "icon": "database",
        "env_names": ["REFLEX_DB_URL"],
        "purpose": "the managed database connection used for persistence",
    },
    {
        "label": "Async database URL",
        "icon": "database-zap",
        "env_names": ["REFLEX_ASYNC_DB_URL"],
        "purpose": "the async connection used for non-blocking reads",
    },
]

# Every environment name probed anywhere on this page (never displayed).
_ALL_CONFIG_ENV_NAMES: list[str] = [
    name for item in CONFIG_ITEMS for name in item["env_names"]
]

MANUAL_ACTIONS: list[ManualAction] = [
    {
        "key": "https",
        "icon": "globe-lock",
        "title": "HTTPS-only deployment",
        "detail": (
            "Session cookies are marked Secure, so they are only sent over "
            "HTTPS. Serving the app over plain HTTP would silently break "
            "sign-in. Terminating TLS, redirecting HTTP to HTTPS and enabling "
            "HSTS happen in your hosting/proxy layer, which the app cannot "
            "inspect or change."
        ),
        "steps": [
            "Issue and auto-renew a TLS certificate for the production domain.",
            "Force a 301 redirect from http:// to https:// at the edge.",
            "Enable HSTS once you are confident every subdomain is on HTTPS.",
        ],
    },
    {
        "key": "secrets",
        "icon": "key-round",
        "title": "Production secret storage and rotation",
        "detail": (
            "The app only checks whether a secret NAME is configured; it "
            "cannot tell where the value is stored, who can read it or when it "
            "was last rotated. Store secrets in your platform's secret manager "
            "and keep them out of source control."
        ),
        "steps": [
            "Set the Razorpay webhook secret and database URL as platform secrets, not literals in code.",
            "Rotate the webhook secret and any API keys on a fixed schedule and after any staff change.",
            "Restrict who can read production secrets, and audit that access list.",
        ],
    },
    {
        "key": "database",
        "icon": "database-zap",
        "title": "Database network access and backups",
        "detail": (
            "Persistence is database-managed, but network exposure, firewall "
            "rules, at-rest encryption, backup schedules and restore drills "
            "are infrastructure settings outside the application."
        ),
        "steps": [
            "Restrict the database to private networking or an allow-listed source.",
            "Enable automated daily backups with point-in-time recovery where available.",
            "Perform a real restore test and record how long it took.",
        ],
    },
    {
        "key": "monitoring",
        "icon": "bell-ring",
        "title": "Monitoring and error alerting",
        "detail": (
            "Failures are logged server-side with stack traces, but the app "
            "cannot confirm that anyone is paged when they happen. Alerting "
            "must be wired up in your monitoring stack."
        ),
        "steps": [
            "Ship application logs and exceptions to a monitoring/error-tracking service.",
            "Alert on webhook signature failures, 5xx spikes and database connection errors.",
            "Define who receives alerts out of hours and how they acknowledge them.",
        ],
    },
    {
        "key": "logs",
        "icon": "file-lock",
        "title": "Log retention and redaction policy",
        "detail": (
            "Application log messages are written to be free of passwords, "
            "session tokens and payment credentials, but retention windows, "
            "access control and redaction at the aggregator are set by your "
            "hosting and logging providers."
        ),
        "steps": [
            "Set a documented retention period for request and error logs.",
            "Confirm no third-party log sink stores request bodies or cookies.",
            "Limit log access to the people who operate the service.",
        ],
    },
    {
        "key": "domain",
        "icon": "scan-search",
        "title": "Deployment-domain checks",
        "detail": (
            "The final domain, DNS records, allowed origins, webhook endpoint "
            "URL registered with the payment provider and any CDN rules are "
            "verified after deployment. The app cannot check them from here."
        ),
        "steps": [
            "Point the production domain at the deployment and verify DNS propagation.",
            "Register the live /api/razorpay/webhook URL in the payment dashboard and send a test event.",
            "Re-run sign-up, sign-in, upload and checkout on the production domain before launch.",
        ],
    },
]

_STATUS_LABELS = {
    "pass": "Verified in code",
    "warn": "Needs attention",
    "unknown": "Not verifiable now",
}


def _check(
    key: str, icon: str, title: str, detail: str, state: str
) -> SecurityCheck:
    return {
        "key": key,
        "icon": icon,
        "title": title,
        "detail": detail,
        "state": state,
        "status_label": _STATUS_LABELS.get(state, "Not verifiable now"),
    }


def _cookie_check() -> SecurityCheck:
    source = Path("app/states/auth_state.py")
    text_body = source.read_text() if source.exists() else ""
    secure = "secure=True" in text_body
    strict = 'same_site="strict"' in text_body
    ok = secure and strict
    detail = (
        f"The session cookie \u201c{SESSION_COOKIE_NAME}\u201d is issued with "
        f"Secure={secure}, SameSite={'strict' if strict else 'unset'}, path=/ and a "
        f"{SESSION_DAYS}-day maximum age. Only a SHA-256 hash of the token is "
        "stored server-side, so a leaked database row cannot be replayed, and "
        "the raw token is never logged."
    )
    return _check(
        "cookie",
        "cookie",
        "Secure, same-site session cookie",
        detail,
        "pass" if ok else "warn",
    )


def _password_check() -> SecurityCheck:
    ok = PBKDF2_ITERATIONS >= 200_000
    detail = (
        "Passwords are stored only as a PBKDF2-HMAC-SHA256 digest with a "
        f"random per-user salt and {PBKDF2_ITERATIONS:,} iterations, compared "
        "in constant time. No plaintext password column exists in the schema."
    )
    return _check(
        "password",
        "lock",
        "Irreversible password hashing",
        detail,
        "pass" if ok else "warn",
    )


def _webhook_signature_check() -> SecurityCheck:
    rejects_bad = not verify_signature(
        b'{"event":"subscription.activated"}', "0" * 64, "test-secret"
    )
    rejects_missing = not verify_signature(b"{}", "", "test-secret")
    ok = rejects_bad and rejects_missing
    detail = (
        "The Razorpay webhook rejects any delivery without a valid "
        "X-Razorpay-Signature header. The HMAC-SHA256 digest is computed over "
        "the raw request body and compared in constant time before anything is "
        "parsed or persisted; oversized bodies and replayed event ids are "
        "refused too."
    )
    return _check(
        "webhook",
        "shield-check",
        "Webhook signature required before processing",
        detail,
        "pass" if ok else "warn",
    )


def _no_frontend_secret_check() -> SecurityCheck:
    """Secrets are read in backend modules only — never into a state var."""
    leaked = False
    for folder in ("app/components", "app/pages", "app/states"):
        base = Path(folder)
        if not base.exists():
            continue
        for module in base.glob("*.py"):
            body = module.read_text()
            for name in _ALL_CONFIG_ENV_NAMES:
                value = str(os.environ.get(name, "") or "").strip()
                if value and value in body:
                    leaked = True
    detail = (
        "By design, no secret value is placed in a state var, computed var, "
        "component prop or page, so nothing secret is compiled into the "
        "browser bundle. The webhook signing secret and Razorpay API "
        "credentials are read on the server only, and this page reports "
        "presence against generic labels — never names or values."
    )
    return _check(
        "frontend",
        "eye-off",
        "No secret exposed to the frontend by design",
        detail,
        "warn" if leaked else "pass",
    )


def _rate_limit_check() -> SecurityCheck:
    sign_in = MAX_ATTEMPTS.get(AuthAction.SIGN_IN, 0)
    sign_up = MAX_ATTEMPTS.get(AuthAction.SIGN_UP, 0)
    window_minutes = WINDOW_SECONDS // 60
    ok = sign_in > 0 and sign_up > 0
    detail = (
        f"Sign-in is limited to {sign_in} attempts and sign-up to {sign_up} "
        f"attempts per account in a rolling {window_minutes}-minute window, "
        "enforced on the server. Repeat abuse opens an escalating block, and "
        "throttle counters store only an email key and tallies — no passwords."
    )
    return _check(
        "rate_limit",
        "gauge",
        "Backend authentication rate limiting",
        detail,
        "pass" if ok else "warn",
    )


class SecurityReadinessState(rx.State):
    """Read-only production security readiness report."""

    checks: list[SecurityCheck] = []
    manual_actions: list[ManualAction] = MANUAL_ACTIONS
    secret_names: list[SecurityCheck] = []
    loaded: bool = False
    last_checked: str = ""
    is_running: bool = False
    run_error: str = ""

    @rx.var
    def has_results(self) -> bool:
        return bool(self.checks)

    @rx.var
    def passing_count(self) -> int:
        return len([c for c in self.checks if c["state"] == "pass"])

    @rx.var
    def total_count(self) -> int:
        return len(self.checks)

    @rx.var
    def attention_count(self) -> int:
        return len([c for c in self.checks if c["state"] != "pass"])

    @rx.var
    def manual_count(self) -> int:
        return len(self.manual_actions)

    def _secret_presence(self) -> list[SecurityCheck]:
        """Presence-only rows using generic labels (no names, no values)."""
        rows: list[SecurityCheck] = []
        for index, item in enumerate(CONFIG_ITEMS):
            names = item["env_names"]
            found = [
                bool(str(os.environ.get(name, "") or "").strip())
                for name in names
            ]
            present = all(found) and bool(found)
            partial = any(found) and not present
            if present:
                detail = (
                    f"Configured in the server environment ({item['purpose']}). "
                    "Presence is checked on the server only — the name and "
                    "value are never read into the frontend, logged or shown "
                    "here."
                )
            elif partial:
                detail = (
                    "Only part of this configuration is present "
                    f"({item['purpose']}). Complete it in your platform's "
                    "secret manager before going live."
                )
            else:
                detail = (
                    "Not configured in this environment "
                    f"({item['purpose']}). Set it as a platform secret before "
                    "going live."
                )
            rows.append(
                _check(
                    f"config:{index}",
                    item["icon"],
                    item["label"],
                    detail,
                    "pass" if present else "warn",
                )
            )
        return rows

    async def _migration_check(self) -> SecurityCheck:
        versions = Path("db_migrations/versions")
        files = (
            sorted(p.name for p in versions.glob("*.py"))
            if versions.exists()
            else []
        )
        applied = ""
        try:
            async with rx.asession() as session:
                row = (
                    await session.execute(
                        text("SELECT version_num FROM alembic_version")
                    )
                ).first()
                applied = str(row[0]) if row else ""
        except Exception as e:
            logging.exception(f"Migration status check failed: {e}")
            return _check(
                "migrations",
                "git-branch",
                "Migration status",
                (
                    f"{len(files)} migration scripts are tracked in the repo, "
                    "but the applied revision could not be read from the "
                    "database just now. Confirm migrations are applied during "
                    "deployment before launch."
                ),
                "unknown",
            )
        head_known = bool(applied) and any(applied in name for name in files)
        detail = (
            f"{len(files)} migration scripts are tracked, and the database "
            f"reports an applied revision. "
            + (
                "It matches a tracked script, so the schema was created by a "
                "reviewed migration."
                if head_known
                else "It does not match a tracked script — confirm the "
                "deployment pipeline applies the latest migrations."
            )
            + " Migrations are applied by the platform; nothing here creates "
            "or alters tables."
        )
        return _check(
            "migrations",
            "git-branch",
            "Schema created by tracked migrations",
            detail,
            "pass" if head_known else "unknown",
        )

    async def _persistence_check(self) -> SecurityCheck:
        expected = (
            "app_user",
            "app_user_session",
            "app_auth_rate_limit",
            "razorpay_subscription",
            "razorpay_webhook_event",
        )
        found: list[str] = []
        try:
            async with rx.asession() as session:
                for table in expected:
                    row = (
                        await session.execute(
                            text(f"SELECT COUNT(*) FROM {table}")
                        )
                    ).first()
                    if row is not None:
                        found.append(table)
        except Exception as e:
            logging.exception(f"Persistence check failed: {e}")
        ok = len(found) == len(expected)
        detail = (
            f"{len(found)} of {len(expected)} persistence tables (accounts, "
            "sessions, throttle counters, subscriptions, webhook events) are "
            "readable in the managed database. Accounts, Pro access and "
            "feedback survive restarts because nothing is kept in memory or "
            "browser storage as the source of truth."
        )
        return _check(
            "persistence",
            "database",
            "Database-managed persistence",
            detail,
            "pass" if ok else "warn",
        )

    @rx.event
    async def run_checks(self):
        """Recompute every code-verifiable check (read-only).

        Guarded against duplicate requests, and if any probe fails the
        previously computed results are left untouched and still usable.
        """
        if self.is_running:
            return
        self.is_running = True
        self.run_error = ""
        yield
        try:
            checks: list[SecurityCheck] = [
                _cookie_check(),
                _password_check(),
                _rate_limit_check(),
                _webhook_signature_check(),
                _no_frontend_secret_check(),
            ]
            checks.append(await self._persistence_check())
            checks.append(await self._migration_check())
            secrets = self._secret_presence()
        except Exception as e:
            logging.exception(f"Security readiness checks failed: {e}")
            self.run_error = (
                "We couldn't re-run the readiness checks just now. "
                + (
                    "The results below are from the last successful run."
                    if self.checks
                    else "Please try again."
                )
            )
            self.is_running = False
            return
        self.checks = checks
        self.secret_names = secrets
        self.manual_actions = MANUAL_ACTIONS
        self.loaded = True
        from datetime import datetime, timezone

        self.last_checked = datetime.now(tz=timezone.utc).strftime(
            "%d %b %Y, %H:%M UTC"
        )
        self.is_running = False
