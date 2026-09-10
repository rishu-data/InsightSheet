"""Public SEO solution page for Excel analytics.

Stateless and dependency-free: it imports no state, auth, upload, dashboard,
analytics or tool module, so the route renders as static semantic HTML with no
backend work.
"""

import reflex as rx

EXCEL_ANALYTICS_TITLE = "Excel Analytics – Analyze Excel Data & Build Business Insights | InsightSheet"
EXCEL_ANALYTICS_DESCRIPTION = (
    "Analyze Excel data with InsightSheet. Turn spreadsheets into dashboards, "
    "KPIs, charts, customer insights, sales analysis and actionable business "
    "insights."
)
EXCEL_ANALYTICS_CANONICAL = "https://reflex-build-generation-silver-apple.reflex.run/solutions/excel-analytics"

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
        "sheet",
        "It starts with rows you already keep",
        "Excel analytics is the practice of reading a spreadsheet as a dataset rather than as cells: one row per transaction, columns with a fixed meaning, and every total derived from those rows.",
    ),
    (
        "columns-3",
        "It depends on defined columns",
        "Before anything can be measured, each column needs a role \u2014 which one is the date, which holds the amount, which identifies the customer, the product and the order.",
    ),
    (
        "calculator",
        "It replaces manual arithmetic",
        "Instead of writing formulas by hand for each new export, the same calculations are applied consistently: totals, counts, averages, growth between periods and rankings.",
    ),
    (
        "layout-dashboard",
        "It ends in a readable view",
        "The output of Excel analytics is not another sheet. It is a small set of KPIs, charts and ranked tables that answer questions you can state in a sentence.",
    ),
]

_WHY_ANALYZE: list[tuple[str, str, str]] = [
    (
        "search",
        "Because the file already holds the answers",
        "Most businesses record enough in a spreadsheet to know their best customers, weakest products and monthly direction. The information is present; it is just not summarised.",
    ),
    (
        "chart-line",
        "To see direction, not just totals",
        "A single grand total says very little. Comparing complete periods shows whether revenue is rising, flat or falling, and by how much.",
    ),
    (
        "users",
        "To understand who the revenue depends on",
        "Grouping orders by customer shows concentration and repeat behaviour, which is usually invisible when rows are sorted by date.",
    ),
    (
        "package",
        "To compare what you sell fairly",
        "Ranking products by revenue and by units separates volume sellers from high-value ones, and highlights a long tail worth reviewing.",
    ),
    (
        "clock",
        "To spend less time rebuilding the same sheet",
        "A repeatable process removes the monthly cost of recreating pivot tables and re-checking formula ranges.",
    ),
    (
        "shield-check",
        "To make numbers defensible",
        "When each figure traces back to specific rows and a stated column mapping, a conversation about the number becomes a conversation about the data.",
    ),
]

_CHALLENGES: list[tuple[str, str, str]] = [
    (
        "heading",
        "Inconsistent headers",
        "Export banners, blank rows above the header, renamed columns between months and two header rows stacked together all make it unclear where the data actually begins.",
    ),
    (
        "calendar",
        "Mixed date formats",
        "Some rows read 05/03/2024, others 2024-03-05 or 5 Mar 24, and a few are stored as text. Mixed formats break any grouping by month until they are standardised.",
    ),
    (
        "copy",
        "Duplicate rows",
        "Re-exported orders, appended files and copy-pasted blocks inflate totals quietly, because a duplicate looks exactly like a legitimate sale.",
    ),
    (
        "circle-slash",
        "Missing values",
        "Blank amounts, missing customer names or empty dates mean a row cannot contribute to every metric. What matters is knowing how many rows are affected before drawing a conclusion.",
    ),
    (
        "type",
        "Numbers stored as text",
        'A column containing \u20b91,200, "1200 ", or a leading apostrophe is text to Excel, so it will not sum correctly and may be silently skipped.',
    ),
    (
        "layers",
        "Multiple sheets",
        "Data split across monthly tabs, with slightly different columns on each, has to be reconciled before any comparison across the year is meaningful.",
    ),
    (
        "circle-help",
        "Unclear definitions",
        'If "revenue" sometimes includes tax, shipping or refunds and sometimes does not, two correct calculations will disagree. Definitions have to be stated, not assumed.',
    ),
    (
        "circle-alert",
        "Manual formula errors",
        "A range that stops one row short, a filter left applied, a pasted formula with a shifted reference \u2014 these produce a number that looks plausible and is wrong.",
    ),
]

