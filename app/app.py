import reflex as rx

from app.pages.about import about_page
from app.pages.admin import ADMIN_TITLE, admin_page
from app.pages.auth import login_page, signup_page
from app.pages.csv_analyzer import (
    CSV_ANALYZER_DESCRIPTION,
    CSV_ANALYZER_TITLE,
    csv_analyzer_page,
)
from app.pages.customer_analytics_solution import (
    CUSTOMER_ANALYTICS_DESCRIPTION,
    CUSTOMER_ANALYTICS_TITLE,
    customer_analytics_solution_page,
)
from app.pages.dashboard import dashboard_page
from app.pages.data_quality import data_quality_page
from app.pages.excel_analytics_solution import (
    EXCEL_ANALYTICS_DESCRIPTION,
    EXCEL_ANALYTICS_TITLE,
    excel_analytics_solution_page,
)
from app.pages.excel_analyzer import (
    EXCEL_ANALYZER_DESCRIPTION,
    EXCEL_ANALYZER_TITLE,
    excel_analyzer_page,
)
from app.pages.feedback import feedback_page
from app.pages.home import HOME_DESCRIPTION, HOME_TITLE, home_page
from app.pages.legal import (
    payment_terms_page,
    privacy_page,
    refund_page,
    support_page,
    terms_page,
)
from app.pages.pricing import pricing_page
from app.pages.profit_margin_calculator import (
    PROFIT_MARGIN_DESCRIPTION,
    PROFIT_MARGIN_TITLE,
    profit_margin_calculator_page,
)
from app.pages.sales_analytics_solution import (
    SALES_ANALYTICS_DESCRIPTION,
    SALES_ANALYTICS_TITLE,
    sales_analytics_solution_page,
)
from app.pages.rfm_calculator import (
    RFM_CALCULATOR_DESCRIPTION,
    RFM_CALCULATOR_TITLE,
    rfm_calculator_page,
)
from app.pages.sales_forecasting import (
    SALES_FORECASTING_DESCRIPTION,
    SALES_FORECASTING_TITLE,
    sales_forecasting_page,
)
from app.pages.sales_growth_calculator import (
    SALES_GROWTH_DESCRIPTION,
    SALES_GROWTH_TITLE,
    sales_growth_calculator_page,
)
from app.pages.security import security_readiness_page
from app.pages.small_business_analytics_solution import (
    SMALL_BUSINESS_ANALYTICS_DESCRIPTION,
    SMALL_BUSINESS_ANALYTICS_TITLE,
    small_business_analytics_solution_page,
)
from app.pages.upload import upload_page
from app.razorpay_webhook import webhook_api
from app.states.admin_state import AdminState
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


NOINDEX: list[dict[str, str]] = [
    {"name": "robots", "content": "noindex,nofollow"}
]

HOME_META: list[dict[str, str]] = [
    {"property": "og:url", "content": "/"},
    {"property": "og:title", "content": HOME_TITLE},
    {"property": "og:description", "content": HOME_DESCRIPTION},
    {"property": "og:type", "content": "website"},
]


# Relative canonical: no truthful production hostname is configured.
HOME_CANONICAL = "/"


def index() -> rx.Component:
    return rx.fragment(
        # Rendered as a document-head element (hoisted into <head>), not a
        # decorative body link, so crawlers read a real canonical tag.
        rx.el.link(rel="canonical", href=HOME_CANONICAL),
        home_page(),
    )


