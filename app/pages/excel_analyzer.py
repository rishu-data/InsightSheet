"""Public SEO landing page for the Excel analytics tool.

Stateless and dependency-free: it imports no auth, upload, dashboard,
analytics, database or subscription state, so the route renders as static
semantic HTML with no backend work.
"""

import reflex as rx

EXCEL_ANALYZER_TITLE = (
    "Excel Analytics Tool – Analyze Excel Files Online | InsightSheet"
)
EXCEL_ANALYZER_DESCRIPTION = (
    "Analyze Excel files online with InsightSheet. Turn Excel data into "
    "dashboards, KPIs, sales insights, customer analysis, charts and "
    "actionable business insights."
)
EXCEL_ANALYZER_CANONICAL = "https://reflex-build-generation-silver-apple.reflex.run/tools/excel-analyzer"

_NAV_LINK = "flex items-center gap-1.5 shrink-0 w-fit rounded-full border border-gray-200 bg-white px-3.5 py-1.5 text-xs font-medium text-gray-600 hover:border-blue-300 hover:text-blue-700 transition-colors"
_FOOTER_LINK = (
    "text-xs font-medium text-gray-500 hover:text-blue-700 transition-colors"
)
_CARD = "rounded-2xl border border-gray-200 bg-white p-5 shadow-sm w-full"
_H2 = "text-2xl font-semibold tracking-tight text-gray-900"
_H3 = "text-sm font-semibold text-gray-900"
_BODY = "text-sm font-medium text-gray-500 mt-1"

_WHAT_IT_DOES: list[tuple[str, str, str]] = [
    (
        "brush-cleaning",
        "Reads a messy export as-is",
        "An Excel analytics tool starts where your file actually is: banner rows above the header, blank lines, duplicated orders and currency symbols inside number columns.",
    ),
    (
        "columns-3",
        "Gives each column a meaning",
        "Once you tell it which column holds the date, revenue, customer, product and order ID, every metric knows exactly what it is measuring.",
    ),
    (
        "calculator",
        "Calculates instead of guessing",
        "Totals, averages, growth and rankings are computed from your own rows, so any number on screen can be traced back to the source data.",
    ),
    (
        "layout-dashboard",
        "Presents it as a dashboard",
        "Instead of a wall of cells you get KPIs, trends and tables you can filter — the same questions you would answer with pivot tables, without building them.",
    ),
]

_HOW_TO_ANALYZE: list[tuple[str, str, str]] = [
    (
        "file-spreadsheet",
        "Start with one flat sheet",
        "Keep one row per transaction and one header row. Merged cells, subtotal rows and side-by-side tables make columns ambiguous.",
    ),
    (
        "calendar",
        "Include a date column",
        "A usable date column is what makes trends, month-over-month change and forecasting possible at all.",
    ),
    (
        "indian-rupee",
        "Include an amount column",
        "Revenue or order value is the backbone of the analysis. Costs are optional and unlock margin views when present.",
    ),
    (
        "user-round",
        "Add customer and product identifiers",
        "Even a plain name column is enough to rank customers, count repeat orders and compare products.",
    ),
]

_WORKFLOW: list[tuple[str, str, str]] = [
    (
        "cloud-upload",
        "Upload",
        "Choose a CSV, XLS or XLSX export. The file is read on the server for your session to build your dashboard.",
    ),
    (
        "wand-sparkles",
        "Clean",
        "Header detection, date standardisation, duplicate removal and currency stripping run automatically and are logged in plain English.",
    ),
    (
        "list-checks",
        "Map columns",
        "Confirm the suggested mapping for date, revenue, customer, product and order ID — you stay in control of what each metric uses.",
    ),
    (
        "gauge",
        "Review quality",
        "A data-quality summary shows missing values, unparsed dates and rows that were dropped, before you read any conclusions.",
    ),
    (
        "layout-dashboard",
        "Read the dashboard",
        "KPIs, revenue trends, customer and product breakdowns, segments, forecasts and written insights, all filterable.",
    ),
    (
        "file-text",
        "Export",
        "Save what you are looking at as a PDF or Excel report to share with your team.",
    ),
]