_HOW_TO_ANALYZE: list[tuple[str, str, str]] = [
    (
        "file-spreadsheet",
        "Flatten the data first",
        "Aim for one sheet, one header row and one row per transaction. Remove merged cells, subtotal rows and side-by-side tables so each column has a single meaning.",
    ),
    (
        "calendar",
        "Fix the date column",
        "Convert every date to one format and drop or flag rows that cannot be parsed. Everything time-based \u2014 trends, growth, seasonality \u2014 rests on this column.",
    ),
    (
        "indian-rupee",
        "Agree one revenue field",
        "Choose the amount you mean by revenue, strip currency symbols and thousands separators, and write down whether tax, shipping and refunds are included.",
    ),
    (
        "user-round",
        "Identify customers consistently",
        "A stable customer identifier, even a cleaned name, lets you count orders per buyer, find repeat purchasers and see how concentrated revenue is.",
    ),
    (
        "package",
        "Name products the same way each time",
        "Consistent product labels are what make ranking, mix and margin comparisons possible across periods.",
    ),
    (
        "list-checks",
        "Check quality before conclusions",
        "Count duplicates removed, unparsed dates and blank amounts first. Knowing what was excluded is part of reading the result honestly.",
    ),
]

_SALES: list[tuple[str, str, str]] = [
    (
        "indian-rupee",
        "Revenue for a period you choose",
        "Total revenue for the whole file or for a filtered date range, so a quarter, a season or a single month can be read on its own terms.",
    ),
    (
        "chart-line",
        "Trend across complete months",
        "Grouping cleaned dates into months shows the shape of sales over time instead of a single flat total.",
    ),
    (
        "percent",
        "Change between periods",
        "Month-over-month and period-over-period change are calculated from complete periods, so a partial current month does not look like a collapse.",
    ),
    (
        "receipt",
        "Orders and average order value",
        "Order count and average order value separate \u201cmore orders\u201d from \u201cbigger orders\u201d when revenue moves, which points to very different actions.",
    ),
    (
        "calendar-check",
        "Seasonal shape",
        "Repeating peaks and quiet stretches become visible once several comparable periods sit side by side.",
    ),
    (
        "circle-alert",
        "Unusual periods",
        "A single very large order or a duplicated import can dominate a month. Spotting it is what keeps the rest of the reading sensible.",
    ),
]

_CUSTOMERS: list[tuple[str, str, str]] = [
    (
        "users",
        "Top customers by revenue",
        "Rank accounts by what they actually spent in the period you are looking at, not by how often their name appears.",
    ),
    (
        "repeat",
        "Repeat versus one-time buyers",
        "Orders per customer show how much of the period depends on returning buyers and how much on first purchases.",
    ),
    (
        "clock",
        "Customers who have gone quiet",
        "Recency highlights accounts that used to order and have stopped, which is usually the least expensive revenue to follow up on.",
    ),
    (
        "grid-2x2",
        "Segments you can act on",
        "Recency, frequency and monetary value group buyers into segments \u2014 keep, nurture, win back \u2014 so a list becomes a decision.",
    ),
    (
        "scale",
        "Revenue concentration",
        "Seeing what share of revenue the largest few accounts represent makes a dependency explicit rather than assumed.",
    ),
    (
        "user-plus",
        "New versus existing",
        "First-order dates split a period into revenue from new buyers and revenue from the existing base.",
    ),
]

