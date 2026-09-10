"""Public SEO landing page for sales forecasting.

Stateless and dependency-free: it imports no auth, upload, dashboard,
forecasting, analytics, database or subscription state, so the route renders
as static semantic HTML with no backend work.
"""

import reflex as rx

SALES_FORECASTING_TITLE = (
    "Sales Forecasting Tool \u2013 Forecast Future Sales | InsightSheet"
)
SALES_FORECASTING_DESCRIPTION = (
    "Forecast future sales using your business data with InsightSheet. "
    "Analyze historical sales trends, identify patterns and plan for future "
    "revenue."
)
SALES_FORECASTING_CANONICAL = "https://reflex-build-generation-silver-apple.reflex.run/tools/sales-forecasting"

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
        "It extends what already happened",
        "A sales forecast is an estimate of future sales built from recorded past sales. It does not create new information \u2014 it summarises the direction and shape of your history and projects that shape forward.",
    ),
    (
        "calendar-range",
        "It always belongs to a period",
        "A forecast is only meaningful with a horizon attached: next month, next quarter, the rest of the year. The shorter and nearer the horizon, the less room there is for conditions to change.",
    ),
    (
        "circle-alert",
        "It is an estimate, not a guarantee",
        "No forecast can know a future price change, a lost account, a supply delay or a change in demand. Treat every projected figure as a planning assumption to be revised, never as a committed outcome.",
    ),
    (
        "layers",
        "It can be read at several levels",
        "The same method applies to the whole business, one product line, one channel or one region. Lower levels have fewer rows behind them, so their estimates are usually less stable.",
    ),
]

_WHY_FORECAST: list[tuple[str, str, str]] = [
    (
        "target",
        "To plan instead of react",
        "A rough expectation for next quarter turns decisions about stock, staffing and spend into choices made in advance rather than corrections made afterwards.",
    ),
    (
        "wallet",
        "To see cash timing, not just totals",
        "Knowing roughly when revenue is expected matters as much as how much. Timing is what determines whether a payment run or a purchase order is comfortable.",
    ),
    (
        "package",
        "To avoid stockouts and overstock",
        "Expected demand per product informs how much to order and when, which is the difference between missed sales and capital sitting on a shelf.",
    ),
    (
        "users",
        "To set targets people can discuss",
        "A target grounded in measured history is easier to agree on, and easier to challenge, than one produced from optimism.",
    ),
    (
        "search",
        "To notice when reality diverges",
        "The value of writing an expectation down is that you can compare it with what actually happened, and investigate the gap.",
    ),
    (
        "scale",
        "To size risk honestly",
        "Comparing an optimistic and a cautious version of the same forecast shows how much of the plan depends on the assumption holding.",
    ),
]

_WHAT_HISTORY_SHOWS: list[tuple[str, str, str]] = [
    (
        "trending-up",
        "Trend \u2014 the underlying direction",
        "Across several consecutive periods, sales usually show a broad direction: rising, flat or falling. Trend is the part of a forecast that carries the most weight, and it needs enough periods to be visible at all.",
    ),
    (
        "calendar-check",
        "Seasonality \u2014 repeating annual shape",
        "Many businesses repeat the same peaks and troughs each year. Seasonality can only be separated from a real change when you have more than one year of comparable history.",
    ),
    (
        "repeat",
        "Recurring patterns \u2014 shorter cycles",
        "Weekday and weekend behaviour, month-end ordering, payday effects or campaign cadence repeat at shorter intervals and shape how a period fills up.",
    ),
    (
        "circle-alert",
        "Anomalies \u2014 one-off distortions",
        "A single unusually large order, a duplicated import, a promotion or an outage produces a spike or dip that is not part of the pattern. Left in, it pulls an estimate with it, so anomalies are worth identifying before projecting anything.",
    ),
    (
        "brush-cleaning",
        "Data gaps \u2014 what history is missing",
        "Missing weeks, inconsistent date formats and rows without amounts weaken a projection quietly. Knowing where the history is thin is part of knowing how much to trust the estimate.",
    ),
    (
        "info",
        "What history cannot show",
        "Past rows contain no knowledge of a future launch, a new competitor or a change in your own pricing. This is precisely why a forecast is an estimate rather than a guarantee, and why it should be revisited as conditions change.",
    ),
]