app = rx.App(
    api_transformer=webhook_api,
    head_components=[
        rx.el.script(
            src="https://www.googletagmanager.com/gtag/js?id=G-Z3Q8KFCD43",
            async_=True,
        ),
        rx.el.script("""
                  window.dataLayer = window.dataLayer || [];
                  function gtag(){dataLayer.push(arguments);}
                  gtag('js', new Date());
                  gtag('config', 'G-Z3Q8KFCD43');
                  """),
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
    ],
    theme=rx.theme(appearance="light"),
)
app.add_page(
    index,
    route="/",
    title=HOME_TITLE,
    description=HOME_DESCRIPTION,
    meta=HOME_META,
)
app.add_page(
    upload_page,
    route="/upload",
    meta=NOINDEX,
    on_load=[AuthState.check_session, SubscriptionState.load_status],
    context={"sitemap": None},
)
app.add_page(
    dashboard_page,
    route="/dashboard",
    meta=NOINDEX,
    context={"sitemap": None},
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
    meta=NOINDEX,
    context={"sitemap": None},
    on_load=[AuthState.check_session, SubscriptionState.load_status],
)
app.add_page(
    feedback_page,
    route="/feedback",
    meta=NOINDEX,
    context={"sitemap": None},
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
    excel_analyzer_page,
    route="/tools/excel-analyzer",
    title=EXCEL_ANALYZER_TITLE,
    description=EXCEL_ANALYZER_DESCRIPTION,
)
app.add_page(
    excel_analytics_solution_page,
    route="/solutions/excel-analytics",
    title=EXCEL_ANALYTICS_TITLE,
    description=EXCEL_ANALYTICS_DESCRIPTION,
)
app.add_page(
    sales_analytics_solution_page,
    route="/solutions/sales-analytics",
    title=SALES_ANALYTICS_TITLE,
    description=SALES_ANALYTICS_DESCRIPTION,
)
app.add_page(
    customer_analytics_solution_page,
    route="/solutions/customer-analytics",
    title=CUSTOMER_ANALYTICS_TITLE,
    description=CUSTOMER_ANALYTICS_DESCRIPTION,
)
app.add_page(
    small_business_analytics_solution_page,
    route="/solutions/small-business-analytics",
    title=SMALL_BUSINESS_ANALYTICS_TITLE,
    description=SMALL_BUSINESS_ANALYTICS_DESCRIPTION,
)
app.add_page(
    csv_analyzer_page,
    route="/tools/csv-analyzer",
    title=CSV_ANALYZER_TITLE,
    description=CSV_ANALYZER_DESCRIPTION,
)
app.add_page(
    rfm_calculator_page,
    route="/tools/rfm-calculator",
    title=RFM_CALCULATOR_TITLE,
    description=RFM_CALCULATOR_DESCRIPTION,
)
app.add_page(
    profit_margin_calculator_page,
    route="/tools/profit-margin-calculator",
    title=PROFIT_MARGIN_TITLE,
    description=PROFIT_MARGIN_DESCRIPTION,
)
app.add_page(
    sales_growth_calculator_page,
    route="/tools/sales-growth-calculator",
    title=SALES_GROWTH_TITLE,
    description=SALES_GROWTH_DESCRIPTION,
)
app.add_page(
    sales_forecasting_page,
    route="/tools/sales-forecasting",
    title=SALES_FORECASTING_TITLE,
    description=SALES_FORECASTING_DESCRIPTION,
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
    context={"sitemap": None},
    on_load=[AuthState.check_session, SubscriptionState.load_status],
)
app.add_page(
    payment_terms_page,
    route="/payment-terms",
    context={"sitemap": None},
    on_load=[AuthState.check_session, SubscriptionState.load_status],
)
app.add_page(
    security_readiness_page,
    route="/security-readiness",
    meta=NOINDEX,
    context={"sitemap": None},
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
app.add_page(
    admin_page,
    route="/admin",
    title=ADMIN_TITLE,
    meta=NOINDEX,
    context={"sitemap": None},
    on_load=AdminState.load_admin,
)
app.add_page(
    login_page,
    route="/login",
    meta=NOINDEX,
    context={"sitemap": None},
    on_load=AuthState.check_session,
)
app.add_page(
    signup_page,
    route="/signup",
    meta=NOINDEX,
    context={"sitemap": None},
    on_load=AuthState.check_session,
)
