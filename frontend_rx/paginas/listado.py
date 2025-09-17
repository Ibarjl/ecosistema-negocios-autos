# Lista de vehículos
# Aquí va el código de la página de listado de vehículos.
"""
Página Listado

Muestra el listado de vehículos disponibles en el marketplace.
"""
import reflex as rx
from frontend_rx.estados.vehiculos import VehiculosState
from frontend_rx.componentes.layout import layout

def vehiculo_card(vehiculo):
    """Componente para mostrar un vehículo individual."""
    return rx.card(
        rx.vstack(
            rx.heading(f"{vehiculo['marca']} {vehiculo['modelo']}", size="4"),
            rx.text(f"Año: {vehiculo['año']}", color="gray"),
            rx.text(f"Tipo: {vehiculo['tipo'].title()}", color="gray"),
            rx.text(f"€{vehiculo['precio']:,}", size="5", weight="bold", color="green"),
            spacing="2"
        ),
        padding="4",
        width="100%"
    )

def filtros_panel():
    """Panel de filtros para los vehículos."""
    return rx.card(
        rx.vstack(
            rx.heading("Filtros", size="4"),
            
            rx.vstack(
                rx.text("Marca:", weight="bold"),
                rx.input(
                    placeholder="Buscar por marca...",
                    value=VehiculosState.filtro_marca,
                    on_change=VehiculosState.set_filtro_marca,
                    width="100%"
                ),
                spacing="1"
            ),
            
            rx.vstack(
                rx.text("Precio máximo:", weight="bold"),
                rx.input(
                    placeholder="Precio máximo...",
                    type="number",
                    value=VehiculosState.filtro_precio_max,
                    on_change=VehiculosState.set_filtro_precio_max,
                    width="100%"
                ),
                spacing="1"
            ),
            
            rx.vstack(
                rx.text("Tipo:", weight="bold"),
                rx.select(
                    ["", "sedan", "hatchback", "suv"],
                    value=VehiculosState.filtro_tipo,
                    on_change=VehiculosState.set_filtro_tipo,
                    placeholder="Todos los tipos",
                    width="100%"
                ),
                spacing="1"
            ),
            
            rx.button(
                "Limpiar Filtros",
                on_click=VehiculosState.limpiar_filtros,
                variant="outline",
                width="100%"
            ),
            
            spacing="4"
        ),
        padding="4"
    )

def listado_page():
    """Página principal de listado de vehículos."""
    return layout(
        rx.vstack(
            rx.heading("🚗 Listado de Vehículos", size="7", text_align="center"),
            rx.text("Encuentra tu vehículo ideal", color="gray", text_align="center"),
            
            rx.hstack(
                # Panel de filtros (lado izquierdo)
                rx.box(
                    filtros_panel(),
                    width="300px"
                ),
                
                # Lista de vehículos (lado derecho)
                rx.vstack(
                    rx.text("Listado de Vehículos", weight="bold"),
                    rx.grid(
                        rx.foreach(
                            VehiculosState.vehiculos,
                            vehiculo_card
                        ),
                        columns="2",
                        spacing="4",
                        width="100%"
                    ),
                    spacing="4",
                    width="100%"
                ),
                
                spacing="6",
                align="start",
                width="100%"
            ),
            
            spacing="6",
            width="100%"
        )
    )