_PLANNING: list[tuple[str, str, str]] = [
    (
        "package",
        "Inventory and purchasing",
        "Expected demand per product and per period informs order quantities, reorder timing and safety stock, especially where lead times are long.",
    ),
    (
        "chart-line",
        "Revenue planning",
        "A projected revenue range gives budgets and targets a starting point that can be traced back to actual sales rather than to a round number.",
    ),
    (
        "wallet",
        "Cash-flow planning",
        "Placing expected revenue on a calendar next to known outgoings shows which weeks are likely to be tight, while there is still time to act.",
    ),
    (
        "users",
        "Capacity and staffing",
        "Anticipated busy and quiet periods inform shifts, hiring and support cover, which are hard to change at short notice.",
    ),
    (
        "megaphone",
        "Marketing and promotion timing",
        "Knowing the expected shape of a season helps decide whether to reinforce a peak or lift a predictable trough.",
    ),
    (
        "scale",
        "Scenario comparison",
        "Planning against a cautious and an optimistic version of the same estimate is usually more useful than committing to one number.",
    ),
]

_HOW_INSIGHTSHEET: list[tuple[str, str, str]] = [
    (
        "cloud-upload",
        "You upload historical sales data",
        "An Excel or CSV export of past orders is enough. Header detection, date standardisation, duplicate removal and currency stripping run automatically and are logged in plain English.",
    ),
    (
        "columns-3",
        "You confirm the date and revenue columns",
        "A forecast needs a usable date and an amount. You review the suggested mapping, so every period total behind the estimate is built from the fields you intended.",
    ),
    (
        "calendar",
        "Your rows are grouped into periods",
        "Cleaned dates are grouped into months so the history the projection reads is your own recorded sales, not an assumption.",
    ),
    (
        "trending-up",
        "Trend and pattern are described first",
        "Direction, repeated shape and unusual periods are surfaced from your own history before any figure is projected forward, so you can see what the estimate rests on.",
    ),
    (
        "circle-alert",
        "Estimates are presented as estimates",
        "Projected values are labelled as projections, kept to short horizons, and never presented as certainties. Where history is too short, sparse or irregular to support a projection, that is stated instead of a number being invented.",
    ),
    (
        "file-down",
        "Findings and exports",
        "Written observations point at specific periods and products, and the view you are reading can be exported as a PDF or Excel report to plan against.",
    ),
]

_AUDIENCE: list[tuple[str, str, str]] = [
    (
        "shopping-cart",
        "Ecommerce and retail",
        "Anticipate seasonal demand per product so purchasing decisions are made before the season rather than during it.",
    ),
    (
        "briefcase",
        "Small business owners",
        "Get a grounded expectation for the coming months without building a forecasting spreadsheet from scratch.",
    ),
    (
        "handshake",
        "Sales teams",
        "Sanity-check pipeline expectations against what the recorded sales history actually supports.",
    ),
    (
        "calculator",
        "Finance and operations",
        "Line expected revenue up against known costs and commitments for cash-flow and budget planning.",
    ),
    (
        "package",
        "Inventory and supply planners",
        "Translate expected demand and lead times into order timing and quantities.",
    ),
    (
        "graduation-cap",
        "Analysts, consultants and students",
        "Profile a sales history quickly, and see clearly which parts of a projection are measured and which are assumed.",
    ),
]

_STEPS: list[tuple[str, str, str]] = [
    (
        "cloud-upload",
        "Step 1 \u2014 Upload your historical sales data",
        "Choose an Excel or CSV export containing order dates and amounts. Cleaning runs automatically and every change is logged.",
    ),
    (
        "columns-3",
        "Step 2 \u2014 Confirm your date and revenue columns",
        "Map the date, amount, product and customer fields so each period total behind the estimate comes from the values you meant.",
    ),
    (
        "chart-line",
        "Step 3 \u2014 Review trends and forecast estimates",
        "Read the trend, seasonality and anomalies in your history, then use the projected periods as planning estimates and revise them as new data arrives.",
    ),
]

