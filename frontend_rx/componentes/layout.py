"""
Componente Layout

Define la estructura y disposición general de la interfaz del marketplace.
"""
import reflex as rx
from frontend_rx.estados.auth import AuthState

def navbar():
    """Componente de navegación superior."""
    return rx.hstack(
        rx.link(
            rx.heading("🚗 AutoMercado", size="6"),
            href="/",
            text_decoration="none",
            color="inherit"
        ),
        rx.spacer(),
        rx.hstack(
            rx.link("Inicio", href="/", padding="2"),
            rx.link("Listado", href="/listado", padding="2"),
            rx.cond(
                AuthState.is_logged_in,
                rx.hstack(
                    rx.text(f"Hola, {AuthState.username}"),
                    rx.button("Cerrar Sesión", on_click=AuthState.logout, variant="outline"),
                    spacing="2"
                ),
                rx.hstack(
                    rx.link("Login", href="/login", padding="2"),
                    rx.link("Registro", href="/registro", padding="2"),
                    spacing="2"
                )
            ),
            spacing="4"
        ),
        justify="between",
        align="center",
        padding="4",
        border_bottom="1px solid #e2e8f0",
        width="100%"
    )

def footer():
    """Componente de pie de página."""
    return rx.center(
        rx.text("(c) 2024 AutoMercado - Marketplace de Vehículos", 
                color="gray", 
                size="2"),
        padding="4",
        border_top="1px solid #e2e8f0",
        width="100%"
    )

def layout(content):
    """Layout principal que envuelve el contenido de las páginas."""
    return rx.vstack(
        navbar(),
        rx.container(
            content,
            max_width="1200px",
            padding="4",
            min_height="calc(100vh - 120px)"
        ),
        footer(),
        spacing="0",
        min_height="100vh",
        width="100%"
    )