"""Public SEO landing page for profit margin analysis.

Stateless and dependency-free: it imports no auth, upload, dashboard,
analytics, database or subscription state, so the route renders as static
semantic HTML with no backend work.
"""

import reflex as rx

PROFIT_MARGIN_TITLE = (
    "Profit Margin Calculator – Calculate Profit Margin | InsightSheet"
)
PROFIT_MARGIN_DESCRIPTION = (
    "Calculate profit margin and understand revenue, cost, profit and "
    "profitability with InsightSheet. Analyze your business data and identify "
    "profitable products and sales."
)
PROFIT_MARGIN_CANONICAL = "https://reflex-build-generation-silver-apple.reflex.run/tools/profit-margin-calculator"

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
        "percent",
        "A ratio, not an amount",
        "Profit margin expresses profit as a share of revenue. Because it is a percentage, a small order and a large order can be compared directly — something a plain profit figure cannot do.",
    ),
    (
        "scale",
        "It measures how much of each sale you keep",
        "A 20% margin means that for every 100 units of revenue, 20 remain after the costs included in the calculation. Which costs are included is a definition you choose and should state.",
    ),
    (
        "layers",
        "Different margins answer different questions",
        "Gross margin uses direct product costs; operating margin also subtracts running costs; net margin subtracts everything. The same business shows several different, all-correct margins.",
    ),
    (
        "search",
        "It is calculated per row, product or period",
        "Margin can be computed for one order, one product, one customer or a whole month. Reading the same definition at different levels is where most of the useful detail appears.",
    ),
]

_RELATIONSHIP: list[tuple[str, str, str]] = [
    (
        "indian-rupee",
        "Revenue — what customers paid",
        "The money coming in from sales before anything is deducted. Revenue growth alone says nothing about whether the sales were worth making.",
    ),
    (
        "receipt",
        "Cost — what those sales consumed",
        "The cost attributable to the revenue you are measuring, such as purchase or production cost per unit. Which costs you attribute determines which margin you are calculating.",
    ),
    (
        "calculator",
        "Profit — revenue minus cost",
        "An absolute amount in currency. It tells you the size of the gain but not its efficiency, so two products with equal profit can be very different businesses.",
    ),
    (
        "percent",
        "Profit margin — profit as a percentage of revenue",
        "Dividing profit by revenue turns the amount into a rate, which makes products, periods and customers of different sizes comparable.",
    ),
]

_WHY_TRACK: list[tuple[str, str, str]] = [
    (
        "trending-up",
        "Revenue can grow while margin shrinks",
        "Discounting, rising supplier costs or a shift in product mix can lift revenue and lower the profit kept from it. Only margin makes that trade visible.",
    ),
    (
        "tags",
        "Pricing and discount decisions",
        "Knowing the margin on a line tells you how much room a discount actually has before the sale stops contributing.",
    ),
    (
        "package",
        "Product and range decisions",
        "Margin per product informs what to promote, reprice, renegotiate or stop carrying — usually alongside volume, not instead of it.",
    ),
    (
        "users",
        "Customer and channel mix",
        "The same product can carry different margins across customers or channels once discounts and delivery costs are attributed.",
    ),
    (
        "calendar-range",
        "Trend matters more than a single figure",
        "One month's margin is a snapshot. The direction across several comparable months is what indicates whether something is changing.",
    ),
    (
        "shield-check",
        "Comparability depends on consistency",
        "A margin is only comparable to another margin calculated the same way, over a similar period, with the same costs included.",
    ),
]

_PRODUCT_LEVEL: list[tuple[str, str, str]] = [
    (
        "columns-3",
        "Revenue and cost per product, side by side",
        "When each row carries both an amount received and a cost, revenue and cost can be summed per product and the difference read as profit and margin.",
    ),
    (
        "arrow-down-up",
        "Rank by margin as well as by revenue",
        "The two rankings rarely match. A top seller by revenue can sit low on margin, and a modest product can be one of the most efficient lines you have.",
    ),
    (
        "chart-column",
        "Volume changes the conclusion",
        "A high margin on a handful of units contributes less profit than a slim margin on a large volume. Margin and units are best read together.",
    ),
    (
        "circle-alert",
        "There is no universal good margin",
        "Acceptable margins differ enormously between industries, business models and cost structures, so we do not publish a target. The useful comparison is against your own products and your own history.",
    ),
    (
        "list-checks",
        "Weak margins are questions, not verdicts",
        "A low-margin product may be a loss leader, a bundled item, or simply mispriced. The analysis identifies where to look; the business context decides what to do.",
    ),
    (
        "brush-cleaning",
        "Cost data quality sets the ceiling",
        "If cost is missing on some rows, or mixes unit cost with total cost, the margin inherits that error — which is why gaps are reported rather than hidden.",
    ),
]