_FAQ: list[tuple[str, str]] = [
    (
        "What is sales forecasting?",
        "Sales forecasting is estimating future sales from recorded past sales. It reads the trend, repeating seasonal shape and recurring patterns in your dated history and projects that shape over a defined horizon. The result is a planning estimate, not a prediction that is guaranteed to occur.",
    ),
    (
        "How do I forecast sales from historical data?",
        "Start with dated sales rows and one consistent revenue field. Group them into equal periods such as months, remove duplicates and obvious anomalies, and look at the direction across several consecutive periods. Where you have more than a year of history, compare the same season year over year to separate seasonality from a real change, then extend the observed pattern over a short horizon and state the assumptions you made.",
    ),
    (
        "Is a sales forecast accurate?",
        "A forecast is an estimate, and its usefulness depends on how much clean, comparable history sits behind it and how stable your conditions are. Short horizons on long, regular histories tend to be more dependable; long horizons, sparse data or a business in flux much less so. We do not publish accuracy figures, because no honest single number describes accuracy across different datasets \u2014 and no forecast can account for events that have not happened yet.",
    ),
    (
        "How much sales history do I need to forecast?",
        "The more complete periods you have, the more there is to read. A few months can show direction; separating seasonality from an underlying change realistically needs more than one year of comparable history. With very little or very irregular data, the sensible output is a description of the trend rather than a projected figure, which is what InsightSheet reports in that case.",
    ),
    (
        "How can forecasting help with inventory and cash-flow planning?",
        "It puts expected demand and expected revenue on a calendar. For inventory, expected demand per product and per period informs order quantities and reorder timing against your lead times. For cash flow, expected revenue placed next to known outgoings shows which weeks are likely to be tight while there is still time to adjust. In both cases the estimate is a starting point for planning that should be revised as actual sales come in.",
    ),
]

_TIMELINE: list[tuple[str, str, str, str, str]] = [
    ("Feb", "h-10", "Historical", "bg-blue-300 border border-blue-400", ""),
    ("Mar", "h-12", "Historical", "bg-blue-400 border border-blue-500", ""),
    ("Apr", "h-11", "Historical", "bg-blue-400 border border-blue-500", ""),
    ("May", "h-16", "Historical", "bg-blue-500 border border-blue-600", ""),
    ("Jun", "h-20", "Historical", "bg-blue-600 border border-blue-700", ""),
    (
        "Jul",
        "h-24",
        "Forecast estimate",
        "bg-amber-50 border-2 border-dashed border-amber-400",
        "estimate",
    ),
    (
        "Aug",
        "h-28",
        "Forecast estimate",
        "bg-amber-50 border-2 border-dashed border-amber-400",
        "estimate",
    ),
]

_PLAN_ROWS: list[tuple[str, str, str, str]] = [
    (
        "Jun \u2014 recorded",
        "Historical observation",
        "\u20b94,60,000",
        "historical",
    ),
    (
        "Jul \u2014 projected",
        "Forecast estimate",
        "\u20b94,90,000 \u2013 \u20b95,40,000",
        "estimate",
    ),
    (
        "Aug \u2014 projected",
        "Forecast estimate",
        "\u20b95,10,000 \u2013 \u20b95,80,000",
        "estimate",
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


def _timeline_bar(item: tuple[str, str, str, str, str]) -> rx.Component:
    return rx.el.li(
        rx.el.div(
            rx.el.div(
                class_name=f"w-full rounded-t-md {item[3]} {item[1]}",
                aria_hidden="true",
            ),
            class_name="flex h-28 w-full items-end",
        ),
        rx.el.span(
            item[0],
            class_name="block text-[10px] font-medium text-gray-500 mt-1 text-center",
        ),
        rx.el.span(
            item[2],
            class_name="sr-only",
        ),
        class_name="flex-1 min-w-0 list-none",
    )


def _timeline() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("chart-line", class_name="h-3.5 w-3.5 text-indigo-600"),
            rx.el.span(
                "Historical months, then forecast months",
                class_name="text-xs font-semibold text-gray-900",
            ),
            class_name="flex items-center gap-2",
        ),
        rx.el.p(
            "Illustrative only \u2014 every height below is an invented sample value used to show shape. These are not real results.",
            class_name="text-[11px] font-medium text-gray-400 mt-1",
        ),
        rx.el.ul(
            *[_timeline_bar(item) for item in _TIMELINE],
            class_name="flex items-end gap-1.5 sm:gap-2 mt-3 p-0 m-0",
        ),
        rx.el.div(
            rx.el.span(
                rx.el.span(
                    class_name="h-2.5 w-2.5 rounded-sm bg-blue-600 shrink-0",
                    aria_hidden="true",
                ),
                "Solid = historical observation",
                class_name="flex items-center gap-1.5 text-[11px] font-medium text-gray-600",
            ),
            rx.el.span(
                rx.el.span(
                    class_name="h-2.5 w-2.5 rounded-sm bg-amber-50 border-2 border-dashed border-amber-400 shrink-0",
                    aria_hidden="true",
                ),
                "Dashed = forecast estimate",
                class_name="flex items-center gap-1.5 text-[11px] font-medium text-amber-800",
            ),
            class_name="flex flex-wrap items-center gap-x-4 gap-y-1 mt-3",
        ),
        class_name="w-full lg:flex-1 min-w-0 rounded-2xl border border-gray-200 bg-white p-4 shadow-sm",
    )


