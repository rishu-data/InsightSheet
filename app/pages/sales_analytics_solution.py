"""Public SEO solution page for sales analytics.

Stateless and dependency-free: it imports no state, auth, upload, dashboard,
analytics, forecasting or tool module, so the route renders as static semantic
HTML with no backend work.
"""

import reflex as rx

SALES_ANALYTICS_TITLE = (
    "Sales Analytics – Analyze Sales Data & Improve Performance | InsightSheet"
)
SALES_ANALYTICS_DESCRIPTION = (
    "Analyze sales data with InsightSheet. Turn Excel and CSV sales data into "
    "dashboards, KPIs, revenue trends, product performance and actionable "
    "sales insights."
)
SALES_ANALYTICS_CANONICAL = "https://reflex-build-generation-silver-apple.reflex.run/solutions/sales-analytics"

_NAV_LINK = "flex items-center gap-1.5 shrink-0 w-fit rounded-full border border-gray-200 bg-white px-3.5 py-1.5 text-xs font-medium text-gray-600 hover:border-blue-300 hover:text-blue-700 transition-colors"
_FOOTER_LINK = (
    "text-xs font-medium text-gray-500 hover:text-blue-700 transition-colors"
)
_CARD = "rounded-2xl border border-gray-200 bg-white p-5 shadow-sm w-full"
_H2 = "text-2xl font-semibold tracking-tight text-gray-900"
_H3 = "text-sm font-semibold text-gray-900"
_BODY = "text-sm font-medium text-gray-500 mt-1"
_INLINE_LINK = "text-xs font-semibold text-blue-700 hover:underline"
_INLINE_TEXT = "text-xs font-medium text-gray-500"

_WHAT_IT_IS: list[tuple[str, str, str]] = [
    (
        "chart-line",
        "It reads recorded sales as a dataset",
        "Sales analytics means treating your order history as data rather than paperwork: one row per sale, columns with a fixed meaning, and every total derived from those rows.",
    ),
    (
        "columns-3",
        "It depends on a few defined fields",
        "A date and an amount are the practical minimum. Customer, product, order ID and cost columns each unlock a further layer of reading.",
    ),
    (
        "gauge",
        "It produces measures, not opinions",
        "Revenue, order count, average order value, growth between periods and rankings are calculations \u2014 the same rows always give the same answer.",
    ),
    (
        "search",
        "It ends in a decision, not a report",
        "The point of the exercise is to name a month, a product or a customer worth acting on, with the evidence attached.",
    ),
]

_WHY_ANALYZE: list[tuple[str, str, str]] = [
    (
        "compass",
        "To know the direction of the business",
        "A grand total says where you are. Comparing complete periods says whether sales are rising, flat or falling, and by how much.",
    ),
    (
        "users",
        "To see who the revenue depends on",
        "Grouping orders by customer exposes concentration and repeat behaviour that is invisible when rows are sorted by date.",
    ),
    (
        "package",
        "To compare what you sell fairly",
        "Ranking products by revenue and by units separates volume sellers from high-value ones and surfaces a long tail worth reviewing.",
    ),
    (
        "circle-alert",
        "To catch problems early",
        "A quiet account, a slipping product line or a duplicated import is easier to fix in the month it appears than at year end.",
    ),
    (
        "handshake",
        "To make sales conversations concrete",
        "A pipeline review moves faster when the accounts and periods being discussed come from recorded history rather than recollection.",
    ),
    (
        "shield-check",
        "To make numbers defensible",
        "When each figure traces back to specific rows and a stated column mapping, a disagreement about a number becomes a question about the data.",
    ),
]

_HOW_TO_ANALYZE: list[tuple[str, str, str]] = [
    (
        "file-spreadsheet",
        "Start from a flat export",
        "One sheet, one header row, one row per order. Remove merged cells, subtotal rows and side-by-side tables so each column carries a single meaning.",
    ),
    (
        "calendar",
        "Standardise the date column",
        "Convert every date to one format and flag rows that cannot be parsed. Trends, growth and seasonality all rest on this column.",
    ),
    (
        "indian-rupee",
        "Agree one revenue field",
        "Choose the amount you mean by revenue, strip currency symbols and separators, and write down whether tax, shipping and refunds are included.",
    ),
    (
        "receipt",
        "Separate orders from amounts",
        "Order count and average order value tell you whether revenue moved because of more sales or bigger ones \u2014 two very different situations.",
    ),
    (
        "calendar-range",
        "Compare complete periods only",
        "A month still in progress will look like a decline. Compare finished months, or the same number of elapsed days in each.",
    ),
    (
        "list-checks",
        "Check quality before conclusions",
        "Count duplicates removed, unparsed dates and blank amounts first. Knowing what was excluded is part of reading a result honestly.",
    ),
]

