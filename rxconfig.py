# rxconfig.py (actualizado)
import reflex as rx

config = rx.Config(
    app_name="main",  # ← Cambiar a "main" porque tu app está en main.py
    db_url="sqlite:///reflex.db",
    env=rx.Env.DEV,
    disable_plugins=['reflex.plugins.sitemap.SitemapPlugin'],  # Silenciar warning
)