def _plan_row(item: tuple[str, str, str, str]) -> rx.Component:
    return rx.el.li(
        rx.el.div(
            rx.el.span(
                item[0],
                class_name="text-[11px] font-semibold text-gray-900 truncate",
            ),
            rx.el.span(
                item[1],
                class_name=rx.cond(
                    item[3] == "estimate",
                    "text-[10px] font-semibold text-amber-800 shrink-0",
                    "text-[10px] font-semibold text-blue-700 shrink-0",
                ),
            ),
            class_name="flex items-center justify-between gap-2",
        ),
        rx.el.span(
            item[2],
            class_name="block text-[11px] font-medium text-gray-600 mt-0.5",
        ),
        class_name=rx.cond(
            item[3] == "estimate",
            "list-none rounded-xl border-2 border-dashed border-amber-400 bg-amber-50 p-2.5",
            "list-none rounded-xl border border-blue-200 bg-blue-50 p-2.5",
        ),
    )


def _plan_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("calendar-range", class_name="h-3.5 w-3.5 text-blue-600"),
            rx.el.span(
                "Planning view",
                class_name="text-xs font-semibold text-gray-900",
            ),
            class_name="flex items-center gap-2",
        ),
        rx.el.p(
            "Illustrative only \u2014 invented sample figures, not measured or predicted revenue.",
            class_name="text-[11px] font-medium text-gray-400 mt-1",
        ),
        rx.el.ul(
            *[_plan_row(item) for item in _PLAN_ROWS],
            class_name="flex flex-col gap-2 mt-3 p-0 m-0",
        ),
        rx.el.p(
            "Projected periods are shown as ranges to make the uncertainty visible. A forecast is an estimate, never a guarantee.",
            class_name="text-[11px] font-medium text-gray-500 mt-3",
        ),
        class_name="w-full lg:flex-1 min-w-0 rounded-2xl border border-gray-200 bg-white p-4 shadow-sm",
    )


def _centerpiece() -> rx.Component:
    return rx.el.figure(
        rx.el.div(
            _timeline(),
            _plan_view(),
            class_name="flex flex-col lg:flex-row items-stretch gap-4 w-full",
        ),
        rx.el.figcaption(
            "Illustration only: the timeline and planning view above use invented sample numbers to show how recorded months and projected months are distinguished. They are not real results and not a prediction \u2014 your own history and estimates are built from your uploaded rows.",
            class_name="text-xs font-medium text-gray-400 mt-3",
        ),
        class_name="w-full m-0",
    )