_REVENUE: list[tuple[str, str, str]] = [
    (
        "indian-rupee",
        "Total and filtered revenue",
        "See revenue for the whole file or for any date range, customer or product you filter to.",
    ),
    (
        "chart-line",
        "Trend over time",
        "Revenue grouped by month shows whether the direction of travel is up, flat or down.",
    ),
    (
        "percent",
        "Month-over-month change",
        "The change between complete months is calculated for you, so you are not comparing a partial month to a full one.",
    ),
    (
        "receipt",
        "Orders and average order value",
        "Order counts and average order value separate 'more orders' from 'bigger orders' when revenue moves.",
    ),
]

_CUSTOMERS: list[tuple[str, str, str]] = [
    (
        "users",
        "Top customers by revenue",
        "Rank accounts by what they actually spent in the period you are looking at.",
    ),
    (
        "repeat",
        "Repeat versus one-time buyers",
        "Order frequency per customer shows how much of your revenue depends on returning buyers.",
    ),
    (
        "clock",
        "Inactive customers",
        "Recency highlights accounts that used to order and have gone quiet, which is usually the cheapest revenue to recover.",
    ),
    (
        "grid-2x2",
        "RFM segmentation",
        "Recency, frequency and monetary value group customers into segments you can act on — keep, nurture or win back.",
    ),
]

_PRODUCTS: list[tuple[str, str, str]] = [
    (
        "package",
        "Best and worst sellers",
        "Compare products by revenue and by units to see which ones carry the period.",
    ),
    (
        "percent",
        "Margin by product",
        "When your file includes cost, revenue rankings and margin rankings can be compared side by side.",
    ),
    (
        "chart-column",
        "Product mix over time",
        "Watch how the share of revenue moves between products from month to month.",
    ),
    (
        "search",
        "Long tail",
        "Products with very few orders are easy to miss in a spreadsheet and easy to spot in a ranked table.",
    ),
]

_KPIS: list[tuple[str, str, str]] = [
    (
        "gauge",
        "KPI cards",
        "Revenue, orders, average order value, customer count and growth sit at the top of the dashboard and update with your filters.",
    ),
    (
        "chart-line",
        "Trend charts",
        "Time-series views for revenue and orders make seasonality and step changes visible at a glance.",
    ),
    (
        "chart-column",
        "Ranked comparisons",
        "Bar-style breakdowns for customers, products and segments answer 'who' and 'what' questions quickly.",
    ),
    (
        "filter",
        "Filters that recalculate",
        "Every KPI and chart is recomputed from the filtered rows, so a segment view is never a stale total.",
    ),
]

_INSIGHTS: list[tuple[str, str, str]] = [
    (
        "lightbulb",
        "Findings in plain English",
        "Written observations describe what the numbers show — concentration, decline, inactivity, unusual months — with the evidence behind each one.",
    ),
    (
        "list-checks",
        "Suggested next steps",
        "Recommendations point at a specific list of customers or products rather than generic advice.",
    ),
    (
        "trending-up",
        "Forecasts, clearly labelled",
        "Projections are fitted to your own complete months and shown with a range, as decision support rather than a promise.",
    ),
    (
        "shield-check",
        "Caveats included",
        "Where the data is thin or a column was partly unparsable, the report says so instead of hiding it.",
    ),
]

