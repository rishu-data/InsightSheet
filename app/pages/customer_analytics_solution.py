"""Public SEO solution page for customer analytics.

Stateless and dependency-free: it imports no state, auth, upload, dashboard,
analytics, RFM, forecasting or tool module, so the route renders as static
semantic HTML with no backend work.
"""

import reflex as rx

CUSTOMER_ANALYTICS_TITLE = "Customer Analytics – Understand Customer Behavior & Segments | InsightSheet"
CUSTOMER_ANALYTICS_DESCRIPTION = (
    "Analyze customer data with InsightSheet. Understand customer behavior, "
    "RFM segments, customer value, retention patterns and actionable customer "
    "insights from Excel and CSV data."
)
CUSTOMER_ANALYTICS_CANONICAL = "https://reflex-build-generation-silver-apple.reflex.run/solutions/customer-analytics"

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
        "users",
        "It reads transactions as customer histories",
        "Customer analytics regroups the same order rows you already keep by buyer instead of by date, so each customer becomes a small history rather than a scattering of lines.",
    ),
    (
        "columns-3",
        "It needs a stable customer identifier",
        "An email, an account code or a consistently spelled name is what links orders together. Without one, every purchase looks like a first purchase.",
    ),
    (
        "calculator",
        "It produces measures, not labels handed down from outside",
        "First and last order date, order count, total and average spend are calculations from your rows. Any segment name attached to them is a convention you choose, not a fact about the customer.",
    ),
    (
        "search",
        "It ends in a shortlist, not a report",
        "The useful output is a named set of accounts worth contacting, keeping or reviewing, with the rows behind each one still visible.",
    ),
]

_WHY_ANALYZE: list[tuple[str, str, str]] = [
    (
        "scale",
        "To see how concentrated revenue is",
        "Grouping orders by buyer shows what share of a period a handful of accounts carried \u2014 a dependency that is invisible in a date-sorted file.",
    ),
    (
        "repeat",
        "To tell repeat business from one-off business",
        "Orders per customer separate a period built on returning buyers from one built on first purchases. The two need very different follow-up.",
    ),
    (
        "clock",
        "To notice customers who stopped",
        "A buyer who ordered every month and has not ordered since spring rarely announces it. Recency makes the gap visible.",
    ),
    (
        "target",
        "To decide where limited attention goes",
        "Most teams can only contact a few accounts a week. A ranked, defined list is a better basis for that choice than recollection.",
    ),
    (
        "package",
        "To see what different buyers actually purchase",
        "Crossing customers with products shows whether your highest-spending accounts buy the same things as everyone else.",
    ),
    (
        "shield-check",
        "To make customer claims checkable",
        'When "our best customers" has a stated definition \u2014 which column, which period, which measure \u2014 a disagreement becomes a question about the data.',
    ),
]

_HOW_TO_UNDERSTAND: list[tuple[str, str, str]] = [
    (
        "file-spreadsheet",
        "Start from a flat transaction export",
        "One sheet, one header row, one row per order, with a customer field on every row. Subtotal rows and side-by-side tables have to go first.",
    ),
    (
        "user-round",
        "Clean the customer field before counting",
        "Trailing spaces, case differences and two spellings of the same company split one buyer into several and understate every repeat measure.",
    ),
    (
        "calendar",
        "Standardise dates, then set a reference date",
        "Recency is measured against a date you choose \u2014 usually the last date in the file. Saying which date you used is part of the result.",
    ),
    (
        "indian-rupee",
        "Agree what spend means",
        "Pick the amount column and write down whether tax, shipping, discounts and refunds are included. Customer value shifts noticeably with that choice.",
    ),
    (
        "calendar-range",
        "Fix the window you are looking at",
        "A twelve-month window and an all-time window produce different top customers. Neither is wrong; mixing them in one conversation is.",
    ),
    (
        "list-checks",
        "Note what the data cannot tell you",
        "Rows without a customer, blank amounts and unparsed dates limit the reading. Counting them first keeps the conclusions honest.",
    ),
]

