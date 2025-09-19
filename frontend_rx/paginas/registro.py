"""
Página Registro

Implementa la página de registro para nuevos usuarios del marketplace.
"""
import reflex as rx
from frontend_rx.estados.auth import AuthState
from frontend_rx.componentes.layout import layout

def registro_page():
    """Página de registro de nuevos usuarios."""
    return layout(
        rx.center(
            rx.card(
                rx.vstack(
                    rx.heading("Crear Cuenta", size="6", text_align="center"),
                    rx.text("Únete a AutoMercado y encuentra tu vehículo ideal", 
                           color="gray", 
                           text_align="center"),
                    
                    rx.vstack(
                        rx.input(
                            placeholder="Nombre completo",
                            value=AuthState.register_name,
                            on_change=AuthState.set_register_name,
                            width="100%"
                        ),
                        rx.input(
                            placeholder="Email",
                            type="email",
                            value=AuthState.register_email,
                            on_change=AuthState.set_register_email,
                            width="100%"
                        ),
                        rx.input(
                            placeholder="Contraseña",
                            type="password",
                            value=AuthState.register_password,
                            on_change=AuthState.set_register_password,
                            width="100%"
                        ),
                        spacing="3",
                        width="100%"
                    ),
                    
                    rx.button(
                        "Crear Cuenta",
                        on_click=AuthState.register,
                        width="100%",
                        size="3"
                    ),
                    
                    rx.divider(),
                    
                    rx.hstack(
                        rx.text("¿Ya tienes cuenta?"),
                        rx.link("Inicia sesión aquí", href="/login", color="blue"),
                        justify="center"
                    ),
                    
                    spacing="4",
                    width="100%"
                ),
                max_width="400px",
                padding="6"
            ),
            min_height="60vh"
        )
    )