_SALES_REVENUE: list[tuple[str, str, str]] = [
    (
        "indian-rupee",
        "Revenue for a period you choose",
        "Total revenue across the whole file or a filtered date range, so a quarter, a season or a single month can be read on its own terms.",
    ),
    (
        "receipt",
        "Orders and average order value",
        "Order count with average order value explains the shape of revenue: more buyers, larger baskets, or both.",
    ),
    (
        "percent",
        "Change between comparable periods",
        "Period-over-period change is calculated from complete periods on the same revenue definition, so the comparison is fair.",
    ),
    (
        "chart-column",
        "Contribution by segment",
        "Splitting revenue by product, customer group or channel shows where a total actually comes from.",
    ),
    (
        "triangle-alert",
        "Outliers that distort a period",
        "A single unusually large order, or a re-imported batch, can dominate a month. Spotting it keeps the rest of the reading sensible.",
    ),
    (
        "scale",
        "Revenue quality, not just size",
        "Where a cost column exists, revenue can be read next to margin so growth is not confused with profitable growth.",
    ),
]

_TRENDS_GROWTH: list[tuple[str, str, str]] = [
    (
        "chart-line",
        "Group rows into months first",
        "A trend needs comparable buckets. Cleaned dates grouped by month turn a list of orders into a shape you can read at a glance.",
    ),
    (
        "trending-up",
        "Look for runs, not single months",
        "One strong month is noise. Several consecutive periods moving the same way is a trend worth investigating.",
    ),
    (
        "calendar-check",
        "Separate season from change",
        "Where you have more than a year of history, comparing the same month last year removes most seasonal distortion.",
    ),
    (
        "arrow-down-up",
        "Find the step, then find the cause",
        "A visible step up or down points at a date, and a date can usually be matched to a price change, a campaign or a lost account.",
    ),
    (
        "percent",
        "Read the rate with the amount",
        "A percentage from a very small base can look dramatic. The currency change beside it keeps the movement in proportion.",
    ),
    (
        "layers",
        "Trend the parts as well as the total",
        "A flat total can hide one product growing while another declines. Per-product and per-customer trends show that immediately.",
    ),
]

_PRODUCTS: list[tuple[str, str, str]] = [
    (
        "package",
        "Best and weakest sellers",
        "Rank products by revenue and by units so a high-volume, low-value item is not mistaken for a top earner.",
    ),
    (
        "percent",
        "Margin where cost is available",
        "If your sheet carries cost, the revenue ranking and the margin ranking can be compared \u2014 they are often not in the same order.",
    ),
    (
        "chart-column",
        "Product mix over time",
        "Watching each product's share of revenue month by month reveals a shift long before the total reflects it.",
    ),
    (
        "search",
        "The long tail",
        "Lines with very few orders are easy to overlook in a spreadsheet and obvious in a ranked table.",
    ),
    (
        "arrow-down-up",
        "Movers between two periods",
        "Comparing periods surfaces the products that rose or fell most, which is usually where a review is worth the time.",
    ),
    (
        "users",
        "Products by customer group",
        "Crossing products with customer segments shows what your most valuable buyers actually purchase.",
    ),
]

_CUSTOMERS: list[tuple[str, str, str]] = [
    (
        "users",
        "Top customers by revenue",
        "Rank accounts by what they spent in the period you are looking at, not by how often their name appears in the file.",
    ),
    (
        "repeat",
        "Repeat versus one-time buyers",
        "Orders per customer show how much of a period depends on returning buyers and how much on first purchases.",
    ),
    (
        "clock",
        "Accounts that have gone quiet",
        "Recency highlights customers who used to order and have stopped \u2014 usually the least expensive revenue to follow up on.",
    ),
    (
        "grid-2x2",
        "Segments you can act on",
        "Recency, frequency and monetary value group buyers into keep, nurture and win-back groups, turning a list into a decision.",
    ),
    (
        "scale",
        "Revenue concentration",
        "Seeing what share of revenue the largest few accounts carry makes a dependency explicit rather than assumed.",
    ),
    (
        "user-plus",
        "New versus existing revenue",
        "First-order dates split a period into revenue from new buyers and revenue from the established base.",
    ),
]