_SEGMENTATION: list[tuple[str, str, str]] = [
    (
        "grid-2x2",
        "A segment is a rule, written down",
        "Segmentation splits buyers by a stated condition \u2014 spend above a threshold, more than one order, no order in six months. The rule is what makes it repeatable.",
    ),
    (
        "tag",
        "Labels are shorthand, not verdicts",
        'Names such as "loyal" or "at risk" are convenient descriptions of a rule. They are conventions used here for readability, not universal categories, and a customer can move between them next month.',
    ),
    (
        "sliders-horizontal",
        "Thresholds belong to your business",
        "A quarterly buyer of machinery and a weekly buyer of consumables cannot share a recency cut-off. Borrowed thresholds produce confident nonsense.",
    ),
    (
        "layers",
        "Keep the number of groups small",
        "Four or five groups you can act on beat twenty you never look at. Segmentation is for deciding, not for taxonomy.",
    ),
    (
        "refresh-cw",
        "Re-run it each period",
        "Segments describe a moment. Re-running the same rules on next month's export shows movement, which is usually more informative than the snapshot.",
    ),
    (
        "circle-alert",
        "Check group sizes before believing them",
        "A segment containing two customers may be interesting, but nothing general should be concluded from it.",
    ),
]

_RFM: list[tuple[str, str, str]] = [
    (
        "clock",
        "R is recency",
        "How long ago the customer last ordered, measured against a stated reference date. Lower is more recent.",
    ),
    (
        "repeat",
        "F is frequency",
        "How many orders that customer placed inside the window you chose \u2014 a count of transactions, not of items.",
    ),
    (
        "indian-rupee",
        "M is monetary value",
        "How much the customer spent in that window, on the amount definition you agreed. Sometimes read as an average per order alongside the total.",
    ),
    (
        "hash",
        "Scores are relative rankings",
        "The usual method ranks customers on each of the three measures and buckets them, often 1\u20135. A score describes a position within your own file, not a rating on any external scale.",
    ),
    (
        "grid-2x2",
        "Combinations suggest where to look",
        "Recent, frequent, high-spend buyers and once-frequent buyers who have gone quiet stand out from the combination rather than from any single measure.",
    ),
    (
        "circle-help",
        "RFM describes, it does not explain",
        "The three measures record what happened. They say nothing about why a customer stopped \u2014 price, a contact leaving, a competitor or simple seasonality are all invisible in the rows.",
    ),
]

_VALUE: list[tuple[str, str, str]] = [
    (
        "indian-rupee",
        "Total spend in a defined window",
        "The simplest value measure, and the one most often quoted without its window attached. Always state the period.",
    ),
    (
        "receipt",
        "Average order value per customer",
        "Separates a buyer placing many small orders from one placing few large ones \u2014 two different accounts to service.",
    ),
    (
        "calendar-range",
        "Order frequency and gap between orders",
        "The typical interval between a customer's orders is what makes a current silence readable as unusual or normal.",
    ),
    (
        "percent",
        "Margin contribution where cost exists",
        "If your sheet carries cost, the highest-revenue customer and the highest-margin customer can be compared. They are often not the same account.",
    ),
    (
        "chart-column",
        "Share of period revenue",
        "Expressing a customer's spend as a share of the period turns a number into a dependency you can see.",
    ),
    (
        "triangle-alert",
        "Value measures are historical",
        "Every figure describes purchases already made. Projecting them forward is an estimate, and should be labelled as one rather than treated as a customer's worth.",
    ),
]

_BEHAVIOUR: list[tuple[str, str, str]] = [
    (
        "calendar-check",
        "When customers buy",
        "Order dates per buyer expose regular monthly rhythms, seasonal buyers and accounts that only appear during promotions.",
    ),
    (
        "package",
        "What they buy",
        "Product mix per customer shows whether a segment is built on one line or spread across the catalogue.",
    ),
    (
        "trending-up",
        "Whether their basket is changing",
        "Comparing a customer's earlier orders with their recent ones shows spend or order size drifting long before the total does.",
    ),
    (
        "user-plus",
        "First purchase and what followed",
        "The first order date splits a period into new and existing revenue, and shows how often a first order was followed by a second.",
    ),
    (
        "arrow-down-up",
        "Movement between periods",
        "The customers who rose or fell most between two comparable periods are usually the shortest useful list on the page.",
    ),
    (
        "circle-alert",
        "Patterns are observations, not motives",
        "A behaviour visible in the rows is worth asking about. The reason for it comes from the customer, not from the spreadsheet.",
    ),
]