_AUDIENCE: list[tuple[str, str, str]] = [
    (
        "shopping-cart",
        "Ecommerce and retail",
        "Turn an order export into product performance, repeat-purchase behaviour and monthly revenue trends.",
    ),
    (
        "briefcase",
        "Small business owners",
        "Get a monthly read on the business without rebuilding pivot tables each time.",
    ),
    (
        "handshake",
        "Sales teams",
        "Rank accounts, find quiet customers and prepare a pipeline conversation from real history.",
    ),
    (
        "calculator",
        "Finance and operations",
        "Check margins, verify data quality and produce a clean report from a messy source file.",
    ),
    (
        "chart-line",
        "Consultants and analysts",
        "Profile a new client's spreadsheet quickly and discuss findings before building a model.",
    ),
    (
        "graduation-cap",
        "Founders and students",
        "Learn a dataset from first principles, with every figure traceable to a row.",
    ),
]

_STEPS: list[tuple[str, str, str]] = [
    (
        "cloud-upload",
        "Step 1 — Upload your Excel file",
        "Pick a CSV, XLS or XLSX export of your sales or transaction data. Cleaning runs automatically and is logged.",
    ),
    (
        "columns-3",
        "Step 2 — Confirm your columns",
        "Map date, revenue, customer, product and order ID so each metric measures the right thing.",
    ),
    (
        "layout-dashboard",
        "Step 3 — Read your dashboard",
        "KPIs, revenue and customer analysis, product performance, charts, insights and exportable reports.",
    ),
]

_FAQ: list[tuple[str, str]] = [
    (
        "Which Excel file types can I analyze?",
        "CSV, XLS and XLSX files up to 10 MB. Real-world exports with banner rows above the header, blank lines and duplicated orders are expected and handled during cleaning.",
    ),
    (
        "Do I need formulas, pivot tables or macros?",
        "No. You do not write any formula. You upload the file, confirm which column is which, and the analysis is computed for you.",
    ),
    (
        "What columns does my file need?",
        "A date column and an amount column are the minimum for trends and totals. Customer, product and order ID columns unlock customer analysis, product performance and order-level metrics.",
    ),
    (
        "How are the numbers calculated?",
        "Every metric is computed from your cleaned rows after you confirm the column mapping. Forecasts are the only estimated figures, and they are labelled as estimates with a range.",
    ),
    (
        "What happens to my file?",
        "Your spreadsheet is processed on this server for your session to build your dashboard. It is not shared with third parties or used to train models.",
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
                    rx.icon("house", class_name="h-3.5 w-3.5"),
                    "Home",
                    href="/",
                    class_name=_NAV_LINK,
                ),
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
                    rx.icon("cloud-upload", class_name="h-3.5 w-3.5"),
                    "Upload a file",
                    href="/upload",
                    class_name="flex items-center gap-1.5 shrink-0 w-fit rounded-full bg-blue-600 px-3.5 py-1.5 text-xs font-semibold text-white hover:bg-blue-700 transition-colors",
                ),
                class_name="flex items-center gap-2 overflow-x-auto",
            ),
            class_name="flex items-center justify-between gap-4 w-full max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 h-16",
        ),
        class_name="w-full border-b border-gray-200 bg-white/85 backdrop-blur-sm sticky top-0 z-10",
    )


def _sheet_row(cells: list[str], head: bool) -> rx.Component:
    return rx.el.div(
        *[
            rx.el.div(
                cell,
                class_name=(
                    "flex-1 min-w-0 truncate px-2 py-1.5 text-[11px] font-semibold text-gray-500"
                    if head
                    else "flex-1 min-w-0 truncate px-2 py-1.5 text-[11px] font-medium text-gray-700"
                ),
            )
            for cell in cells
        ],
        class_name=(
            "flex items-center border-b border-gray-200 bg-gray-50"
            if head
            else "flex items-center border-b border-gray-100"
        ),
    )


def _bar(height: str, label: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(class_name=f"w-full rounded-t-md bg-blue-600 {height}"),
            class_name="flex h-20 w-full items-end",
        ),
        rx.el.span(
            label,
            class_name="block text-[10px] font-medium text-gray-400 mt-1 text-center",
        ),
        class_name="flex-1 min-w-0",
    )


