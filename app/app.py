import reflex as rx

from app.pages.about import about_page
from app.pages.auth import login_page, signup_page
from app.pages.dashboard import dashboard_page
from app.pages.data_quality import data_quality_page
from app.pages.feedback import feedback_page
from app.pages.legal import (
    payment_terms_page,
    privacy_page,
    refund_page,
    support_page,
    terms_page,
)
from app.pages.pricing import pricing_page
from app.pages.security import security_readiness_page
from app.pages.upload import upload_page
from app.razorpay_webhook import webhook_api
from app.states.ask_state import AskState
from app.states.auth_state import AuthState
from app.states.dashboard_state import DashboardState
from app.states.feedback_state import FeedbackState
from app.states.filter_state import FilterState
from app.states.forecast_state import ForecastState
from app.states.insight_state import InsightState
from app.states.profit_state import ProfitState
from app.states.report_state import ReportState
from app.states.rfm_state import RFMState
from app.states.security_state import SecurityReadinessState
from app.states.subscription_state import SubscriptionState


def index() -> rx.Component:
    return upload_page()


app = rx.App(
    api_transformer=webhook_api,
    theme=rx.theme(appearance="light"),
    head_components=[
    rx.el.script(
            src="https://www.googletagmanager.com/gtag/js?id=G-Z3Q8KFCD43",
            async_=True,
        ),
        rx.el.script(
            """
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());
            gtag('config', 'G-Z3Q8KFCD43');
            """),
    rx.el.title(
    "InsightSheet – AI Business Analytics from Excel & CSV Data"
),
rx.el.meta(
    name="description",
    content="Turn Excel and CSV data into interactive business dashboards, AI-powered insights, customer analytics, forecasting and actionable reports with InsightSheet.",
),
        rx.el.meta(
            name="google-site-verification",
            content="XrNMyDksjgrV8Yac6jj-dWw99yxQjvI_317dBMmP2Ys",
        ),
        rx.el.style(".rx-built-with-reflex { display: none !important; }"),
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(
            rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""
        ),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap",
            rel="stylesheet",
        ),
    ]
)
app.add_page(
    index,
    route="/",
    on_load=[AuthState.check_session, SubscriptionState.load_status],
)
app.add_page(
    dashboard_page,
    route="/dashboard",
    on_load=[
        AuthState.check_session,
        SubscriptionState.load_status,
        FilterState.build_filters,
        DashboardState.compute_metrics,
        ProfitState.compute_profit,
        RFMState.compute_rfm,
        InsightState.compute_insights,
        ForecastState.compute_forecast,
        AskState.prepare,
        ReportState.prepare,
    ],
)
app.add_page(
    data_quality_page,
    route="/data-quality",
    on_load=[AuthState.check_session, SubscriptionState.load_status],
)
app.add_page(
    feedback_page,
    route="/feedback",
    on_load=[
        AuthState.check_session,
        SubscriptionState.load_status,
        FeedbackState.load_feedback,
    ],
)
app.add_page(
    pricing_page,
    route="/pricing",
    on_load=[AuthState.check_session, SubscriptionState.load_status],
)
app.add_page(
    about_page,
    route="/about",
    on_load=[AuthState.check_session, SubscriptionState.load_status],
)
app.add_page(
    privacy_page,
    route="/privacy",
    on_load=[AuthState.check_session, SubscriptionState.load_status],
)
app.add_page(
    terms_page,
    route="/terms",
    on_load=[AuthState.check_session, SubscriptionState.load_status],
)
app.add_page(
    refund_page,
    route="/refund-policy",
    on_load=[AuthState.check_session, SubscriptionState.load_status],
)
app.add_page(
    payment_terms_page,
    route="/payment-terms",
    on_load=[AuthState.check_session, SubscriptionState.load_status],
)
app.add_page(
    security_readiness_page,
    route="/security-readiness",
    on_load=[
        AuthState.check_session,
        SubscriptionState.load_status,
        SecurityReadinessState.run_checks,
    ],
)
app.add_page(
    support_page,
    route="/support",
    on_load=[AuthState.check_session, SubscriptionState.load_status],
)
app.add_page(login_page, route="/login", on_load=AuthState.check_session)
app.add_page(signup_page, route="/signup", on_load=AuthState.check_session)
