"""Public marketing homepage.

Deliberately lightweight: it imports no upload, dashboard, analytics,
database, auth or subscription state, so `/` renders without any backend work.
"""

import json

import reflex as rx

HOME_TITLE = "AI-Powered Excel & CSV Analytics | InsightSheet"
HOME_DESCRIPTION = (
    "Analyze Excel and CSV data with AI-powered dashboards, business insights, "
    "RFM segmentation, profitability analysis, forecasting and automated reports."
)

_WEBSITE_JSONLD = json.dumps(
    {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "InsightSheet",
        "url": "/",
        "description": HOME_DESCRIPTION,
    },
    separators=(",", ":"),
)

_SOFTWARE_JSONLD = json.dumps(
    {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": "InsightSheet",
        "url": "/",
        "applicationCategory": "BusinessApplication",
        "operatingSystem": "Web browser",
        "description": HOME_DESCRIPTION,
        "offers": [
            {
                "@type": "Offer",
                "name": "Free",
                "price": "0",
                "priceCurrency": "INR",
            },
            {
                "@type": "Offer",
                "name": "Pro",
                "price": "199",
                "priceCurrency": "INR",
            },
        ],
    },
    separators=(",", ":"),
)

_NAV_LINK = "flex items-center gap-1.5 shrink-0 w-fit rounded-full border border-gray-200 bg-white px-3.5 py-1.5 text-xs font-medium text-gray-600 hover:border-blue-300 hover:text-blue-700 transition-colors"
_FOOTER_LINK = (
    "text-xs font-medium text-gray-500 hover:text-blue-700 transition-colors"
)

_STEPS: list[tuple[str, str, str]] = [
    (
        "cloud-upload",
        "1. Upload your Excel or CSV file",
        "Bring a raw export — CSV, XLS or XLSX. Banner rows, blank lines and duplicates are handled for you.",
    ),
    (
        "wand-sparkles",
        "2. Let InsightSheet clean it",
        "Header detection, date standardisation and currency stripping run automatically and are logged in plain English.",
    ),
    (
        "columns-3",
        "3. Confirm your columns",
        "Map date, revenue, customer, product and order ID so every metric knows what it is measuring.",
    ),
    (
        "layout-dashboard",
        "4. Read your dashboard",
        "Revenue trends, customers, products, segments, forecasts and insights — all calculated from your cleaned rows.",
    ),
]

_FEATURES: list[tuple[str, str, str]] = [
    (
        "sheet",
        "Excel & CSV upload",
        "Upload spreadsheets up to 10 MB and get cleaned, analysis-ready rows without writing a formula.",
    ),
    (
        "layout-dashboard",
        "Interactive dashboards",
        "KPIs, revenue trends and month-over-month change recalculated live as you filter your data.",
    ),
    (
        "users",
        "Revenue & customer analysis",
        "See top customers and products, order counts, average order value and customer inactivity.",
    ),
    (
        "grid-2x2",
        "RFM segmentation",
        "Group customers by recency, frequency and monetary value to see who to keep, win back or nurture.",
    ),
    (
        "percent",
        "Profitability analysis",
        "Bring cost data into the picture to see margin by product and customer, not just revenue.",
    ),
    (
        "trending-up",
        "Sales forecasting",
        "Project the coming months from your own complete months of revenue, with an honest confidence range.",
    ),
    (
        "lightbulb",
        "Automated business insights",
        "Plain-English findings and recommendations derived from your rows — with the evidence behind them.",
    ),
    (
        "file-text",
        "PDF & Excel reports",
        "Export what you are looking at as a shareable report for your team or stakeholders.",
    ),
]