_PRODUCTS: list[tuple[str, str, str]] = [
    (
        "package",
        "Best and weakest sellers",
        "Compare products by revenue and by units so a high-volume, low-value item is not confused with a top earner.",
    ),
    (
        "percent",
        "Margin where cost is available",
        "If your sheet carries a cost column, revenue rankings and margin rankings can be compared side by side \u2014 they are often not the same order.",
    ),
    (
        "chart-column",
        "Product mix over time",
        "Watching each product\u2019s share of revenue month by month shows a shift long before the total reflects it.",
    ),
    (
        "search",
        "The long tail",
        "Products with very few orders are easy to overlook in a spreadsheet and obvious in a ranked table.",
    ),
    (
        "users",
        "Products by customer group",
        "Crossing products with customer segments shows what your best buyers actually purchase.",
    ),
    (
        "arrow-down-up",
        "Movers between periods",
        "Comparing two periods surfaces the products that rose or fell most, which is where a review is usually worth the time.",
    ),
]

_KPIS: list[tuple[str, str, str]] = [
    (
        "gauge",
        "A KPI needs a definition",
        "\u201cRevenue\u201d, \u201corders\u201d and \u201cactive customers\u201d only mean something once the column, the period and the inclusions are stated. Definition comes before display.",
    ),
    (
        "layout-dashboard",
        "A dashboard limits what you read",
        "A small set of KPI cards at the top answers the recurring questions first, so detail is something you go to rather than wade through.",
    ),
    (
        "chart-line",
        "Charts show shape, tables show specifics",
        "A trend line makes direction and seasonality visible; a ranked table names the customers and products behind it.",
    ),
    (
        "filter",
        "Filters must recalculate",
        "When a filter is applied, every KPI and chart should be recomputed from the filtered rows \u2014 a segment view next to a whole-file total is misleading.",
    ),
    (
        "eye",
        "Fewer numbers, better read",
        "A dashboard with six well-defined KPIs is more useful than one with thirty, because each one is actually looked at.",
    ),
    (
        "shield-check",
        "Data quality belongs on the dashboard",
        "Rows excluded, dates that failed to parse and blank amounts should sit next to the KPIs, not in a separate note nobody opens.",
    ),
]

_REPORTING: list[tuple[str, str, str]] = [
    (
        "file-text",
        "A report is a fixed view",
        "Exporting what you are reading turns a live dashboard into a dated artefact you can attach to a decision or a meeting.",
    ),
    (
        "repeat",
        "Repeatable each period",
        "Running the same mapping on next month\u2019s export produces a comparable report, which is what makes period-to-period comparison valid.",
    ),
    (
        "list-checks",
        "State the assumptions",
        "A useful report records the column mapping, the date range and what was excluded, so a reader can judge the numbers rather than trust them.",
    ),
    (
        "share-2",
        "Written for someone else",
        "Findings in plain sentences, each pointing at specific customers, products or months, travel better than a screenshot of a sheet.",
    ),
    (
        "download",
        "PDF and Excel outputs",
        "A PDF suits sharing and filing; an Excel export suits a colleague who wants to continue working with the rows.",
    ),
    (
        "clock",
        "Kept as a record",
        "Reports from previous periods are what let you check later whether a decision matched what the data said at the time.",
    ),
]