_KPIS: list[tuple[str, str, str]] = [
    (
        "gauge",
        "A KPI needs a definition first",
        "\u201cRevenue\u201d, \u201corders\u201d and \u201cactive customers\u201d only mean something once the column, the period and the inclusions are stated.",
    ),
    (
        "layout-dashboard",
        "A dashboard limits what you read",
        "A small set of KPI cards answers the recurring questions first, so detail becomes something you go to rather than wade through.",
    ),
    (
        "chart-line",
        "Charts show shape, tables name specifics",
        "A trend line makes direction and seasonality visible; a ranked table names the customers and products behind it.",
    ),
    (
        "filter",
        "Filters must recalculate everything",
        "When a filter narrows the rows, every KPI and chart should recompute from those rows \u2014 a segment view beside a whole-file total misleads.",
    ),
    (
        "target",
        "KPIs sales teams actually use",
        "Revenue, order count, average order value, active and repeat customers, top products and period-over-period change cover most weekly reviews.",
    ),
    (
        "shield-check",
        "Data quality belongs on the dashboard",
        "Rows excluded, dates that failed to parse and blank amounts should sit beside the KPIs, not in a note nobody opens.",
    ),
]

_FORECASTING: list[tuple[str, str, str]] = [
    (
        "chart-spline",
        "A forecast is an estimate, not a guarantee",
        "Any projection is a calculation from past rows. It describes what recent history implies, and it can be wrong \u2014 it is never a promise about future sales.",
    ),
    (
        "history",
        "It needs enough recorded history",
        "A handful of months cannot support a confident projection. Where the data is too thin, saying so is more useful than producing a number.",
    ),
    (
        "calendar-range",
        "Seasonality changes the reading",
        "A projection built on a peak season will overstate a quiet one. Comparing the same season in previous years is the sanity check.",
    ),
    (
        "circle-alert",
        "Assumptions must be visible",
        "The period used, the revenue definition and the rows excluded all shape the estimate, so they belong next to it.",
    ),
    (
        "clipboard-list",
        "Use it for planning ranges",
        "Estimates are most useful as a range for stock, staffing or cash-flow discussion \u2014 not as a target to be defended.",
    ),
    (
        "refresh-cw",
        "Revisit it each period",
        "Re-running the estimate as new months arrive shows whether the assumption behind it still holds.",
    ),
]

_HOW_INSIGHTSHEET: list[tuple[str, str, str]] = [
    (
        "cloud-upload",
        "You upload the sales export you already have",
        "An XLSX, XLS or CSV file is enough. Banner rows, blank lines, duplicated orders and currency symbols inside number columns are expected rather than something to fix first.",
    ),
    (
        "wand-sparkles",
        "Cleaning is logged, not hidden",
        "Header detection, date standardisation, duplicate removal and currency stripping run automatically, and each change is described in plain English.",
    ),
    (
        "columns-3",
        "You confirm the column mapping",
        "Suggested roles for date, revenue, customer, product and order ID are shown for you to accept or change, so every metric measures the field you intended.",
    ),
    (
        "gauge",
        "Quality is reported before conclusions",
        "Missing values, unparsed dates and rows dropped during cleaning are summarised first, so you know how much of the file each number rests on.",
    ),
    (
        "calculator",
        "Every figure comes from your rows",
        "KPIs, revenue trends, product rankings and customer segments are calculated from your cleaned data. Nothing is imported from outside your file and no benchmark is assumed.",
    ),
    (
        "lightbulb",
        "Findings point at specific evidence",
        "Written observations name the months, customers or products involved, and forecast figures are labelled as estimates rather than guarantees.",
    ),
]