_USE_CASES: list[tuple[str, str, str]] = [
    (
        "shopping-cart",
        "Ecommerce & retail",
        "Turn an order export into product performance, repeat-purchase behaviour and monthly revenue trends.",
    ),
    (
        "briefcase",
        "Small businesses",
        "Replace manual pivot tables with a dashboard you can rebuild in minutes each month.",
    ),
    (
        "handshake",
        "Sales teams",
        "Rank customers, spot accounts that have gone quiet and forecast the next quarter's revenue.",
    ),
    (
        "calculator",
        "Finance & operations",
        "Check margins, review data quality and produce a clean report from a messy source file.",
    ),
    (
        "chart-line",
        "Consultants & analysts",
        "Profile a new client's spreadsheet quickly and show findings without building a model first.",
    ),
    (
        "graduation-cap",
        "Founders & students",
        "Understand a dataset from first principles — every number is traceable back to your rows.",
    ),
]

_FAQ: list[tuple[str, str, str]] = [
    (
        "sheet",
        "What files can I analyse?",
        "CSV, XLS and XLSX files up to 10 MB. Messy exports with banner rows, blank lines and duplicates are expected.",
    ),
    (
        "shield-check",
        "Is my spreadsheet stored anywhere?",
        "Your file is processed on this server for your session to produce your dashboard — it is not shared with third parties or used to train models.",
    ),
    (
        "calculator",
        "Where do the numbers come from?",
        "Every figure is calculated from your cleaned rows after you confirm the column mapping. Nothing is estimated except forecasts, which are clearly labelled as estimates.",
    ),
    (
        "credit-card",
        "Do I need to pay to start?",
        "No. The Free plan covers upload, cleaning, basic KPIs and dashboards. Pro adds forecasting, RFM segmentation, profitability, AI insights and reports.",
    ),
    (
        "trending-up",
        "How accurate is the forecasting?",
        "Forecasts are fitted to your own complete months of revenue and shown with a confidence indicator and prediction range. They are decision support, not guarantees.",
    ),
    (
        "life-buoy",
        "How do I get help?",
        "Support is handled over email — see the Contact / Support page for what to include in your first message.",
    ),
]


def _nav() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.a(
                rx.el.div(
                    rx.icon("sheet", class_name="h-4 w-4 text-white"),
                    class_name="flex items-center justify-center h-8 w-8 rounded-lg bg-blue-600 shrink-0",
                ),
                rx.el.div(
                    rx.el.span(
                        "InsightSheet",
                        class_name="block text-base font-semibold text-gray-900",
                    ),
                    rx.el.span(
                        "Spreadsheet analytics",
                        class_name="block text-xs font-medium text-gray-500",
                    ),
                    class_name="min-w-0",
                ),
                href="/",
                class_name="flex items-center gap-2.5 shrink-0",
            ),
            rx.el.nav(
                rx.el.a(
                    rx.icon("info", class_name="h-3.5 w-3.5"),
                    "About",
                    href="/about",
                    class_name=_NAV_LINK,
                ),
                rx.el.a(
                    rx.icon("credit-card", class_name="h-3.5 w-3.5"),
                    "Pricing",
                    href="/pricing",
                    class_name=_NAV_LINK,
                ),
                rx.el.a(
                    rx.icon("life-buoy", class_name="h-3.5 w-3.5"),
                    "Support",
                    href="/support",
                    class_name=_NAV_LINK,
                ),
                rx.el.a(
                    rx.icon("log-in", class_name="h-3.5 w-3.5"),
                    "Sign in",
                    href="/login",
                    class_name="flex items-center gap-1.5 shrink-0 w-fit rounded-full bg-blue-600 px-3.5 py-1.5 text-xs font-semibold text-white hover:bg-blue-700 transition-colors",
                ),
                class_name="flex items-center gap-2 overflow-x-auto",
            ),
            class_name="flex items-center justify-between gap-4 w-full max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 h-16",
        ),
        class_name="w-full border-b border-gray-200 bg-white/85 backdrop-blur-sm sticky top-0 z-10",
    )


def _sheet_cells(cells: list[str], head: bool) -> list[rx.Component]:
    style = (
        "flex-1 min-w-0 truncate px-2 py-1.5 text-[11px] font-semibold text-gray-500"
        if head
        else "flex-1 min-w-0 truncate px-2 py-1.5 text-[11px] font-medium text-gray-700"
    )
    return [rx.el.div(cell, class_name=style) for cell in cells]