_HOW_INSIGHTSHEET: list[tuple[str, str, str]] = [
    (
        "cloud-upload",
        "You upload the export you already have",
        "An XLSX, XLS or CSV file is enough. Banner rows, blank lines, duplicated orders and currency symbols inside number columns are expected rather than a problem to fix first.",
    ),
    (
        "wand-sparkles",
        "Cleaning is logged, not hidden",
        "Header detection, date standardisation, duplicate removal and currency stripping run automatically, and each change is described in plain English so you can see what happened to your rows.",
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
        "Every figure is computed from your rows",
        "KPIs, trends, rankings and segments are calculated from your cleaned data after you confirm the mapping. Nothing is imported from outside your file and no benchmark is assumed.",
    ),
    (
        "lightbulb",
        "Findings point at specific evidence",
        "Written observations name the months, customers or products involved, and forecast figures are labelled as estimates. Where the data is too thin to support a statement, that is said instead.",
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
        "Get a monthly read on the business without rebuilding pivot tables from scratch each time.",
    ),
    (
        "handshake",
        "Sales teams",
        "Rank accounts, find customers who have gone quiet and prepare a conversation from recorded history.",
    ),
    (
        "calculator",
        "Finance and operations",
        "Check margins where cost exists, review data quality and produce a clean report from a messy source file.",
    ),
    (
        "chart-line",
        "Consultants and analysts",
        "Profile a new client\u2019s spreadsheet quickly and discuss findings before committing to a model.",
    ),
    (
        "graduation-cap",
        "Founders and students",
        "Learn a dataset from first principles, with every figure traceable back to a row and a mapping.",
    ),
]

_STEPS: list[tuple[str, str, str]] = [
    (
        "cloud-upload",
        "Step 1 \u2014 Upload your Excel file",
        "Choose an XLSX, XLS or CSV export of your sales or transaction data. Cleaning runs automatically and every change is logged.",
    ),
    (
        "columns-3",
        "Step 2 \u2014 Confirm your columns",
        "Map date, revenue, customer, product and order ID so each KPI, chart and ranking measures the field you meant.",
    ),
    (
        "layout-dashboard",
        "Step 3 \u2014 Read your dashboard and export it",
        "Review KPIs, sales and customer analysis, product performance and written findings, then export the view as a PDF or Excel report.",
    ),
]

_FAQ: list[tuple[str, str]] = [
    (
        "What is Excel analytics?",
        "Excel analytics means treating a spreadsheet as a dataset instead of as cells: giving each column a defined role, cleaning the rows so they can be compared, and then calculating totals, trends, rankings and segments from those rows. The result is a small set of KPIs, charts and tables that answer specific questions, with each number traceable back to the data it came from.",
    ),
    (
        "How can I analyze Excel data?",
        "Start with a flat sheet \u2014 one header row and one row per transaction \u2014 then confirm which columns hold the date, the amount, the customer and the product. Cleaning comes next: standardise the date format, strip currency symbols and separators from amounts, remove duplicated rows and note the blanks. With InsightSheet you upload the file, review the suggested column mapping, and the calculations are applied from those mapped, cleaned columns, so you do not write or maintain any formula.",
    ),
    (
        "How do I analyze sales data in Excel?",
        "A date column and an amount column are the practical minimum: together they support revenue totals, monthly trends and change between periods. Optional fields extend the reading \u2014 a customer column adds repeat-purchase, recency and segmentation views, a product column adds performance and mix comparisons, an order ID supports order counts and average order value, and a cost column enables margin views. Anything missing simply limits which sales sections can be filled in.",
    ),
    (
        "Can I create a dashboard from an Excel file?",
        "Yes. Once the columns are mapped, a dashboard can be built from defined KPIs such as revenue, orders, average order value and customer count, alongside trend charts and ranked tables for customers and products. The important part is that each KPI has a stated definition \u2014 which column, which period, what is included \u2014 and that every figure recalculates from the filtered rows when you narrow the view.",
    ),
    (
        "Can InsightSheet analyze Excel files?",
        "Yes \u2014 XLSX, XLS and CSV exports are supported. InsightSheet cleans your uploaded file and logs what it changed, asks you to confirm the column mapping, reports data quality checks before showing conclusions, and then computes KPIs, trends, customer segments and product rankings from your own rows. Written findings name the specific months, customers or products behind them, forecast values are labelled as estimates, and where the data is too sparse to support a statement it says so rather than inventing one.",
    ),
]

_SHEET_ROWS: list[list[str]] = [
    ["2024-03-05", "Acme Ltd", "Starter", "\u20b914,200"],
    ["2024-03-18", "Nova Co", "Pro", "\u20b926,400"],
    ["2024-04-02", "Vertex", "Pro", "\u20b919,850"],
    ["2024-04-27", "Acme Ltd", "Starter", "\u20b911,300"],
]