_AUDIENCE: list[tuple[str, str, str]] = [
    (
        "shopping-cart",
        "Ecommerce and retail",
        "Turn an order export into product performance, repeat-purchase behaviour and a monthly revenue trend.",
    ),
    (
        "briefcase",
        "Small business owners",
        "Get a monthly read on sales without rebuilding pivot tables from scratch each time.",
    ),
    (
        "handshake",
        "Sales teams and managers",
        "Rank accounts, spot customers who have gone quiet and prepare a review from recorded history.",
    ),
    (
        "calculator",
        "Finance and operations",
        "Check margin where cost exists, review data quality and produce a clean report from a messy source file.",
    ),
    (
        "chart-line",
        "Analysts and consultants",
        "Profile a client's sales file quickly and agree the comparison basis before modelling anything.",
    ),
    (
        "graduation-cap",
        "Founders and students",
        "Learn how sales analysis works on real rows, with every figure traceable to the data and the mapping.",
    ),
]

_STEPS: list[tuple[str, str, str]] = [
    (
        "cloud-upload",
        "Step 1 \u2014 Upload your Excel or CSV sales file",
        "Choose an export containing order dates and amounts. Cleaning runs automatically and every change is logged.",
    ),
    (
        "columns-3",
        "Step 2 \u2014 Confirm your sales columns",
        "Map date, revenue, customer, product and order ID so each KPI, trend and ranking measures the field you meant.",
    ),
    (
        "layout-dashboard",
        "Step 3 \u2014 Read your sales dashboard and export it",
        "Review KPIs, revenue trends, product and customer performance and written findings, then export the view as a PDF or Excel report.",
    ),
]

_FAQ: list[tuple[str, str]] = [
    (
        "What is sales analytics?",
        "Sales analytics is the practice of reading recorded sales as a dataset instead of as paperwork: giving each column a defined role, cleaning the rows so periods can be compared, and then calculating revenue, orders, growth, product rankings and customer segments from those rows. The output is a small set of KPIs, charts and tables that answer specific questions, with every number traceable back to the data behind it.",
    ),
    (
        "How can I analyze sales data?",
        "Begin with a flat export \u2014 one header row and one row per order \u2014 then confirm which columns hold the date, the amount, the customer and the product. Standardise the dates, strip currency symbols from amounts, remove duplicated rows and note the blanks. With InsightSheet you upload the file, review the suggested column mapping, and the calculations are applied from those cleaned, mapped columns, so you do not write or maintain formulas yourself.",
    ),
    (
        "What sales KPIs should a business track?",
        "There is no universal list, and the right one depends on what you sell and how often. In practice a short set covers most weekly reviews: total revenue for the period, order count, average order value, active customers, repeat-customer share, top products by revenue, and change against the previous comparable period. What matters more than the list is that each KPI has a stated definition \u2014 which column, which period, and what is included \u2014 so the same figure means the same thing next month.",
    ),
    (
        "Can I analyze sales data from Excel or CSV?",
        "Yes. XLSX, XLS and CSV exports are all supported, which covers most accounting systems, ecommerce platforms and point-of-sale tools. A date column and an amount column are the practical minimum; customer, product, order ID and cost columns each add further sections. If your export is a plain text file, the CSV analytics tool covers the same ground as the Excel one.",
    ),
    (
        "Can InsightSheet create sales dashboards?",
        "Yes. Once you confirm the column mapping, InsightSheet builds a dashboard from your uploaded rows: KPI cards, a monthly revenue trend, product and customer rankings, segment views and data-quality checks, with filters that recalculate every figure from the filtered rows. Written findings name the months, products or customers involved, forecast values are labelled as estimates rather than guarantees, and where the data is too sparse to support a statement it says so instead of inventing one.",
    ),
]

_TREND_BARS: list[tuple[str, str, str]] = [
    ("Jan", "h-8", "bg-blue-300"),
    ("Feb", "h-10", "bg-blue-400"),
    ("Mar", "h-9", "bg-blue-400"),
    ("Apr", "h-14", "bg-blue-500"),
    ("May", "h-16", "bg-blue-600"),
    ("Jun", "h-20", "bg-blue-600"),
]

_KPI_TILES: list[tuple[str, str]] = [
    ("Revenue", "\u20b94,60,000"),
    ("Orders", "128"),
    ("Avg order value", "\u20b93,594"),
    ("Active customers", "41"),
]

