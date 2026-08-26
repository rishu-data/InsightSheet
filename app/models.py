"""Persistent database models for accounts, sessions, feedback and billing.

Only non-sensitive data is stored here. Plaintext passwords, raw session
tokens, card numbers, CVV, UPI PIN, banking passwords, API keys, webhook
secrets and signatures are never persisted — only irreversible hashes of the
password and of the session token are kept.
"""

from __future__ import annotations

import enum
from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    MappedAsDataclass,
    mapped_column,
)


class Base(MappedAsDataclass, DeclarativeBase, kw_only=True):
    """Single declarative base shared by every model in this app."""


class User(Base):
    """A secure user account.

    Stores an email, a normalised lookup key and an irreversible password
    hash. There is never a plaintext password column, and no payment or
    frontend activation fields live here.
    """

    __tablename__ = "app_user"
    __table_args__ = (Index("ix_app_user_is_active", "is_active"),)

    id: Mapped[int] = mapped_column(primary_key=True, init=False)

    email: Mapped[str] = mapped_column(String(320), unique=True, index=True)
    email_normalized: Mapped[str] = mapped_column(
        String(320), unique=True, index=True
    )
    display_name: Mapped[str | None] = mapped_column(
        String(120), default=None, nullable=True
    )

    # Irreversible hash (for example PBKDF2/scrypt) — never a plaintext password.
    password_hash: Mapped[str] = mapped_column(String(255))
    password_algorithm: Mapped[str] = mapped_column(
        String(32), default="pbkdf2_sha256"
    )
    password_updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), default=None, nullable=True
    )

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    last_login_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), default=None, nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        init=False,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=True,
    )

    # No ORM relationships are declared on purpose: on dataclass-mapped models
    # a `relationship(..., default=None, init=False)` writes None into the
    # related attribute at construction time, and on flush SQLAlchemy lets that
    # empty relationship win over an explicitly assigned foreign key, which
    # nulled out `app_user_session.user_id`. Child rows are always written with
    # their `user_id` column directly instead.


class UserSession(Base):
    """A server-side session identifying the current user.

    Only a hash of the opaque session token is stored, so a leaked database row
    cannot be replayed as a session cookie.
    """

    __tablename__ = "app_user_session"
    __table_args__ = (
        Index("ix_app_user_session_user_id", "user_id"),
        Index("ix_app_user_session_expires_at", "expires_at"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, init=False)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("app_user.id", ondelete="CASCADE"), index=True
    )

    # SHA-256 (or stronger) hash of the random session token — never the token.
    session_token_hash: Mapped[str] = mapped_column(
        String(128), unique=True, index=True
    )

    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    revoked_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), default=None, nullable=True
    )
    last_seen_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), default=None, nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        init=False,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=True,
    )


class Feedback(Base):
    """One feedback submission belonging to a single user.

    Stores only: feedback id, user id, rating, category, message, submitted_at.
    """

    __tablename__ = "app_feedback"
    __table_args__ = (
        Index("ix_app_feedback_user_submitted", "user_id", "submitted_at"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, init=False)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("app_user.id", ondelete="CASCADE"), index=True
    )

    rating: Mapped[int] = mapped_column(Integer)
    category: Mapped[str] = mapped_column(String(64))
    message: Mapped[str] = mapped_column(Text)

    submitted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), init=False, server_default=func.now()
    )


class AuthAction(enum.StrEnum):
    """Which authentication action a rate-limit counter belongs to."""

    SIGN_IN = "SIGN_IN"
    SIGN_UP = "SIGN_UP"


