"""Public SEO landing page for RFM customer segmentation.

Stateless and dependency-free: it imports no auth, upload, dashboard,
analytics, database or subscription state, so the route renders as static
semantic HTML with no backend work.
"""

import reflex as rx

RFM_CALCULATOR_TITLE = (
    "RFM Analysis Tool – Customer Segmentation Calculator | InsightSheet"
)
RFM_CALCULATOR_DESCRIPTION = (
    "Analyze customers using Recency, Frequency and Monetary (RFM) analysis. "
    "Understand customer segments and identify your best, loyal and at-risk "
    "customers with InsightSheet."
)
RFM_CALCULATOR_CANONICAL = "https://reflex-build-generation-silver-apple.reflex.run/tools/rfm-calculator"

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
        "grid-2x2",
        "Three behavioural questions",
        "RFM analysis describes a customer by how recently they bought, how often they buy and how much they have spent. Those three facts already separate an active buyer from one drifting away.",
    ),
    (
        "receipt",
        "Built from transactions you already have",
        "Nothing extra needs collecting: a purchase history with a date, a customer identifier and an order amount is enough to compute all three dimensions.",
    ),
    (
        "layers",
        "Behaviour instead of demographics",
        "Where demographic grouping guesses who someone is, RFM reads what they actually did — which is usually the better predictor of what they will do next.",
    ),
    (
        "list-checks",
        "Groups you can act on",
        "The point is not the score itself but the shortlist it produces: which customers to keep close, which to nurture and which to contact before they lapse.",
    ),
]

_DIMENSIONS: list[tuple[str, str, str]] = [
    (
        "clock",
        "Recency — when did they last buy?",
        "Measured as the time between a customer's most recent order and the end of the period you are analysing. A short gap usually means attention now is well spent; a long gap is the earliest visible sign of churn.",
    ),
    (
        "repeat",
        "Frequency — how often do they buy?",
        "The number of distinct orders in the period. Frequency separates a habit from a one-off purchase, and it is what makes repeat revenue predictable rather than lucky.",
    ),
    (
        "indian-rupee",
        "Monetary — how much have they spent?",
        "Total (or average) order value across the period. It shows the commercial weight behind each relationship, so effort can be aimed where it changes the numbers.",
    ),
]

_SCORING: list[tuple[str, str, str]] = [
    (
        "arrow-down-up",
        "Rank, then band",
        "Each dimension is usually turned into a score by ranking customers against one another and splitting them into bands — for example quintiles or quartiles. Scoring is relative to your own dataset, not to an industry table.",
    ),
    (
        "sliders-horizontal",
        "There is no single universal model",
        "Band counts, whether recency is inverted, whether monetary uses total or average value, and the length of the period are all choices. Different reasonable choices give different labels for the same customer, so the definition matters more than the number.",
    ),
    (
        "calendar-range",
        "The window changes the answer",
        'A twelve-month window and a ninety-day window describe different behaviour. Subscription, wholesale and retail businesses all have different normal buying gaps, so "recent" has to be defined against your own cadence.',
    ),
    (
        "grid-2x2",
        "Segments are combinations",
        "Segmentation reads the three scores together. High recency with high frequency behaves nothing like high monetary value that has gone quiet, even though both customers may have spent the same amount.",
    ),
]

_ACTIONS: list[tuple[str, str, str]] = [
    (
        "star",
        "Best customers — recent, frequent, high value",
        "They score well on all three dimensions. Protect the relationship: early access, direct contact, reliable service. Any friction here is the most expensive kind.",
    ),
    (
        "heart-handshake",
        "Loyal customers — frequent, consistently recent",
        "They buy regularly, often at a moderate value. Growth here comes from increasing order value or cadence rather than from acquisition, and they are your most credible source of referrals and feedback.",
    ),
    (
        "triangle-alert",
        "At-risk customers — used to buy, now quiet",
        "Strong frequency or monetary history with weak recency. This is where a small, timely contact recovers revenue you have already paid to acquire — and where waiting a quarter usually means losing it.",
    ),
    (
        "user-plus",
        "New and one-time buyers",
        "Recent but with a single order and little history. The useful action is a second purchase, since the step from one order to two is what turns a buyer into a segment worth protecting.",
    ),
    (
        "moon",
        "Lapsed and low-value customers",
        "Low across all three dimensions. Knowing who they are is mostly about where not to spend, so budget and attention go to segments that can still move.",
    ),
    (
        "list-checks",
        "From label to action list",
        "A segment is only useful when it becomes a named list of customers with an owner and a next step — which is why the names of the rows matter more than the colours of the grid.",
    ),
]

