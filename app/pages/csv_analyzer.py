"""Public SEO landing page for the CSV analytics tool.

Stateless and dependency-free: it imports no auth, upload, dashboard,
analytics, database or subscription state, so the route renders as static
semantic HTML with no backend work.
"""

import reflex as rx

CSV_ANALYZER_TITLE = (
    "CSV Analytics Tool – Analyze CSV Files Online | InsightSheet"
)
CSV_ANALYZER_DESCRIPTION = (
    "Analyze CSV files online with InsightSheet. Turn CSV data into "
    "dashboards, KPIs, sales insights, customer analysis, charts and "
    "actionable business insights."
)
CSV_ANALYZER_CANONICAL = (
    "https://reflex-build-generation-silver-apple.reflex.run/tools/csv-analyzer"
)

_NAV_LINK = "flex items-center gap-1.5 shrink-0 w-fit rounded-full border border-gray-200 bg-white px-3.5 py-1.5 text-xs font-medium text-gray-600 hover:border-blue-300 hover:text-blue-700 transition-colors"
_FOOTER_LINK = (
    "text-xs font-medium text-gray-500 hover:text-blue-700 transition-colors"
)
_CARD = "rounded-2xl border border-gray-200 bg-white p-5 shadow-sm w-full"
_H2 = "text-2xl font-semibold tracking-tight text-gray-900"
_H3 = "text-sm font-semibold text-gray-900"
_BODY = "text-sm font-medium text-gray-500 mt-1"

_WHAT_IT_IS: list[tuple[str, str, str]] = [
    (
        "file-text",
        "It reads plain text as data",
        "A CSV file is only rows of separated text. A CSV analytics tool parses those rows back into typed columns — dates as dates, amounts as numbers — before anything is measured.",
    ),
    (
        "columns-3",
        "It gives each column a role",
        "Once you say which field holds the date, the amount, the customer and the product, every metric on screen knows exactly what it is counting.",
    ),
    (
        "calculator",
        "It calculates, it does not estimate",
        "Totals, growth, rankings and averages are computed from your own rows, so any figure can be traced back to the lines in your file.",
    ),
    (
        "layout-dashboard",
        "It ends in a dashboard",
        "Instead of scrolling a text file or a wall of cells, you read KPIs, trends and ranked tables you can filter.",
    ),
]

_HOW_TO_ANALYZE: list[tuple[str, str, str]] = [
    (
        "table",
        "Keep one header row",
        "The first row should be column names only — no title banner, no blank spacer row above it. Clear names make column mapping obvious.",
    ),
    (
        "separator-horizontal",
        "Know your delimiter",
        "Commas are the norm, but exports also use semicolons or tabs, especially from European locales. Being aware of which one your file uses avoids a single-column import.",
    ),
    (
        "languages",
        "Watch the encoding",
        "UTF-8 is the safest choice. Files saved in a legacy encoding can show mangled accents or currency symbols, which is worth fixing at export time.",
    ),
    (
        "list",
        "One record per row",
        "Each line should be one transaction or event. Subtotal lines, merged sections and multi-line notes inside a field make rows ambiguous.",
    ),
    (
        "calendar",
        "Include a date field",
        "A single consistent date column is what makes trends, month-over-month change and forecasting possible at all.",
    ),
    (
        "indian-rupee",
        "Include revenue, customer and product fields",
        "An amount column anchors every total; customer and product names unlock rankings, repeat-purchase views and product comparisons. Cost, if present, adds margin.",
    ),
]

_WORKFLOW: list[tuple[str, str, str]] = [
    (
        "cloud-upload",
        "Upload the file",
        "Choose your CSV export. It is read on the server for your session to build your dashboard.",
    ),
    (
        "wand-sparkles",
        "Automatic cleaning",
        "Header detection, date standardisation, duplicate removal and currency stripping run for you and are logged in plain English.",
    ),
    (
        "list-checks",
        "Confirm the mapping",
        "Review the suggested date, revenue, customer, product and order ID columns — you stay in control of what each metric uses.",
    ),
    (
        "gauge",
        "Check data quality",
        "A quality summary shows missing values, unparsed dates and dropped rows before you draw any conclusion.",
    ),
    (
        "layout-dashboard",
        "Read the dashboard",
        "KPIs, revenue trends, customer and product breakdowns, segments and written findings, all filterable.",
    ),
    (
        "file-down",
        "Export the result",
        "Save the view you are looking at as a PDF or Excel report to share with your team.",
    ),
]