_AT_RISK_LOYAL: list[tuple[str, str, str]] = [
    (
        "heart",
        "Loyal is a description of recorded behaviour",
        "Frequent, recent, sustained ordering over several periods is what the rows can show. It is a pattern, not a statement about how a customer feels.",
    ),
    (
        "triangle-alert",
        "At risk means an unusual silence",
        "A customer whose current gap since ordering is much longer than their own historical gap is worth a look \u2014 the comparison is to their own pattern, not to an average.",
    ),
    (
        "star",
        "High value and high frequency can diverge",
        "A rare but very large buyer and a small weekly buyer are both valuable in different ways, and confusing them leads to the wrong follow-up.",
    ),
    (
        "user-minus",
        "One-time buyers deserve their own group",
        "A single order says almost nothing yet. Treating first-time buyers as churned overstates a problem you may not have.",
    ),
    (
        "phone",
        "The output is a conversation, not a verdict",
        "A flagged account is a prompt to check the relationship. The data cannot tell you whether the customer left, paused or simply bought elsewhere once.",
    ),
    (
        "list-checks",
        "Keep the flags reviewable",
        "Every flagged customer should come with the rows and thresholds that produced the flag, so a colleague can disagree with the rule rather than the name.",
    ),
]

_KPIS: list[tuple[str, str, str]] = [
    (
        "gauge",
        "A customer KPI needs a definition first",
        '"Active customers", "repeat rate" and "average customer value" only mean something once the window, the amount column and the identifier are stated.',
    ),
    (
        "users",
        "Active and repeat customer counts",
        "How many distinct buyers ordered in the period, and how many of those had ordered before, is the shortest useful pair of customer numbers.",
    ),
    (
        "percent",
        "Repeat share of revenue",
        "The proportion of a period's revenue coming from returning buyers separates a base you can build on from a period of one-off sales.",
    ),
    (
        "receipt",
        "Average orders and spend per customer",
        "Read together, they explain a change in customer revenue: more buyers, more orders each, or larger orders.",
    ),
    (
        "filter",
        "Filters must recalculate every figure",
        "When you narrow to a segment or a date range, KPIs and tables should recompute from those rows \u2014 a segment view beside a whole-file total misleads.",
    ),
    (
        "shield-check",
        "Data quality belongs beside the KPIs",
        "Rows without a customer, duplicate orders removed and unparsed dates change what a customer count means, so they should be visible next to it.",
    ),
]

_RETENTION: list[tuple[str, str, str]] = [
    (
        "repeat",
        "Retention is measured, not assumed",
        "Whether buyers from an earlier period ordered again in a later one is a count you can make from your rows, period by period.",
    ),
    (
        "clipboard-list",
        "Analysis supports a decision, it does not make one",
        "A list of quiet accounts tells you where to look. Whether to call, discount or do nothing remains a judgement about the relationship.",
    ),
    (
        "circle-alert",
        "Correlation is not causation",
        "If contacted customers later ordered more, the data cannot show that the contact caused it. Timing, seasonality and who you chose to contact are all mixed in.",
    ),
    (
        "flask-conical",
        "Test rather than conclude",
        "A change tried on a defined group and measured over comparable periods is far more informative than a pattern noticed after the fact.",
    ),
    (
        "history",
        "Record the assumptions with the decision",
        "The window, the thresholds and the exclusions used are what let you revisit a decision later and see whether the reasoning still holds.",
    ),
    (
        "eye",
        "Watch the same measures over time",
        "Retention is only readable as a series. One period's number, without the ones before it, has no direction.",
    ),
]