_HOW_INSIGHTSHEET: list[tuple[str, str, str]] = [
    (
        "cloud-upload",
        "You upload a sales file",
        "An Excel or CSV export of orders is enough. Header detection, date standardisation, duplicate removal and currency stripping run automatically and are logged in plain English.",
    ),
    (
        "columns-3",
        "You confirm the revenue and cost columns",
        "Profitability analysis needs an amount column and a cost column. You review the suggested mapping, so every calculation uses the field you intended.",
    ),
    (
        "calculator",
        "Profit and margin are computed from your rows",
        "Profit is revenue minus cost, and margin is that profit divided by revenue, applied per row and then aggregated to product, customer and period level.",
    ),
    (
        "package",
        "Products are compared by margin and by revenue",
        "Ranked views show which lines contribute most profit, which are least efficient and where the two rankings disagree.",
    ),
    (
        "gauge",
        "Gaps in cost data are reported, not assumed",
        "Rows without usable cost are excluded from margin rather than treated as zero cost, and the count is shown so you know the coverage.",
    ),
    (
        "file-down",
        "Findings and exports",
        "Written observations point at specific products, and the view you are reading can be exported as a PDF or Excel report.",
    ),
]

_AUDIENCE: list[tuple[str, str, str]] = [
    (
        "shopping-cart",
        "Ecommerce and retail",
        "Compare margin across a catalogue where discounts and supplier prices change often.",
    ),
    (
        "briefcase",
        "Small business owners",
        "See which lines actually carry the month without maintaining a costing spreadsheet.",
    ),
    (
        "calculator",
        "Finance and operations",
        "Check cost coverage, verify margin consistency and produce a clean profitability report from a raw export.",
    ),
    (
        "handshake",
        "Sales and pricing teams",
        "Know how much discount room a line has before agreeing to it.",
    ),
    (
        "chart-line",
        "Analysts and consultants",
        "Profile a client's revenue and cost file quickly, and agree on the margin definition before modelling.",
    ),
    (
        "graduation-cap",
        "Founders and students",
        "Learn the revenue, cost, profit and margin relationship on a real file, with every figure traceable to rows.",
    ),
]

_STEPS: list[tuple[str, str, str]] = [
    (
        "cloud-upload",
        "Step 1 — Upload your sales and cost data",
        "Choose an Excel or CSV export containing order amounts and, for margin, a cost field. Cleaning runs automatically.",
    ),
    (
        "columns-3",
        "Step 2 — Confirm your revenue and cost columns",
        "Map the amount, cost, product and date fields so profit and margin are calculated from the values you meant.",
    ),
    (
        "percent",
        "Step 3 — Read your profitability analysis",
        "Review profit and margin overall, by product and over time, then act on the lines that stand out.",
    ),
]

_FAQ: list[tuple[str, str]] = [
    (
        "What is profit margin?",
        "Profit margin is profit expressed as a percentage of revenue. It describes how much of each unit of revenue is left after the costs you include in the calculation, which makes sales of different sizes comparable.",
    ),
    (
        "How do I calculate profit margin?",
        "Subtract cost from revenue to get profit, divide that by revenue, then multiply by 100: (Revenue − Cost) ÷ Revenue × 100. If revenue is zero the division is undefined, so no meaningful percentage exists for that row or period.",
    ),
    (
        "What is a good profit margin?",
        "There is no single answer, and we do not claim one. Acceptable margins vary widely by industry, business model and cost structure. The comparison that helps is against your own products, channels and previous periods, using the same cost definition each time.",
    ),
    (
        "What is the difference between profit and profit margin?",
        "Profit is an amount of money; profit margin is a rate. Two products can both make the same profit while one keeps a much larger share of its revenue — which is why margin, not profit alone, shows efficiency.",
    ),
    (
        "How can I find my most profitable products?",
        "Attribute revenue and cost to each product, then read the products ranked by profit and by margin alongside their volume. Products that rank high on revenue but low on margin, or the reverse, are usually where the useful decisions are.",
    ),
]