_REVENUE: list[tuple[str, str, str]] = [
    (
        "indian-rupee",
        "Total and filtered revenue",
        "See revenue for the whole file, or for any date range, customer or product you filter to.",
    ),
    (
        "chart-line",
        "Revenue trend",
        "Grouped by month, the trend shows whether the direction of travel is up, flat or down.",
    ),
    (
        "percent",
        "Month-over-month change",
        "Change is measured between complete months, so a partial month never looks like a collapse.",
    ),
    (
        "receipt",
        "Orders and average order value",
        "Order counts alongside average order value separate 'more orders' from 'bigger orders'.",
    ),
]

_CUSTOMERS: list[tuple[str, str, str]] = [
    (
        "users",
        "Top customers by revenue",
        "Rank accounts by what they actually spent in the period on screen.",
    ),
    (
        "repeat",
        "Repeat versus one-time buyers",
        "Order frequency per customer shows how much revenue depends on returning buyers.",
    ),
    (
        "clock",
        "Customers who went quiet",
        "Recency surfaces accounts that used to order and stopped — usually the cheapest revenue to recover.",
    ),
    (
        "grid-2x2",
        "RFM segmentation",
        "Recency, frequency and monetary value group customers into segments you can act on.",
    ),
]

_PRODUCTS: list[tuple[str, str, str]] = [
    (
        "package",
        "Best and weakest sellers",
        "Compare products by revenue and by units to see which ones carry the period.",
    ),
    (
        "percent",
        "Margin by product",
        "When your CSV includes cost, revenue rankings and margin rankings can be read side by side.",
    ),
    (
        "chart-column",
        "Product mix over time",
        "Watch how each product's share of revenue moves from month to month.",
    ),
    (
        "search",
        "The long tail",
        "Products with only a handful of orders are easy to miss in a text file and easy to spot in a ranked table.",
    ),
]

_KPIS: list[tuple[str, str, str]] = [
    (
        "gauge",
        "KPI cards",
        "Revenue, orders, average order value, customer count and growth sit at the top and follow your filters.",
    ),
    (
        "chart-line",
        "Trend charts",
        "Time-series views for revenue and orders make seasonality and step changes visible at a glance.",
    ),
    (
        "chart-column",
        "Ranked comparisons",
        "Bar-style breakdowns for customers, products and segments answer 'who' and 'what' quickly.",
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
        "Written observations describe what the rows show — concentration, decline, inactivity, unusual months — with the evidence behind each one.",
    ),
    (
        "list-checks",
        "Recommendations you can act on",
        "Suggestions point at a specific list of customers or products rather than generic advice.",
    ),
    (
        "trending-up",
        "Forecasts, clearly labelled",
        "Projections are fitted to your own complete months and shown with a range, as decision support rather than a promise.",
    ),
    (
        "shield-check",
        "Caveats kept visible",
        "Where a column was partly unparsable or the data is thin, the report says so instead of hiding it.",
    ),
]

_AUDIENCE: list[tuple[str, str, str]] = [
    (
        "shopping-cart",
        "Ecommerce and retail",
        "Most storefronts and payment gateways export CSV — turn that order file into product and repeat-purchase analysis.",
    ),
    (
        "briefcase",
        "Small business owners",
        "Get a monthly read on the business without rebuilding a pivot table each time.",
    ),
    (
        "handshake",
        "Sales teams",
        "Rank accounts, find quiet customers and prepare a pipeline conversation from real history.",
    ),
    (
        "calculator",
        "Finance and operations",
        "Verify data quality, check margins and produce a clean report from a raw system export.",
    ),
    (
        "chart-line",
        "Analysts and consultants",
        "Profile a new client's CSV quickly and discuss findings before building a model.",
    ),
    (
        "graduation-cap",
        "Founders and students",
        "Learn a dataset from first principles, with every figure traceable to a line in the file.",
    ),
]