_HOW_INSIGHTSHEET: list[tuple[str, str, str]] = [
    (
        "cloud-upload",
        "You upload the customer transaction export you already have",
        "An XLSX, XLS or CSV file with dated orders is enough. Banner rows, blank lines, duplicated orders and currency symbols inside number columns are expected rather than something to fix first.",
    ),
    (
        "wand-sparkles",
        "Cleaning is logged, not hidden",
        "Header detection, date standardisation, duplicate removal and currency stripping run automatically, and each change is described in plain English.",
    ),
    (
        "columns-3",
        "You confirm the column mapping",
        "Suggested roles for date, amount, customer, product and order ID are shown for you to accept or change, so every customer measure reads the field you intended.",
    ),
    (
        "gauge",
        "Quality is reported before conclusions",
        "Rows missing a customer, blank amounts and dates that could not be parsed are summarised first, so you know how much of the file each figure rests on.",
    ),
    (
        "calculator",
        "Every customer figure comes from your rows",
        "Recency, frequency, monetary value, segment groupings and rankings are calculated from your cleaned data. Nothing is imported from outside your file and no industry benchmark is assumed.",
    ),
    (
        "lightbulb",
        "Findings name the evidence and stay within it",
        "Written observations point at the specific customers, months or products involved, segment labels are presented as the rules that produced them, and where the data is too thin to support a statement that is said instead.",
    ),
]

_AUDIENCE: list[tuple[str, str, str]] = [
    (
        "shopping-cart",
        "Ecommerce and retail",
        "Turn an order export into repeat-purchase behaviour, buyer segments and a list of accounts that have gone quiet.",
    ),
    (
        "briefcase",
        "Small business owners",
        "See which customers the month actually depended on, without rebuilding a pivot table each time.",
    ),
    (
        "handshake",
        "Sales and account teams",
        "Prepare a week of calls from recorded history: top accounts, unusual silences and buyers whose orders are shrinking.",
    ),
    (
        "megaphone",
        "Marketing and retention",
        "Define groups by rule rather than by feel, and measure the next period on the same definitions.",
    ),
    (
        "calculator",
        "Finance and operations",
        "Check revenue concentration, and margin per customer where a cost column exists, before committing to terms.",
    ),
    (
        "graduation-cap",
        "Analysts, consultants and students",
        "Profile a customer file quickly, agree the window and thresholds, and keep every figure traceable to a row.",
    ),
]

_STEPS: list[tuple[str, str, str]] = [
    (
        "cloud-upload",
        "Step 1 \u2014 Upload your Excel or CSV customer transaction file",
        "Choose an export with order dates, amounts and a customer field. Cleaning runs automatically and every change is logged.",
    ),
    (
        "columns-3",
        "Step 2 \u2014 Confirm your customer columns",
        "Map customer, date and amount \u2014 plus product and order ID if you have them \u2014 so each recency, frequency and value figure reads the field you meant.",
    ),
    (
        "users",
        "Step 3 \u2014 Read your customer view and export it",
        "Review customer KPIs, RFM groupings, value rankings, purchase behaviour and flagged accounts, then export the view as a PDF or Excel report.",
    ),
]

