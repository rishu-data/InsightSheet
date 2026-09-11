"""Public SEO solution page for small business analytics.

Stateless and dependency-free: it imports no state, auth, upload, dashboard,
analytics, RFM, forecasting, tool or other SEO module, so the route renders as
static semantic HTML with no backend work.
"""

import reflex as rx

SMALL_BUSINESS_ANALYTICS_TITLE = "Small Business Analytics – Analyze Business Data & Make Better Decisions | InsightSheet"
SMALL_BUSINESS_ANALYTICS_DESCRIPTION = (
    "Analyze small business data with InsightSheet. Turn Excel and CSV files "
    "into dashboards, KPIs, sales insights, customer analysis, profitability "
    "insights and forecasts."
)
SMALL_BUSINESS_ANALYTICS_CANONICAL = "https://reflex-build-generation-silver-apple.reflex.run/solutions/small-business-analytics"

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
_GRID_3 = "grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 w-full"
_GRID_2 = "grid grid-cols-1 md:grid-cols-2 gap-4 w-full"

_WHAT_IT_IS: list[tuple[str, str, str]] = [
    (
        "briefcase",
        "It is the ordinary records of a small business, read as data",
        "Small business analytics means treating the sales export, the invoice list or the point-of-sale download as a dataset: one row per transaction, each column with a fixed meaning, and every total derived from those rows rather than typed by hand.",
    ),
    (
        "columns-3",
        "It works with the columns you already keep",
        "A date and an amount are the practical minimum. A customer field, a product field, an order reference and a cost column each open up a further layer of reading, without any new system to adopt.",
    ),
    (
        "calculator",
        "It produces measures, not opinions",
        "Revenue for a period, order count, average order value, repeat customers, product rankings and margin where cost exists are all calculations. The same rows always give the same answer.",
    ),
    (
        "search",
        "It ends in a decision small enough to act on",
        "The useful output is a named month, product, customer or price worth reviewing this week, with the rows behind it still visible.",
    ),
    (
        "ruler",
        "It is scaled to a small team, not a data department",
        "A handful of clearly defined numbers reviewed every month is worth more to a small business than an elaborate model nobody maintains.",
    ),
    (
        "shield-check",
        "It is checkable by design",
        "When each figure names its column, its period and its exclusions, a disagreement about a number becomes a question about the data instead of an argument.",
    ),
]

_WHY_DATA: list[tuple[str, str, str]] = [
    (
        "compass",
        "To know the direction, not just the total",
        "A grand total says where you are. Comparing complete periods on the same definition says whether the business is rising, flat or falling, and by roughly how much.",
    ),
    (
        "users",
        "To see who the revenue actually depends on",
        "Grouping orders by buyer usually shows a small number of accounts carrying a large share of a period — a dependency worth knowing before it changes.",
    ),
    (
        "package",
        "To stop guessing which products earn",
        "Ranking lines by revenue, by units and, where cost exists, by margin separates the busy products from the ones that pay for the month.",
    ),
    (
        "circle-alert",
        "To catch small problems while they are small",
        "A quiet customer, a slipping product, a duplicated import or a price that no longer covers cost is far cheaper to fix in the month it appears.",
    ),
    (
        "clock",
        "To spend less time on the monthly report",
        "Recomputing the same summary from a clean export takes minutes. Rebuilding it by hand each month takes an evening and introduces new mistakes.",
    ),
    (
        "handshake",
        "To make conversations concrete",
        "A conversation with an accountant, a lender or a partner moves faster when the periods and accounts being discussed come from recorded history.",
    ),
]

_CHALLENGES: list[tuple[str, str, str]] = [
    (
        "file-warning",
        "Inconsistent exports",
        "Two exports of the same report can arrive with different column names, extra banner rows, merged cells or a date format that changed halfway down. Anything built on the old shape quietly breaks.",
    ),
    (
        "clock",
        "Limited time",
        "In a small business the person who understands the numbers is usually also selling, invoicing and packing. Analysis that takes a whole evening simply does not happen.",
    ),
    (
        "circle-help",
        "Unclear definitions",
        'If "revenue" sometimes includes tax and shipping and sometimes does not, two honest people produce two different figures for the same month and neither is wrong.',
    ),
    (
        "eraser",
        "Missing and malformed values",
        "Blank amounts, rows with no customer, dates that will not parse and currency symbols inside number columns all change what a total means, and are easy to sum straight past.",
    ),
    (
        "table",
        "Manual reporting",
        "Copying ranges between sheets, re-pointing formulas and rebuilding a pivot table every month is slow, hard to check and impossible to hand over.",
    ),
    (
        "copy",
        "Duplicates and re-imports",
        "A batch imported twice, or an order appearing in two exports, inflates a period without looking obviously wrong. Counting what was removed is part of trusting the result.",
    ),
    (
        "calendar-x",
        "Incomplete periods",
        "Comparing a month still in progress with a finished one always looks like a decline. Fair comparison means finished periods, or the same elapsed days in each.",
    ),
    (
        "users-round",
        "Names that do not match",
        "Trailing spaces, capitalisation and two spellings of one company split a single customer into several and understate every repeat measure.",
    ),
]

