import reflex as rx

from app.components.legal import (
    SUPPORT_EMAIL,
    bullet,
    bullet_card,
    legal_card,
    legal_grid,
    legal_intro,
    related_policies,
    review_notice,
)
from app.components.sidebar import page_shell


def _body(*sections: rx.Component) -> rx.Component:
    return rx.el.div(
        *sections,
        review_notice(),
        related_policies(),
        class_name="flex flex-col gap-6 w-full",
    )


def privacy_page() -> rx.Component:
    return page_shell(
        "legal",
        "Privacy Policy",
        "What data InsightSheet holds, why it is held and how long it stays",
        _body(
            legal_intro(
                "shield",
                "Privacy Policy",
                "InsightSheet is a spreadsheet analytics tool. We collect the minimum needed to run "
                "your account, process the file you upload and manage your plan. We do not sell your "
                "data and we do not use your spreadsheet contents to advertise to you.",
            ),
            legal_grid(
                legal_card(
                    "user",
                    "Account data",
                    "When you create an account we store your email address, an optional display name and "
                    "your password as an irreversible hash — never in plain text. This is used to sign you "
                    "in, keep your work tied to you and contact you about your account.",
                ),
                legal_card(
                    "sheet",
                    "Spreadsheet processing",
                    "CSV/XLS/XLSX files are uploaded to this server, cleaned and analysed to produce your "
                    "dashboard. Figures are computed from your cleaned rows. Files are processed for your "
                    "session and are not shared with third parties or used to train models.",
                ),
                legal_card(
                    "message-square-heart",
                    "Feedback storage",
                    "Feedback you submit — rating, message and, if you are signed in, the account it came "
                    "from — is stored so we can review it and improve the product. Please do not include "
                    "confidential business figures or personal data in feedback messages.",
                ),
                legal_card(
                    "credit-card",
                    "Subscription and payment data",
                    "Card details are never collected or stored by InsightSheet. Payments are handled by our "
                    "payment provider, which returns only a subscription reference and status that we store "
                    "against your account to unlock Pro features.",
                ),
                legal_card(
                    "activity",
                    "Technical logs",
                    "Standard server logs (timestamps, request paths, error traces) are kept for security "
                    "and debugging. They may include your IP address and are retained only as long as they "
                    "are useful for operating the service.",
                ),
                legal_card(
                    "user-x",
                    "Your choices",
                    f"You can request a copy of your account data, correction of it, or deletion of your "
                    f"account and stored feedback by writing to {SUPPORT_EMAIL}. Deleting your account "
                    "removes Pro access tied to it.",
                ),
            ),
            bullet_card(
                "list-checks",
                "How we handle your data in practice",
                bullet(
                    "We keep only what a feature actually needs — no hidden profiling of your spreadsheet contents."
                ),
                bullet(
                    "Passwords are hashed, and sessions are used only to keep you signed in."
                ),
                bullet(
                    "Third parties are limited to the infrastructure and payment providers required to run the service."
                ),
                bullet(
                    "We will tell registered users about material changes to this policy on this page."
                ),
                bullet(
                    "Data-protection obligations vary by country; the specific legal bases, retention periods and cross-border transfer terms that apply to you should be confirmed by a qualified professional."
                ),
            ),
        ),
    )