_FAQ: list[tuple[str, str]] = [
    (
        "What is customer analytics?",
        "Customer analytics is the practice of regrouping recorded transactions by buyer instead of by date, so that each customer becomes a short history: when they first and last ordered, how often, how much they spent and what they bought. From those measures you can rank customers, group them by rules you define, and see who has been ordering recently and who has not. Every figure is a calculation from your own rows, and it describes purchases already made rather than predicting what a customer will do next.",
    ),
    (
        "How can I analyze customer data?",
        "Start with a flat transaction export \u2014 one header row, one row per order \u2014 that carries a customer field on every row. Clean that field first, because trailing spaces and two spellings of one company split a single buyer into several. Standardise the dates, decide which amount column you mean by spend and whether tax, shipping and refunds are included, then fix the window you are looking at and the reference date recency is measured against. With InsightSheet you upload the file, review the suggested column mapping, and the customer measures are calculated from those cleaned, mapped columns, so you do not write or maintain formulas yourself.",
    ),
    (
        "What is RFM customer segmentation?",
        "RFM stands for recency, frequency and monetary value: how long ago a customer last ordered, how many orders they placed in the window you chose, and how much they spent in it. Customers are usually ranked on each of the three measures and placed into buckets \u2014 often 1 to 5 \u2014 and the combination of the three scores is then used to group them. It is important to read those scores as positions within your own file rather than ratings on any external scale, and to treat any segment name attached to a combination as a convenient label for the rule behind it, not as a fixed category the customer belongs to.",
    ),
    (
        "How can customer analytics help a business?",
        "Mainly by narrowing attention. It shows how much of a period's revenue a few accounts carried, which buyers return and which ordered once, and whose current silence is unusual compared with their own past pattern \u2014 which is a practical basis for deciding who to contact this week and what to review. What it cannot do is explain why any of that happened, or show that an action caused a later change: the rows record what was bought and when, and timing, seasonality and who you chose to contact are all mixed together in them. Used well, the analysis supports a decision and leaves the causal question to be tested deliberately.",
    ),
    (
        "Can InsightSheet analyze customer data from Excel or CSV?",
        "Yes. XLSX, XLS and CSV exports are supported, which covers most accounting systems, ecommerce platforms and point-of-sale tools. A date column, an amount column and a customer field are the practical minimum; product, order ID and cost columns each add further sections. After you confirm the column mapping, InsightSheet computes recency, frequency, monetary value, customer rankings and rule-based groupings from your cleaned rows, reports data-quality issues such as rows without a customer before showing conclusions, and states when the data is too sparse to support a finding instead of inventing one.",
    ),
]

_SAMPLE_CUSTOMERS: list[list[str]] = [
    ["Sample: Acme Ltd", "2024-06-14", "9", "\u20b91,42,000"],
    ["Sample: Nova Co", "2024-06-02", "4", "\u20b968,500"],
    ["Sample: Vertex", "2024-02-19", "6", "\u20b997,300"],
    ["Sample: Lumen", "2024-05-28", "1", "\u20b912,400"],
]

_RFM_OUTPUTS: list[tuple[str, str, str]] = [
    (
        "Sample: Acme Ltd",
        "R 5 \u00b7 F 5 \u00b7 M 5",
        "border-green-200 bg-green-50 text-green-800",
    ),
    (
        "Sample: Nova Co",
        "R 4 \u00b7 F 3 \u00b7 M 3",
        "border-blue-200 bg-blue-50 text-blue-800",
    ),
    (
        "Sample: Vertex",
        "R 1 \u00b7 F 4 \u00b7 M 4",
        "border-red-200 bg-red-50 text-red-800",
    ),
    (
        "Sample: Lumen",
        "R 4 \u00b7 F 1 \u00b7 M 1",
        "border-amber-200 bg-amber-50 text-amber-800",
    ),
]

_VALUE_BARS: list[tuple[str, str]] = [
    ("Sample: Acme Ltd", "w-full"),
    ("Sample: Vertex", "w-3/4"),
    ("Sample: Nova Co", "w-1/2"),
    ("Sample: Lumen", "w-1/6"),
]

_STATUS_NOTES: list[tuple[str, str, str]] = [
    (
        "Sample label: frequent recent buyer",
        "Applied here to the sample row with the most recent sample order date and the highest sample order count \u2014 an invented example of a rule, not a real customer or a benchmark.",
        "border-green-200 bg-green-50 text-green-800",
    ),
    (
        "Sample label: unusual silence",
        "Applied here to a sample row whose sample gap since its last order is far longer than its own earlier sample gaps. Invented for illustration only.",
        "border-red-200 bg-red-50 text-red-800",
    ),
    (
        "Sample label: single sample order",
        "Applied here to a sample row with one order, kept separate because one purchase supports no conclusion. Invented for illustration only.",
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


def _customer_head(cells: list[str]) -> rx.Component:
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


def _customer_row(cells: list[str]) -> rx.Component:
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


def _customer_table() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("users", class_name="h-3.5 w-3.5 text-gray-400"),
            rx.el.span(
                "sample_customers.csv",
                class_name="text-xs font-medium text-gray-500",
            ),
            class_name="flex items-center gap-2",
        ),
        rx.el.p(
            "Illustrative sample rows \u2014 the names, dates, counts and amounts below are invented for this illustration, not real customers or results.",
            class_name="text-[11px] font-medium text-gray-400 mt-1",
        ),
        rx.el.table(
            rx.el.caption(
                "Illustrative sample customer rows used to show the shape of a customer transaction summary. All values are invented.",
                class_name="sr-only",
            ),
            rx.el.thead(
                _customer_head(["Customer", "Last order", "Orders", "Spend"]),
            ),
            rx.el.tbody(
                *[_customer_row(row) for row in _SAMPLE_CUSTOMERS],
            ),
            class_name="table-auto w-full mt-3",
        ),
        class_name="w-full lg:flex-1 min-w-0 rounded-2xl border border-gray-200 bg-white p-4 shadow-sm",
    )