_HOW_TO_ANALYZE: list[tuple[str, str, str]] = [
    (
        "file-spreadsheet",
        "Start from one flat export",
        "One sheet, one header row, one row per transaction. Subtotal rows, merged cells and two tables side by side have to go before anything else is worth calculating.",
    ),
    (
        "calendar",
        "Standardise the dates first",
        "Convert every date to one format and count the rows that cannot be parsed. Trends, growth, seasonality and recency all rest on this single column.",
    ),
    (
        "indian-rupee",
        "Agree exactly one revenue field",
        "Pick the amount column you mean, strip currency symbols and separators, and write down whether tax, shipping, discounts and refunds are inside it.",
    ),
    (
        "receipt",
        "Separate orders from amounts",
        "Order count beside average order value explains why revenue moved — more sales, larger sales, or both. The total alone cannot tell you.",
    ),
    (
        "users",
        "Group by customer as well as by date",
        "The same rows read per buyer give first and last order date, order count and spend, which is where repeat business and quiet accounts become visible.",
    ),
    (
        "package",
        "Rank products both ways",
        "By revenue and by units, so a high-volume low-value line is not mistaken for a top earner, and the long tail is actually seen.",
    ),
    (
        "percent",
        "Bring in cost if you have it",
        "Where a cost or purchase-price column exists, gross profit and margin per line can sit beside revenue, so growth is not confused with profitable growth.",
    ),
    (
        "list-checks",
        "Note the limits before the conclusions",
        "Duplicates removed, unparsed dates, blank amounts and rows without a customer belong next to the numbers, not in a footnote nobody reads.",
    ),
]

_SALES_REVENUE: list[tuple[str, str, str]] = [
    (
        "indian-rupee",
        "Revenue for a period you choose",
        "Total revenue across the whole file or a filtered date range, so a month, a season or a quarter can be read on its own terms rather than only as a lifetime total.",
    ),
    (
        "receipt",
        "Orders and average order value",
        "Read together they give the shape of a period: more transactions, bigger baskets, or a mix of the two.",
    ),
    (
        "percent",
        "Change between comparable periods",
        "Period-over-period change calculated from complete periods on one revenue definition, so the comparison is fair rather than flattering.",
    ),
    (
        "chart-line",
        "A monthly trend, not a single number",
        "Cleaned dates grouped into months turn a long list of orders into a shape you can read at a glance — steady, rising, falling or seasonal.",
    ),
    (
        "triangle-alert",
        "Outliers that distort a period",
        "One unusually large order, or a re-imported batch, can dominate a small month. Spotting it keeps the rest of the reading sensible.",
    ),
    (
        "layers",
        "Where the total came from",
        "Splitting revenue by product, customer or channel shows the composition behind a figure, which is what makes it actionable.",
    ),
]

_CUSTOMERS: list[tuple[str, str, str]] = [
    (
        "users",
        "Top customers for the period you are reading",
        "Rank accounts by what they actually spent in the window, not by how often their name appears in the file.",
    ),
    (
        "repeat",
        "Repeat business versus first purchases",
        "Orders per customer separate a month built on returning buyers from one built on new ones. The two call for very different follow-up.",
    ),
    (
        "clock",
        "Accounts that have gone quiet",
        "A buyer whose current gap since ordering is much longer than their own usual gap is worth a call — the comparison is to their history, not to an average.",
    ),
    (
        "grid-2x2",
        "Groups defined by rules you write down",
        "Recency, frequency and spend can be combined into a few groups you can act on. Any label attached to a group is shorthand for its rule, not a verdict on the customer.",
    ),
    (
        "scale",
        "Revenue concentration",
        "Expressing the largest few accounts as a share of the period makes a dependency explicit instead of assumed.",
    ),
    (
        "user-plus",
        "New versus existing revenue",
        "First-order dates split a period into revenue from new buyers and revenue from the established base — a useful check on whether growth is being bought or earned.",
    ),
]

_PRODUCTS: list[tuple[str, str, str]] = [
    (
        "package",
        "Best and weakest sellers",
        "A ranked table by revenue and by units, so volume and value are not confused with each other.",
    ),
    (
        "chart-column",
        "Product mix over time",
        "Each line's share of revenue month by month reveals a shift long before the overall total reflects it.",
    ),
    (
        "search",
        "The long tail you stopped looking at",
        "Lines with very few orders are easy to miss in a spreadsheet and obvious in a ranking — often the shortest list of decisions available.",
    ),
    (
        "arrow-down-up",
        "Movers between two periods",
        "The products that rose or fell most between comparable periods are usually where a review is worth the time.",
    ),
    (
        "users",
        "What different buyers purchase",
        "Crossing products with customer groups shows whether your highest-spending accounts buy the same things as everyone else.",
    ),
    (
        "boxes",
        "Practical follow-through",
        "Product findings usually turn into stock, pricing or promotion decisions, so the ranking is more useful with units and margin beside revenue.",
    ),
]