_PRODUCT_ROWS: list[tuple[str, str, str]] = [
    ("Starter plan", "\u20b91,80,000", "w-full"),
    ("Pro plan", "\u20b91,45,000", "w-4/5"),
    ("Add-on pack", "\u20b975,000", "w-2/5"),
]

_CUSTOMER_SIGNALS: list[tuple[str, str, str]] = [
    (
        "Repeat share",
        "62% of sample orders came from returning sample customers.",
        "border-green-200 bg-green-50 text-green-800",
    ),
    (
        "Quiet accounts",
        "4 sample customers have not ordered in the last two sample months.",
        "border-amber-200 bg-amber-50 text-amber-800",
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


def _trend_bar(item: tuple[str, str, str]) -> rx.Component:
    return rx.el.li(
        rx.el.div(
            rx.el.div(
                class_name=f"w-full rounded-t-md {item[2]} {item[1]}",
                aria_hidden="true",
            ),
            class_name="flex h-20 w-full items-end",
        ),
        rx.el.span(
            item[0],
            class_name="block text-[10px] font-medium text-gray-400 mt-1 text-center",
        ),
        class_name="flex-1 min-w-0 list-none",
    )


def _trend_panel() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("chart-line", class_name="h-3.5 w-3.5 text-indigo-600"),
            rx.el.span(
                "Sample monthly revenue trend",
                class_name="text-xs font-semibold text-gray-900",
            ),
            class_name="flex items-center gap-2",
        ),
        rx.el.p(
            "Illustrative only \u2014 the bar heights are invented sample values used to show shape. They are not real revenue, a benchmark or a prediction.",
            class_name="text-[11px] font-medium text-gray-400 mt-1",
        ),
        rx.el.ul(
            *[_trend_bar(item) for item in _TREND_BARS],
            class_name="flex items-end gap-2 mt-3 p-0 m-0",
        ),
        rx.el.p(
            "Read as: three steady sample months, then three rising ones \u2014 the shape a sustained increase makes.",
            class_name="text-[11px] font-medium text-gray-500 mt-3",
        ),
        class_name="w-full lg:flex-1 min-w-0 rounded-2xl border border-gray-200 bg-white p-4 shadow-sm",
    )


def _kpi_tile(item: tuple[str, str]) -> rx.Component:
    return rx.el.li(
        rx.el.span(
            item[0], class_name="block text-[10px] font-medium text-gray-500"
        ),
        rx.el.span(
            item[1], class_name="block text-sm font-semibold text-gray-900"
        ),
        class_name="min-w-0 list-none rounded-xl border border-gray-200 bg-gray-50 p-2.5",
    )


def _product_row(item: tuple[str, str, str]) -> rx.Component:
    return rx.el.li(
        rx.el.div(
            rx.el.span(
                item[0],
                class_name="text-[11px] font-medium text-gray-600 truncate",
            ),
            rx.el.span(
                item[1],
                class_name="text-[11px] font-semibold text-gray-900 shrink-0",
            ),
            class_name="flex items-center justify-between gap-2",
        ),
        rx.el.div(
            rx.el.div(
                class_name=f"h-2 rounded-full bg-indigo-500 {item[2]}",
                aria_hidden="true",
            ),
            class_name="w-full h-2 rounded-full bg-gray-100 mt-1",
        ),
        class_name="list-none",
    )


def _customer_signal(item: tuple[str, str, str]) -> rx.Component:
    return rx.el.li(
        rx.el.span(item[0], class_name="block text-[11px] font-semibold"),
        rx.el.span(item[1], class_name="block text-[11px] font-medium"),
        class_name=f"list-none rounded-xl border p-2.5 {item[2]}",
    )


