"""Per-account feedback capture backed by the managed database.

Every submission is stored in the `app_feedback` table against the signed-in
user id, and only that user's own history is ever loaded back. Signed-out
visitors are asked to sign in instead of storing anonymous feedback.

Only feedback id, user id, rating, category, message and submitted_at are
persisted. Nothing here touches Razorpay, pricing or Pro features.
"""

import logging
from typing import TypedDict

import reflex as rx
from sqlalchemy import select

from app.models import Feedback
from app.states.auth_state import current_user

CATEGORIES: list[str] = [
    "Overall Experience",
    "Dashboard",
    "Analytics",
    "AI Insights",
    "RFM Analysis",
    "Forecasting",
    "Reports & Exports",
    "Data Upload",
    "Other",
]

DEFAULT_CATEGORY = "Overall Experience"
SUCCESS_MESSAGE = "Thank you for your feedback! \u2b50"
SIGN_IN_REQUIRED = (
    "Please sign in to save feedback to your account — we don't store "
    "anonymous feedback."
)
HISTORY_LIMIT = 100

RATING_LABELS: dict[int, str] = {
    0: "No rating selected yet",
    1: "Poor",
    2: "Fair",
    3: "Good",
    4: "Very good",
    5: "Excellent",
}


class FeedbackEntry(TypedDict):
    id: str
    rating: int
    category: str
    message: str
    submitted_at: str


class FeedbackState(rx.State):
    """Holds the feedback form and this account's saved submissions."""

    rating: int = 0
    category: str = DEFAULT_CATEGORY
    message: str = ""

    error_message: str = ""
    success_message: str = ""
    is_submitting: bool = False
    is_loading: bool = False
    form_key: int = 0
    signed_in: bool = False

    entries: list[FeedbackEntry] = []

    @rx.var
    def has_rating(self) -> bool:
        return 1 <= self.rating <= 5

    @rx.var
    def rating_label(self) -> str:
        return RATING_LABELS.get(self.rating, RATING_LABELS[0])

    @rx.var
    def rating_display(self) -> str:
        if not self.has_rating:
            return "Not rated"
        return f"{self.rating} of 5"

    @rx.var
    def character_count(self) -> int:
        return len(self.message.strip())

    @rx.var
    def can_submit(self) -> bool:
        return self.has_rating and bool(self.message.strip())

    @rx.var
    def submission_count(self) -> int:
        return len(self.entries)

    @rx.var
    def has_entries(self) -> bool:
        return len(self.entries) > 0

    @rx.var
    def average_rating_display(self) -> str:
        if not self.entries:
            return "\u2014"
        total = sum(int(entry["rating"]) for entry in self.entries)
        return f"{total / len(self.entries):.1f} / 5"

    @rx.event
    def select_rating(self, value: int):
        try:
            rating = int(value)
        except (TypeError, ValueError):
            rating = 0
        self.rating = rating if 1 <= rating <= 5 else 0
        self.error_message = ""
        self.success_message = ""

    @rx.event
    def select_category(self, value: str):
        choice = str(value or "")
        self.category = choice if choice in CATEGORIES else DEFAULT_CATEGORY
        self.success_message = ""

    @rx.event
    def set_message(self, value: str):
        self.message = str(value or "")
        if self.message.strip():
            self.error_message = ""
        self.success_message = ""

    @rx.event
    def clear_form(self):
        self._reset_form()
        self.error_message = ""
        self.success_message = ""

    def _reset_form(self) -> None:
        self.rating = 0
        self.category = DEFAULT_CATEGORY
        self.message = ""
        self.form_key += 1

    @staticmethod
    def _to_entry(row: Feedback) -> FeedbackEntry:
        stamp = row.submitted_at
        return FeedbackEntry(
            id=f"feedback-{int(row.id)}",
            rating=int(row.rating or 0),
            category=str(row.category or DEFAULT_CATEGORY),
            message=str(row.message or ""),
            submitted_at=(
                stamp.strftime("%b %d, %Y at %H:%M") if stamp else ""
            ),
        )

    @rx.event
    async def load_feedback(self):
        """Load only the signed-in user's own saved feedback."""
        user_id, _email = await current_user(self)
        self.signed_in = user_id > 0
        if not user_id:
            self.entries = []
            return
        self.is_loading = True
        yield
        try:
            async with rx.asession() as session:
                rows = (
                    await session.scalars(
                        select(Feedback)
                        .where(Feedback.user_id == user_id)
                        .order_by(
                            Feedback.submitted_at.desc(), Feedback.id.desc()
                        )
                        .limit(HISTORY_LIMIT)
                    )
                ).all()
                self.entries = [self._to_entry(row) for row in rows]
        except Exception as e:
            logging.exception(f"Loading feedback history failed: {e}")
            self.entries = []
            self.error_message = (
                "We couldn't load your feedback history just now. "
                "Please refresh and try again."
            )
        finally:
            self.is_loading = False

    @rx.event
    async def submit_feedback(self, form_data: dict):
        """Validate, save against the current account, then reset the form."""
        typed = str(form_data.get("message", "") or "")
        text = (typed if typed.strip() else self.message).strip()
        self.success_message = ""

        user_id, _email = await current_user(self)
        self.signed_in = user_id > 0
        if not user_id:
            self.entries = []
            self.error_message = SIGN_IN_REQUIRED
            return

        if not self.has_rating and not text:
            self.error_message = (
                "Please choose a star rating and tell us what you think "
                "before submitting."
            )
            return
        if not self.has_rating:
            self.error_message = (
                "Please choose a star rating from 1 to 5 before submitting."
            )
            return
        if not text:
            self.error_message = (
                "Please write a short note about your experience before "
                "submitting — empty feedback can't be sent."
            )
            return

        self.error_message = ""
        self.is_submitting = True
        yield
        category = (
            self.category if self.category in CATEGORIES else DEFAULT_CATEGORY
        )
        try:
            async with rx.asession() as session:
                record = Feedback(
                    user_id=user_id,
                    rating=int(self.rating),
                    category=category,
                    message=text[:5000],
                )
                # Guard the foreign key explicitly so a submission is never
                # written without its owning account.
                if record.user_id != user_id:
                    record.user_id = user_id
                session.add(record)
                await session.flush()
                if record.user_id is None or int(record.user_id) != user_id:
                    await session.rollback()
                    raise ValueError(
                        "Feedback insert aborted: owner id did not persist"
                    )
                await session.commit()
                await session.refresh(record)
                entry = self._to_entry(record)
            self.entries.insert(0, entry)
            del self.entries[HISTORY_LIMIT:]
            self._reset_form()
            self.success_message = SUCCESS_MESSAGE
        except Exception as e:
            logging.exception(f"Error saving feedback: {e}")
            self.error_message = (
                "Something went wrong saving that feedback. Please try again."
            )
        finally:
            self.is_submitting = False