_PROFITABILITY: list[tuple[str, str, str]] = [
    (
        "percent",
        "Margin needs a cost column",
        "Gross profit is revenue minus cost of the goods sold. Without a cost, purchase-price or unit-cost column, only turnover can be calculated — and saying so is better than estimating.",
    ),
    (
        "calculator",
        "Amount and rate answer different questions",
        "Gross profit in currency shows what a line contributed; margin as a percentage shows how efficiently it did so. A high-margin, low-volume line can matter less than it looks.",
    ),
    (
        "package",
        "Profitability per product",
        "The revenue ranking and the margin ranking are often in a different order, which is exactly the finding worth having.",
    ),
    (
        "users",
        "Profitability per customer",
        "Where cost exists, the largest customer and the most profitable customer can be compared before discounts or terms are agreed.",
    ),
    (
        "tag",
        "Discounts show up in margin first",
        "A steady revenue line with a falling margin usually points at discounting, rising costs or a changed product mix.",
    ),
    (
        "circle-alert",
        "Gross profit is not net profit",
        "Rent, wages, software and tax sit outside a sales export. Margin from these rows describes trading, not the profit of the business as a whole.",
    ),
]

_KPIS: list[tuple[str, str, str]] = [
    (
        "gauge",
        "A KPI needs a definition before it needs a chart",
        '"Revenue", "orders" and "active customers" only mean something once the column, the period and the inclusions are stated. Write the definition once and reuse it.',
    ),
    (
        "layout-dashboard",
        "A dashboard limits what you read",
        "A small set of KPI cards answers the recurring questions first, so detail becomes something you go to deliberately rather than wade through every month.",
    ),
    (
        "target",
        "A short set covers most small businesses",
        "Revenue for the period, order count, average order value, active and repeat customers, top products and change against the previous comparable period.",
    ),
    (
        "chart-line",
        "Charts show shape, tables name specifics",
        "A trend line makes direction and seasonality visible; a ranked table names the customers and products behind it. Both are needed.",
    ),
    (
        "filter",
        "Filters must recalculate everything",
        "When you narrow to a date range or a segment, every KPI and chart should recompute from those rows. A filtered view beside a whole-file total misleads.",
    ),
    (
        "shield-check",
        "Data quality belongs beside the KPIs",
        "Rows excluded, dates that failed to parse and blank amounts change what a figure means, so they should be visible next to it rather than hidden.",
    ),
]

_FORECASTING: list[tuple[str, str, str]] = [
    (
        "chart-spline",
        "A forecast is an uncertain estimate, never a guarantee",
        "Any projection is a calculation from rows already recorded. It describes what past history implies, it can be wrong, and it must never be read as a promise about future sales.",
    ),
    (
        "history",
        "It needs enough recorded history",
        "A few months cannot support a confident projection. Where the history is too short or too irregular, stating that limitation is more useful than producing a number.",
    ),
    (
        "calendar-range",
        "Seasonality changes the reading",
        "An estimate built on a peak season will overstate a quiet one. Comparing the same season in earlier years is the sanity check.",
    ),
    (
        "circle-alert",
        "Assumptions must travel with the estimate",
        "The period used, the revenue definition and the rows excluded all shape the projection, so they belong next to it rather than in a separate note.",
    ),
    (
        "clipboard-list",
        "Use it as a planning range",
        "Estimates are most useful as a range for stock, staffing or cash-flow discussion — not as a target to be defended once it exists.",
    ),
    (
        "refresh-cw",
        "Revisit it every period",
        "Re-running the estimate as new months arrive shows whether the assumption behind it still holds, which is usually the more valuable output.",
    ),
]

_TRENDS_OPPORTUNITIES: list[tuple[str, str, str]] = [
    (
        "trending-up",
        "Trends are recorded, not predicted",
        "Several consecutive periods moving the same way is a trend in your data. It describes what happened; it does not promise the next month.",
    ),
    (
        "lightbulb",
        "Opportunities are places to look",
        "A product growing quietly, a customer group buying more often or a line with unusually strong margin are prompts for a decision, not conclusions in themselves.",
    ),
    (
        "circle-alert",
        "Problems show up as changes in pattern",
        "A regular buyer going silent, a margin drifting down or a month that depends on one order are all visible in rows long before they appear in a bank balance.",
    ),
    (
        "git-compare",
        "Correlation is not causation",
        "If a campaign month also had higher sales, the data cannot show the campaign caused it. Seasonality, price changes, one large order and who you contacted are all mixed together in the same rows.",
    ),
    (
        "flask-conical",
        "Test rather than conclude",
        "A change tried deliberately on a defined group and measured over comparable periods is far more informative than a pattern noticed after the fact.",
    ),
    (
        "history",
        "Record the assumptions with the decision",
        "The window, the definitions and the exclusions used are what let you revisit a decision later and see whether the reasoning still holds.",
    ),
]

_HOW_INSIGHTSHEET: list[tuple[str, str, str]] = [
    (
        "cloud-upload",
        "You upload the business export you already have",
        "An XLSX, XLS or CSV file is enough. Banner rows, blank lines, duplicated orders and currency symbols inside number columns are expected rather than something to tidy up first.",
    ),
    (
        "wand-sparkles",
        "Cleaning is logged, not hidden",
        "Header detection, date standardisation, duplicate removal and currency stripping run automatically, and each change is described in plain English so you can see what was done.",
    ),
    (
        "columns-3",
        "You confirm the column mapping",
        "Suggested roles for date, revenue, customer, product, order ID and cost are shown for you to accept or change, so every figure measures the field you intended.",
    ),
    (
        "gauge",
        "Quality is reported before conclusions",
        "Missing values, unparsed dates and rows dropped during cleaning are summarised first, so you know how much of the file each number rests on.",
    ),
    (
        "calculator",
        "Every figure comes from your own rows",
        "KPIs, revenue trends, customer groupings, product rankings and margin where cost exists are calculated from your cleaned data. Nothing is imported from outside your file and no industry benchmark is assumed.",
    ),
    (
        "lightbulb",
        "Findings stay inside the evidence",
        "Written observations name the months, customers or products involved, projections are labelled as uncertain estimates rather than guarantees, and where the data is too sparse to support a statement that is said instead.",
    ),
]