_HOW_INSIGHTSHEET: list[tuple[str, str, str]] = [
    (
        "cloud-upload",
        "You upload a transaction file",
        "An Excel or CSV export of orders is enough. Cleaning — header detection, date standardisation, duplicate removal and currency stripping — runs automatically and is logged in plain English.",
    ),
    (
        "columns-3",
        "You confirm which column is which",
        "Date, customer, order amount and order ID drive the whole calculation, so you review the suggested mapping before anything is scored.",
    ),
    (
        "calculator",
        "Recency, frequency and monetary value are computed per customer",
        "Each customer's last order date, order count and spend are derived from your own cleaned rows, relative to the period in your file.",
    ),
    (
        "grid-2x2",
        "Customers are grouped into readable segments",
        "The three measures are combined into segments you can browse, filter and sort, with the definition used shown alongside the result.",
    ),
    (
        "table",
        "Every segment opens into real customer rows",
        "You can see which accounts sit behind a segment, so the analysis ends in a list you can work through rather than a chart.",
    ),
    (
        "file-down",
        "Findings and exports",
        "Written observations point at specific customers, and the view you are looking at can be exported as a PDF or Excel report.",
    ),
]

_AUDIENCE: list[tuple[str, str, str]] = [
    (
        "shopping-cart",
        "Ecommerce and retail",
        "Repeat purchase is the whole business model, so recency and frequency directly explain the month.",
    ),
    (
        "briefcase",
        "Small business owners",
        "Get a monthly read on which customers are still active without maintaining a CRM.",
    ),
    (
        "handshake",
        "Sales and account teams",
        "Prioritise outreach by history rather than by whoever answered last, and prepare a call with facts.",
    ),
    (
        "megaphone",
        "Marketing and retention",
        "Aim campaigns at a defined segment instead of the whole list, and measure the effect on the same segments afterwards.",
    ),
    (
        "chart-line",
        "Analysts and consultants",
        "Profile a client's order history quickly and agree on segment definitions before building anything heavier.",
    ),
    (
        "graduation-cap",
        "Founders and students",
        "Learn segmentation from first principles on a real file, with every figure traceable to rows.",
    ),
]

_STEPS: list[tuple[str, str, str]] = [
    (
        "cloud-upload",
        "Step 1 — Upload your transaction data",
        "Choose an Excel or CSV export containing order dates, customer identifiers and order amounts. Cleaning runs automatically.",
    ),
    (
        "columns-3",
        "Step 2 — Confirm your customer and order columns",
        "Map date, customer, amount and order ID so recency, frequency and monetary value are measured from the right fields.",
    ),
    (
        "grid-2x2",
        "Step 3 — Read your RFM segments",
        "Review segment groupings, open the customer lists behind them and act on best, loyal and at-risk accounts.",
    ),
]

_FAQ: list[tuple[str, str]] = [
    (
        "What is RFM analysis?",
        "RFM analysis is a way of describing each customer by three behaviours taken from their purchase history: recency (how recently they bought), frequency (how often) and monetary value (how much they spent). Combining those three lets you group customers into segments and act on them.",
    ),
    (
        "How is an RFM score calculated?",
        "Typically customers are ranked on each dimension and split into bands, such as quintiles, giving a score per dimension that is then read as a combination. There is no single universal model: the number of bands, the period length and whether monetary value uses total or average spend are all definitional choices that change the result.",
    ),
    (
        "What data do I need for RFM analysis?",
        "A transaction-level file with one row per order and three fields: an order date, a customer identifier (an email or even a plain name is enough) and an order amount. An order ID improves frequency accuracy where a single order spans several rows.",
    ),
    (
        "How do I identify my best, loyal and at-risk customers?",
        "Best customers score well on all three dimensions. Loyal customers show consistent frequency and recent activity. At-risk customers have strong frequency or spend in their history but weak recency — they used to buy and have gone quiet, which is usually the cheapest revenue to recover.",
    ),
    (
        "How often should I run RFM analysis?",
        "Often enough to catch a change while it is still reversible. Monthly or quarterly suits most businesses, though a shorter cycle makes sense where the normal buying gap is measured in weeks. Keeping the same definition each time is what makes segment movement comparable.",
    ),
]

_MATRIX_ROWS: list[tuple[str, str, str, str, str, str]] = [
    (
        "High spend",
        "Champions",
        "bg-blue-50 border-blue-200 text-blue-800",
        "Needs attention",
        "bg-amber-50 border-amber-200 text-amber-800",
        "Can't lose",
    ),
    (
        "Medium spend",
        "Loyal",
        "bg-indigo-50 border-indigo-200 text-indigo-800",
        "Cooling off",
        "bg-amber-50 border-amber-200 text-amber-800",
        "At risk",
    ),
    (
        "Low spend",
        "Promising",
        "bg-gray-50 border-gray-200 text-gray-700",
        "Needs nurture",
        "bg-gray-50 border-gray-200 text-gray-700",
        "Lapsed",
    ),
]

