"""Public SEO landing page for sales growth analysis.

Stateless and dependency-free: it imports no auth, upload, dashboard,
analytics, database or subscription state, so the route renders as static
semantic HTML with no backend work.
"""

import reflex as rx

SALES_GROWTH_TITLE = (
    "Sales Growth Calculator \u2013 Calculate Sales Growth | InsightSheet"
)
SALES_GROWTH_DESCRIPTION = (
    "Calculate and understand sales growth over time with InsightSheet. "
    "Analyze revenue trends, compare sales periods and discover business "
    "growth opportunities."
)
SALES_GROWTH_CANONICAL = "https://reflex-build-generation-silver-apple.reflex.run/tools/sales-growth-calculator"

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
        "trending-up",
        "It compares one period with another",
        "Sales growth is the change in sales between two periods, usually expressed as a percentage. On its own a single month's revenue has no direction; growth is what gives it one.",
    ),
    (
        "percent",
        "A rate, not an amount",
        "Because growth is a percentage of the earlier period, a small business and a large one can be compared on the same scale. The underlying amounts remain useful context.",
    ),
    (
        "calendar-range",
        "The periods must be equivalent",
        "Month against month, quarter against quarter, year against year. Comparing a full month with a part-month is the most common way a growth figure becomes misleading.",
    ),
    (
        "layers",
        "It can be read at several levels",
        "Growth can be calculated for the whole business, one product, one channel or one customer. The same definition applied at different levels is where most of the useful detail lives.",
    ),
]

_HOW_MEASURED: list[tuple[str, str, str]] = [
    (
        "calendar",
        "Period-over-period",
        "This month against last month. Responsive to recent change, but also the most exposed to seasonality and to short-month effects.",
    ),
    (
        "calendar-check",
        "Year-over-year",
        "This month against the same month last year. Comparing like seasons removes most seasonal distortion, but it needs at least a year of history.",
    ),
    (
        "chart-line",
        "Cumulative or year-to-date",
        "Sales so far this year against the same span last year. Smoother than a single month and useful for progress against a plan.",
    ),
    (
        "receipt",
        "Growth in orders and average order value",
        "Revenue growth can come from more orders, larger orders, or both. Measuring order count and average order value separately explains which.",
    ),
    (
        "sigma",
        "Absolute change alongside the percentage",
        "A percentage from a small base can look dramatic. Reading the currency change next to it keeps the size of the movement honest.",
    ),
    (
        "shield-check",
        "One consistent definition",
        "Growth figures are only comparable when the same revenue field, the same filters and the same period length are used each time.",
    ),
]

_COMPARING: list[tuple[str, str, str]] = [
    (
        "columns-3",
        "Choose two comparable windows",
        "Equal length, aligned boundaries, and complete data in both. Two full calendar months, or two 30-day windows, are both fine as long as you stay consistent.",
    ),
    (
        "circle-alert",
        "Exclude incomplete periods",
        "A month still in progress will almost always look like a decline. Compare complete periods, or compare the same number of elapsed days in each.",
    ),
    (
        "filter",
        "Apply the same filters to both sides",
        "If the current period excludes refunds, cancellations or a particular channel, the previous period must exclude them too.",
    ),
    (
        "brush-cleaning",
        "Check for duplicates and gaps",
        "A duplicated batch of orders in one period, or a week of missing rows in the other, changes the percentage without anything changing in the business.",
    ),
]

_WHY_TRENDS: list[tuple[str, str, str]] = [
    (
        "chart-line",
        "Direction beats a single figure",
        "One period tells you where you are; several consecutive periods tell you where you are heading, which is what most decisions actually need.",
    ),
    (
        "search",
        "It shows when something changed",
        "A visible step up or down in the trend points at a date, and a date can usually be matched to a campaign, a price change or a lost account.",
    ),
    (
        "package",
        "It separates the business from the noise",
        "A trend across several periods makes it easier to tell an ordinary fluctuation from a sustained move.",
    ),
    (
        "handshake",
        "It informs planning conversations",
        "Targets, hiring and stock decisions are easier to discuss with a measured trend than with an impression of how the month felt.",
    ),
    (
        "users",
        "It prompts better questions",
        "Growth rarely explains itself. The value of the number is that it tells you which segment, product or period to look at next.",
    ),
    (
        "scale",
        "It keeps growth in proportion",
        "Reading percentage change together with the underlying amounts avoids over-reacting to movement from a very small base.",
    ),
]