_AUDIENCE: list[tuple[str, str, str]] = [
    (
        "store",
        "Shops and local retailers",
        "Turn a point-of-sale export into a monthly trend, product rankings and a clear read on which lines carried the period.",
    ),
    (
        "shopping-cart",
        "Ecommerce sellers",
        "Read repeat-purchase behaviour, average order value and product mix from an order export without building a pivot table each month.",
    ),
    (
        "briefcase",
        "Owner-managers and founders",
        "Get a defensible monthly picture in minutes, and take the same definitions into the next conversation with an accountant or lender.",
    ),
    (
        "wrench",
        "Service businesses and trades",
        "Analyse invoices by client, job type and month to see where the work and the margin actually came from.",
    ),
    (
        "handshake",
        "Small sales and account teams",
        "Prepare a week of follow-up from recorded history: top accounts, unusual silences and buyers whose orders are shrinking.",
    ),
    (
        "calculator",
        "Bookkeepers, accountants and consultants",
        "Profile a client's file quickly, agree the revenue definition and the comparison basis, and keep every figure traceable to a row.",
    ),
]

_STEPS: list[tuple[str, str, str]] = [
    (
        "cloud-upload",
        "Step 1 — Upload your Excel or CSV business file",
        "Choose an export containing dated transactions and amounts. Cleaning runs automatically and every change is logged in plain English.",
    ),
    (
        "columns-3",
        "Step 2 — Confirm your business columns",
        "Map date, revenue, customer, product, order ID and cost where you have them, so each KPI, ranking and margin figure reads the field you meant.",
    ),
    (
        "layout-dashboard",
        "Step 3 — Read your dashboard and export it",
        "Review KPIs, revenue trends, customer and product performance, profitability where cost exists and written findings, then export the view as a PDF or Excel report.",
    ),
]

_FAQ: list[tuple[str, str]] = [
    (
        "What is small business analytics?",
        "Small business analytics is the practice of reading the records a small business already keeps — a sales export, an invoice list, a point-of-sale download — as a dataset rather than as paperwork. Each column is given a defined role, the rows are cleaned so periods can be compared, and revenue, order counts, average order value, repeat customers, product rankings and margin where a cost column exists are calculated from those rows. The output is a short set of KPIs, charts and tables that answer specific questions, with every figure traceable back to the data behind it. It describes what has already been recorded rather than predicting what will happen next.",
    ),
    (
        "How can a small business analyze its data?",
        "Begin with one flat export: a single sheet, one header row and one row per transaction, with subtotal rows and merged cells removed. Standardise the date column and count the rows that will not parse, choose exactly one amount column as revenue and write down whether tax, shipping, discounts and refunds are included, then clean the customer field so two spellings of one company do not become two buyers. From there, compare complete periods rather than a finished month against one still in progress. With InsightSheet you upload that file, review the suggested column mapping and adjust it, and the calculations are applied from those cleaned, mapped columns — so you are not writing or maintaining formulas yourself.",
    ),
    (
        "What business data should a small business track?",
        "There is no universal list, and the right one depends on what you sell and how often you sell it. In practice a small number of well-defined fields carries most of the value: a transaction date, an amount, a customer identifier, a product or service name, an order or invoice reference, and a cost figure if you have one. Those six fields support revenue by period, order count, average order value, repeat and active customer counts, product rankings and gross margin. What matters more than the length of the list is consistency: the same columns, the same meaning and the same inclusions every month, so this month's figure can honestly be compared with last month's.",
    ),
    (
        "Can I analyze small business data from Excel or CSV?",
        "Yes. XLSX, XLS and CSV exports are supported, which covers most accounting packages, ecommerce platforms, invoicing tools and point-of-sale systems. A date column and an amount column are the practical minimum; customer, product, order ID and cost columns each add further sections of analysis. Messy files are expected — banner rows, blank lines, duplicated orders and currency symbols inside number columns are handled during cleaning, and the changes made are listed so you can see them. If your export is a plain text file rather than a workbook, the CSV route covers the same ground as the Excel one.",
    ),
    (
        "Can InsightSheet help with small business analytics?",
        "Yes, within clear limits. After you confirm the column mapping, InsightSheet builds a dashboard from your uploaded rows: KPI cards, a monthly revenue trend, customer and product performance, rule-based customer groupings, margin where a cost column exists, data-quality checks, and filters that recalculate every figure from the filtered rows. Written findings name the specific months, customers or products involved, and projections are presented as uncertain estimates rather than guarantees. What it does not do is import outside benchmarks, assume industry averages, or claim that one thing caused another — the rows record what was sold and when, and the causal question stays with you.",
    ),
]