def _kpi_tile(label: str, value: str, value_class: str) -> rx.Component:
    return rx.el.div(
        rx.el.span(
            label, class_name="block text-[10px] font-medium text-gray-500"
        ),
        rx.el.span(
            value, class_name=f"block text-sm font-semibold {value_class}"
        ),
        class_name="flex-1 min-w-0 rounded-xl border border-gray-200 bg-gray-50 p-2.5",
    )


def _flow_diagram() -> rx.Component:
    return rx.el.figure(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("sheet", class_name="h-3.5 w-3.5 text-gray-400"),
                    rx.el.span(
                        "excel_export.xlsx",
                        class_name="text-xs font-medium text-gray-500",
                    ),
                    class_name="flex items-center gap-2 mb-2",
                ),
                _sheet_row(["Date", "Customer", "Product", "Amount"], True),
                _sheet_row(
                    ["2024-03-05", "Acme Ltd", "Starter", "₹14,200"], False
                ),
                _sheet_row(["2024-03-18", "Nova Co", "Pro", "₹26,400"], False),
                _sheet_row(["2024-04-02", "Vertex", "Pro", "₹19,850"], False),
                _sheet_row(
                    ["2024-04-27", "Acme Ltd", "Starter", "₹11,300"], False
                ),
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
                        "layout-dashboard",
                        class_name="h-3.5 w-3.5 text-blue-600",
                    ),
                    rx.el.span(
                        "Excel dashboard",
                        class_name="text-xs font-semibold text-gray-900",
                    ),
                    class_name="flex items-center gap-2",
                ),
                rx.el.div(
                    _kpi_tile("Revenue", "₹71,750", "text-gray-900"),
                    _kpi_tile("Orders", "4", "text-gray-900"),
                    _kpi_tile("Customers", "3", "text-gray-900"),
                    class_name="flex items-stretch gap-2 mt-3",
                ),
                rx.el.div(
                    _bar("h-8", "Jan"),
                    _bar("h-12", "Feb"),
                    _bar("h-16", "Mar"),
                    _bar("h-14", "Apr"),
                    _bar("h-20", "May"),
                    class_name="flex items-end gap-2 mt-4",
                ),
                class_name="w-full lg:flex-1 min-w-0 rounded-2xl border border-gray-200 bg-white p-4 shadow-sm",
            ),
            class_name="flex flex-col lg:flex-row items-stretch gap-4 w-full",
        ),
        rx.el.figcaption(
            "Illustration: a flat Excel sheet on the left becomes mapped columns, KPIs and a revenue trend on the right. Figures shown are sample values.",
            class_name="text-xs font-medium text-gray-400 mt-3",
        ),
        class_name="w-full m-0",
    )


def _hero() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.span(
                rx.icon("sheet", class_name="h-3.5 w-3.5"),
                "Excel analytics tool",
                class_name="flex items-center gap-1.5 w-fit rounded-full bg-indigo-50 px-3 py-1 text-xs font-semibold text-indigo-700",
            ),
            rx.el.h1(
                "Excel Analytics Tool – Analyze Your Excel Data",
                class_name="text-3xl sm:text-4xl font-semibold tracking-tight text-gray-900 mt-4",
            ),
            rx.el.p(
                "Analyze Excel files online without writing a formula. Upload an XLSX, XLS or CSV "
                "export and InsightSheet cleans it, maps your columns and builds a dashboard with "
                "KPIs, revenue and sales analysis, customer and product breakdowns, charts and "
                "written business insights — all calculated from your own rows.",
                class_name="text-base font-medium text-gray-500 mt-4 max-w-2xl",
            ),
            rx.el.div(
                rx.el.a(
                    rx.icon("cloud-upload", class_name="h-4 w-4"),
                    "Analyze an Excel file",
                    href="/upload",
                    class_name="flex items-center gap-2 w-fit rounded-xl bg-blue-600 px-4 py-2.5 text-sm font-semibold text-white hover:bg-blue-700 transition-colors",
                ),
                rx.el.a(
                    rx.icon("arrow-down", class_name="h-4 w-4"),
                    "See how it works",
                    href="#how-it-works",
                    class_name="flex items-center gap-2 w-fit rounded-xl border border-gray-300 bg-white px-4 py-2.5 text-sm font-semibold text-gray-700 hover:bg-gray-50 transition-colors",
                ),
                class_name="flex flex-wrap items-center gap-3 mt-6",
            ),
            rx.el.p(
                rx.el.span(
                    "Prefer the full overview first? Read about the whole ",
                    class_name="text-xs font-medium text-gray-500",
                ),
                rx.el.a(
                    "InsightSheet spreadsheet analytics platform",
                    href="/",
                    class_name="text-xs font-semibold text-blue-700 hover:underline",
                ),
                rx.el.span(".", class_name="text-xs font-medium text-gray-500"),
                class_name="mt-4",
            ),
            class_name="w-full lg:flex-1 min-w-0",
        ),
        rx.el.div(_flow_diagram(), class_name="w-full lg:flex-1 min-w-0"),
        class_name="flex flex-col lg:flex-row items-center gap-8 w-full rounded-2xl border border-gray-200 bg-white p-6 sm:p-8 shadow-sm",
    )