def _hero() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.span(
                rx.icon("chart-line", class_name="h-3.5 w-3.5"),
                "Sales forecasting tool",
                class_name="flex items-center gap-1.5 w-fit rounded-full bg-indigo-50 px-3 py-1 text-xs font-semibold text-indigo-700",
            ),
            rx.el.h1(
                "Sales Forecasting Tool \u2013 Predict Future Sales",
                class_name="text-3xl sm:text-4xl font-semibold tracking-tight text-gray-900 mt-4",
            ),
            rx.el.p(
                "Forecasting starts with history. Upload a file of past dated sales, confirm which "
                "columns hold the date and the amount, and InsightSheet groups your rows into "
                "periods and describes the trend, seasonality and unusual periods it finds \u2014 then "
                "presents short-horizon projections as clearly labelled estimates you can plan "
                "against and revise, not as guaranteed outcomes.",
                class_name="text-base font-medium text-gray-500 mt-4 max-w-2xl",
            ),
            rx.el.div(
                rx.el.a(
                    "Forecast My Sales",
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
                rx.el.span(
                    ", or see how a whole file is analysed with the ",
                    class_name=_INLINE_TEXT,
                ),
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
        rx.el.div(*[_card(item) for item in items], class_name=grid),
        id=section_id,
        class_name="flex flex-col gap-4 w-full",
    )


def _estimates_note() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.h2("Forecasts Are Estimates, Not Guarantees", class_name=_H2),
            rx.el.p(
                "The single most important thing to hold in mind when reading any projected figure.",
                class_name="text-sm font-medium text-gray-500 mt-1 max-w-3xl",
            ),
            class_name="w-full",
        ),
        rx.el.div(
            rx.el.p(
                rx.el.span(
                    "What a projection can and cannot do: ",
                    class_name="text-sm font-semibold text-amber-800",
                ),
                rx.el.span(
                    "a projection extends measured patterns from your own recorded rows. It cannot "
                    "know about a future price change, a new competitor, a supply delay, a lost or "
                    "won account, or a shift in demand \u2014 none of those events exist in your "
                    "history yet. That is why InsightSheet labels projected periods as estimates, "
                    "keeps horizons short, shows ranges rather than single certainties, and says so "
                    "plainly when your history is too short or too irregular to support a projection "
                    "at all.",
                    class_name="text-sm font-medium text-amber-800",
                ),
                class_name="rounded-xl border border-amber-200 bg-amber-50 p-3",
            ),
            rx.el.p(
                "Used well, an estimate is a planning assumption you write down, compare against "
                "actual sales as they arrive, and revise. Used badly, it becomes a promise nobody "
                "made. We publish no accuracy claims, because accuracy depends entirely on your "
                "data and your conditions.",
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
                "The shortest path from a historical sales export to forecast estimates you can plan with.",
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
                "What people usually want to know before forecasting sales for the first time.",
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
            rx.el.h2("Turn your sales history into a plan", class_name=_H2),
            rx.el.p(
                "Upload a historical sales export, confirm your date and revenue columns, and read "
                "the trend and clearly labelled estimates behind it. You can start on the Free plan.",
                class_name="text-sm font-medium text-gray-500 mt-1 max-w-2xl",
            ),
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
                    ". To see which customers are likely to keep buying, see the ",
                    class_name=_INLINE_TEXT,
                ),
                rx.el.a(
                    "RFM analysis tool",
                    href="/tools/rfm-calculator",
                    class_name=_INLINE_LINK,
                ),
                rx.el.span(
                    ", and to check whether expected revenue is profitable, use the ",
                    class_name=_INLINE_TEXT,
                ),
                rx.el.a(
                    "profit margin calculator",
                    href="/tools/profit-margin-calculator",
                    class_name=_INLINE_LINK,
                ),
                rx.el.span(".", class_name=_INLINE_TEXT),
                class_name="mt-3",
            ),
            class_name="min-w-0 flex-1",
        ),
        rx.el.div(
            rx.el.a(
                "Forecast My Sales",
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
                    "Sales growth calculator",
                    href="/tools/sales-growth-calculator",
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


def sales_forecasting_page() -> rx.Component:
    return rx.el.div(
        # Hoisted into <head> as a real canonical tag.
        rx.el.link(rel="canonical", href=SALES_FORECASTING_CANONICAL),
        _nav(),
        rx.el.main(
            _hero(),
            _section(
                "What Sales Forecasting Means",
                "An estimate of future sales derived from recorded past sales, always tied to a period and always open to revision.",
                _WHAT_IT_IS,
                "grid grid-cols-1 md:grid-cols-2 gap-4 w-full",
            ),
            _section(
                "Why Businesses Forecast Sales",
                "Forecasting is less about knowing the future than about making decisions early enough to matter.",
                _WHY_FORECAST,
                "grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 w-full",
            ),
            _section(
                "What Historical Sales Data Reveals",
                "Trend, seasonality, recurring patterns and anomalies are what a projection is built from \u2014 and what limits it.",
                _WHAT_HISTORY_SHOWS,
                "grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 w-full",
            ),
            _estimates_note(),
            _section(
                "How Forecasting Supports Planning",
                "Inventory, revenue, cash flow and capacity decisions all need an expectation to work against.",
                _PLANNING,
                "grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 w-full",
            ),
            _section(
                "How InsightSheet Uses Your Historical Sales Data",
                "Your uploaded rows drive every period total and every observation \u2014 nothing is assumed or imported from elsewhere.",
                _HOW_INSIGHTSHEET,
                "grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 w-full",
            ),
            _section(
                "Who Benefits From Sales Forecasting",
                "Anyone who records dated sales and has to commit to stock, spend or staffing before the period arrives.",
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