def _rfm_chip(item: tuple[str, str, str]) -> rx.Component:
    return rx.el.li(
        rx.el.span(item[0], class_name="block text-[11px] font-semibold"),
        rx.el.span(item[1], class_name="block text-[11px] font-medium"),
        class_name=f"list-none rounded-xl border p-2.5 {item[2]}",
    )


def _value_bar(item: tuple[str, str]) -> rx.Component:
    return rx.el.li(
        rx.el.span(
            item[0],
            class_name="block text-[11px] font-medium text-gray-600 truncate",
        ),
        rx.el.div(
            rx.el.div(
                class_name=f"h-2 rounded-full bg-indigo-500 {item[1]}",
                aria_hidden="true",
            ),
            class_name="w-full h-2 rounded-full bg-gray-100 mt-1",
        ),
        class_name="list-none",
    )


def _status_note(item: tuple[str, str, str]) -> rx.Component:
    return rx.el.li(
        rx.el.span(item[0], class_name="block text-[11px] font-semibold"),
        rx.el.span(item[1], class_name="block text-[11px] font-medium"),
        class_name=f"list-none rounded-xl border p-2.5 {item[2]}",
    )


def _outputs() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("grid-2x2", class_name="h-3.5 w-3.5 text-blue-600"),
            rx.el.span(
                "Sample RFM, value and status outputs",
                class_name="text-xs font-semibold text-gray-900",
            ),
            class_name="flex items-center gap-2",
        ),
        rx.el.p(
            "Illustrative only \u2014 every score, bar length and segment label below is invented for this illustration. None of it is a real result, a rating on any external scale or a benchmark.",
            class_name="text-[11px] font-medium text-gray-400 mt-1",
        ),
        rx.el.span(
            "Sample RFM scores (invented, ranked within these four sample rows only)",
            class_name="block text-[10px] font-semibold text-gray-500 mt-3",
        ),
        rx.el.ul(
            *[_rfm_chip(item) for item in _RFM_OUTPUTS],
            class_name="grid grid-cols-1 sm:grid-cols-2 gap-2 mt-1 p-0 m-0",
        ),
        rx.el.span(
            "Sample customer value ranking (invented)",
            class_name="block text-[10px] font-semibold text-gray-500 mt-4",
        ),
        rx.el.ul(
            *[_value_bar(item) for item in _VALUE_BARS],
            class_name="flex flex-col gap-2 mt-1 p-0 m-0",
        ),
        rx.el.span(
            "Sample status labels (conventions, not universal categories)",
            class_name="block text-[10px] font-semibold text-gray-500 mt-4",
        ),
        rx.el.ul(
            *[_status_note(item) for item in _STATUS_NOTES],
            class_name="flex flex-col gap-2 mt-1 p-0 m-0",
        ),
        class_name="w-full lg:flex-1 min-w-0 rounded-2xl border border-gray-200 bg-white p-4 shadow-sm",
    )