_LEDGER_ROWS: list[list[str]] = [
    [
        "2024-06-03",
        "Sample: Acme Ltd",
        "Sample: Starter kit",
        "2",
        "₹18,000",
        "₹11,700",
    ],
    [
        "2024-06-11",
        "Sample: Nova Co",
        "Sample: Service plan",
        "1",
        "₹24,500",
        "₹14,200",
    ],
    [
        "2024-06-18",
        "Sample: Acme Ltd",
        "Sample: Add-on pack",
        "3",
        "₹9,000",
        "₹6,300",
    ],
    [
        "2024-06-24",
        "Sample: Vertex",
        "Sample: Starter kit",
        "1",
        "₹9,000",
        "₹5,850",
    ],
    [
        "2024-06-29",
        "Sample: Lumen",
        "Sample: Service plan",
        "1",
        "₹24,500",
        "₹15,900",
    ],
]

_SNAPSHOT_TILES: list[tuple[str, str, str]] = [
    ("Sample revenue", "₹85,000", "June sample rows only"),
    ("Sample orders", "5", "Counted from the sample ledger"),
    ("Sample customers", "4", "Distinct sample names"),
    ("Sample avg order", "₹17,000", "Sample revenue ÷ sample orders"),
]

_SNAPSHOT_PRODUCTS: list[tuple[str, str, str]] = [
    ("Sample: Service plan", "₹49,000", "w-full"),
    ("Sample: Starter kit", "₹27,000", "w-3/5"),
    ("Sample: Add-on pack", "₹9,000", "w-1/5"),
]

_SNAPSHOT_MARGIN: list[tuple[str, str, str]] = [
    (
        "Sample gross profit",
        "₹31,050 — sample revenue minus the sample cost column above.",
        "border-green-200 bg-green-50 text-green-800",
    ),
    (
        "Sample margin rate",
        "36.5% — an invented illustrative rate, not a benchmark or a target.",
        "border-green-200 bg-green-50 text-green-800",
    ),
    (
        "Sample data-quality note",
        "0 sample rows dropped, 0 sample dates unparsed — invented for this illustration.",
        "border-amber-200 bg-amber-50 text-amber-800",
    ),
]

_SNAPSHOT_TREND: list[tuple[str, str, str]] = [
    ("Feb", "h-8", "bg-blue-300"),
    ("Mar", "h-10", "bg-blue-400"),
    ("Apr", "h-9", "bg-blue-400"),
    ("May", "h-14", "bg-blue-500"),
    ("Jun", "h-16", "bg-blue-600"),
]

_SNAPSHOT_STATUS: list[tuple[str, str, str]] = [
    (
        "Sample status: repeat sample buyer",
        "Applied here to the one sample name appearing on two sample rows. An invented example of a rule, not a real customer.",
        "border-green-200 bg-green-50 text-green-800",
    ),
    (
        "Sample status: single sample order",
        "Applied here to sample names with one row, kept separate because one purchase supports no conclusion. Invented for illustration.",
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


def _ledger_head() -> rx.Component:
    return rx.el.tr(
        *[
            rx.el.th(
                cell,
                scope="col",
                class_name="truncate px-2 py-1.5 text-left text-[11px] font-semibold text-gray-500",
            )
            for cell in [
                "Date",
                "Customer",
                "Product",
                "Qty",
                "Amount",
                "Cost",
            ]
        ],
        class_name="bg-gray-50 border-b border-gray-200",
    )


def _ledger_row(cells: list[str]) -> rx.Component:
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


def _ledger_panel() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("file-spreadsheet", class_name="h-3.5 w-3.5 text-gray-400"),
            rx.el.span(
                "sample_business_ledger.csv",
                class_name="text-xs font-medium text-gray-500",
            ),
            class_name="flex items-center gap-2",
        ),
        rx.el.p(
            "Illustrative sample ledger — every date, name, product, quantity, amount and cost below is invented for this illustration, not a real transaction or result.",
            class_name="text-[11px] font-medium text-gray-400 mt-1",
        ),
        rx.el.table(
            rx.el.caption(
                "Illustrative sample sales ledger used to show the shape of a small business export. All values are invented.",
                class_name="sr-only",
            ),
            rx.el.thead(_ledger_head()),
            rx.el.tbody(*[_ledger_row(row) for row in _LEDGER_ROWS]),
            class_name="table-auto w-full mt-3",
        ),
        class_name="w-full lg:flex-1 min-w-0 rounded-2xl border border-gray-200 bg-white p-4 shadow-sm",
    )


def _snapshot_tile(item: tuple[str, str, str]) -> rx.Component:
    return rx.el.li(
        rx.el.span(
            item[0], class_name="block text-[10px] font-medium text-gray-500"
        ),
        rx.el.span(
            item[1], class_name="block text-sm font-semibold text-gray-900"
        ),
        rx.el.span(
            item[2], class_name="block text-[10px] font-medium text-gray-400"
        ),
        class_name="min-w-0 list-none rounded-xl border border-gray-200 bg-gray-50 p-2.5",
    )


def _snapshot_product(item: tuple[str, str, str]) -> rx.Component:
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


