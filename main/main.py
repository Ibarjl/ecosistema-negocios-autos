# main/main.py (corregido para nueva versión de Reflex)
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
            rx.text(f"Marca: {vehiculo['marca']}", weight="bold"),  # font_weight → weight
            rx.text(f"Modelo: {vehiculo['modelo']}"),
            rx.text(f"Precio: €{vehiculo['precio']:,}"),
            spacing="2"  # "0.5rem" → "2"
        ),
        padding="4"  # "1rem" → "4"
    )

def index():
    return rx.container(
        rx.vstack(
            rx.heading("🚗 AutoMercado", size="8"),  # Corregido ✅
            rx.text("Listado de Vehículos Disponibles"),
            rx.grid(
                *[vehiculo_card(v) for v in vehiculos_db],
                columns="3",  # [1, 2, 3] → "3" (simplificado por ahora)
                spacing="4"
            ),
            spacing="4",  # "2rem" → "4"
            align="center"
        ),
        max_width="1200px",
        padding="4"  # "2rem" → "4"
    )

app = rx.App()
app.add_page(index, route="/")