_KPI_TILES: list[tuple[str, str, str]] = [
    ("Revenue", "\u20b971,750", "text-gray-900"),
    ("Orders", "4", "text-gray-900"),
    ("Customers", "3", "text-gray-900"),
]

_CHART_BARS: list[tuple[str, str]] = [
    ("h-8", "Jan"),
    ("h-12", "Feb"),
    ("h-16", "Mar"),
    ("h-14", "Apr"),
    ("h-20", "May"),
]

_INSIGHT_LINES: list[tuple[str, str]] = [
    (
        "Repeat buyer identified",
        "One sample customer appears in two sample months.",
    ),
    (
        "Product mix",
        "Two sample products carry the sample revenue shown.",
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


def _sheet_head(cells: list[str]) -> rx.Component:
    return rx.el.tr(
        *[
            rx.el.th(
                cell,
                scope="col",
                class_name="truncate px-2 py-1.5 text-left text-[11px] font-semibold text-gray-500",
            )
            for cell in cells
        ],
        class_name="bg-gray-50 border-b border-gray-200",
    )


def _sheet_body_row(cells: list[str]) -> rx.Component:
    return rx.el.tr(
        *[
            rx.el.td(
                cell,
                class_name="truncate px-2 py-1.5 text-[11px] font-medium text-gray-700",
            )
            for cell in cells
        ],
        class_name="border-b border-gray-100",
    )


def _worksheet() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("sheet", class_name="h-3.5 w-3.5 text-gray-400"),
            rx.el.span(
                "sample_sales.xlsx",
                class_name="text-xs font-medium text-gray-500",
            ),
            class_name="flex items-center gap-2",
        ),
        rx.el.p(
            "Illustrative sample worksheet \u2014 these four rows are invented, not real data.",
            class_name="text-[11px] font-medium text-gray-400 mt-1",
        ),
        rx.el.table(
            rx.el.caption(
                "Illustrative sample worksheet rows used to show the shape of an Excel export.",
                class_name="sr-only",
            ),
            rx.el.thead(
                _sheet_head(["Date", "Customer", "Product", "Amount"]),
            ),
            rx.el.tbody(
                *[_sheet_body_row(row) for row in _SHEET_ROWS],
            ),
            class_name="table-auto w-full mt-3",
        ),
        class_name="w-full lg:flex-1 min-w-0 rounded-2xl border border-gray-200 bg-white p-4 shadow-sm",
    )


def _kpi_tile(item: tuple[str, str, str]) -> rx.Component:
    return rx.el.li(
        rx.el.span(
            item[0], class_name="block text-[10px] font-medium text-gray-500"
        ),
        rx.el.span(
            item[1], class_name=f"block text-sm font-semibold {item[2]}"
        ),
        class_name="flex-1 min-w-0 list-none rounded-xl border border-gray-200 bg-gray-50 p-2.5",
    )


def _bar(item: tuple[str, str]) -> rx.Component:
    return rx.el.li(
        rx.el.div(
            rx.el.div(
                class_name=f"w-full rounded-t-md bg-blue-600 {item[0]}",
                aria_hidden="true",
            ),
            class_name="flex h-20 w-full items-end",
        ),
        rx.el.span(
            item[1],
            class_name="block text-[10px] font-medium text-gray-400 mt-1 text-center",
        ),
        class_name="flex-1 min-w-0 list-none",
    )


def _insight_line(item: tuple[str, str]) -> rx.Component:
    return rx.el.li(
        rx.el.span(
            item[0],
            class_name="block text-[11px] font-semibold text-gray-900",
        ),
        rx.el.span(
            item[1],
            class_name="block text-[11px] font-medium text-gray-600",
        ),
        class_name="list-none rounded-xl border border-blue-200 bg-blue-50 p-2.5",
    )