def _snapshot_note(item: tuple[str, str, str]) -> rx.Component:
    return rx.el.li(
        rx.el.span(item[0], class_name="block text-[11px] font-semibold"),
        rx.el.span(item[1], class_name="block text-[11px] font-medium"),
        class_name=f"list-none rounded-xl border p-2.5 {item[2]}",
    )


def _snapshot_bar(item: tuple[str, str, str]) -> rx.Component:
    return rx.el.li(
        rx.el.div(
            rx.el.div(
                class_name=f"w-full rounded-t-md {item[2]} {item[1]}",
                aria_hidden="true",
            ),
            class_name="flex h-16 w-full items-end",
        ),
        rx.el.span(
            item[0],
            class_name="block text-[10px] font-medium text-gray-400 mt-1 text-center",
        ),
        class_name="flex-1 min-w-0 list-none",
    )


def _outputs_panel() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("layout-dashboard", class_name="h-3.5 w-3.5 text-blue-600"),
            rx.el.span(
                "Sample revenue, order, customer, product, margin and trend outputs",
                class_name="text-xs font-semibold text-gray-900",
            ),
            class_name="flex items-center gap-2",
        ),
        rx.el.p(
            "Illustrative only — every value, name, bar, status and forecast note below is invented for this illustration. None of it is a real result, an industry benchmark or a prediction.",
            class_name="text-[11px] font-medium text-gray-400 mt-1",
        ),
        rx.el.span(
            "Sample KPIs (invented)",
            class_name="block text-[10px] font-semibold text-gray-500 mt-3",
        ),
        rx.el.ul(
            *[_snapshot_tile(item) for item in _SNAPSHOT_TILES],
            class_name="grid grid-cols-2 gap-2 mt-1 p-0 m-0",
        ),
        rx.el.span(
            "Sample product performance (invented)",
            class_name="block text-[10px] font-semibold text-gray-500 mt-4",
        ),
        rx.el.ul(
            *[_snapshot_product(item) for item in _SNAPSHOT_PRODUCTS],
            class_name="flex flex-col gap-2 mt-1 p-0 m-0",
        ),
        rx.el.span(
            "Sample profitability (invented)",
            class_name="block text-[10px] font-semibold text-gray-500 mt-4",
        ),
        rx.el.ul(
            *[_snapshot_note(item) for item in _SNAPSHOT_MARGIN],
            class_name="flex flex-col gap-2 mt-1 p-0 m-0",
        ),
        rx.el.span(
            "Sample monthly trend (invented bar heights, shape only)",
            class_name="block text-[10px] font-semibold text-gray-500 mt-4",
        ),
        rx.el.ul(
            *[_snapshot_bar(item) for item in _SNAPSHOT_TREND],
            class_name="flex items-end gap-2 mt-1 p-0 m-0",
        ),
        rx.el.span(
            "Sample customer status labels (rules, not verdicts)",
            class_name="block text-[10px] font-semibold text-gray-500 mt-4",
        ),
        rx.el.ul(
            *[_snapshot_note(item) for item in _SNAPSHOT_STATUS],
            class_name="flex flex-col gap-2 mt-1 p-0 m-0",
        ),
        rx.el.p(
            "Sample forecast note: an invented illustrative estimate would appear here as a range, clearly labelled uncertain and not a guarantee. No projection is shown or implied by this illustration.",
            class_name="text-[11px] font-medium text-gray-500 mt-4 rounded-xl border border-gray-200 bg-gray-50 p-2.5",
        ),
        class_name="w-full lg:flex-1 min-w-0 rounded-2xl border border-gray-200 bg-white p-4 shadow-sm",
    )


def _snapshot() -> rx.Component:
    return rx.el.figure(
        rx.el.div(
            _ledger_panel(),
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
            _outputs_panel(),
            class_name="flex flex-col lg:flex-row items-stretch gap-4 w-full",
        ),
        rx.el.figcaption(
            "Illustration only: a compact sample sales ledger on the left feeding labelled revenue, order, customer, product, margin and trend outputs on the right, shown to explain how a small business operating snapshot is read. "
            "Every date, name, product, quantity, amount, cost, bar, status label and forecast note above is invented for this illustration — none of it is a real result, an industry benchmark or a prediction. "
            "Your own figures are calculated from the rows you upload and the column mapping you confirm.",
            class_name="text-xs font-medium text-gray-400 mt-3",
        ),
        class_name="w-full m-0",
    )