def terms_page() -> rx.Component:
    return page_shell(
        "legal",
        "Terms of Service",
        "The basic rules for using InsightSheet",
        _body(
            legal_intro(
                "file-text",
                "Terms of Service",
                "By creating an account or uploading a file you agree to use InsightSheet as described "
                "here. These terms are intentionally short and general — they describe how the product "
                "is meant to be used rather than attempting to cover every legal scenario.",
            ),
            legal_grid(
                legal_card(
                    "user-check",
                    "Your account",
                    "You are responsible for keeping your password safe and for activity under your account. "
                    "Use a real email address so we can reach you about access, billing or security matters.",
                ),
                legal_card(
                    "upload",
                    "Your content",
                    "You keep ownership of the spreadsheets you upload. You confirm you have the right to "
                    "upload them and that doing so does not breach anyone else's confidentiality, privacy or "
                    "contractual rights.",
                ),
                legal_card(
                    "ban",
                    "Acceptable use",
                    "Do not attempt to break, overload or reverse-engineer the service, upload malicious "
                    "files, or use it for unlawful purposes. We may suspend accounts that do.",
                ),
                legal_card(
                    "calculator",
                    "Results are analytical, not advice",
                    "Dashboards, forecasts, segments and AI-generated insights are calculated from the data "
                    "you provide. They are decision support, not financial, tax, legal or investment advice, "
                    "and should be sanity-checked before you act on them.",
                ),
                legal_card(
                    "server",
                    "Availability",
                    "We aim to keep InsightSheet available and accurate, but the service is provided on an "
                    "as-is basis and may be interrupted for maintenance, upgrades or reasons outside our control.",
                ),
                legal_card(
                    "refresh-cw",
                    "Changes and termination",
                    "Features may be added, changed or removed as the product develops. You may stop using "
                    "the service at any time; we may end access where these terms are broken.",
                ),
            ),
            bullet_card(
                "info",
                "Points to confirm with a professional",
                bullet(
                    "Limitation of liability, indemnity and warranty wording differs by jurisdiction and is not attempted in detail here."
                ),
                bullet(
                    "Governing law, dispute resolution and consumer-protection carve-outs must be set for your specific market."
                ),
                bullet(
                    "If you process personal data of others through InsightSheet, a data-processing agreement may be required."
                ),
            ),
        ),
    )


def refund_page() -> rx.Component:
    return page_shell(
        "legal",
        "Refund & Cancellation Policy",
        "How cancellations and refund requests are handled",
        _body(
            legal_intro(
                "receipt",
                "Refund & Cancellation Policy",
                "The Free plan needs no cancellation. For the paid Pro subscription, this page explains "
                "how to cancel, what happens to your access afterwards and how refund requests are "
                "reviewed. Prices and plan contents are shown on the Pricing page and are unchanged by "
                "this policy.",
            ),
            legal_grid(
                legal_card(
                    "circle-x",
                    "Cancelling a subscription",
                    f"You can cancel at any time by writing to {SUPPORT_EMAIL} from your account email. "
                    "Cancellation stops future renewals — it is not a request for a refund of the period "
                    "already paid unless you ask for one.",
                ),
                legal_card(
                    "clock",
                    "Access after cancelling",
                    "Pro features remain available until the end of the billing period you have already "
                    "paid for. After that your account reverts to the Free plan; your account, cleaned "
                    "uploads and feedback are not deleted by cancelling.",
                ),
                legal_card(
                    "rotate-ccw",
                    "Refund requests",
                    "Tell us your account email, the payment reference and what went wrong. We review "
                    "requests individually and prioritise cases where you were charged twice, charged after "
                    "cancelling, or could not use Pro because of a fault on our side.",
                ),
                legal_card(
                    "credit-card",
                    "How refunds are paid",
                    "Approved refunds are returned through the original payment method by our payment "
                    "provider. The time for the money to appear depends on your bank or card issuer, not "
                    "on InsightSheet.",
                ),
                legal_card(
                    "circle-slash",
                    "What is normally not refunded",
                    "Periods you actively used, and charges you dispute long after the fact, are normally "
                    "not refunded. Where a mandatory consumer right applies in your country, that right "
                    "takes precedence over this page.",
                ),
                legal_card(
                    "mail",
                    "Response expectations",
                    "We aim to acknowledge cancellation and refund emails within 2 business days and to "
                    "reach a decision within 7 business days, keeping you updated if a provider is involved.",
                ),
            ),
            bullet_card(
                "scale",
                "Please have this reviewed before relying on it commercially",
                bullet(
                    "Statutory cooling-off and cancellation rights vary by country and may override these timelines."
                ),
                bullet(
                    "Your payment provider's own chargeback and refund rules also apply to every transaction."
                ),
                bullet(
                    "Tax treatment of refunds should be confirmed with a qualified accountant."
                ),
            ),
        ),
    )