_SCORECARD_ROWS: list[tuple[str, str, str, str, str]] = [
    ("Acme Ltd", "12 days", "9 orders", "₹184,000", "Champions"),
    ("Nova Co", "34 days", "6 orders", "₹96,400", "Loyal"),
    ("Vertex", "128 days", "7 orders", "₹142,300", "At risk"),
    ("Larkin", "9 days", "1 order", "₹11,300", "Promising"),
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


def _matrix_cell(label: str, style: str) -> rx.Component:
    return rx.el.td(
        rx.el.span(
            label,
            class_name=f"block w-full rounded-lg border px-2 py-2 text-[11px] font-semibold text-center {style}",
        ),
        class_name="p-1 align-middle",
    )


def _matrix_row(row: tuple[str, str, str, str, str, str]) -> rx.Component:
    return rx.el.tr(
        rx.el.th(
            row[0],
            scope="row",
            class_name="p-1 text-left text-[11px] font-medium text-gray-500 whitespace-nowrap",
        ),
        _matrix_cell(row[1], row[2]),
        _matrix_cell(row[3], row[4]),
        _matrix_cell(row[5], "bg-rose-50 border-rose-200 text-rose-800"),
        class_name="",
    )


def _matrix() -> rx.Component:
    return rx.el.table(
        rx.el.caption(
            "Illustrative RFM segmentation matrix — sample segment names only, not results from real data.",
            class_name="caption-bottom text-xs font-medium text-gray-400 pt-2 text-left",
        ),
        rx.el.thead(
            rx.el.tr(
                rx.el.th(
                    "Monetary \u2193 / Recency \u2192",
                    scope="col",
                    class_name="p-1 text-left text-[10px] font-semibold text-gray-400 whitespace-nowrap",
                ),
                rx.el.th(
                    "Recent",
                    scope="col",
                    class_name="p-1 text-[10px] font-semibold text-gray-500",
                ),
                rx.el.th(
                    "Slipping",
                    scope="col",
                    class_name="p-1 text-[10px] font-semibold text-gray-500",
                ),
                rx.el.th(
                    "Dormant",
                    scope="col",
                    class_name="p-1 text-[10px] font-semibold text-gray-500",
                ),
            )
        ),
        rx.el.tbody(*[_matrix_row(row) for row in _MATRIX_ROWS]),
        class_name="table-auto w-full",
    )


def _scorecard_row(row: tuple[str, str, str, str, str]) -> rx.Component:
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
            rx.el.span(
                row[4],
                class_name="inline-block w-fit rounded-full bg-indigo-50 px-2 py-0.5 text-[10px] font-semibold text-indigo-700",
            ),
            class_name="px-2 py-1.5 border-b border-gray-100",
        ),
    )


def _scorecard() -> rx.Component:
    return rx.el.table(
        rx.el.caption(
            "Illustrative customer scorecard — the names, gaps, order counts and amounts are made-up sample values, not real results.",
            class_name="caption-bottom text-xs font-medium text-gray-400 pt-2 text-left",
        ),
        rx.el.thead(
            rx.el.tr(
                rx.el.th(
                    "Customer",
                    scope="col",
                    class_name="px-2 py-1.5 text-left text-[10px] font-semibold text-gray-500 bg-gray-50 border-b border-gray-200",
                ),
                rx.el.th(
                    "Recency",
                    scope="col",
                    class_name="px-2 py-1.5 text-left text-[10px] font-semibold text-gray-500 bg-gray-50 border-b border-gray-200",
                ),
                rx.el.th(
                    "Frequency",
                    scope="col",
                    class_name="px-2 py-1.5 text-left text-[10px] font-semibold text-gray-500 bg-gray-50 border-b border-gray-200",
                ),
                rx.el.th(
                    "Monetary",
                    scope="col",
                    class_name="px-2 py-1.5 text-left text-[10px] font-semibold text-gray-500 bg-gray-50 border-b border-gray-200",
                ),
                rx.el.th(
                    "Segment",
                    scope="col",
                    class_name="px-2 py-1.5 text-left text-[10px] font-semibold text-gray-500 bg-gray-50 border-b border-gray-200",
                ),
            )
        ),
        rx.el.tbody(*[_scorecard_row(row) for row in _SCORECARD_ROWS]),
        class_name="table-auto w-full",
    )