def _card(item: tuple[str, str, str]) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(item[0], class_name="h-4 w-4 text-blue-600"),
            class_name="flex items-center justify-center h-9 w-9 rounded-lg bg-blue-50 shrink-0",
        ),
        rx.el.div(
            rx.el.h3(item[1], class_name=_H3),
            rx.el.p(item[2], class_name=_BODY),
            class_name="min-w-0",
        ),
        class_name=f"flex items-start gap-3 {_CARD}",
    )


def _section(
    heading: str,
    subtitle: str,
    items: list[tuple[str, str, str]],
    grid: str,
    section_id: str = "",
) -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.h2(heading, class_name=_H2),
            rx.el.p(
                subtitle,
                class_name="text-sm font-medium text-gray-500 mt-1 max-w-3xl",
            ),
            class_name="w-full",
        ),
        rx.el.div(
            *[_card(item) for item in items],
            class_name=grid,
        ),
        id=section_id,
        class_name="flex flex-col gap-4 w-full",
    )


def _step_card(item: tuple[str, str, str]) -> rx.Component:
    return rx.el.li(
        rx.el.div(
            rx.icon(item[0], class_name="h-4 w-4 text-indigo-600"),
            class_name="flex items-center justify-center h-9 w-9 rounded-lg bg-indigo-50 shrink-0",
        ),
        rx.el.div(
            rx.el.h3(item[1], class_name=_H3),
            rx.el.p(item[2], class_name=_BODY),
            class_name="min-w-0",
        ),
        class_name=f"flex items-start gap-3 {_CARD} list-none",
    )


def _how_it_works() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.h2("How It Works in Three Steps", class_name=_H2),
            rx.el.p(
                "The shortest path from an Excel file to numbers you can act on.",
                class_name="text-sm font-medium text-gray-500 mt-1 max-w-3xl",
            ),
            class_name="w-full",
        ),
        rx.el.ol(
            *[_step_card(item) for item in _STEPS],
            class_name="grid grid-cols-1 md:grid-cols-3 gap-4 w-full p-0 m-0",
        ),
        id="how-it-works",
        class_name="flex flex-col gap-4 w-full",
    )


def _faq_item(item: tuple[str, str]) -> rx.Component:
    return rx.el.div(
        rx.el.h3(item[0], class_name=_H3),
        rx.el.p(item[1], class_name=_BODY),
        class_name=_CARD,
    )


def _faq() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.h2("Frequently Asked Questions", class_name=_H2),
            rx.el.p(
                "What people usually want to know before analyzing their first Excel file.",
                class_name="text-sm font-medium text-gray-500 mt-1 max-w-3xl",
            ),
            class_name="w-full",
        ),
        rx.el.div(
            *[_faq_item(item) for item in _FAQ],
            class_name="grid grid-cols-1 md:grid-cols-2 gap-4 w-full",
        ),
        class_name="flex flex-col gap-4 w-full",
    )


