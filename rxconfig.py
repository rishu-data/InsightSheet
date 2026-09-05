import reflex as rx

config = rx.Config(
    app_name="app",
    show_reflex_badge=False,
    plugins=[rx.plugins.TailwindV4Plugin()],
    # The custom public-only /sitemap.xml endpoint is served by the app itself,
    # so Reflex's default sitemap generator is explicitly disabled.
    disable_plugins=[rx.plugins.SitemapPlugin],
)