def _signals_panel() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("layout-dashboard", class_name="h-3.5 w-3.5 text-blue-600"),
            rx.el.span(
                "Sample KPI, product and customer signals",
                class_name="text-xs font-semibold text-gray-900",
            ),
            class_name="flex items-center gap-2",
        ),
        rx.el.p(
            "Illustrative only \u2014 every value below is an invented sample, not a real result, benchmark or forecast.",
            class_name="text-[11px] font-medium text-gray-400 mt-1",
        ),
        rx.el.span(
            "Sample KPIs",
            class_name="block text-[10px] font-semibold text-gray-500 mt-3",
        ),
        rx.el.ul(
            *[_kpi_tile(item) for item in _KPI_TILES],
            class_name="grid grid-cols-2 gap-2 mt-1 p-0 m-0",
        ),
        rx.el.span(
            "Sample top products by revenue",
            class_name="block text-[10px] font-semibold text-gray-500 mt-4",
        ),
        rx.el.ul(
            *[_product_row(item) for item in _PRODUCT_ROWS],
            class_name="flex flex-col gap-2 mt-1 p-0 m-0",
        ),
        rx.el.span(
            "Sample customer signals",
            class_name="block text-[10px] font-semibold text-gray-500 mt-4",
        ),
        rx.el.ul(
            *[_customer_signal(item) for item in _CUSTOMER_SIGNALS],
            class_name="flex flex-col gap-2 mt-1 p-0 m-0",
        ),
        class_name="w-full lg:flex-1 min-w-0 rounded-2xl border border-gray-200 bg-white p-4 shadow-sm",
    )


def _workspace() -> rx.Component:
    return rx.el.figure(
        rx.el.div(
            _trend_panel(),
            _signals_panel(),
            class_name="flex flex-col lg:flex-row items-stretch gap-4 w-full",
        ),
        rx.el.figcaption(
            "Illustration only: a compact sample revenue trend beside sample KPI, product and customer signals, shown to explain how a sales view is read. "
            "Every number, bar and share above is invented for this illustration \u2014 none of it is a real result, an industry benchmark or a prediction. "
            "Your own figures are calculated from the rows you upload and the column mapping you confirm.",
            class_name="text-xs font-medium text-gray-400 mt-3",
        ),
        class_name="w-full m-0",
    )


def _hero() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.span(
                rx.icon("chart-line", class_name="h-3.5 w-3.5"),
                "Sales analytics",
                class_name="flex items-center gap-1.5 w-fit rounded-full bg-indigo-50 px-3 py-1 text-xs font-semibold text-indigo-700",
            ),
            rx.el.h1(
                "Sales Analytics \u2013 Turn Your Sales Data Into Actionable Insights",
                class_name="text-3xl sm:text-4xl font-semibold tracking-tight text-gray-900 mt-4",
            ),
            rx.el.p(
                "Most businesses already record enough in a sales export to answer their own "
                "questions \u2014 the rows are simply not summarised. Sales analytics gives each column a "
                "defined meaning, cleans the data so periods can be compared, and turns the file into "
                "dashboards, clearly defined KPIs, revenue trends, product and customer performance "
                "and written findings you can trace back to specific rows.",
                class_name="text-base font-medium text-gray-500 mt-4 max-w-2xl",
            ),
            rx.el.div(
                rx.el.a(
                    "Analyze Sales Data",
                    href="/upload",
                    class_name="w-fit rounded-xl bg-blue-600 px-4 py-2.5 text-sm font-semibold text-white hover:bg-blue-700 transition-colors",
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
                    "New here? Start with the ", class_name=_INLINE_TEXT
                ),
                rx.el.a(
                    "InsightSheet spreadsheet analytics overview",
                    href="/",
                    class_name=_INLINE_LINK,
                ),
                rx.el.span(", read the wider ", class_name=_INLINE_TEXT),
                rx.el.a(
                    "Excel analytics solution",
                    href="/solutions/excel-analytics",
                    class_name=_INLINE_LINK,
                ),
                rx.el.span(", or go straight to the ", class_name=_INLINE_TEXT),
                rx.el.a(
                    "Excel analytics tool",
                    href="/tools/excel-analyzer",
                    class_name=_INLINE_LINK,
                ),
                rx.el.span(
                    " \u2014 if your export is a plain text file, the ",
                    class_name=_INLINE_TEXT,
                ),
                rx.el.a(
                    "CSV analytics tool",
                    href="/tools/csv-analyzer",
                    class_name=_INLINE_LINK,
                ),
                rx.el.span(" covers the same ground.", class_name=_INLINE_TEXT),
                class_name="mt-4 max-w-2xl",
            ),
            class_name="w-full lg:flex-1 min-w-0",
        ),
        rx.el.div(_workspace(), class_name="w-full lg:flex-1 min-w-0"),
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
        rx.el.div(*[_card(item) for item in items], class_name=grid),
        id=section_id,
        class_name="flex flex-col gap-4 w-full",
    )