def _sheet_row(cells: list[str], head: bool) -> rx.Component:
    return rx.el.div(
        *_sheet_cells(cells, head),
        class_name=(
            "flex items-center border-b border-gray-200 bg-gray-50"
            if head
            else "flex items-center border-b border-gray-100"
        ),
    )


def _bar(height: str, label: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                class_name=f"w-full rounded-t-md bg-blue-600 {height}",
            ),
            class_name="flex h-24 w-full items-end",
        ),
        rx.el.span(
            label,
            class_name="block text-[10px] font-medium text-gray-400 mt-1 text-center",
        ),
        class_name="flex-1 min-w-0",
    )


def _centerpiece() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("sheet", class_name="h-3.5 w-3.5 text-gray-400"),
                rx.el.span(
                    "sales_export.xlsx",
                    class_name="text-xs font-medium text-gray-500",
                ),
                class_name="flex items-center gap-2 mb-2",
            ),
            _sheet_row(["Date", "Customer", "Product", "Revenue"], True),
            _sheet_row(["2024-01-04", "Acme Ltd", "Starter", "₹12,400"], False),
            _sheet_row(["2024-01-11", "Nova Co", "Pro", "₹31,900"], False),
            _sheet_row(["2024-02-02", "Acme Ltd", "Pro", "₹28,150"], False),
            _sheet_row(["2024-02-19", "Vertex", "Starter", "₹9,750"], False),
            class_name="w-full lg:flex-1 min-w-0 rounded-2xl border border-gray-200 bg-white p-4 shadow-sm",
        ),
        rx.el.div(
            rx.icon(
                "arrow-right",
                class_name="hidden lg:block h-5 w-5 text-indigo-500 shrink-0",
            ),
            rx.icon(
                "arrow-down",
                class_name="lg:hidden h-5 w-5 text-indigo-500 shrink-0",
            ),
            class_name="flex items-center justify-center shrink-0",
        ),
        rx.el.div(
            rx.el.div(
                rx.icon(
                    "layout-dashboard", class_name="h-3.5 w-3.5 text-blue-600"
                ),
                rx.el.span(
                    "Revenue dashboard",
                    class_name="text-xs font-semibold text-gray-900",
                ),
                class_name="flex items-center gap-2",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        "Revenue",
                        class_name="block text-[10px] font-medium text-gray-500",
                    ),
                    rx.el.span(
                        "₹82,200",
                        class_name="block text-sm font-semibold text-gray-900",
                    ),
                    class_name="flex-1 min-w-0 rounded-xl border border-gray-200 bg-gray-50 p-2.5",
                ),
                rx.el.div(
                    rx.el.span(
                        "Orders",
                        class_name="block text-[10px] font-medium text-gray-500",
                    ),
                    rx.el.span(
                        "4",
                        class_name="block text-sm font-semibold text-gray-900",
                    ),
                    class_name="flex-1 min-w-0 rounded-xl border border-gray-200 bg-gray-50 p-2.5",
                ),
                rx.el.div(
                    rx.el.span(
                        "Growth",
                        class_name="block text-[10px] font-medium text-gray-500",
                    ),
                    rx.el.span(
                        "+18%",
                        class_name="block text-sm font-semibold text-green-600",
                    ),
                    class_name="flex-1 min-w-0 rounded-xl border border-gray-200 bg-gray-50 p-2.5",
                ),
                class_name="flex items-stretch gap-2 mt-3",
            ),
            rx.el.div(
                _bar("h-10", "Jan"),
                _bar("h-16", "Feb"),
                _bar("h-14", "Mar"),
                _bar("h-20", "Apr"),
                _bar("h-24", "May"),
                class_name="flex items-end gap-2 mt-4",
            ),
            class_name="w-full lg:flex-1 min-w-0 rounded-2xl border border-gray-200 bg-white p-4 shadow-sm",
        ),
        class_name="flex flex-col lg:flex-row items-stretch gap-4 w-full",
    )