_PATTERNS: list[tuple[str, str, str]] = [
    (
        "trending-up",
        "Sustained growth",
        "Several consecutive periods of increase, in the same direction, on a stable revenue definition. One strong period is not a trend; a run of them is worth investigating.",
    ),
    (
        "minus",
        "Flat performance",
        "Small movements around a steady level. Flat is not automatically bad — it can mean stability, capacity limits or a mature product — but it does mean growth is not coming from where you are looking.",
    ),
    (
        "trending-down",
        "Decline",
        "Repeated decreases. Worth splitting into fewer customers, fewer orders per customer, or smaller orders, because each points somewhere different.",
    ),
    (
        "calendar-range",
        "Seasonality",
        "A pattern that repeats at the same points each year. Where you have more than one year of history, comparing the same season year-over-year is how you tell a season from a change.",
    ),
    (
        "package",
        "Product mix effects",
        "Total sales can be flat while the composition shifts between products. Per-product growth shows whether one line is quietly replacing another.",
    ),
    (
        "users",
        "Customer mix effects",
        "Growth concentrated in a few accounts, or driven by new versus returning buyers, behaves very differently over time — so it is worth reading growth per customer group too.",
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
        "You confirm the date and revenue columns",
        "Growth needs a usable date and an amount. You review the suggested mapping, so every period total is built from the fields you intended.",
    ),
    (
        "calendar",
        "Rows are grouped into periods",
        "Cleaned dates are grouped by month so period totals, and the change between them, come from your own rows rather than from an assumption.",
    ),
    (
        "percent",
        "Period-over-period change is calculated",
        "Change is measured between complete months, and where a previous period has no sales the percentage is left blank rather than invented.",
    ),
    (
        "chart-line",
        "Trends, products and customers",
        "The revenue trend, product breakdowns and customer views let you see whether a change is broad or concentrated in part of the business.",
    ),
    (
        "file-down",
        "Findings and exports",
        "Written observations point at specific periods, products or customers, and the view you are reading can be exported as a PDF or Excel report.",
    ),
]

_AUDIENCE: list[tuple[str, str, str]] = [
    (
        "shopping-cart",
        "Ecommerce and retail",
        "Compare months and seasons across a catalogue where promotions and product mix change often.",
    ),
    (
        "briefcase",
        "Small business owners",
        "Get a monthly read on whether sales are actually moving, without rebuilding a spreadsheet each time.",
    ),
    (
        "handshake",
        "Sales teams",
        "See which accounts and products grew or slipped between two periods before a pipeline review.",
    ),
    (
        "calculator",
        "Finance and operations",
        "Produce a consistent growth figure from a raw export, with the data-quality caveats visible.",
    ),
    (
        "chart-line",
        "Analysts and consultants",
        "Profile a client's sales history quickly and agree on the comparison basis before modelling.",
    ),
    (
        "graduation-cap",
        "Founders and students",
        "Learn how period comparison works on a real file, with every figure traceable to rows.",
    ),
]

_STEPS: list[tuple[str, str, str]] = [
    (
        "cloud-upload",
        "Step 1 \u2014 Upload your sales data",
        "Choose an Excel or CSV export containing order dates and amounts. Cleaning runs automatically and is logged.",
    ),
    (
        "columns-3",
        "Step 2 \u2014 Confirm your date and revenue columns",
        "Map the date, amount, product and customer fields so each period total is built from the values you meant.",
    ),
    (
        "trending-up",
        "Step 3 \u2014 Read your growth and trends",
        "Compare complete periods, follow the revenue trend and see whether change is broad or concentrated.",
    ),
]