def _outputs() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("layout-dashboard", class_name="h-3.5 w-3.5 text-blue-600"),
            rx.el.span(
                "KPI, chart and insight outputs",
                class_name="text-xs font-semibold text-gray-900",
            ),
            class_name="flex items-center gap-2",
        ),
        rx.el.p(
            "Illustrative only \u2014 every value and bar height below is an invented sample, not a real result.",
            class_name="text-[11px] font-medium text-gray-400 mt-1",
        ),
        rx.el.span(
            "Sample KPIs",
            class_name="block text-[10px] font-semibold text-gray-500 mt-3",
        ),
        rx.el.ul(
            *[_kpi_tile(item) for item in _KPI_TILES],
            class_name="flex items-stretch gap-2 mt-1 p-0 m-0",
        ),
        rx.el.span(
            "Sample revenue chart",
            class_name="block text-[10px] font-semibold text-gray-500 mt-4",
        ),
        rx.el.ul(
            *[_bar(item) for item in _CHART_BARS],
            class_name="flex items-end gap-2 mt-1 p-0 m-0",
        ),
        rx.el.span(
            "Sample written insights",
            class_name="block text-[10px] font-semibold text-gray-500 mt-4",
        ),
        rx.el.ul(
            *[_insight_line(item) for item in _INSIGHT_LINES],
            class_name="flex flex-col gap-2 mt-1 p-0 m-0",
        ),
        class_name="w-full lg:flex-1 min-w-0 rounded-2xl border border-gray-200 bg-white p-4 shadow-sm",
    )


def _workspace() -> rx.Component:
    return rx.el.figure(
        rx.el.div(
            _worksheet(),
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
            _outputs(),
            class_name="flex flex-col lg:flex-row items-stretch gap-4 w-full",
        ),
        rx.el.figcaption(
            "Illustration only: a small sample worksheet on the left feeding labelled KPI, chart and insight outputs on the right. "
            "All values shown are invented samples used to explain the flow \u2014 they are not real results, benchmarks or predictions. "
            "Your own outputs are calculated from the rows you upload and the column mapping you confirm.",
            class_name="text-xs font-medium text-gray-400 mt-3",
        ),
        class_name="w-full m-0",
    )