def _hero() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.span(
                rx.icon("sparkles", class_name="h-3.5 w-3.5"),
                "Spreadsheet analytics without formulas",
                class_name="flex items-center gap-1.5 w-fit rounded-full bg-indigo-50 px-3 py-1 text-xs font-semibold text-indigo-700",
            ),
            rx.el.h1(
                "AI-Powered Excel & CSV Analytics for Your Business",
                class_name="text-3xl sm:text-4xl font-semibold tracking-tight text-gray-900 mt-4",
            ),
            rx.el.p(
                "Upload an Excel or CSV export and InsightSheet cleans it, builds an interactive "
                "dashboard and analyses your revenue and customers — including RFM segmentation, "
                "profitability, forecasting, automated business insights and shareable reports.",
                class_name="text-base font-medium text-gray-500 mt-4 max-w-2xl",
            ),
            rx.el.div(
                rx.button(
                    rx.icon("cloud-upload", class_name="h-4 w-4"),
                    "Upload a spreadsheet",
                    on_click=rx.redirect("/upload"),
                    class_name="flex items-center gap-2 w-fit rounded-xl bg-blue-600 px-4 py-2.5 text-sm font-semibold text-white hover:bg-blue-700 transition-colors",
                ),
                rx.el.a(
                    rx.icon("credit-card", class_name="h-4 w-4"),
                    "See pricing",
                    href="/pricing",
                    class_name="flex items-center gap-2 w-fit rounded-xl border border-gray-300 bg-white px-4 py-2.5 text-sm font-semibold text-gray-700 hover:bg-gray-50 transition-colors",
                ),
                rx.el.a(
                    rx.icon("layout-dashboard", class_name="h-4 w-4"),
                    "Explore Features",
                    href="#features",
                    class_name="flex items-center gap-2 w-fit rounded-xl border border-blue-200 bg-blue-50 px-4 py-2.5 text-sm font-semibold text-blue-700 hover:bg-blue-100 transition-colors",
                ),
                class_name="flex flex-wrap items-center gap-3 mt-6",
            ),
            rx.el.div(
                rx.icon(
                    "lock", class_name="h-3.5 w-3.5 text-gray-400 shrink-0"
                ),
                rx.el.p(
                    "Your file is processed on this server for your session and never shared.",
                    class_name="text-xs font-medium text-gray-500",
                ),
                class_name="flex items-center gap-2 mt-4",
            ),
            class_name="w-full lg:flex-1 min-w-0",
        ),
        rx.el.div(_centerpiece(), class_name="w-full lg:flex-1 min-w-0"),
        class_name="flex flex-col lg:flex-row items-center gap-8 w-full rounded-2xl border border-gray-200 bg-white p-6 sm:p-8 shadow-sm",
    )


def _icon_card(item: tuple[str, str, str]) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(item[0], class_name="h-4 w-4 text-blue-600"),
            class_name="flex items-center justify-center h-9 w-9 rounded-lg bg-blue-50 shrink-0",
        ),
        rx.el.div(
            rx.el.h3(item[1], class_name="text-sm font-semibold text-gray-900"),
            rx.el.p(
                item[2], class_name="text-sm font-medium text-gray-500 mt-1"
            ),
            class_name="min-w-0",
        ),
        class_name="flex items-start gap-3 rounded-2xl border border-gray-200 bg-white p-5 shadow-sm w-full",
    )


def _icon_cards(items: list[tuple[str, str, str]]) -> list[rx.Component]:
    return [_icon_card(item) for item in items]


def _section(
    heading: str,
    subtitle: str,
    items: list[tuple[str, str, str]],
    grid: str,
    section_id: str = "",
) -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.h2(
                heading,
                class_name="text-2xl font-semibold tracking-tight text-gray-900",
            ),
            rx.el.p(
                subtitle,
                class_name="text-sm font-medium text-gray-500 mt-1 max-w-3xl",
            ),
            class_name="w-full",
        ),
        rx.el.div(
            *_icon_cards(items),
            class_name=grid,
        ),
        id=section_id,
        class_name="flex flex-col gap-4 w-full",
    )