def _workspace() -> rx.Component:
    return rx.el.figure(
        rx.el.div(
            _customer_table(),
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
            "Illustration only: a compact set of sample customer rows on the left feeding labelled RFM, customer-value and status outputs on the right, shown to explain how a customer view is read. "
            "Every name, date, count, amount, score and segment label above is invented for this illustration \u2014 none of it is a real customer, a real result, an industry benchmark or a prediction, and the labels are naming conventions rather than fixed categories. "
            "Your own figures are calculated from the rows you upload and the column mapping you confirm.",
            class_name="text-xs font-medium text-gray-400 mt-3",
        ),
        class_name="w-full m-0",
    )


def _hero() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.span(
                rx.icon("users", class_name="h-3.5 w-3.5"),
                "Customer analytics",
                class_name="flex items-center gap-1.5 w-fit rounded-full bg-indigo-50 px-3 py-1 text-xs font-semibold text-indigo-700",
            ),
            rx.el.h1(
                "Customer Analytics \u2013 Turn Customer Data Into Actionable Insights",
                class_name="text-3xl sm:text-4xl font-semibold tracking-tight text-gray-900 mt-4",
            ),
            rx.el.p(
                "The order history you already keep contains a short story for every buyer: when "
                "they first appeared, how often they return, how much they spend and when they last "
                "came back. Customer analytics regroups those rows by customer, gives each measure a "
                "stated definition, and turns the file into recency, frequency and value figures, "
                "rule-based segments and a shortlist of accounts worth your attention \u2014 each one "
                "traceable to the rows behind it.",
                class_name="text-base font-medium text-gray-500 mt-4 max-w-2xl",
            ),
            rx.el.div(
                rx.el.a(
                    "Analyze Customer Data",
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
                rx.el.span(" and ", class_name=_INLINE_TEXT),
                rx.el.a(
                    "sales analytics solution",
                    href="/solutions/sales-analytics",
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


def _rfm_note() -> rx.Component:
    return rx.el.div(
        rx.el.p(
            rx.el.span(
                "RFM scores are relative, and segment names are conventions. ",
                class_name="text-sm font-semibold text-amber-800",
            ),
            rx.el.span(
                "Recency, frequency and monetary scores rank customers against each other inside the "
                "file and window you chose \u2014 they are not ratings on any external or industry scale. "
                "Any label attached to a score combination is shorthand for the rule that produced it, "
                "not a permanent category, and the same customer may fall into a different group next "
                "period. RFM describes purchases already recorded; it does not explain why a customer "
                "bought or stopped buying.",
                class_name="text-sm font-medium text-amber-800",
            ),
        ),
        class_name="rounded-2xl border border-amber-200 bg-amber-50 p-5 w-full",
    )


def _rfm_section() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.h2("RFM Analysis", class_name=_H2),
            rx.el.p(
                "Recency, frequency and monetary value \u2014 three measures taken from your own rows, and read as rankings within your own file.",
                class_name="text-sm font-medium text-gray-500 mt-1 max-w-3xl",
            ),
            class_name="w-full",
        ),
        _rfm_note(),
        rx.el.div(
            *[_card(item) for item in _RFM],
            class_name="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 w-full",
        ),
        rx.el.p(
            rx.el.span(
                "To produce these three measures from your own file, use the ",
                class_name=_INLINE_TEXT,
            ),
            rx.el.a(
                "RFM analysis tool",
                href="/tools/rfm-calculator",
                class_name=_INLINE_LINK,
            ),
            rx.el.span(".", class_name=_INLINE_TEXT),
        ),
        class_name="flex flex-col gap-4 w-full",
    )


def _related_tools() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.h2("Related Analyses From the Same File", class_name=_H2),
            rx.el.p(
                "The same uploaded transaction rows can be read from several other angles.",
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
                    " shows margin per line rather than turnover. To measure the change you have already had, use the ",
                    class_name=_INLINE_TEXT,
                ),
                rx.el.a(
                    "sales growth calculator",
                    href="/tools/sales-growth-calculator",
                    class_name=_INLINE_LINK,
                ),
                rx.el.span(
                    ", and to project from recorded history \u2014 as an estimate rather than a guarantee \u2014 see ",
                    class_name=_INLINE_TEXT,
                ),
                rx.el.a(
                    "sales forecasting",
                    href="/tools/sales-forecasting",
                    class_name=_INLINE_LINK,
                ),
                rx.el.span(
                    ". For whole-file views, see the ", class_name=_INLINE_TEXT
                ),
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
                rx.el.span(", the ", class_name=_INLINE_TEXT),
                rx.el.a(
                    "Excel analytics tool",
                    href="/tools/excel-analyzer",
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
                "The shortest path from a customer transaction export to a shortlist you can act on.",
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
                "What people usually want to know before analyzing a customer file for the first time.",
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
            rx.el.h2(
                "Read your customer history from your own rows",
                class_name=_H2,
            ),
            rx.el.p(
                "Upload an Excel or CSV transaction export, confirm which columns hold your "
                "customer, date and amount, and read recency, frequency and value figures, "
                "rule-based segments and flagged accounts built from your own data. You can start "
                "on the Free plan.",
                class_name="text-sm font-medium text-gray-500 mt-1 max-w-2xl",
            ),
            class_name="min-w-0 flex-1",
        ),
        rx.el.div(
            rx.el.a(
                "Analyze Customer Data",
                href="/upload",
                class_name="w-fit rounded-xl bg-indigo-600 px-4 py-2.5 text-sm font-semibold text-white hover:bg-indigo-700 transition-colors",
            ),
            rx.el.a(
                rx.icon("grid-2x2", class_name="h-4 w-4"),
                "RFM analysis tool",
                href="/tools/rfm-calculator",
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


def customer_analytics_solution_page() -> rx.Component:
    return rx.el.div(
        # Hoisted into <head> as a real canonical tag.
        rx.el.link(rel="canonical", href=CUSTOMER_ANALYTICS_CANONICAL),
        _nav(),
        rx.el.main(
            _hero(),
            _section(
                "What Customer Analytics Means",
                "Regrouping the transactions you already record by buyer, with each measure defined before it is used.",
                _WHAT_IT_IS,
                "grid grid-cols-1 md:grid-cols-2 gap-4 w-full",
            ),
            _section(
                "Why Businesses Analyze Customer Data",
                "The reasons are practical: dependency, repeat business, unusual silences and where limited attention should go.",
                _WHY_ANALYZE,
                "grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 w-full",
            ),
            _section(
                "How to Understand Customer Behavior and Value",
                "A short preparation checklist that decides how much your customer analysis can actually tell you.",
                _HOW_TO_UNDERSTAND,
                "grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 w-full",
            ),
            _section(
                "Customer Segmentation",
                "Splitting buyers by rules you write down \u2014 and treating the names you give those rules as shorthand rather than truth.",
                _SEGMENTATION,
                "grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 w-full",
            ),
            _rfm_section(),
            _section(
                "Customer Value Analysis",
                "How much a customer has spent, how they spend it, and why every value measure needs its window stated.",
                _VALUE,
                "grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 w-full",
            ),
            _section(
                "Customer Purchase Behavior",
                "When customers buy, what they buy, and how their pattern has changed \u2014 observed, not interpreted.",
                _BEHAVIOUR,
                "grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 w-full",
            ),
            _section(
                "At-Risk and Loyal Customer Identification",
                "Both are descriptions of recorded behaviour against a customer's own history, produced by rules you can inspect.",
                _AT_RISK_LOYAL,
                "grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 w-full",
            ),
            _section(
                "Customer KPIs and Insights",
                "A handful of well-defined customer numbers, each with its window, its column and its data-quality caveat attached.",
                _KPIS,
                "grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 w-full",
            ),
            _section(
                "How Customer Analysis Supports Retention and Decisions",
                "Analysis narrows where to look. It does not establish that an action caused a later change.",
                _RETENTION,
                "grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 w-full",
            ),
            _section(
                "How InsightSheet Analyzes Uploaded Excel and CSV Customer Data",
                "Your uploaded rows and your confirmed column mapping drive every figure \u2014 nothing is assumed or imported from elsewhere.",
                _HOW_INSIGHTSHEET,
                "grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 w-full",
            ),
            _section(
                "Who Benefits From Customer Analytics",
                "Anyone who records dated transactions with a customer field and has to decide who to focus on next.",
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