def _centerpiece() -> rx.Component:
    return rx.el.figure(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("grid-2x2", class_name="h-3.5 w-3.5 text-blue-600"),
                    rx.el.span(
                        "Segmentation matrix",
                        class_name="text-xs font-semibold text-gray-900",
                    ),
                    class_name="flex items-center gap-2 mb-2",
                ),
                _matrix(),
                class_name="w-full lg:flex-1 min-w-0 overflow-x-auto rounded-2xl border border-gray-200 bg-white p-4 shadow-sm",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon("table", class_name="h-3.5 w-3.5 text-indigo-600"),
                    rx.el.span(
                        "Customer scorecard",
                        class_name="text-xs font-semibold text-gray-900",
                    ),
                    class_name="flex items-center gap-2 mb-2",
                ),
                _scorecard(),
                class_name="w-full lg:flex-1 min-w-0 overflow-x-auto rounded-2xl border border-gray-200 bg-white p-4 shadow-sm",
            ),
            class_name="flex flex-col lg:flex-row items-stretch gap-4 w-full",
        ),
        rx.el.figcaption(
            "Illustration only: every segment name, gap, order count and amount above is a sample used to show the layout. Your own segments are calculated from your uploaded rows.",
            class_name="text-xs font-medium text-gray-400 mt-3",
        ),
        class_name="w-full m-0",
    )


def _hero() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.span(
                rx.icon("grid-2x2", class_name="h-3.5 w-3.5"),
                "RFM analysis tool",
                class_name="flex items-center gap-1.5 w-fit rounded-full bg-indigo-50 px-3 py-1 text-xs font-semibold text-indigo-700",
            ),
            rx.el.h1(
                "RFM Analysis Tool – Analyze Your Customers",
                class_name="text-3xl sm:text-4xl font-semibold tracking-tight text-gray-900 mt-4",
            ),
            rx.el.p(
                "Recency, Frequency and Monetary analysis turns a plain order history into customer "
                "segments you can act on. Upload a transaction file, confirm which columns hold the "
                "date, customer and amount, and InsightSheet computes each customer's recency, order "
                "frequency and spend — then groups them so your best, loyal and at-risk customers "
                "become named lists rather than guesses.",
                class_name="text-base font-medium text-gray-500 mt-4 max-w-2xl",
            ),
            rx.el.div(
                rx.el.a(
                    rx.icon("cloud-upload", class_name="h-4 w-4"),
                    "Analyze Customer Data",
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
                    ", or read how a whole file is analysed with the ",
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
                "The shortest path from an order history to customer segments you can act on.",
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
                "What people usually want to know before running their first RFM analysis.",
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
            rx.el.h2("Segment your customers now", class_name=_H2),
            rx.el.p(
                "Upload a transaction export, confirm your customer and order columns, and read your "
                "RFM segments. You can start on the Free plan.",
                class_name="text-sm font-medium text-gray-500 mt-1 max-w-2xl",
            ),
            class_name="min-w-0 flex-1",
        ),
        rx.el.div(
            rx.el.a(
                rx.icon("cloud-upload", class_name="h-4 w-4"),
                "Analyze Customer Data",
                href="/upload",
                class_name="flex items-center gap-2 w-fit rounded-xl bg-indigo-600 px-4 py-2.5 text-sm font-semibold text-white hover:bg-indigo-700 transition-colors",
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


def rfm_calculator_page() -> rx.Component:
    return rx.el.div(
        # Hoisted into <head> as a real canonical tag.
        rx.el.link(rel="canonical", href=RFM_CALCULATOR_CANONICAL),
        _nav(),
        rx.el.main(
            _hero(),
            _section(
                "What RFM Analysis Is",
                "A compact way of describing customer behaviour using only the orders you already have on file.",
                _WHAT_IT_IS,
                "grid grid-cols-1 md:grid-cols-2 gap-4 w-full",
            ),
            _section(
                "Recency, Frequency and Monetary Value",
                "Three separate measures — each answers a different question, and they are only useful read together.",
                _DIMENSIONS,
                "grid grid-cols-1 md:grid-cols-3 gap-4 w-full",
            ),
            _section(
                "How RFM Scoring and Segmentation Work",
                "Scoring is a set of choices about your own data, not a fixed formula everyone shares.",
                _SCORING,
                "grid grid-cols-1 md:grid-cols-2 gap-4 w-full",
            ),
            _section(
                "Identifying Best, Loyal and At-Risk Customers",
                "What each group looks like in the numbers, and the action that usually follows.",
                _ACTIONS,
                "grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 w-full",
            ),
            _section(
                "How InsightSheet Provides RFM Insights",
                "Your uploaded transaction data drives every figure — nothing is assumed or imported from elsewhere.",
                _HOW_INSIGHTSHEET,
                "grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 w-full",
            ),
            _section(
                "Who Can Use RFM Analysis",
                "Anyone with repeat customers and a record of their orders.",
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