def _forecast_note() -> rx.Component:
    return rx.el.div(
        rx.el.p(
            rx.el.span(
                "Forecasts are estimates, not guarantees. ",
                class_name="text-sm font-semibold text-amber-800",
            ),
            rx.el.span(
                "Any projection shown is calculated from the sales history you upload. It describes "
                "what those past rows imply, it can be wrong, and it should never be read as a "
                "promise about future sales. Where the recorded history is too short or too "
                "irregular to support an estimate, that limitation is stated instead of a number.",
                class_name="text-sm font-medium text-amber-800",
            ),
        ),
        class_name="rounded-2xl border border-amber-200 bg-amber-50 p-5 w-full",
    )


def _forecasting_section() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.h2("Sales Forecasting and Planning", class_name=_H2),
            rx.el.p(
                "Projecting from recorded history to support a planning conversation \u2014 with the limits of the estimate stated up front.",
                class_name="text-sm font-medium text-gray-500 mt-1 max-w-3xl",
            ),
            class_name="w-full",
        ),
        _forecast_note(),
        rx.el.div(
            *[_card(item) for item in _FORECASTING],
            class_name="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 w-full",
        ),
        rx.el.p(
            rx.el.span(
                "To see how projections are produced from your own rows, see ",
                class_name=_INLINE_TEXT,
            ),
            rx.el.a(
                "sales forecasting",
                href="/tools/sales-forecasting",
                class_name=_INLINE_LINK,
            ),
            rx.el.span(
                ". To measure the change you have already had, use the ",
                class_name=_INLINE_TEXT,
            ),
            rx.el.a(
                "sales growth calculator",
                href="/tools/sales-growth-calculator",
                class_name=_INLINE_LINK,
            ),
            rx.el.span(".", class_name=_INLINE_TEXT),
            class_name="",
        ),
        class_name="flex flex-col gap-4 w-full",
    )