_BRIDGE_STEPS: list[tuple[str, str, str, str]] = [
    ("Revenue", "₹100", "w-full", "bg-blue-600"),
    ("Product cost", "−₹62", "w-3/5", "bg-amber-500"),
    ("Other direct cost", "−₹12", "w-1/5", "bg-amber-400"),
    ("Profit", "₹26", "w-1/4", "bg-green-600"),
]

_PRODUCT_ROWS: list[tuple[str, str, str, str, str, str]] = [
    ("Starter kit", "₹42,000", "₹29,400", "₹12,600", "30.0%", "w-3/4"),
    ("Pro bundle", "₹68,000", "₹57,800", "₹10,200", "15.0%", "w-2/5"),
    ("Accessory", "₹9,500", "₹5,700", "₹3,800", "40.0%", "w-full"),
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


def _bridge_row(item: tuple[str, str, str, str]) -> rx.Component:
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
            rx.el.div(class_name=f"h-2.5 rounded-full {item[2]} {item[3]}"),
            class_name="w-full h-2.5 rounded-full bg-gray-100 mt-1",
        ),
        class_name="list-none",
    )


def _bridge() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("scale", class_name="h-3.5 w-3.5 text-blue-600"),
            rx.el.span(
                "Revenue-to-profit bridge",
                class_name="text-xs font-semibold text-gray-900",
            ),
            class_name="flex items-center gap-2",
        ),
        rx.el.p(
            "Illustrative only — sample values per ₹100 of revenue, not real results.",
            class_name="text-[11px] font-medium text-gray-400 mt-1",
        ),
        rx.el.ul(
            *[_bridge_row(item) for item in _BRIDGE_STEPS],
            class_name="flex flex-col gap-3 mt-3 p-0 m-0",
        ),
        rx.el.p(
            "Sample margin: 26 ÷ 100 × 100 = 26.0%",
            class_name="text-[11px] font-semibold text-green-700 mt-3",
        ),
        class_name="w-full lg:flex-1 min-w-0 rounded-2xl border border-gray-200 bg-white p-4 shadow-sm",
    )


def _product_row(row: tuple[str, str, str, str, str, str]) -> rx.Component:
    return rx.el.tr(
        rx.el.th(
            row[0],
            scope="row",
            class_name="px-2 py-1.5 text-left text-[11px] font-semibold text-gray-800 whitespace-nowrap border-b border-gray-100",
        ),
        rx.el.td(
            row[1],
            class_name="px-2 py-1.5 text-[11px] font-medium text-gray-600 border-b border-gray-100",
        ),
        rx.el.td(
            row[2],
            class_name="px-2 py-1.5 text-[11px] font-medium text-gray-600 border-b border-gray-100",
        ),
        rx.el.td(
            row[3],
            class_name="px-2 py-1.5 text-[11px] font-medium text-gray-600 border-b border-gray-100",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.span(
                    row[4],
                    class_name="text-[11px] font-semibold text-gray-900",
                ),
                rx.el.div(
                    rx.el.div(
                        class_name=f"h-1.5 rounded-full bg-indigo-500 {row[5]}"
                    ),
                    class_name="w-16 h-1.5 rounded-full bg-gray-100 mt-1",
                ),
                class_name="min-w-0",
            ),
            class_name="px-2 py-1.5 border-b border-gray-100",
        ),
    )