_FAQ: list[tuple[str, str]] = [
    (
        "What is sales growth?",
        "Sales growth is the change in sales between two comparable periods, usually stated as a percentage of the earlier period. It describes direction and pace rather than size, which is why it is read alongside the underlying revenue amounts.",
    ),
    (
        "How do I calculate sales growth?",
        "Subtract the previous period's sales from the current period's sales, divide by the previous period's sales, then multiply by 100: (Current period sales \u2212 Previous period sales) \u00f7 Previous period sales \u00d7 100. Both periods must cover an equivalent span and use the same revenue definition.",
    ),
    (
        "What is a good sales growth rate?",
        "There is no single figure, and we do not claim one. What counts as healthy depends on your industry, stage, seasonality and how large the base period was. The useful comparison is against your own history and against the same season in previous years.",
    ),
    (
        "How do I compare this month's sales to last month?",
        "Use two complete months, apply identical filters to both, and total the same revenue field in each. If the current month is still running, compare the same number of elapsed days in each month instead, otherwise the partial month will look like a decline.",
    ),
    (
        "Why are my sales declining?",
        "The percentage does not answer that on its own, but the breakdown usually narrows it down: fewer customers ordering, the same customers ordering less often, smaller average orders, a weak product line, or a seasonal low. Splitting the decline by product and by customer shows which of those applies to your data.",
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

_PERIOD_ROWS: list[tuple[str, str, str, str, str]] = [
    ("Previous period (May)", "\u20b94,00,000", "w-4/5", "bg-gray-400", ""),
    (
        "Current period (June)",
        "\u20b94,60,000",
        "w-full",
        "bg-blue-600",
        "",
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


def _period_row(item: tuple[str, str, str, str, str]) -> rx.Component:
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


def _period_compare() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("columns-3", class_name="h-3.5 w-3.5 text-blue-600"),
            rx.el.span(
                "Two-period comparison",
                class_name="text-xs font-semibold text-gray-900",
            ),
            class_name="flex items-center gap-2",
        ),
        rx.el.p(
            "Illustrative only \u2014 invented sample totals for two complete months, not real results.",
            class_name="text-[11px] font-medium text-gray-400 mt-1",
        ),
        rx.el.ul(
            *[_period_row(item) for item in _PERIOD_ROWS],
            class_name="flex flex-col gap-3 mt-3 p-0 m-0",
        ),
        rx.el.p(
            "Sample growth: (4,60,000 \u2212 4,00,000) \u00f7 4,00,000 \u00d7 100 = 15.0%",
            class_name="text-[11px] font-semibold text-green-700 mt-3",
        ),
        class_name="w-full lg:flex-1 min-w-0 rounded-2xl border border-gray-200 bg-white p-4 shadow-sm",
    )


def _trend_bar(item: tuple[str, str, str]) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(class_name=f"w-full rounded-t-md {item[2]} {item[1]}"),
            class_name="flex h-20 w-full items-end",
        ),
        rx.el.span(
            item[0],
            class_name="block text-[10px] font-medium text-gray-400 mt-1 text-center",
        ),
        class_name="flex-1 min-w-0",
    )


def _trend() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("chart-line", class_name="h-3.5 w-3.5 text-indigo-600"),
            rx.el.span(
                "Revenue trend by month",
                class_name="text-xs font-semibold text-gray-900",
            ),
            class_name="flex items-center gap-2",
        ),
        rx.el.p(
            "Illustrative only \u2014 the bar heights are made-up sample values used to show shape, not measured revenue.",
            class_name="text-[11px] font-medium text-gray-400 mt-1",
        ),
        rx.el.div(
            *[_trend_bar(item) for item in _TREND_BARS],
            class_name="flex items-end gap-2 mt-3",
        ),
        rx.el.p(
            "Read as: two flat months, then three rising months \u2014 the shape a sustained increase makes.",
            class_name="text-[11px] font-medium text-gray-500 mt-3",
        ),
        class_name="w-full lg:flex-1 min-w-0 rounded-2xl border border-gray-200 bg-white p-4 shadow-sm",
    )


def _centerpiece() -> rx.Component:
    return rx.el.figure(
        rx.el.div(
            _period_compare(),
            _trend(),
            class_name="flex flex-col lg:flex-row items-stretch gap-4 w-full",
        ),
        rx.el.figcaption(
            "Illustration only: the comparison and the trend above use invented sample numbers to show how two periods and a run of months are read. They are not real results \u2014 your own figures are calculated from your uploaded rows.",
            class_name="text-xs font-medium text-gray-400 mt-3",
        ),
        class_name="w-full m-0",
    )


