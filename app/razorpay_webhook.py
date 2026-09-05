"""Secure Razorpay webhook endpoint (backend only).

Security rules enforced here:
  * `RAZORPAY_WEBHOOK_SECRET` is read from the environment only. It is never
    hardcoded, logged, echoed in a response, or returned in an error.
  * Every request must carry `X-Razorpay-Signature`, verified with HMAC-SHA256
    over the *raw* request body and compared in constant time.
  * Nothing is processed before the signature is verified.
  * Responses are short JSON messages. Stack traces are never returned; failures
    are logged server-side with `logging.exception` and answered generically.
  * Only safe billing metadata is persisted (ids, plan, status, amount,
    currency, method). Card numbers, CVV, UPI PIN, tokens, signatures and the
    secret itself are never stored.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import logging
import os
from datetime import datetime, timezone
from typing import Any

import reflex as rx
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, PlainTextResponse, Response
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError

from app.models import Subscription, SubscriptionStatus, User, WebhookEvent

SECRET_ENV_VAR = "RAZORPAY_WEBHOOK_SECRET"
SIGNATURE_HEADER = "X-Razorpay-Signature"
EVENT_ID_HEADER = "x-razorpay-event-id"
WEBHOOK_ROUTE = "/api/razorpay/webhook"

MAX_BODY_BYTES = 1_000_000  # Razorpay payloads are tiny; reject anything huge.
MAX_IDENTIFIER = 320

ACTIVE_EVENTS: frozenset[str] = frozenset(
    {"subscription.activated", "subscription.charged", "payment.captured"}
)
PENDING_EVENTS: frozenset[str] = frozenset(
    {
        "subscription.authenticated",
        "subscription.pending",
        "payment.authorized",
    }
)
FAILED_EVENTS: frozenset[str] = frozenset(
    {"payment.failed", "subscription.halted"}
)
CANCELLED_EVENTS: frozenset[str] = frozenset({"subscription.cancelled"})
EXPIRED_EVENTS: frozenset[str] = frozenset(
    {"subscription.completed", "subscription.expired"}
)

# A PENDING signal must never downgrade a status that already carries meaning.
PENDING_OVERRIDABLE: frozenset[SubscriptionStatus] = frozenset(
    {SubscriptionStatus.FREE, SubscriptionStatus.PENDING}
)

# Note keys that may legitimately carry an app-level user identifier.
NOTE_KEYS: tuple[str, ...] = (
    "user_id",
    "userid",
    "user",
    "account_id",
    "account",
    "identifier",
    "customer_email",
    "email",
)


def _text(value: object, limit: int = MAX_IDENTIFIER) -> str:
    """Coerce any payload value into a short, safe string."""
    if value is None or isinstance(value, (dict, list, tuple, set)):
        return ""
    text = str(value).strip()
    if not text or text.lower() in ("none", "null", "nan"):
        return ""
    return text[:limit]


def _entity(payload: dict[str, Any], key: str) -> dict[str, Any]:
    block = payload.get(key)
    if not isinstance(block, dict):
        return {}
    entity = block.get("entity")
    return entity if isinstance(entity, dict) else {}


def _notes(*entities: dict[str, Any]) -> dict[str, Any]:
    merged: dict[str, Any] = {}
    for entity in entities:
        notes = entity.get("notes")
        if isinstance(notes, dict):
            merged.update(notes)
    return merged


def _stamp(value: object) -> datetime:
    """Convert a Razorpay epoch second value into an aware datetime."""
    try:
        seconds = int(value)  # type: ignore[arg-type]
        if 0 < seconds < 4_000_000_000:
            return datetime.fromtimestamp(seconds, tz=timezone.utc)
    except (TypeError, ValueError):
        pass
    return datetime.now(tz=timezone.utc)


def _fallback_event_id(body: bytes) -> str:
    """Deterministic id derived from the already-verified raw body."""
    return f"body-{hashlib.sha256(body).hexdigest()}"[:128]


def verify_signature(body: bytes, signature: str, secret: str) -> bool:
    """Constant-time HMAC-SHA256 check of the raw body against the header."""
    if not body or not signature or not secret:
        return False
    expected = hmac.new(
        secret.encode("utf-8"), body, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature.strip().lower())


def resolve_user_identifier(payload: dict[str, Any]) -> str:
    """Derive a stable identifier from safe payload fields only.

    There is no auth system in the app, so the identifier is taken from the
    payload in a documented priority order and is never derived from browser
    state: subscription notes, customer notes/payment notes, email, contact,
    customer id, subscription id, then payment order/payment id.
    """
    subscription = _entity(payload, "subscription")
    payment = _entity(payload, "payment")
    customer = _entity(payload, "customer")
    notes = _notes(subscription, customer, payment)

    for key in NOTE_KEYS:
        candidate = _text(notes.get(key))
        if candidate:
            return candidate

    for source in (subscription, customer, payment):
        for key in ("customer_email", "email"):
            candidate = _text(source.get(key))
            if candidate:
                return candidate

    for source in (subscription, customer, payment):
        candidate = _text(source.get("contact"))
        if candidate:
            return candidate

    for source in (subscription, payment):
        candidate = _text(source.get("customer_id"))
        if candidate:
            return candidate
    candidate = _text(customer.get("id"))
    if candidate:
        return candidate

    candidate = _text(subscription.get("id"))
    if candidate:
        return candidate
    candidate = _text(payment.get("order_id")) or _text(payment.get("id"))
    return candidate


def safe_metadata(event_name: str, payload: dict[str, Any]) -> str:
    """Build a compact, non-sensitive JSON note about the event."""
    subscription = _entity(payload, "subscription")
    payment = _entity(payload, "payment")
    data: dict[str, str | int] = {"event": event_name[:128]}
    for label, value in (
        ("subscription_id", subscription.get("id")),
        ("plan_id", subscription.get("plan_id")),
        ("subscription_status", subscription.get("status")),
        ("payment_id", payment.get("id")),
        ("order_id", payment.get("order_id")),
        ("payment_status", payment.get("status")),
        ("method", payment.get("method")),
        ("currency", payment.get("currency") or subscription.get("currency")),
    ):
        text = _text(value, 64)
        if text:
            data[label] = text
    amount = payment.get("amount")
    if isinstance(amount, (int, float)) and 0 <= float(amount) < 1e12:
        data["amount_minor_units"] = int(amount)
    return json.dumps(data, separators=(",", ":"))[:2000]


def _target_status(
    event_name: str, current: SubscriptionStatus | None
) -> SubscriptionStatus | None:
    """Map a verified event name to the status it should produce, if any."""
    if event_name in ACTIVE_EVENTS:
        return SubscriptionStatus.ACTIVE
    if event_name in FAILED_EVENTS:
        return SubscriptionStatus.PAYMENT_FAILED
    if event_name in CANCELLED_EVENTS:
        return SubscriptionStatus.CANCELLED
    if event_name in EXPIRED_EVENTS:
        return SubscriptionStatus.EXPIRED
    if event_name in PENDING_EVENTS:
        if current is None or current in PENDING_OVERRIDABLE:
            return SubscriptionStatus.PENDING
        return None
    return None


def verified_target_status(
    event_name: str,
    current: SubscriptionStatus | None,
    owner_verified: bool,
) -> SubscriptionStatus | None:
    """Status to apply, refusing ACTIVE when ownership is not verified."""
    target = _target_status(event_name, current)
    if target is SubscriptionStatus.ACTIVE and not owner_verified:
        if current is None or current in PENDING_OVERRIDABLE:
            return SubscriptionStatus.PENDING
        return None
    return target


async def _find_subscription(
    session,
    subscription_id: str,
    user_identifier: str,
    verified_app_user_id: int | None = None,
) -> Subscription | None:
    """Locate the row this event applies to, without ever stealing a row.

    A row matched by Razorpay subscription id is always authoritative for that
    subscription. A row matched only by `user_identifier` is used **only** when
    it is unlinked or already linked to the verified app user, so an event
    carrying someone else's identifier can never take over their row.
    """
    if subscription_id:
        rows = (
            await session.scalars(
                select(Subscription)
                .where(Subscription.razorpay_subscription_id == subscription_id)
                .order_by(Subscription.id)
            )
        ).all()
        if rows:
            # Prefer the row owned by the verified app user, else the oldest —
            # this keeps exactly one local row authoritative per subscription.
            if verified_app_user_id is not None:
                for row in rows:
                    if int(row.app_user_id or 0) == verified_app_user_id:
                        return row
            for row in rows:
                if row.app_user_id is not None:
                    return row
            return rows[0]
    if user_identifier:
        row = (
            await session.scalars(
                select(Subscription).where(
                    Subscription.user_identifier == user_identifier
                )
            )
        ).first()
        if row is None:
            return None
        owner = row.app_user_id
        if owner is None or (
            verified_app_user_id is not None
            and int(owner) == verified_app_user_id
        ):
            return row
        return None
    return None


async def _find_app_user_id(session, user_identifier: str) -> int | None:
    """Match a resolved identifier to an existing app account by email.

    Never creates an account and never touches credentials — it only looks up
    `app_user.email` / `app_user.email_normalized` case-insensitively.
    """
    candidate = str(user_identifier or "").strip().lower()
    if not candidate or "@" not in candidate:
        return None
    try:
        row = (
            await session.scalars(
                select(User).where(
                    (func.lower(User.email_normalized) == candidate)
                    | (func.lower(User.email) == candidate)
                )
            )
        ).first()
    except Exception as e:
        logging.exception(f"App user lookup for webhook failed: {e}")
        return None
    if row is None or not row.is_active:
        return None
    return int(row.id)


async def process_event(
    event_name: str,
    event_id: str,
    payload: dict[str, Any],
    created_at: object,
) -> tuple[int, dict[str, str | bool]]:
    """Persist a verified event exactly once and apply its status change."""
    subscription_entity = _entity(payload, "subscription")
    payment_entity = _entity(payload, "payment")
    subscription_id = _text(subscription_entity.get("id"), 64)
    payment_id = _text(payment_entity.get("id"), 64)
    plan_id = _text(subscription_entity.get("plan_id"), 64)
    user_identifier = resolve_user_identifier(payload)

    async with rx.asession() as session:
        seen = (
            await session.scalars(
                select(WebhookEvent).where(
                    WebhookEvent.razorpay_event_id == event_id
                )
            )
        ).first()
        if seen is not None:
            return (
                200,
                {
                    "status": "ok",
                    "message": "Event already processed.",
                    "duplicate": True,
                },
            )

        record: Subscription | None = None
        applied: SubscriptionStatus | None = None
        if user_identifier:
            # Ownership is verified ONLY by matching the payload identifier to
            # an existing app_user email / email_normalized.
            app_user_id = await _find_app_user_id(session, user_identifier)
            record = await _find_subscription(
                session, subscription_id, user_identifier, app_user_id
            )
            if (
                record is not None
                and app_user_id is not None
                and record.app_user_id is None
            ):
                # Link the existing row instead of inserting a duplicate.
                record.app_user_id = app_user_id
            owner_verified = app_user_id is not None or (
                record is not None and record.app_user_id is not None
            )
            current = record.status if record is not None else None
            # Ownership ambiguous => record the signal, never grant Pro access.
            target = verified_target_status(event_name, current, owner_verified)
            if target is not None:
                now = _stamp(created_at)
                if record is None:
                    record = Subscription(
                        user_identifier=user_identifier,
                        razorpay_subscription_id=subscription_id or None,
                        razorpay_payment_id=payment_id or None,
                        razorpay_plan_id=plan_id or None,
                        status=target,
                        app_user_id=app_user_id,
                    )
                    session.add(record)
                else:
                    record.status = target
                    if subscription_id:
                        record.razorpay_subscription_id = subscription_id
                    if payment_id:
                        record.razorpay_payment_id = payment_id
                    if plan_id:
                        record.razorpay_plan_id = plan_id
                if target is SubscriptionStatus.ACTIVE:
                    record.activated_at = now
                elif target is SubscriptionStatus.CANCELLED:
                    record.cancelled_at = now
                elif target is SubscriptionStatus.EXPIRED:
                    record.expires_at = now
                applied = target

        session.add(
            WebhookEvent(
                razorpay_event_id=event_id,
                event_name=event_name[:128],
                razorpay_subscription_id=subscription_id or None,
                razorpay_payment_id=payment_id or None,
                resulting_status=applied,
                safe_metadata=safe_metadata(event_name, payload),
            )
        )
        try:
            await session.commit()
        except IntegrityError:
            # Concurrent delivery of the same event id: treat as a duplicate.
            logging.exception("Unexpected error")
            await session.rollback()
            return (
                200,
                {
                    "status": "ok",
                    "message": "Event already processed.",
                    "duplicate": True,
                },
            )

    if applied is None:
        message = (
            "Event recorded without a subscription status change."
            if user_identifier
            else "Event recorded; no user identifier could be associated."
        )
        return (200, {"status": "ok", "message": message, "duplicate": False})
    return (
        200,
        {
            "status": "ok",
            "message": f"Subscription status set to {applied.value}.",
            "duplicate": False,
        },
    )


webhook_api = FastAPI(
    title="InsightSheet webhooks",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)


def _json(status_code: int, message: str, **extra: object) -> JSONResponse:
    body: dict[str, object] = {
        "status": "ok" if status_code < 400 else "error",
        "message": message,
    }
    body.update(extra)
    return JSONResponse(content=body, status_code=status_code)


@webhook_api.post(WEBHOOK_ROUTE)
async def razorpay_webhook(request: Request) -> JSONResponse:
    """Verify and process a Razorpay webhook delivery."""
    try:
        body = await request.body()
    except Exception as e:
        logging.exception(f"Razorpay webhook: unreadable request body: {e}")
        return _json(400, "Request body could not be read.")

    secret = str(os.environ.get(SECRET_ENV_VAR, "") or "").strip()
    if not secret:
        logging.error(
            "Razorpay webhook rejected: webhook secret is not configured."
        )
        return _json(503, "Webhook processing is not configured.")

    if not body:
        return _json(400, "Empty request body.")
    if len(body) > MAX_BODY_BYTES:
        return _json(413, "Request body too large.")

    signature = str(request.headers.get(SIGNATURE_HEADER, "") or "")
    if not signature:
        return _json(400, "Missing signature header.")
    if not verify_signature(body, signature, secret):
        logging.warning("Razorpay webhook rejected: invalid signature.")
        return _json(401, "Invalid signature.")

    try:
        parsed = json.loads(body.decode("utf-8"))
    except Exception as e:
        logging.exception(f"Razorpay webhook: invalid JSON payload: {e}")
        return _json(400, "Payload is not valid JSON.")
    if not isinstance(parsed, dict):
        return _json(400, "Payload must be a JSON object.")

    event_name = _text(parsed.get("event"), 128)
    if not event_name:
        return _json(400, "Payload is missing an event name.")

    payload = parsed.get("payload")
    payload = payload if isinstance(payload, dict) else {}
    event_id = _text(request.headers.get(EVENT_ID_HEADER), 128) or (
        _fallback_event_id(body)
    )

    try:
        status_code, response = await process_event(
            event_name, event_id, payload, parsed.get("created_at")
        )
    except Exception as e:
        logging.exception(
            f"Razorpay webhook: failed to process event “{event_name}”: {e}"
        )
        return _json(500, "Event could not be processed.")
    return JSONResponse(content=response, status_code=status_code)


@webhook_api.get(WEBHOOK_ROUTE)
async def razorpay_webhook_probe() -> JSONResponse:
    """Razorpay only POSTs here; answer probes without leaking configuration."""
    return _json(405, "Use POST for webhook deliveries.")


# ---------------------------------------------------------------------------
# Public crawler endpoints (no invented hostname: everything is derived from
# the incoming request base URL).
# ---------------------------------------------------------------------------

PUBLIC_ROUTES: tuple[str, ...] = (
    "/",
    "/about",
    "/pricing",
    "/privacy",
    "/terms",
    "/refund-policy",
    "/payment-terms",
    "/support",
)

PRIVATE_ROUTES: tuple[str, ...] = (
    "/upload",
    "/dashboard",
    "/data-quality",
    "/feedback",
    "/security-readiness",
    "/login",
    "/signup",
    "/api/",
)


def _site_base(request: Request) -> str:
    """Origin of the incoming request, without a trailing slash."""
    try:
        return str(request.base_url).rstrip("/")
    except Exception as e:
        logging.exception(f"Could not read request base URL: {e}")
        return ""


def build_robots_txt(base_url: str) -> str:
    lines = ["User-agent: *", "Allow: /"]
    lines.extend(f"Disallow: {path}" for path in PRIVATE_ROUTES)
    if base_url:
        lines.append(f"Sitemap: {base_url}/sitemap.xml")
    return "\n".join(lines) + "\n"


def build_sitemap_xml(base_url: str) -> str:
    from xml.sax.saxutils import escape

    entries = []
    for path in PUBLIC_ROUTES:
        loc = f"{base_url}{path}" if base_url else path
        entries.append(f"  <url><loc>{escape(loc)}</loc></url>")
    body = "\n".join(entries)
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{body}\n"
        "</urlset>\n"
    )


@webhook_api.get("/robots.txt", include_in_schema=False)
async def robots_txt(request: Request) -> PlainTextResponse:
    """Allow public crawling, keep application routes out of the index."""
    return PlainTextResponse(
        content=build_robots_txt(_site_base(request)),
        media_type="text/plain; charset=utf-8",
    )


@webhook_api.get("/sitemap.xml", include_in_schema=False)
async def sitemap_xml(request: Request) -> Response:
    """List only the public pages that actually exist."""
    return Response(
        content=build_sitemap_xml(_site_base(request)),
        media_type="application/xml",
    )