def _product_table() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("package", class_name="h-3.5 w-3.5 text-indigo-600"),
            rx.el.span(
                "Product margin comparison",
                class_name="text-xs font-semibold text-gray-900",
            ),
            class_name="flex items-center gap-2 mb-2",
        ),
        rx.el.table(
            rx.el.caption(
                "Illustrative product margin comparison — every product name and amount is a made-up sample value, not a real result.",
                class_name="caption-bottom text-xs font-medium text-gray-400 pt-2 text-left",
            ),
            rx.el.thead(
                rx.el.tr(
                    rx.el.th(
                        "Product",
                        scope="col",
                        class_name="px-2 py-1.5 text-left text-[10px] font-semibold text-gray-500 bg-gray-50 border-b border-gray-200",
                    ),
                    rx.el.th(
                        "Revenue",
                        scope="col",
                        class_name="px-2 py-1.5 text-left text-[10px] font-semibold text-gray-500 bg-gray-50 border-b border-gray-200",
                    ),
                    rx.el.th(
                        "Cost",
                        scope="col",
                        class_name="px-2 py-1.5 text-left text-[10px] font-semibold text-gray-500 bg-gray-50 border-b border-gray-200",
                    ),
                    rx.el.th(
                        "Profit",
                        scope="col",
                        class_name="px-2 py-1.5 text-left text-[10px] font-semibold text-gray-500 bg-gray-50 border-b border-gray-200",
                    ),
                    rx.el.th(
                        "Margin",
                        scope="col",
                        class_name="px-2 py-1.5 text-left text-[10px] font-semibold text-gray-500 bg-gray-50 border-b border-gray-200",
                    ),
                )
            ),
            rx.el.tbody(*[_product_row(row) for row in _PRODUCT_ROWS]),
            class_name="table-auto w-full",
        ),
        class_name="w-full lg:flex-1 min-w-0 overflow-x-auto rounded-2xl border border-gray-200 bg-white p-4 shadow-sm",
    )


def _centerpiece() -> rx.Component:
    return rx.el.figure(
        rx.el.div(
            _bridge(),
            _product_table(),
            class_name="flex flex-col lg:flex-row items-stretch gap-4 w-full",
        ),
        rx.el.figcaption(
            "Illustration only: the bridge and the product table above use invented sample numbers to show how revenue, cost, profit and margin relate. They are not real results — your own figures are calculated from your uploaded rows.",
            class_name="text-xs font-medium text-gray-400 mt-3",
        ),
        class_name="w-full m-0",
    )