def _hero() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.span(
                rx.icon("trending-up", class_name="h-3.5 w-3.5"),
                "Sales growth calculator",
                class_name="flex items-center gap-1.5 w-fit rounded-full bg-indigo-50 px-3 py-1 text-xs font-semibold text-indigo-700",
            ),
            rx.el.h1(
                "Sales Growth Calculator \u2013 Analyze Your Sales Growth",
                class_name="text-3xl sm:text-4xl font-semibold tracking-tight text-gray-900 mt-4",
            ),
            rx.el.p(
                "Sales growth turns two period totals into a rate you can compare across months, "
                "products and customers. Upload a sales file, confirm which columns hold the date "
                "and the amount, and InsightSheet groups your rows into periods and calculates the "
                "change from your own data \u2014 so growth, flat performance and decline become "
                "measured rather than assumed.",
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
            rx.el.h2("The Sales Growth Formula", class_name=_H2),
            rx.el.p(
                "One expression, and one case where a percentage simply cannot be produced.",
                class_name="text-sm font-medium text-gray-500 mt-1 max-w-3xl",
            ),
            class_name="w-full",
        ),
        rx.el.div(
            rx.el.h3("The standard sales growth percentage", class_name=_H3),
            rx.el.p(
                rx.el.code(
                    "(Current period sales \u2212 Previous period sales) \u00f7 Previous period sales \u00d7 100",
                    class_name="inline-block w-fit rounded-lg border border-indigo-200 bg-white px-3 py-1.5 text-sm font-semibold text-indigo-800",
                ),
                class_name="mt-2",
            ),
            rx.el.p(
                "Read it in two moves: the subtraction gives the change as an amount, and dividing "
                "that change by the previous period converts the amount into a percentage of where "
                "you started. A negative result is a decline of the same size.",
                class_name=_BODY,
            ),
            rx.el.p(
                rx.el.span(
                    "Note on zero previous-period sales: ",
                    class_name="text-sm font-semibold text-amber-800",
                ),
                rx.el.span(
                    "when the previous period has no sales the division has no defined result, so no "
                    "meaningful growth percentage exists for that comparison. Going from 0 to any "
                    "amount is not \u201c100% growth\u201d and not \u201cinfinite growth\u201d \u2014 it is a new "
                    "period of trading with nothing comparable behind it. InsightSheet leaves the "
                    "percentage blank in those cases and shows the absolute change instead.",
                    class_name="text-sm font-medium text-amber-800",
                ),
                class_name="mt-3 rounded-xl border border-amber-200 bg-amber-50 p-3",
            ),
            rx.el.p(
                "The same caution applies to a very small previous period: a tiny base can produce a "
                "very large percentage from a modest change, which is why the currency amount is "
                "shown next to it.",
                class_name=_BODY,
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
                "The shortest path from a sales export to a growth figure you can trust.",
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
                "What people usually want to know before measuring sales growth for the first time.",
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
            rx.el.h2("Measure your sales growth now", class_name=_H2),
            rx.el.p(
                "Upload a sales export, confirm your date and revenue columns, and compare complete "
                "periods with the trend behind them. You can start on the Free plan.",
                class_name="text-sm font-medium text-gray-500 mt-1 max-w-2xl",
            ),
            rx.el.p(
                rx.el.span(
                    "Want to know who is growing? See the ",
                    class_name="text-xs font-medium text-gray-500",
                ),
                rx.el.a(
                    "RFM analysis tool",
                    href="/tools/rfm-calculator",
                    class_name="text-xs font-semibold text-blue-700 hover:underline",
                ),
                rx.el.span(
                    ". To check whether that growth is profitable, use the ",
                    class_name="text-xs font-medium text-gray-500",
                ),
                rx.el.a(
                    "profit margin calculator",
                    href="/tools/profit-margin-calculator",
                    class_name="text-xs font-semibold text-blue-700 hover:underline",
                ),
                rx.el.span(".", class_name="text-xs font-medium text-gray-500"),
                class_name="mt-3",
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
                    "Profit margin calculator",
                    href="/tools/profit-margin-calculator",
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


def sales_growth_calculator_page() -> rx.Component:
    return rx.el.div(
        # Hoisted into <head> as a real canonical tag.
        rx.el.link(rel="canonical", href=SALES_GROWTH_CANONICAL),
        _nav(),
        rx.el.main(
            _hero(),
            _section(
                "What Sales Growth Means",
                "A comparison between two periods, expressed as a rate so periods of different size can be read together.",
                _WHAT_IT_IS,
                "grid grid-cols-1 md:grid-cols-2 gap-4 w-full",
            ),
            _section(
                "How Businesses Measure Sales Growth",
                "Several standard bases, each answering a slightly different question.",
                _HOW_MEASURED,
                "grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 w-full",
            ),
            _section(
                "Comparing Two Sales Periods",
                "Most misleading growth figures come from an unfair comparison rather than a wrong calculation.",
                _COMPARING,
                "grid grid-cols-1 md:grid-cols-2 gap-4 w-full",
            ),
            _formula(),
            _section(
                "Why Revenue and Sales Trends Matter",
                "A percentage tells you what changed; the trend around it tells you whether it matters.",
                _WHY_TRENDS,
                "grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 w-full",
            ),
            _section(
                "Reading Growth, Flat Performance, Decline and Seasonality",
                "Patterns worth recognising \u2014 each one is a prompt to look closer, not a conclusion on its own.",
                _PATTERNS,
                "grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 w-full",
            ),
            _section(
                "How InsightSheet Analyses Sales Growth",
                "Your uploaded sales data drives every period total \u2014 nothing is assumed or imported from elsewhere.",
                _HOW_INSIGHTSHEET,
                "grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 w-full",
            ),
            _section(
                "Who Benefits From Growth Analysis",
                "Anyone who records dated sales and needs to know which way they are moving.",
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