def _related_tools() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.h2("Related Analyses From the Same File", class_name=_H2),
            rx.el.p(
                "Each of these reads the same uploaded sales rows from a different angle.",
                class_name="text-sm font-medium text-gray-500 mt-1 max-w-3xl",
            ),
            class_name="w-full",
        ),
        rx.el.div(
            rx.el.p(
                rx.el.span(
                    "To group buyers by recency, frequency and value, use the ",
                    class_name=_INLINE_TEXT,
                ),
                rx.el.a(
                    "RFM analysis tool",
                    href="/tools/rfm-calculator",
                    class_name=_INLINE_LINK,
                ),
                rx.el.span(
                    ". Where your sheet carries cost as well as revenue, the ",
                    class_name=_INLINE_TEXT,
                ),
                rx.el.a(
                    "profit margin calculator",
                    href="/tools/profit-margin-calculator",
                    class_name=_INLINE_LINK,
                ),
                rx.el.span(
                    " shows margin rather than turnover. For a whole-file view of a spreadsheet, see the ",
                    class_name=_INLINE_TEXT,
                ),
                rx.el.a(
                    "Excel analytics solution",
                    href="/solutions/excel-analytics",
                    class_name=_INLINE_LINK,
                ),
                rx.el.span(" and the ", class_name=_INLINE_TEXT),
                rx.el.a(
                    "CSV analytics tool",
                    href="/tools/csv-analyzer",
                    class_name=_INLINE_LINK,
                ),
                rx.el.span(".", class_name=_INLINE_TEXT),
            ),
            class_name=_CARD,
        ),
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
                "The shortest path from a sales export to numbers you can act on and share.",
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
                "What people usually want to know before analyzing a sales file for the first time.",
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
            rx.el.h2("Turn your sales export into a dashboard", class_name=_H2),
            rx.el.p(
                "Upload an Excel or CSV sales file, confirm which columns hold your date, amount, "
                "customer and product, and read KPIs, revenue trends and rankings built from your "
                "own rows. You can start on the Free plan.",
                class_name="text-sm font-medium text-gray-500 mt-1 max-w-2xl",
            ),
            class_name="min-w-0 flex-1",
        ),
        rx.el.div(
            rx.el.a(
                "Analyze Sales Data",
                href="/upload",
                class_name="w-fit rounded-xl bg-indigo-600 px-4 py-2.5 text-sm font-semibold text-white hover:bg-indigo-700 transition-colors",
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
                    "Excel analytics solution",
                    href="/solutions/excel-analytics",
                    class_name=_FOOTER_LINK,
                ),
                rx.el.a(
                    "Excel analytics tool",
                    href="/tools/excel-analyzer",
                    class_name=_FOOTER_LINK,
                ),
                rx.el.a(
                    "CSV analytics tool",
                    href="/tools/csv-analyzer",
                    class_name=_FOOTER_LINK,
                ),
                rx.el.a(
                    "RFM analysis tool",
                    href="/tools/rfm-calculator",
                    class_name=_FOOTER_LINK,
                ),
                rx.el.a(
                    "Profit margin calculator",
                    href="/tools/profit-margin-calculator",
                    class_name=_FOOTER_LINK,
                ),
                rx.el.a(
                    "Sales growth calculator",
                    href="/tools/sales-growth-calculator",
                    class_name=_FOOTER_LINK,
                ),
                rx.el.a(
                    "Sales forecasting",
                    href="/tools/sales-forecasting",
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


def sales_analytics_solution_page() -> rx.Component:
    return rx.el.div(
        # Hoisted into <head> as a real canonical tag.
        rx.el.link(rel="canonical", href=SALES_ANALYTICS_CANONICAL),
        _nav(),
        rx.el.main(
            _hero(),
            _section(
                "What Sales Analytics Means",
                "Reading recorded orders as a dataset with defined columns, rather than as a file to be summed by hand.",
                _WHAT_IT_IS,
                "grid grid-cols-1 md:grid-cols-2 gap-4 w-full",
            ),
            _section(
                "Why Businesses Analyze Sales Data",
                "The reasons are practical: direction, dependency, comparison and problems caught early.",
                _WHY_ANALYZE,
                "grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 w-full",
            ),
            _section(
                "How to Analyze Sales and Revenue Performance",
                "A short preparation checklist that decides how much your analysis can actually tell you.",
                _HOW_TO_ANALYZE,
                "grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 w-full",
            ),
            _section(
                "Sales and Revenue Analysis",
                "Read the size and composition of revenue, not just the total at the bottom of a column.",
                _SALES_REVENUE,
                "grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 w-full",
            ),
            _section(
                "Sales Trends and Growth Analysis",
                "How to identify a trend, tell it apart from seasonality, and find the date something changed.",
                _TRENDS_GROWTH,
                "grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 w-full",
            ),
            _section(
                "Product Performance Analysis",
                "Compare what you sell by revenue, by volume and \u2014 where cost exists \u2014 by margin.",
                _PRODUCTS,
                "grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 w-full",
            ),
            _section(
                "Customer Sales Analysis",
                "Who buys, how often, who has stopped, and how concentrated the revenue is.",
                _CUSTOMERS,
                "grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 w-full",
            ),
            _section(
                "Sales KPIs and Dashboards",
                "A dashboard is only as good as the definitions behind the numbers on it \u2014 which is what makes it useful to a sales team week after week.",
                _KPIS,
                "grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 w-full",
            ),
            _forecasting_section(),
            _section(
                "How InsightSheet Analyzes Uploaded Excel and CSV Sales Data",
                "Your uploaded rows and your confirmed column mapping drive every figure \u2014 nothing is assumed or imported from elsewhere.",
                _HOW_INSIGHTSHEET,
                "grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 w-full",
            ),
            _section(
                "Who Benefits From Sales Analytics",
                "Anyone who records dated sales and has to explain what they mean to someone else.",
                _AUDIENCE,
                "grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 w-full",
            ),
            _how_it_works(),
            _related_tools(),
            _faq(),
            _cta(),
            class_name="flex flex-col gap-10 w-full max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-10",
        ),
        _footer(),
        class_name="font-['Inter'] flex min-h-screen w-full flex-col bg-gray-50",
    )