def _cta() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.h2("Analyze your Excel file now", class_name=_H2),
            rx.el.p(
                "Upload a spreadsheet, confirm your columns and read your dashboard. "
                "You can start on the Free plan.",
                class_name="text-sm font-medium text-gray-500 mt-1 max-w-2xl",
            ),
            class_name="min-w-0 flex-1",
        ),
        rx.el.div(
            rx.el.a(
                rx.icon("cloud-upload", class_name="h-4 w-4"),
                "Upload an Excel file",
                href="/upload",
                class_name="flex items-center gap-2 w-fit rounded-xl bg-indigo-600 px-4 py-2.5 text-sm font-semibold text-white hover:bg-indigo-700 transition-colors",
            ),
            rx.el.a(
                rx.icon("house", class_name="h-4 w-4"),
                "Back to home",
                href="/",
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
                rx.el.a("Home", href="/", class_name=_FOOTER_LINK),
                rx.el.a("About", href="/about", class_name=_FOOTER_LINK),
                rx.el.a("Pricing", href="/pricing", class_name=_FOOTER_LINK),
                rx.el.a(
                    "Privacy Policy", href="/privacy", class_name=_FOOTER_LINK
                ),
                rx.el.a(
                    "Terms of Service", href="/terms", class_name=_FOOTER_LINK
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


def excel_analyzer_page() -> rx.Component:
    return rx.el.div(
        # Hoisted into <head> as a real canonical tag.
        rx.el.link(rel="canonical", href=EXCEL_ANALYZER_CANONICAL),
        _nav(),
        rx.el.main(
            _hero(),
            _section(
                "What an Excel Analytics Tool Does",
                "It takes the spreadsheet you already have and turns it into measured answers instead of cells.",
                _WHAT_IT_DOES,
                "grid grid-cols-1 md:grid-cols-2 gap-4 w-full",
            ),
            _section(
                "How to Analyze an Excel File",
                "A few small things about your file decide how much the analysis can tell you.",
                _HOW_TO_ANALYZE,
                "grid grid-cols-1 md:grid-cols-2 gap-4 w-full",
            ),
            _section(
                "From Upload to Dashboard",
                "The full workflow, in the order you will actually experience it.",
                _WORKFLOW,
                "grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 w-full",
            ),
            _section(
                "Revenue and Sales Analysis",
                "Read the direction of the business, not just the total at the bottom of a column.",
                _REVENUE,
                "grid grid-cols-1 md:grid-cols-2 gap-4 w-full",
            ),
            _section(
                "Customer Analysis",
                "Who buys, how often, and who stopped — from the same file.",
                _CUSTOMERS,
                "grid grid-cols-1 md:grid-cols-2 gap-4 w-full",
            ),
            _section(
                "Product Performance",
                "Compare what you sell by revenue, volume and, when cost is available, margin.",
                _PRODUCTS,
                "grid grid-cols-1 md:grid-cols-2 gap-4 w-full",
            ),
            _section(
                "KPIs and Charts",
                "A compact dashboard layout that recalculates with every filter you apply.",
                _KPIS,
                "grid grid-cols-1 md:grid-cols-2 gap-4 w-full",
            ),
            _section(
                "Business Insights and Recommendations",
                "Analysis is only useful if it ends in something you can do next.",
                _INSIGHTS,
                "grid grid-cols-1 md:grid-cols-2 gap-4 w-full",
            ),
            _section(
                "Who Can Use It",
                "Anyone whose numbers currently live in a spreadsheet.",
                _AUDIENCE,
                "grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 w-full",
            ),
            _how_it_works(),
            _faq(),
            _cta(),
            class_name="flex flex-col gap-10 w-full max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-10",
        ),
        _footer(),
        class_name="font-['Inter'] flex min-h-screen w-full flex-col bg-gray-50",
    )