def _hero() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.span(
                rx.icon("briefcase", class_name="h-3.5 w-3.5"),
                "Small business analytics",
                class_name="flex items-center gap-1.5 w-fit rounded-full bg-indigo-50 px-3 py-1 text-xs font-semibold text-indigo-700",
            ),
            rx.el.h1(
                "Small Business Analytics – Make Better Decisions With Your Data",
                class_name="text-3xl sm:text-4xl font-semibold tracking-tight text-gray-900 mt-4",
            ),
            rx.el.p(
                "Most small businesses already record enough to answer their own questions — the "
                "rows are simply never summarised. Small business analytics gives each column a "
                "defined meaning, cleans the export so periods can be compared, and turns the file "
                "into dashboards, clearly defined KPIs, sales and revenue insights, customer and "
                "product analysis, profitability where cost exists, and uncertain forecast "
                "estimates you can trace back to specific rows.",
                class_name="text-base font-medium text-gray-500 mt-4 max-w-2xl",
            ),
            rx.el.div(
                rx.el.a(
                    "Analyze My Business Data",
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
                rx.el.span(", then read the ", class_name=_INLINE_TEXT),
                rx.el.a(
                    "Excel analytics solution",
                    href="/solutions/excel-analytics",
                    class_name=_INLINE_LINK,
                ),
                rx.el.span(", the ", class_name=_INLINE_TEXT),
                rx.el.a(
                    "sales analytics solution",
                    href="/solutions/sales-analytics",
                    class_name=_INLINE_LINK,
                ),
                rx.el.span(" and the ", class_name=_INLINE_TEXT),
                rx.el.a(
                    "customer analytics solution",
                    href="/solutions/customer-analytics",
                    class_name=_INLINE_LINK,
                ),
                rx.el.span(
                    " — or go straight to the ", class_name=_INLINE_TEXT
                ),
                rx.el.a(
                    "Excel analytics tool",
                    href="/tools/excel-analyzer",
                    class_name=_INLINE_LINK,
                ),
                rx.el.span(
                    ". If your export is a plain text file, the ",
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
        rx.el.div(_snapshot(), class_name="w-full lg:flex-1 min-w-0"),
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


def _profitability_section() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.h2("Profitability Analysis", class_name=_H2),
            rx.el.p(
                "Turnover is not earnings. Where a cost column exists, margin can be read beside revenue — and where it does not, that limit is stated.",
                class_name="text-sm font-medium text-gray-500 mt-1 max-w-3xl",
            ),
            class_name="w-full",
        ),
        rx.el.div(
            *[_card(item) for item in _PROFITABILITY], class_name=_GRID_3
        ),
        rx.el.p(
            rx.el.span(
                "To work margin out line by line from your own sheet, use the ",
                class_name=_INLINE_TEXT,
            ),
            rx.el.a(
                "profit margin calculator",
                href="/tools/profit-margin-calculator",
                class_name=_INLINE_LINK,
            ),
            rx.el.span(".", class_name=_INLINE_TEXT),
        ),
        class_name="flex flex-col gap-4 w-full",
    )


def _forecast_note() -> rx.Component:
    return rx.el.div(
        rx.el.p(
            rx.el.span(
                "Forecasts are uncertain estimates, not guarantees. ",
                class_name="text-sm font-semibold text-amber-800",
            ),
            rx.el.span(
                "Any projection shown is calculated from the history you upload. It describes what "
                "those past rows imply, it can be wrong, and it must never be read as a promise "
                "about future sales, cash or demand. Where the recorded history is too short or too "
                "irregular to support an estimate, that limitation is stated instead of a number.",
                class_name="text-sm font-medium text-amber-800",
            ),
        ),
        class_name="rounded-2xl border border-amber-200 bg-amber-50 p-5 w-full",
    )


def _forecasting_section() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.h2("Sales Forecasting", class_name=_H2),
            rx.el.p(
                "Projecting from recorded history to support a planning conversation — with the uncertainty stated up front.",
                class_name="text-sm font-medium text-gray-500 mt-1 max-w-3xl",
            ),
            class_name="w-full",
        ),
        _forecast_note(),
        rx.el.div(*[_card(item) for item in _FORECASTING], class_name=_GRID_3),
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
                ". To measure the change you have already had rather than an estimate of the next period, use the ",
                class_name=_INLINE_TEXT,
            ),
            rx.el.a(
                "sales growth calculator",
                href="/tools/sales-growth-calculator",
                class_name=_INLINE_LINK,
            ),
            rx.el.span(".", class_name=_INLINE_TEXT),
        ),
        class_name="flex flex-col gap-4 w-full",
    )