_STEPS: list[tuple[str, str, str]] = [
    (
        "cloud-upload",
        "Step 1 — Upload your CSV file",
        "Pick a CSV export of your sales or transaction data. Parsing and cleaning run automatically and are logged.",
    ),
    (
        "columns-3",
        "Step 2 — Confirm your columns",
        "Map date, revenue, customer, product and order ID so each metric measures the right field.",
    ),
    (
        "layout-dashboard",
        "Step 3 — Read your dashboard",
        "KPIs, revenue and customer analysis, product performance, charts, insights and exportable reports.",
    ),
]

_FAQ: list[tuple[str, str]] = [
    (
        "What kind of CSV files can I analyze?",
        "Comma-separated exports of sales, order or transaction data up to 10 MB. Real-world files with banner rows above the header, blank lines and duplicated orders are expected and handled during cleaning.",
    ),
    (
        "What if my file uses semicolons or tabs instead of commas?",
        "Delimiter handling is part of parsing, so semicolon and tab separated exports are read too. If a preview ever looks like a single column, re-exporting as comma separated UTF-8 is the quickest fix.",
    ),
    (
        "Which columns does my CSV need?",
        "A date column and an amount column are the minimum for trends and totals. Customer, product and order ID columns unlock customer analysis, product performance and order-level metrics.",
    ),
    (
        "Do I need formulas or any spreadsheet skills?",
        "No. You upload the file, confirm which column is which, and every metric is computed for you — there is nothing to write.",
    ),
    (
        "What happens to my CSV file?",
        "It is processed on this server for your session to build your dashboard. It is not shared with third parties or used to train models.",
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


def _raw_line(text: str, head: bool) -> rx.Component:
    return rx.el.div(
        text,
        class_name=(
            "truncate px-2 py-1.5 text-[11px] font-semibold text-gray-500 bg-gray-50 border-b border-gray-200"
            if head
            else "truncate px-2 py-1.5 text-[11px] font-medium text-gray-700 border-b border-gray-100"
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


def _centerpiece() -> rx.Component:
    return rx.el.figure(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "file-text", class_name="h-3.5 w-3.5 text-gray-400"
                    ),
                    rx.el.span(
                        "orders_export.csv",
                        class_name="text-xs font-medium text-gray-500",
                    ),
                    class_name="flex items-center gap-2 mb-2",
                ),
                _raw_line("date,customer,product,amount", True),
                _raw_line("2024-03-05,Acme Ltd,Starter,14200", False),
                _raw_line("2024-03-18,Nova Co,Pro,26400", False),
                _raw_line("2024-04-02,Vertex,Pro,19850", False),
                _raw_line("2024-04-27,Acme Ltd,Starter,11300", False),
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
                        "CSV dashboard",
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
                    _bar("h-11", "Feb"),
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
            "Illustration only: raw comma-separated lines on the left become mapped columns, KPIs and a revenue trend on the right. All figures shown are illustrative sample values, not results from real data.",
            class_name="text-xs font-medium text-gray-400 mt-3",
        ),
        class_name="w-full m-0",
    )


def _hero() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.span(
                rx.icon("file-text", class_name="h-3.5 w-3.5"),
                "CSV analytics tool",
                class_name="flex items-center gap-1.5 w-fit rounded-full bg-indigo-50 px-3 py-1 text-xs font-semibold text-indigo-700",
            ),
            rx.el.h1(
                "CSV Analytics Tool – Analyze Your CSV Data",
                class_name="text-3xl sm:text-4xl font-semibold tracking-tight text-gray-900 mt-4",
            ),
            rx.el.p(
                "Analyze CSV files online without writing a formula. Upload a comma-separated "
                "export and InsightSheet parses it, cleans it, maps your columns and builds a "
                "dashboard with KPIs, revenue and sales analysis, customer and product "
                "breakdowns, charts and written business insights — all calculated from your own rows.",
                class_name="text-base font-medium text-gray-500 mt-4 max-w-2xl",
            ),
            rx.el.div(
                rx.el.a(
                    rx.icon("cloud-upload", class_name="h-4 w-4"),
                    "Analyze CSV File",
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
                    "New here? Start with the ",
                    class_name="text-xs font-medium text-gray-500",
                ),
                rx.el.a(
                    "InsightSheet spreadsheet analytics overview",
                    href="/",
                    class_name="text-xs font-semibold text-blue-700 hover:underline",
                ),
                rx.el.span(
                    ", or if your data lives in a workbook use the ",
                    class_name="text-xs font-medium text-gray-500",
                ),
                rx.el.a(
                    "Excel analytics tool",
                    href="/tools/excel-analyzer",
                    class_name="text-xs font-semibold text-blue-700 hover:underline",
                ),
                rx.el.span(".", class_name="text-xs font-medium text-gray-500"),
                class_name="mt-4 max-w-2xl",
            ),
            class_name="w-full lg:flex-1 min-w-0",
        ),
        rx.el.div(_centerpiece(), class_name="w-full lg:flex-1 min-w-0"),
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
                "The shortest path from a CSV export to numbers you can act on.",
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
                "What people usually want to know before analyzing their first CSV file.",
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
            rx.el.h2("Analyze your CSV file now", class_name=_H2),
            rx.el.p(
                "Upload a comma-separated export, confirm your columns and read your dashboard. "
                "You can start on the Free plan.",
                class_name="text-sm font-medium text-gray-500 mt-1 max-w-2xl",
            ),
            class_name="min-w-0 flex-1",
        ),
        rx.el.div(
            rx.el.a(
                rx.icon("cloud-upload", class_name="h-4 w-4"),
                "Analyze CSV File",
                href="/upload",
                class_name="flex items-center gap-2 w-fit rounded-xl bg-indigo-600 px-4 py-2.5 text-sm font-semibold text-white hover:bg-indigo-700 transition-colors",
            ),
            rx.el.a(
                rx.icon("sheet", class_name="h-4 w-4"),
                "Excel analytics tool",
                href="/tools/excel-analyzer",
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
                    "Excel analytics tool",
                    href="/tools/excel-analyzer",
                    class_name=_FOOTER_LINK,
                ),
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


def csv_analyzer_page() -> rx.Component:
    return rx.el.div(
        # Hoisted into <head> as a real canonical tag.
        rx.el.link(rel="canonical", href=CSV_ANALYZER_CANONICAL),
        _nav(),
        rx.el.main(
            _hero(),
            _section(
                "What a CSV Analytics Tool Is",
                "A CSV file holds your data but tells you nothing on its own — this turns those lines into measured answers.",
                _WHAT_IT_IS,
                "grid grid-cols-1 md:grid-cols-2 gap-4 w-full",
            ),
            _section(
                "How to Analyze a CSV File",
                "A few practical details about the file decide how much the analysis can tell you.",
                _HOW_TO_ANALYZE,
                "grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 w-full",
            ),
            _section(
                "From Upload to Dashboard",
                "The full workflow, in the order you will actually experience it.",
                _WORKFLOW,
                "grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 w-full",
            ),
            _section(
                "Sales and Revenue Analysis",
                "Read the direction of the business, not just a total at the bottom of a column.",
                _REVENUE,
                "grid grid-cols-1 md:grid-cols-2 gap-4 w-full",
            ),
            _section(
                "Customer Analysis",
                "Who buys, how often, and who stopped — from the same CSV.",
                _CUSTOMERS,
                "grid grid-cols-1 md:grid-cols-2 gap-4 w-full",
            ),
            _section(
                "Product Performance",
                "Compare what you sell by revenue, volume and, when cost is present, margin.",
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
                "Analysis is only useful if it ends in something you can do next — with the evidence attached.",
                _INSIGHTS,
                "grid grid-cols-1 md:grid-cols-2 gap-4 w-full",
            ),
            _section(
                "Who It Is For",
                "Anyone whose numbers arrive as a CSV export.",
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