def _hero() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.span(
                rx.icon("sheet", class_name="h-3.5 w-3.5"),
                "Excel analytics",
                class_name="flex items-center gap-1.5 w-fit rounded-full bg-indigo-50 px-3 py-1 text-xs font-semibold text-indigo-700",
            ),
            rx.el.h1(
                "Excel Analytics \u2013 Turn Your Excel Data Into Business Insights",
                class_name="text-3xl sm:text-4xl font-semibold tracking-tight text-gray-900 mt-4",
            ),
            rx.el.p(
                "Most businesses already record enough in a spreadsheet to answer their own "
                "questions \u2014 the rows are simply not summarised. Excel analytics gives each column "
                "a defined meaning, cleans the data so periods can be compared, and turns the file "
                "into dashboards, clearly defined KPIs, charts and written findings you can trace "
                "back to specific rows.",
                class_name="text-base font-medium text-gray-500 mt-4 max-w-2xl",
            ),
            rx.el.div(
                rx.el.a(
                    "Analyze Excel Data",
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


def _related_tools() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.h2("Related Analyses From the Same File", class_name=_H2),
            rx.el.p(
                "Each of these reads the same uploaded rows from a different angle.",
                class_name="text-sm font-medium text-gray-500 mt-1 max-w-3xl",
            ),
            class_name="w-full",
        ),
        rx.el.div(
            rx.el.p(
                rx.el.span(
                    "To measure the change you have already had, use the ",
                    class_name=_INLINE_TEXT,
                ),
                rx.el.a(
                    "sales growth calculator",
                    href="/tools/sales-growth-calculator",
                    class_name=_INLINE_LINK,
                ),
                rx.el.span(
                    ". To estimate the coming months from your recorded history, see ",
                    class_name=_INLINE_TEXT,
                ),
                rx.el.a(
                    "sales forecasting",
                    href="/tools/sales-forecasting",
                    class_name=_INLINE_LINK,
                ),
                rx.el.span(
                    ". To group buyers by recency, frequency and value, use the ",
                    class_name=_INLINE_TEXT,
                ),
                rx.el.a(
                    "RFM analysis tool",
                    href="/tools/rfm-calculator",
                    class_name=_INLINE_LINK,
                ),
                rx.el.span(
                    ". And where your sheet carries cost as well as revenue, the ",
                    class_name=_INLINE_TEXT,
                ),
                rx.el.a(
                    "profit margin calculator",
                    href="/tools/profit-margin-calculator",
                    class_name=_INLINE_LINK,
                ),
                rx.el.span(
                    " shows margin rather than turnover.",
                    class_name=_INLINE_TEXT,
                ),
                class_name="",
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
                "The shortest path from an Excel export to numbers you can act on and share.",
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
                "What people usually want to know before analyzing an Excel file for the first time.",
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
            rx.el.h2("Turn your spreadsheet into a dashboard", class_name=_H2),
            rx.el.p(
                "Upload an Excel export, confirm which columns hold your date, amount, customer and "
                "product, and read KPIs, charts and findings built from your own rows. You can start "
                "on the Free plan.",
                class_name="text-sm font-medium text-gray-500 mt-1 max-w-2xl",
            ),
            class_name="min-w-0 flex-1",
        ),
        rx.el.div(
            rx.el.a(
                "Analyze Excel Data",
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


def excel_analytics_solution_page() -> rx.Component:
    return rx.el.div(
        # Hoisted into <head> as a real canonical tag.
        rx.el.link(rel="canonical", href=EXCEL_ANALYTICS_CANONICAL),
        _nav(),
        rx.el.main(
            _hero(),
            _section(
                "What Excel Analytics Means",
                "Reading a spreadsheet as a dataset with defined columns, rather than as cells to be summed by hand.",
                _WHAT_IT_IS,
                "grid grid-cols-1 md:grid-cols-2 gap-4 w-full",
            ),
            _section(
                "Why Businesses Analyze Spreadsheet Data",
                "The reasons are practical: direction, dependency, comparison and time saved.",
                _WHY_ANALYZE,
                "grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 w-full",
            ),
            _section(
                "Common Excel Data Challenges",
                "Almost every real export has some of these. Naming them is the first step to a number you can defend.",
                _CHALLENGES,
                "grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4 w-full",
            ),
            _section(
                "How to Analyze Sales, Revenue, Customers and Products",
                "A short preparation checklist that decides how much your analysis can actually tell you.",
                _HOW_TO_ANALYZE,
                "grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 w-full",
            ),
            _section(
                "Excel Sales Analysis",
                "Read the direction of the business, not just the total at the bottom of a column.",
                _SALES,
                "grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 w-full",
            ),
            _section(
                "Excel Customer Analysis",
                "Who buys, how often, who stopped and how concentrated the revenue is.",
                _CUSTOMERS,
                "grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 w-full",
            ),
            _section(
                "Excel Product Performance Analysis",
                "Compare what you sell by revenue, volume and \u2014 where cost exists \u2014 margin.",
                _PRODUCTS,
                "grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 w-full",
            ),
            _section(
                "Excel KPI and Dashboard Analysis",
                "A dashboard is only as good as the definitions behind the numbers on it.",
                _KPIS,
                "grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 w-full",
            ),
            _section(
                "Excel Business Reporting",
                "Turning a view into a dated, repeatable record someone else can read.",
                _REPORTING,
                "grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 w-full",
            ),
            _section(
                "How InsightSheet Turns Excel Data Into Traceable Insights",
                "Your uploaded rows and your confirmed column mapping drive every figure \u2014 nothing is assumed or imported from elsewhere.",
                _HOW_INSIGHTSHEET,
                "grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 w-full",
            ),
            _section(
                "Who Benefits From Excel Analytics",
                "Anyone whose numbers currently live in a spreadsheet and have to be explained to someone.",
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