def _related() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.h2("Related Analyses From the Same File", class_name=_H2),
            rx.el.p(
                "One uploaded business export can be read from several different angles.",
                class_name="text-sm font-medium text-gray-500 mt-1 max-w-3xl",
            ),
            class_name="w-full",
        ),
        rx.el.div(
            rx.el.p(
                rx.el.span(
                    "For a whole-file view of a workbook, see the ",
                    class_name=_INLINE_TEXT,
                ),
                rx.el.a(
                    "Excel analytics solution",
                    href="/solutions/excel-analytics",
                    class_name=_INLINE_LINK,
                ),
                rx.el.span(
                    " and the ",
                    class_name=_INLINE_TEXT,
                ),
                rx.el.a(
                    "Excel analytics tool",
                    href="/tools/excel-analyzer",
                    class_name=_INLINE_LINK,
                ),
                rx.el.span(
                    ". For plain text exports, the ", class_name=_INLINE_TEXT
                ),
                rx.el.a(
                    "CSV analytics tool",
                    href="/tools/csv-analyzer",
                    class_name=_INLINE_LINK,
                ),
                rx.el.span(
                    " covers the same ground. For revenue, trends and product performance in depth, read the ",
                    class_name=_INLINE_TEXT,
                ),
                rx.el.a(
                    "sales analytics solution",
                    href="/solutions/sales-analytics",
                    class_name=_INLINE_LINK,
                ),
                rx.el.span(
                    "; for buyers, repeat behaviour and segments, the ",
                    class_name=_INLINE_TEXT,
                ),
                rx.el.a(
                    "customer analytics solution",
                    href="/solutions/customer-analytics",
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
                    "; for margin per line, the ", class_name=_INLINE_TEXT
                ),
                rx.el.a(
                    "profit margin calculator",
                    href="/tools/profit-margin-calculator",
                    class_name=_INLINE_LINK,
                ),
                rx.el.span(
                    "; for change between periods, the ",
                    class_name=_INLINE_TEXT,
                ),
                rx.el.a(
                    "sales growth calculator",
                    href="/tools/sales-growth-calculator",
                    class_name=_INLINE_LINK,
                ),
                rx.el.span(
                    "; and for uncertain projections, ", class_name=_INLINE_TEXT
                ),
                rx.el.a(
                    "sales forecasting",
                    href="/tools/sales-forecasting",
                    class_name=_INLINE_LINK,
                ),
                rx.el.span(
                    ". A short introduction to all of it sits on the ",
                    class_name=_INLINE_TEXT,
                ),
                rx.el.a(
                    "InsightSheet home page",
                    href="/",
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
                "The shortest path from an everyday business export to numbers you can act on and share.",
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
                "What small business owners usually want to know before analyzing their own file for the first time.",
                class_name="text-sm font-medium text-gray-500 mt-1 max-w-3xl",
            ),
            class_name="w-full",
        ),
        rx.el.div(
            *[_faq_item(item) for item in _FAQ],
            class_name=_GRID_2,
        ),
        class_name="flex flex-col gap-4 w-full",
    )


def _cta() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.h2("Read your business from your own rows", class_name=_H2),
            rx.el.p(
                "Upload an Excel or CSV export, confirm which columns hold your date, amount, "
                "customer, product and cost, and read KPIs, revenue trends, customer and product "
                "performance and margin built from your own data. You can start on the Free plan.",
                class_name="text-sm font-medium text-gray-500 mt-1 max-w-2xl",
            ),
            class_name="min-w-0 flex-1",
        ),
        rx.el.div(
            rx.el.a(
                "Analyze My Business Data",
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
                    "Sales analytics solution",
                    href="/solutions/sales-analytics",
                    class_name=_FOOTER_LINK,
                ),
                rx.el.a(
                    "Customer analytics solution",
                    href="/solutions/customer-analytics",
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


def small_business_analytics_solution_page() -> rx.Component:
    return rx.el.div(
        # Hoisted into <head> as a real canonical tag.
        rx.el.link(rel="canonical", href=SMALL_BUSINESS_ANALYTICS_CANONICAL),
        _nav(),
        rx.el.main(
            _hero(),
            _section(
                "What Small Business Analytics Means",
                "Reading the records you already keep as a dataset with defined columns, at a scale a small team can actually maintain.",
                _WHAT_IT_IS,
                _GRID_3,
            ),
            _section(
                "Why Small Businesses Should Use Data in Decisions",
                "The reasons are practical: direction, dependency, fair comparison, problems caught early and time saved.",
                _WHY_DATA,
                _GRID_3,
            ),
            _section(
                "Common Challenges With Small Business Data",
                "Almost every difficulty is one of these, and each one is easier to handle once it is named.",
                _CHALLENGES,
                _GRID_2,
            ),
            _section(
                "How to Analyze Your Business Data",
                "A short preparation checklist that decides how much your analysis can honestly tell you.",
                _HOW_TO_ANALYZE,
                _GRID_3,
            ),
            _section(
                "Sales and Revenue Analytics",
                "Read the size, shape and composition of revenue rather than only the total at the bottom of a column.",
                _SALES_REVENUE,
                _GRID_3,
            ),
            _section(
                "Customer Analytics",
                "Who buys, how often, who has stopped, and how much of a period depends on a few accounts.",
                _CUSTOMERS,
                _GRID_3,
            ),
            _section(
                "Product Performance",
                "Compare what you sell by revenue, by volume and — where cost exists — by margin.",
                _PRODUCTS,
                _GRID_3,
            ),
            _profitability_section(),
            _section(
                "Business KPIs and Dashboards",
                "A handful of clearly defined numbers, recomputed the same way each month, is what makes reporting simple.",
                _KPIS,
                _GRID_3,
            ),
            _forecasting_section(),
            _section(
                "Finding Trends, Opportunities and Problems",
                "Analytics can show what your rows recorded and where to look next — it cannot show that one thing caused another.",
                _TRENDS_OPPORTUNITIES,
                _GRID_3,
            ),
            _section(
                "How InsightSheet Analyzes Uploaded Excel and CSV Business Data",
                "Your uploaded rows and your confirmed column mapping drive every figure — nothing is assumed or imported from elsewhere.",
                _HOW_INSIGHTSHEET,
                _GRID_3,
            ),
            _section(
                "Who Benefits From Small Business Analytics",
                "Anyone who records dated transactions and has to explain what they mean to someone else.",
                _AUDIENCE,
                _GRID_3,
            ),
            _how_it_works(),
            _related(),
            _faq(),
            _cta(),
            class_name="flex flex-col gap-10 w-full max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-10",
        ),
        _footer(),
        class_name="font-['Inter'] flex min-h-screen w-full flex-col bg-gray-50",
    )
