# main.py (actualizado)
import reflex as rx

# Datos de prueba temporales
vehiculos_db = [
    {"id": 1, "marca": "BMW", "modelo": "Serie 3", "precio": 25000},
    {"id": 2, "marca": "Mercedes", "modelo": "Clase A", "precio": 30000},
    {"id": 3, "marca": "Audi", "modelo": "A4", "precio": 28000}
]

def vehiculo_card(vehiculo):
    return rx.card(
        rx.vstack(
            rx.text(f"Marca: {vehiculo['marca']}", font_weight="bold"),
            rx.text(f"Modelo: {vehiculo['modelo']}"),
            rx.text(f"Precio: €{vehiculo['precio']:,}"),
            spacing="0.5rem"
        ),
        padding="1rem",
        border="1px solid #e2e8f0"
    )

def index():
    return rx.container(
        rx.vstack(
            rx.heading("🚗 AutoMercado", size="2xl"),
            rx.text("Listado de Vehículos Disponibles"),
            rx.grid(
                *[vehiculo_card(v) for v in vehiculos_db],
                columns=[1, 2, 3],  # Responsive: 1 col en móvil, 2 en tablet, 3 en desktop
                spacing="4"
            ),
            spacing="2rem",
            align="center"
        ),
        max_width="1200px",
        padding="2rem"
    )

app = rx.App()
app.add_page(index, route="/")