class AuthRateLimit(Base):
    """Rolling attempt counters used to throttle authentication abuse.

    One row per (throttle_key, action). The throttle key is an opaque,
    non-sensitive identifier such as a normalised email or a hash of the
    client address — never a password, token or payment credential.
    """

    __tablename__ = "app_auth_rate_limit"
    __table_args__ = (
        Index(
            "uq_app_auth_rate_limit_key_action",
            "throttle_key",
            "action",
            unique=True,
        ),
        Index("ix_app_auth_rate_limit_window_started_at", "window_started_at"),
        Index("ix_app_auth_rate_limit_blocked_until", "blocked_until"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, init=False)

    # Opaque throttle scope, e.g. "email:user@example.com" or "ip:<hash>".
    throttle_key: Mapped[str] = mapped_column(String(255), index=True)

    action: Mapped[AuthAction] = mapped_column(
        Enum(
            AuthAction,
            name="app_auth_rate_limit_action",
            native_enum=False,
            validate_strings=True,
            length=32,
        )
    )

    # Attempts inside the current window, plus a lifetime failure tally.
    attempt_count: Mapped[int] = mapped_column(Integer, default=0)
    failure_count: Mapped[int] = mapped_column(Integer, default=0)

    # Window timing: when the current counting window opened and closes.
    window_started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), default=None, nullable=True
    )
    window_expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), default=None, nullable=True
    )

    # Block timing: while blocked_until is in the future, requests are denied.
    blocked_until: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), default=None, nullable=True
    )
    block_count: Mapped[int] = mapped_column(Integer, default=0)

    last_attempt_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), default=None, nullable=True
    )
    last_success_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), default=None, nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        init=False,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=True,
    )


class SubscriptionStatus(enum.StrEnum):
    """Lifecycle of a Razorpay subscription as reflected by verified webhooks."""

    FREE = "FREE"
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    PAYMENT_FAILED = "PAYMENT_FAILED"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"


class Subscription(Base):
    """Current subscription state for a single user identifier.

    `user_identifier` is an app-level identifier (for example an email or an
    opaque session/account id) — never a payment credential.
    """

    __tablename__ = "razorpay_subscription"
    __table_args__ = (
        Index("ix_razorpay_subscription_status", "status"),
        Index(
            "ix_razorpay_subscription_subscription_id",
            "razorpay_subscription_id",
        ),
        Index("ix_razorpay_subscription_app_user_id", "app_user_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, init=False)

    user_identifier: Mapped[str] = mapped_column(
        String(320), unique=True, index=True
    )

    # Optional link to the authenticated application account. Nullable so
    # pre-existing rows (and webhook events for unknown identifiers) keep
    # working with the `user_identifier` email fallback.
    app_user_id: Mapped[int | None] = mapped_column(
        ForeignKey("app_user.id", ondelete="SET NULL"),
        default=None,
        nullable=True,
    )

    razorpay_subscription_id: Mapped[str | None] = mapped_column(
        String(64), default=None, nullable=True
    )
    razorpay_payment_id: Mapped[str | None] = mapped_column(
        String(64), default=None, nullable=True
    )
    razorpay_plan_id: Mapped[str | None] = mapped_column(
        String(64), default=None, nullable=True
    )

    status: Mapped[SubscriptionStatus] = mapped_column(
        Enum(
            SubscriptionStatus,
            name="razorpay_subscription_status",
            native_enum=False,
            validate_strings=True,
            length=32,
        ),
        default=SubscriptionStatus.FREE,
    )

    activated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), default=None, nullable=True
    )
    cancelled_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), default=None, nullable=True
    )
    expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), default=None, nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        init=False,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=True,
    )


class WebhookEvent(Base):
    """One row per Razorpay webhook event id, used for idempotent processing.

    Stores only the event id, the event name, when it was processed and a short
    safe note (for example the subscription id it applied to). Raw payloads,
    signatures and secrets are never stored.
    """

    __tablename__ = "razorpay_webhook_event"
    __table_args__ = (Index("ix_razorpay_webhook_event_name", "event_name"),)

    id: Mapped[int] = mapped_column(primary_key=True, init=False)

    razorpay_event_id: Mapped[str] = mapped_column(
        String(128), unique=True, index=True
    )
    event_name: Mapped[str] = mapped_column(String(128))

    razorpay_subscription_id: Mapped[str | None] = mapped_column(
        String(64), default=None, nullable=True
    )
    razorpay_payment_id: Mapped[str | None] = mapped_column(
        String(64), default=None, nullable=True
    )

    resulting_status: Mapped[SubscriptionStatus | None] = mapped_column(
        Enum(
            SubscriptionStatus,
            name="razorpay_webhook_event_status",
            native_enum=False,
            validate_strings=True,
            length=32,
        ),
        default=None,
        nullable=True,
    )

    safe_metadata: Mapped[str | None] = mapped_column(
        Text, default=None, nullable=True
    )

    processed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), init=False, server_default=func.now()
    )
