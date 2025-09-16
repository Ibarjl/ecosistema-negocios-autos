import reflex as rx

vehiculos_db = [
    {"id": 1, "marca": "BMW", "modelo": "Serie 3", "precio": 25000},
    {"id": 2, "marca": "Mercedes", "modelo": "Clase A", "precio": 30000},
    {"id": 3, "marca": "Audi", "modelo": "A4", "precio": 28000}
]

def vehiculo_card(vehiculo):
    return rx.card(
        rx.text(f"Marca: {vehiculo['marca']}", font_weight="bold"),
        rx.text(f"Modelo: {vehiculo['modelo']}"),
        rx.text(f"Precio: ${vehiculo['precio']}")
    )

def index():
    return rx.container(
        rx.heading("Listado de Vehículos", size="lg"),
        rx.grid(
            *[vehiculo_card(v) for v in vehiculos_db],
            columns=3,
            gap=4
        )
    )

app = rx.App()
app.add_page(index, route="/")