def _hero() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.span(
                rx.icon("percent", class_name="h-3.5 w-3.5"),
                "Profit margin calculator",
                class_name="flex items-center gap-1.5 w-fit rounded-full bg-indigo-50 px-3 py-1 text-xs font-semibold text-indigo-700",
            ),
            rx.el.h1(
                "Profit Margin Calculator – Analyze Your Business Profitability",
                class_name="text-3xl sm:text-4xl font-semibold tracking-tight text-gray-900 mt-4",
            ),
            rx.el.p(
                "Profit margin turns revenue and cost into a rate you can compare across products, "
                "customers and months. Upload a sales file that includes cost, confirm which columns "
                "hold revenue and cost, and InsightSheet calculates profit and margin from your own "
                "rows — so profitable and less-profitable lines become visible instead of assumed.",
                class_name="text-base font-medium text-gray-500 mt-4 max-w-2xl",
            ),
            rx.el.div(
                rx.el.a(
                    "Analyze Business Data",
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
                    "New here? Start with the ",
                    class_name="text-xs font-medium text-gray-500",
                ),
                rx.el.a(
                    "InsightSheet spreadsheet analytics overview",
                    href="/",
                    class_name="text-xs font-semibold text-blue-700 hover:underline",
                ),
                rx.el.span(
                    ", or see how a whole file is analysed with the ",
                    class_name="text-xs font-medium text-gray-500",
                ),
                rx.el.a(
                    "Excel analytics tool",
                    href="/tools/excel-analyzer",
                    class_name="text-xs font-semibold text-blue-700 hover:underline",
                ),
                rx.el.span(
                    " and the ",
                    class_name="text-xs font-medium text-gray-500",
                ),
                rx.el.a(
                    "CSV analytics tool",
                    href="/tools/csv-analyzer",
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


def _formula() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.h2("Revenue, Cost, Profit and Profit Margin", class_name=_H2),
            rx.el.p(
                "Four related but different figures. Three are amounts; only the last one is a rate.",
                class_name="text-sm font-medium text-gray-500 mt-1 max-w-3xl",
            ),
            class_name="w-full",
        ),
        rx.el.div(
            *[_card(item) for item in _RELATIONSHIP],
            class_name="grid grid-cols-1 md:grid-cols-2 gap-4 w-full",
        ),
        rx.el.div(
            rx.el.h3("The standard profit margin formula", class_name=_H3),
            rx.el.p(
                rx.el.code(
                    "(Revenue \u2212 Cost) \u00f7 Revenue \u00d7 100",
                    class_name="inline-block w-fit rounded-lg border border-indigo-200 bg-white px-3 py-1.5 text-sm font-semibold text-indigo-800",
                ),
                class_name="mt-2",
            ),
            rx.el.p(
                "Read it in two moves: revenue minus cost gives profit as an amount, and dividing that "
                "profit by revenue converts the amount into a percentage of the sale.",
                class_name=_BODY,
            ),
            rx.el.p(
                rx.el.span(
                    "Note on zero revenue: ",
                    class_name="text-sm font-semibold text-amber-800",
                ),
                rx.el.span(
                    "when revenue is zero the division has no defined result, so no meaningful "
                    "percentage can be produced for that row, product or period. A refund-only or "
                    "sale-free period may still have a profit or loss amount, but not a margin — "
                    "InsightSheet leaves the margin blank in those cases instead of showing 0% or 100%.",
                    class_name="text-sm font-medium text-amber-800",
                ),
                class_name="mt-3 rounded-xl border border-amber-200 bg-amber-50 p-3",
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
                "The shortest path from a sales and cost export to profit and margin you can act on.",
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
                "What people usually want to know before analysing margins for the first time.",
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
            rx.el.h2("Analyse your profitability now", class_name=_H2),
            rx.el.p(
                "Upload a sales export with cost, confirm your revenue and cost columns, and read "
                "profit and margin by product and by month. You can start on the Free plan.",
                class_name="text-sm font-medium text-gray-500 mt-1 max-w-2xl",
            ),
            rx.el.p(
                rx.el.span(
                    "Looking at customers rather than products? See the ",
                    class_name="text-xs font-medium text-gray-500",
                ),
                rx.el.a(
                    "RFM analysis tool",
                    href="/tools/rfm-calculator",
                    class_name="text-xs font-semibold text-blue-700 hover:underline",
                ),
                rx.el.span(".", class_name="text-xs font-medium text-gray-500"),
                class_name="mt-3",
            ),
            class_name="min-w-0 flex-1",
        ),
        rx.el.div(
            rx.el.a(
                "Analyze Business Data",
                href="/upload",
                class_name="w-fit rounded-xl bg-indigo-600 px-4 py-2.5 text-sm font-semibold text-white hover:bg-indigo-700 transition-colors",
            ),
            rx.el.a(
                rx.icon("file-text", class_name="h-4 w-4"),
                "CSV analytics tool",
                href="/tools/csv-analyzer",
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


def profit_margin_calculator_page() -> rx.Component:
    return rx.el.div(
        # Hoisted into <head> as a real canonical tag.
        rx.el.link(rel="canonical", href=PROFIT_MARGIN_CANONICAL),
        _nav(),
        rx.el.main(
            _hero(),
            _section(
                "What Profit Margin Is",
                "A percentage that describes how much of your revenue survives the costs you count against it.",
                _WHAT_IT_IS,
                "grid grid-cols-1 md:grid-cols-2 gap-4 w-full",
            ),
            _formula(),
            _section(
                "Why Businesses Track Profit Margins",
                "Because revenue alone can move in the right direction while the business gets worse.",
                _WHY_TRACK,
                "grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 w-full",
            ),
            _section(
                "Finding Profitable and Less-Profitable Products",
                "Product-level revenue and cost show where profit actually comes from — judged against your own range, not an industry target.",
                _PRODUCT_LEVEL,
                "grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 w-full",
            ),
            _section(
                "How InsightSheet Analyses Profitability",
                "Your uploaded sales and cost data drives every figure — nothing is assumed or imported from elsewhere.",
                _HOW_INSIGHTSHEET,
                "grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 w-full",
            ),
            _section(
                "Who Benefits From Margin Analysis",
                "Anyone who sells something and records what it cost.",
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