def _cta() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.h2(
                "Ready to turn your spreadsheet into a dashboard?",
                class_name="text-2xl font-semibold tracking-tight text-gray-900",
            ),
            rx.el.p(
                "Start on the Free plan — no card details required. Upload a file, confirm your "
                "columns and read your numbers in minutes.",
                class_name="text-sm font-medium text-gray-500 mt-1 max-w-2xl",
            ),
            class_name="min-w-0 flex-1",
        ),
        rx.el.div(
            rx.el.a(
                rx.icon("cloud-upload", class_name="h-4 w-4"),
                "Start free",
                href="/upload",
                class_name="flex items-center gap-2 w-fit rounded-xl bg-indigo-600 px-4 py-2.5 text-sm font-semibold text-white hover:bg-indigo-700 transition-colors",
            ),
            rx.el.a(
                rx.icon("info", class_name="h-4 w-4"),
                "How it works",
                href="/about",
                class_name="flex items-center gap-2 w-fit rounded-xl border border-gray-300 bg-white px-4 py-2.5 text-sm font-semibold text-gray-700 hover:bg-gray-50 transition-colors",
            ),
            class_name="flex flex-wrap items-center gap-3 shrink-0",
        ),
        class_name="flex flex-wrap items-center justify-between gap-4 rounded-2xl border border-indigo-200 bg-indigo-50 p-6 sm:p-8 w-full",
    )


def _footer() -> rx.Component:
    return rx.el.footer(
        rx.el.div(
            rx.el.p(
                "\u00a9 InsightSheet \u2014 spreadsheet analytics",
                class_name="text-xs font-medium text-gray-500",
            ),
            rx.el.nav(
                rx.el.a("About", href="/about", class_name=_FOOTER_LINK),
                rx.el.a("Pricing", href="/pricing", class_name=_FOOTER_LINK),
                rx.el.a(
                    "Privacy Policy", href="/privacy", class_name=_FOOTER_LINK
                ),
                rx.el.a(
                    "Terms of Service", href="/terms", class_name=_FOOTER_LINK
                ),
                rx.el.a(
                    "Refund & Cancellation",
                    href="/refund-policy",
                    class_name=_FOOTER_LINK,
                ),
                rx.el.a(
                    "Payment & Subscription",
                    href="/payment-terms",
                    class_name=_FOOTER_LINK,
                ),
                rx.el.a(
                    "Contact / Support",
                    href="/support",
                    class_name=_FOOTER_LINK,
                ),
                class_name="flex flex-wrap items-center gap-x-4 gap-y-2",
            ),
            class_name="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 w-full max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-6",
        ),
        class_name="w-full border-t border-gray-200 bg-white mt-auto",
    )


def home_page() -> rx.Component:
    return rx.el.div(
        rx.el.script(_WEBSITE_JSONLD, type="application/ld+json"),
        rx.el.script(_SOFTWARE_JSONLD, type="application/ld+json"),
        _nav(),
        rx.el.main(
            _hero(),
            _section(
                "How InsightSheet Works",
                "Four steps from a raw export to a dashboard you can trust.",
                _STEPS,
                "grid grid-cols-1 md:grid-cols-2 gap-4 w-full",
            ),
            _section(
                "Features",
                "Everything you need to analyse a sales spreadsheet, from cleaning to reporting.",
                _FEATURES,
                "grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4 w-full",
                "features",
            ),
            _section(
                "Use Cases",
                "Built for anyone whose numbers currently live in a spreadsheet.",
                _USE_CASES,
                "grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 w-full",
            ),
            _section(
                "FAQ",
                "The questions we are asked most often before the first upload.",
                _FAQ,
                "grid grid-cols-1 md:grid-cols-2 gap-4 w-full",
            ),
            _cta(),
            class_name="flex flex-col gap-10 w-full max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-10",
        ),
        _footer(),
        class_name="font-['Inter'] flex min-h-screen w-full flex-col bg-gray-50",
    )
