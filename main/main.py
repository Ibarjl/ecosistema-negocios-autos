# main/main.py - AutoMercado - Versión simplificada
import reflex as rx

# Estado simple para autenticación
class AuthState(rx.State):
    is_logged_in: bool = False
    username: str = ""
    login_email: str = ""
    login_password: str = ""
    register_name: str = ""
    register_email: str = ""
    register_password: str = ""
    
    def login(self):
        if self.login_email == "test@test.com" and self.login_password == "123456":
            self.is_logged_in = True
            self.username = "Usuario Demo"
            return rx.redirect("/listado")
        else:
            return rx.window_alert("Credenciales incorrectas. Usa: test@test.com / 123456")
    
    def register(self):
        """Simula el proceso de registro."""
        if self.register_name and self.register_email and self.register_password:
            self.is_logged_in = True
            self.username = self.register_name
            return rx.redirect("/listado")
        else:
            return rx.window_alert("Por favor completa todos los campos")

# Estado simple para vehículos
class VehiculosState(rx.State):
    vehiculos: list[dict] = [
        {"id": 1, "marca": "BMW", "modelo": "Serie 3", "precio": 25000, "año": 2020},
        {"id": 2, "marca": "Mercedes", "modelo": "Clase A", "precio": 30000, "año": 2021},
        {"id": 3, "marca": "Audi", "modelo": "A4", "precio": 28000, "año": 2019},
        {"id": 4, "marca": "Toyota", "modelo": "Corolla", "precio": 22000, "año": 2022},
        {"id": 5, "marca": "Volkswagen", "modelo": "Golf", "precio": 24000, "año": 2020},
    ]

# Componente simple de navbar
def navbar():
    return rx.hstack(
        rx.link(rx.heading("🚗 AutoMercado", size="6"), href="/"),
        rx.spacer(),
        rx.hstack(
            rx.link("Inicio", href="/"),
            rx.link("Listado", href="/listado"),
            rx.link("Login", href="/login"),
            rx.link("Registro", href="/registro"),
            spacing="4"
        ),
        justify="between",
        padding="4",
        border_bottom="1px solid #e2e8f0",
        width="100%"
    )

# Componente de vehículo
def vehiculo_card(vehiculo):
    return rx.card(
        rx.vstack(
            rx.heading(f"{vehiculo['marca']} {vehiculo['modelo']}", size="4"),
            rx.text(f"Año: {vehiculo['año']}", color="gray"),
            rx.text(f"€{vehiculo['precio']:,}", size="5", weight="bold", color="green"),
            spacing="2"
        ),
        padding="4",
        width="100%"
    )

# Páginas
def index():
    return rx.vstack(
        navbar(),
        rx.container(
            rx.vstack(
                rx.heading("🚗 Bienvenido a AutoMercado", size="8", text_align="center"),
                rx.text("El marketplace líder en vehículos", size="5", color="gray", text_align="center"),
                rx.hstack(
                    rx.link(rx.button("Ver Listado", size="4"), href="/listado"),
                    rx.link(rx.button("Iniciar Sesión", variant="outline", size="4"), href="/login"),
                    rx.link(rx.button("Registrarse", variant="soft", size="4"), href="/registro"),
                    spacing="4",
                    justify="center"
                ),
                spacing="6",
                align="center",
                min_height="60vh",
                justify="center"
            ),
            max_width="1200px",
            padding="4"
        ),
        spacing="0",
        width="100%"
    )

def login_page():
    return rx.vstack(
        navbar(),
        rx.container(
            rx.center(
                rx.card(
                    rx.vstack(
                        rx.heading("Iniciar Sesión", size="6", text_align="center"),
                        rx.input(
                            placeholder="Email",
                            type="email",
                            value=AuthState.login_email,
                            on_change=AuthState.set_login_email,
                            width="100%"
                        ),
                        rx.input(
                            placeholder="Contraseña",
                            type="password",
                            value=AuthState.login_password,
                            on_change=AuthState.set_login_password,
                            width="100%"
                        ),
                        rx.button("Iniciar Sesión", on_click=AuthState.login, width="100%"),
                        rx.divider(),
                        rx.hstack(
                            rx.text("¿No tienes cuenta?"),
                            rx.link("Regístrate aquí", href="/registro", color="blue"),
                            justify="center"
                        ),
                        rx.text("Demo: test@test.com / 123456", color="gray", size="2"),
                        spacing="4",
                        width="100%"
                    ),
                    max_width="400px",
                    padding="6"
                ),
                min_height="60vh"
            ),
            max_width="1200px",
            padding="4"
        ),
        spacing="0",
        width="100%"
    )

def registro_page():
    return rx.vstack(
        navbar(),
        rx.container(
            rx.center(
                rx.card(
                    rx.vstack(
                        rx.heading("Crear Cuenta", size="6", text_align="center"),
                        rx.text("Únete a AutoMercado y encuentra tu vehículo ideal", 
                               color="gray", 
                               text_align="center"),
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
                        rx.button("Crear Cuenta", on_click=AuthState.register, width="100%"),
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
            ),
            max_width="1200px",
            padding="4"
        ),
        spacing="0",
        width="100%"
    )

def listado_page():
    return rx.vstack(
        navbar(),
        rx.container(
            rx.vstack(
                rx.heading("🚗 Listado de Vehículos", size="7", text_align="center"),
                rx.grid(
                    rx.foreach(VehiculosState.vehiculos, vehiculo_card),
                    columns="3",
                    spacing="4",
                    width="100%"
                ),
                spacing="6",
                width="100%"
            ),
            max_width="1200px",
            padding="4"
        ),
        spacing="0",
        width="100%"
    )

# Configuración de la aplicación
app = rx.App()
app.add_page(index, route="/")
app.add_page(login_page, route="/login")
app.add_page(registro_page, route="/registro")
app.add_page(listado_page, route="/listado")