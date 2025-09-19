"""
Estado de Autenticación

Maneja el estado de autenticación de usuarios en el marketplace.
"""
import reflex as rx

class AuthState(rx.State):
    """Estado para manejo de autenticación."""
    
    # Variables de estado
    is_logged_in: bool = False
    username: str = ""
    email: str = ""
    
    # Variables para formularios
    login_email: str = ""
    login_password: str = ""
    register_name: str = ""
    register_email: str = ""
    register_password: str = ""
    
    def login(self):
        """Simula el proceso de login."""
        # Login simple para demo (test@test.com / 123456)
        if self.login_email == "test@test.com" and self.login_password == "123456":
            self.is_logged_in = True
            self.username = "Usuario Demo"
            self.email = self.login_email
            return rx.redirect("/listado")
        else:
            return rx.window_alert("Credenciales incorrectas. Usa: test@test.com / 123456")
    
    def register(self):
        """Simula el proceso de registro."""
        if self.register_name and self.register_email and self.register_password:
            self.is_logged_in = True
            self.username = self.register_name
            self.email = self.register_email
            return rx.redirect("/listado")
        else:
            return rx.window_alert("Por favor completa todos los campos")
    
    def logout(self):
        """Cierra la sesión del usuario."""
        self.is_logged_in = False
        self.username = ""
        self.email = ""
        return rx.redirect("/")