def payment_terms_page() -> rx.Component:
    return page_shell(
        "legal",
        "Payment & Subscription Terms",
        "How billing, renewals and Pro activation work",
        _body(
            legal_intro(
                "credit-card",
                "Payment & Subscription Terms",
                "InsightSheet offers a Free plan and a paid Pro subscription. Checkout is handled on a "
                "secure external payment page — InsightSheet never sees or stores your card details.",
            ),
            legal_grid(
                legal_card(
                    "lock",
                    "Who processes your payment",
                    "Payments are collected by our third-party payment provider under its own terms. We "
                    "receive only a subscription identifier and status, which we store against your account.",
                ),
                legal_card(
                    "user-check",
                    "Pro activation",
                    "Pro unlocks against the signed-in account that completed checkout. Sign in with the "
                    "same account before paying, and use the Refresh status button on the Pricing page if "
                    "activation has not appeared yet.",
                ),
                legal_card(
                    "repeat",
                    "Billing cycle and renewals",
                    "The Pro plan is billed on a recurring monthly cycle and renews automatically until "
                    "cancelled. The amount and currency shown at checkout is what is charged.",
                ),
                legal_card(
                    "circle-alert",
                    "Failed payments",
                    "If a renewal payment fails, Pro features may be paused until payment succeeds. Your "
                    "account and data remain intact while this is resolved.",
                ),
                legal_card(
                    "percent",
                    "Taxes and fees",
                    "Prices are shown as charged at checkout. Any taxes, bank charges or currency-conversion "
                    "fees applied by your card issuer are outside our control.",
                ),
                legal_card(
                    "tag",
                    "Price changes",
                    "Existing subscribers are told in advance of any change to the subscription price, and "
                    "can cancel before the new price takes effect. Current pricing always lives on the "
                    "Pricing page.",
                ),
            ),
            bullet_card(
                "list-checks",
                "Good to know",
                bullet(
                    "Cancelling and refunds are covered on the Refund & Cancellation Policy page."
                ),
                bullet(
                    "Keep the confirmation email from the payment provider — its reference makes support requests much faster."
                ),
                bullet(
                    "Invoicing, tax registration and payment-regulation obligations depend on where you and your business are based and should be confirmed by a qualified professional."
                ),
            ),
        ),
    )


def support_page() -> rx.Component:
    return page_shell(
        "legal",
        "Contact / Support",
        "How to reach us and what to expect",
        _body(
            legal_intro(
                "life-buoy",
                "Contact / Support",
                "Support is handled over email by a small team. Clear details in your first message "
                "usually mean we can fix things in one reply.",
            ),
            legal_grid(
                legal_card(
                    "mail",
                    "General support",
                    f"Write to {SUPPORT_EMAIL} for questions about uploads, cleaning, mapping or the "
                    "dashboard. Include the page you were on and what you expected to see.",
                ),
                legal_card(
                    "credit-card",
                    "Billing and subscriptions",
                    f"For payment, activation, cancellation or refund questions, email {SUPPORT_EMAIL} "
                    "from your account email address and include the payment reference from your "
                    "provider's confirmation.",
                ),
                legal_card(
                    "shield",
                    "Privacy and data requests",
                    f"Access, correction and deletion requests also go to {SUPPORT_EMAIL}. We confirm "
                    "you own the account before acting on a data request.",
                ),
                legal_card(
                    "clock",
                    "Response expectations",
                    "We aim to reply within 2 business days, Monday to Friday. There is no phone or live "
                    "chat channel, and we do not offer a guaranteed uptime or response SLA on the Free plan.",
                ),
                legal_card(
                    "message-square-heart",
                    "Feature ideas and feedback",
                    "Product suggestions are best sent through the in-app Feedback page so they are stored "
                    "with your rating and reviewed together with everyone else's.",
                ),
                legal_card(
                    "lock",
                    "Please don't email us your data",
                    "Do not attach spreadsheets containing personal or confidential business data to support "
                    "emails. Describe the column names and the problem instead, and we will guide you.",
                ),
            ),
            bullet_card(
                "list-checks",
                "What to include in a support email",
                bullet(
                    "Your account email address and whether you are on the Free or Pro plan."
                ),
                bullet(
                    "The page or step where the problem happened, and the exact message shown."
                ),
                bullet(
                    "Roughly how many rows and which columns your file has — not the file itself."
                ),
                bullet(
                    "For billing issues, the payment reference and the date of the charge."
                ),
            ),
        ),
    )
