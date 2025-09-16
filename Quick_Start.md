# 🚗 QUICK START - ECOSISTEMA AUTOS (SOLO REFLEX)

## 🔧 IBAR (Tech Backend) - Modelos y Base de Datos
```python
# backend_reflex/app/modelos/vehiculo.py
"""
Modelo Vehiculo
Contiene la definición y lógica del modelo Vehiculo para el ecosistema de negocios de autos.
"""
import reflex as rx
from typing import Optional
from enum import Enum
from datetime import datetime

class TipoMotor(Enum):
    GASOLINA = "gasolina"
    DIESEL = "diesel" 
    HIBRIDO = "hibrido"
    ELECTRICO = "electrico"
    HIBRIDO_ENCHUFABLE = "hibrido_enchufable"

class EstadoVehiculo(Enum):
    DISPONIBLE = "disponible"
    RESERVADO = "reservado"
    VENDIDO = "vendido"

class Vehiculo(rx.Model, table=True):
    id: Optional[int] = rx.Field(primary_key=True)
    marca: str = rx.Field(max_length=50)
    modelo: str = rx.Field(max_length=100)
    año: int = rx.Field(ge=1900, le=2030)
    tipo_motor: TipoMotor
    precio: float = rx.Field(ge=0)
    kilometraje: int = rx.Field(ge=0)
    ubicacion: str = rx.Field(max_length=100)
    estado: EstadoVehiculo = EstadoVehiculo.DISPONIBLE
    fecha_creacion: datetime = rx.Field(default_factory=datetime.now)
    
    # Método de utilidad
    @property
    def precio_formateado(self) -> str:
        return f"€{self.precio:,.0f}"
```

```python
# backend_reflex/app/modelos/usuario.py
"""
Modelo Usuario
Contiene la definición y lógica del modelo Usuario para el ecosistema de negocios de autos.
"""
import reflex as rx
from typing import Optional
from datetime import datetime
from enum import Enum

class TipoUsuario(Enum):
    PARTICULAR = "particular"
    CONCESIONARIA = "concesionaria"
    ADMIN = "admin"

class Usuario(rx.Model, table=True):
    id: Optional[int] = rx.Field(primary_key=True)
    email: str = rx.Field(unique=True, max_length=255)
    password_hash: str = rx.Field(max_length=255)
    nombre: str = rx.Field(max_length=100)
    apellido: str = rx.Field(max_length=100)
    telefono: Optional[str] = rx.Field(max_length=20)
    tipo_usuario: TipoUsuario = TipoUsuario.PARTICULAR
    ciudad: str = rx.Field(max_length=100)
    provincia: str = rx.Field(max_length=100)
    fecha_registro: datetime = rx.Field(default_factory=datetime.now)
    activo: bool = True
    
    @property
    def nombre_completo(self) -> str:
        return f"{self.nombre} {self.apellido}"
```

## 👩‍💻 DANIELA (Backend Developer) - Estado de Autenticación Reflex
```python
# backend_reflex/app/autenticacion/main.py
"""
Estado de Autenticación con Reflex
Reemplaza el FastAPI anterior con lógica pura de Reflex
"""
import reflex as rx
from typing import Optional
import bcrypt
import jwt
from datetime import datetime, timedelta
from ..modelos.usuario import Usuario, TipoUsuario
from sqlmodel import select

class AuthState(rx.State):
    """Estado global de autenticación usando Reflex"""
    
    # Usuario actual
    usuario_actual: Optional[Usuario] = None
    token: Optional[str] = None
    is_loading: bool = False
    error_message: str = ""
    success_message: str = ""
    
    # Campos del formulario
    form_email: str = ""
    form_password: str = ""
    form_nombre: str = ""
    form_apellido: str = ""
    form_telefono: str = ""
    form_ciudad: str = ""
    form_provincia: str = ""

    @rx.var
    def is_authenticated(self) -> bool:
        """Verifica si el usuario está autenticado"""
        return self.usuario_actual is not None

    def limpiar_formulario(self):
        """Limpia todos los campos del formulario"""
        self.form_email = ""
        self.form_password = ""
        self.form_nombre = ""
        self.form_apellido = ""
        self.form_telefono = ""
        self.form_ciudad = ""
        self.form_provincia = ""
        self.error_message = ""
        self.success_message = ""

    def registrar_usuario(self):
        """Registra un nuevo usuario"""
        self.is_loading = True
        self.error_message = ""
        
        try:
            # Validaciones básicas
            if not self.form_email or not self.form_password:
                self.error_message = "Email y contraseña son requeridos"
                self.is_loading = False
                return
            
            with rx.session() as session:
                # Verificar si el usuario ya existe
                usuario_existente = session.exec(
                    select(Usuario).where(Usuario.email == self.form_email)
                ).first()
                
                if usuario_existente:
                    self.error_message = "Este email ya está registrado"
                    self.is_loading = False
                    return
                
                # Hash de la contraseña
                password_hash = bcrypt.hashpw(
                    self.form_password.encode('utf-8'),
                    bcrypt.gensalt()
                ).decode('utf-8')
                
                # Crear nuevo usuario
                nuevo_usuario = Usuario(
                    email=self.form_email,
                    password_hash=password_hash,
                    nombre=self.form_nombre,
                    apellido=self.form_apellido,
                    telefono=self.form_telefono,
                    ciudad=self.form_ciudad,
                    provincia=self.form_provincia
                )
                
                session.add(nuevo_usuario)
                session.commit()
                session.refresh(nuevo_usuario)
                
                # Auto-login tras registro
                self.usuario_actual = nuevo_usuario
                self.token = self._generar_token(nuevo_usuario.id)
                self.success_message = "¡Registro exitoso!"
                self.limpiar_formulario()
                
                # Redirigir al home
                return rx.redirect("/")
                
        except Exception as e:
            self.error_message = f"Error en el registro: {str(e)}"
        finally:
            self.is_loading = False

    def iniciar_sesion(self):
        """Inicia sesión del usuario"""
        self.is_loading = True
        self.error_message = ""
        
        try:
            with rx.session() as session:
                usuario = session.exec(
                    select(Usuario).where(Usuario.email == self.form_email)
                ).first()
                
                if not usuario or not bcrypt.checkpw(
                    self.form_password.encode('utf-8'),
                    usuario.password_hash.encode('utf-8')
                ):
                    self.error_message = "Email o contraseña incorrectos"
                    self.is_loading = False
                    return
                
                if not usuario.activo:
                    self.error_message = "Cuenta desactivada"
                    self.is_loading = False
                    return
                
                self.usuario_actual = usuario
                self.token = self._generar_token(usuario.id)
                self.success_message = "¡Bienvenido!"
                self.limpiar_formulario()
                
                # Redirigir al home
                return rx.redirect("/")
                
        except Exception as e:
            self.error_message = f"Error al iniciar sesión: {str(e)}"
        finally:
            self.is_loading = False

    def cerrar_sesion(self):
        """Cierra la sesión del usuario"""
        self.usuario_actual = None
        self.token = None
        self.success_message = "Sesión cerrada"
        return rx.redirect("/")

    def _generar_token(self, usuario_id: int) -> str:
        """Genera un JWT token"""
        payload = {
            'usuario_id': usuario_id,
            'exp': datetime.utcnow() + timedelta(days=7)
        }
        return jwt.encode(payload, "clave-secreta-jwt", algorithm="HS256")
```

## 👨‍💻 JMB (Tech Lead Frontend) - Layout y Páginas Base
```python
# frontend_reflex/componentes/layout.py
"""
Componente Layout
Define la estructura y disposición general de la interfaz del marketplace.
"""
import reflex as rx
from backend_reflex.app.autenticacion.main import AuthState

def navbar() -> rx.Component:
    return rx.hstack(
        # Logo/Marca
        rx.link(
            rx.hstack(
                rx.text("🚗", font_size="2xl"),
                rx.text("AutoMercado", font_size="xl", font_weight="bold"),
                spacing="0.5rem"
            ),
            href="/",
            text_decoration="none"
        ),
        
        rx.spacer(),
        
        # Navegación
        rx.hstack(
            rx.link("Catálogo", href="/listado", padding="0.5rem"),
            rx.cond(
                AuthState.is_authenticated,
                rx.link("Vender Auto", href="/publicar", padding="0.5rem")
            ),
            spacing="1rem"
        ),
        
        rx.spacer(),
        
        # Área de usuario
        rx.cond(
            AuthState.is_authenticated,
            # Usuario logueado
            rx.hstack(
                rx.text(f"Hola, {AuthState.usuario_actual.nombre}"),
                rx.button(
                    "Cerrar Sesión",
                    on_click=AuthState.cerrar_sesion,
                    variant="outline",
                    size="sm"
                ),
                spacing="1rem"
            ),
            # Usuario no logueado
            rx.hstack(
                rx.link(
                    rx.button("Iniciar Sesión", variant="outline"),
                    href="/login"
                ),
                rx.link(
                    rx.button("Registrarse", color_scheme="blue"),
                    href="/registro"
                ),
                spacing="1rem"
            )
        ),
        
        width="100%",
        padding="1rem 2rem",
        bg="white",
        box_shadow="sm",
        border_bottom="1px solid #e2e8f0",
        position="sticky",
        top="0",
        z_index="1000"
    )

def page_layout(content: rx.Component) -> rx.Component:
    return rx.vstack(
        navbar(),
        rx.container(
            content,
            max_width="1200px",
            padding="2rem 1rem",
            min_height="calc(100vh - 80px)"
        ),
        width="100%",
        spacing="0"
    )
```

```python
# frontend_reflex/paginas/home.py
"""
Página Home
Página principal del marketplace de autos.
"""
import reflex as rx
from ..componentes.layout import page_layout

def home() -> rx.Component:
    return page_layout(
        rx.vstack(
            # Hero Section
            rx.vstack(
                rx.heading(
                    "Encuentra el auto perfecto",
                    size="2xl",
                    text_align="center"
                ),
                rx.text(
                    "Miles de autos nuevos y usados te esperan",
                    font_size="xl",
                    color="gray.600",
                    text_align="center"
                ),
                rx.hstack(
                    rx.link(
                        rx.button(
                            "Ver Catálogo",
                            size="lg",
                            color_scheme="blue"
                        ),
                        href="/listado"
                    ),
                    rx.link(
                        rx.button(
                            "Vender mi Auto",
                            size="lg",
                            variant="outline"
                        ),
                        href="/publicar"
                    ),
                    spacing="2rem"
                ),
                spacing="2rem",
                padding="4rem 0"
            ),
            
            # Sección de marcas populares
            rx.vstack(
                rx.heading("Marcas Populares", size="xl"),
                rx.hstack(
                    rx.text("BMW"),
                    rx.text("Mercedes"),
                    rx.text("Audi"),
                    rx.text("Toyota"),
                    rx.text("Volkswagen"),
                    spacing="2rem",
                    wrap="wrap"
                ),
                spacing="1rem",
                align="center"
            ),
            
            spacing="4rem",
            align="center"
        )
    )
```

## 👨‍💻 ALESSANDRO (Frontend Developer) - Gestión de Vehículos
```python
# frontend_reflex/estados/vehiculos.py
"""
Estado Vehiculos
Gestiona el estado de la lista y detalles de vehículos en el marketplace.
"""
import reflex as rx
from typing import List, Optional
from backend_reflex.app.modelos.vehiculo import Vehiculo, TipoMotor, EstadoVehiculo
from sqlmodel import select

class VehiculosState(rx.State):
    vehiculos: List[Vehiculo] = []
    vehiculo_seleccionado: Optional[Vehiculo] = None
    is_loading: bool = False
    error_message: str = ""
    
    # Filtros
    filtro_marca: str = ""
    filtro_tipo_motor: str = ""
    precio_min: int = 0
    precio_max: int = 100000
    
    # Paginación
    pagina_actual: int = 1
    vehiculos_por_pagina: int = 12

    def cargar_vehiculos(self):
        """Carga todos los vehículos disponibles"""
        self.is_loading = True
        try:
            with rx.session() as session:
                query = select(Vehiculo).where(Vehiculo.estado == EstadoVehiculo.DISPONIBLE)
                vehiculos = session.exec(query).all()
                self.vehiculos = list(vehiculos)
        except Exception as e:
            self.error_message = f"Error al cargar vehículos: {str(e)}"
        finally:
            self.is_loading = False

    def seleccionar_vehiculo(self, vehiculo_id: int):
        """Selecciona un vehículo para ver detalles"""
        try:
            with rx.session() as session:
                vehiculo = session.get(Vehiculo, vehiculo_id)
                if vehiculo:
                    self.vehiculo_seleccionado = vehiculo
                    return rx.redirect(f"/detalle/{vehiculo_id}")
        except Exception as e:
            self.error_message = f"Error al cargar vehículo: {str(e)}"

    @rx.var
    def vehiculos_filtrados(self) -> List[Vehiculo]:
        """Aplica filtros a la lista de vehículos"""
        vehiculos = self.vehiculos
        
        if self.filtro_marca:
            vehiculos = [
                v for v in vehiculos 
                if self.filtro_marca.lower() in v.marca.lower()
            ]
        
        if self.filtro_tipo_motor:
            vehiculos = [
                v for v in vehiculos 
                if v.tipo_motor.value == self.filtro_tipo_motor
            ]
        
        vehiculos = [
            v for v in vehiculos 
            if self.precio_min <= v.precio <= self.precio_max
        ]
        
        return vehiculos

    def resetear_filtros(self):
        """Resetea todos los filtros"""
        self.filtro_marca = ""
        self.filtro_tipo_motor = ""
        self.precio_min = 0
        self.precio_max = 100000
```

```python
# frontend_reflex/componentes/vehiculo_card.py
"""
Componente VehiculoCard
Representa la tarjeta visual de un vehículo en el listado del marketplace.
"""
import reflex as rx
from backend_reflex.app.modelos.vehiculo import Vehiculo
from ..estados.vehiculos import VehiculosState

def vehiculo_card(vehiculo: Vehiculo) -> rx.Component:
    return rx.card(
        rx.vstack(
            # Imagen del vehículo
            rx.image(
                src="/placeholder-auto.jpg",  # Reemplazar con imagen real
                width="100%",
                height="200px",
                object_fit="cover",
                border_radius="md"
            ),
            
            # Información del vehículo
            rx.vstack(
                rx.heading(
                    f"{vehiculo.marca} {vehiculo.modelo}",
                    size="lg",
                    color="gray.800"
                ),
                rx.text(
                    f"Año {vehiculo.año} • {vehiculo.tipo_motor.value.title()}",
                    color="gray.600"
                ),
                rx.text(
                    f"{vehiculo.kilometraje:,} km • {vehiculo.ubicacion}",
                    color="gray.500",
                    font_size="sm"
                ),
                spacing="0.5rem",
                align="start"
            ),
            
            # Precio y botón
            rx.hstack(
                rx.text(
                    vehiculo.precio_formateado,
                    font_size="xl",
                    font_weight="bold",
                    color="green.600"
                ),
                rx.spacer(),
                rx.button(
                    "Ver Detalles",
                    on_click=lambda: VehiculosState.seleccionar_vehiculo(vehiculo.id),
                    color_scheme="blue",
                    size="sm"
                ),
                width="100%"
            ),
            
            spacing="1rem"
        ),
        max_width="300px",
        padding="1rem",
        border="1px solid #e2e8f0",
        border_radius="lg",
        _hover={
            "box_shadow": "lg",
            "transform": "translateY(-2px)",
            "transition": "all 0.2s"
        }
    )
```

## 👨‍💻 CARLOS (Frontend Developer) - Sistema de Checkout
```python
# frontend_reflex/estados/checkout.py
"""
Estado Checkout
Gestiona el estado y lógica del proceso de checkout en el marketplace.
"""
import reflex as rx
from typing import Optional
from backend_reflex.app.modelos.vehiculo import Vehiculo
from backend_reflex.app.autenticacion.main import AuthState

class CheckoutState(rx.State):
    # Vehículo a comprar
    vehiculo_checkout: Optional[Vehiculo] = None
    
    # Datos del proceso
    paso_actual: int = 1
    is_processing: bool = False
    checkout_completado: bool = False
    
    # Datos adicionales del comprador
    mensaje_vendedor: str = ""
    forma_contacto: str = "telefono"
    
    # Estado de confirmación
    mensaje_confirmacion: str = ""

    def iniciar_checkout(self, vehiculo_id: int):
        """Inicia el proceso de checkout"""
        try:
            with rx.session() as session:
                vehiculo = session.get(Vehiculo, vehiculo_id)
                if vehiculo:
                    self.vehiculo_checkout = vehiculo
                    self.paso_actual = 1
                    self.checkout_completado = False
                    return rx.redirect("/checkout")
        except Exception as e:
            print(f"Error al iniciar checkout: {e}")

    def siguiente_paso(self):
        """Avanza al siguiente paso del checkout"""
        if self.paso_actual < 3:
            self.paso_actual += 1

    def paso_anterior(self):
        """Retrocede al paso anterior"""
        if self.paso_actual > 1:
            self.paso_actual -= 1

    def finalizar_compra(self):
        """Procesa la compra final"""
        self.is_processing = True
        
        # Simular procesamiento (aquí iría lógica real)
        # En un caso real, aquí se:
        # 1. Crearía un registro de transacción
        # 2. Enviaría emails de confirmación
        # 3. Notificaría al vendedor
        
        self.mensaje_confirmacion = f"""
        ¡Solicitud de compra enviada exitosamente!
        
        Te contactaremos pronto para coordinar:
        • Inspección del vehículo
        • Documentación necesaria
        • Forma de pago
        
        Vehículo: {self.vehiculo_checkout.marca} {self.vehiculo_checkout.modelo}
        Precio: {self.vehiculo_checkout.precio_formateado}
        """
        
        self.checkout_completado = True
        self.paso_actual = 3
        self.is_processing = False

    def reiniciar_checkout(self):
        """Reinicia el proceso de checkout"""
        self.vehiculo_checkout = None
        self.paso_actual = 1
        self.checkout_completado = False
        self.mensaje_vendedor = ""
        self.mensaje_confirmacion = ""
        return rx.redirect("/listado")
```

## 👨‍💻 JL (DevOps) - Configuración Simplificada Solo Reflex
```bash
# setup.sh - Solo para Reflex
#!/bin/bash
echo "🚗 Configurando Ecosistema Autos (Solo Reflex)..."

# Crear virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt
pip install reflex
pip install bcrypt  # Para hash de contraseñas
pip install PyJWT   # Para tokens JWT

# Crear .env
if [ ! -f .env ]; then
cat > .env << EOL
# Configuración de base de datos
DATABASE_URL=sqlite:///./ecosistema_autos.db

# JWT Secret (cambiar en producción)
JWT_SECRET_KEY=tu-clave-super-secreta-cambiar-en-produccion

# Configuración de Reflex
REFLEX_DB_URL=sqlite:///./reflex.db
EOL
fi

# Inicializar base de datos
echo "Inicializando base de datos..."
reflex db init
reflex db migrate

echo "✅ Setup completo!"
echo "Para ejecutar: reflex run"
echo "Visita: http://localhost:3000"
```

```python
# requirements.txt - Actualizado
reflex>=0.4.0
bcrypt>=4.0.0
PyJWT>=2.8.0
sqlmodel>=0.0.14
```

```dockerfile
# Dockerfile - Solo Reflex
FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copiar código
COPY . .

# Exponer puerto de Reflex
EXPOSE 3000

# Comando para ejecutar
CMD ["reflex", "run", "--env", "prod", "--backend-only"]
```

## 👩‍💻 JUSTINA (QA) - Tests para Reflex
```python
# backend_reflex/pruebas/test_vehiculos.py
"""
Tests de vehículos
Contiene pruebas unitarias y de integración para la gestión de vehículos en el ecosistema de negocios de autos.
"""
import pytest
import reflex as rx
from backend_reflex.app.modelos.vehiculo import Vehiculo, TipoMotor, EstadoVehiculo
from frontend_reflex.estados.vehiculos import VehiculosState

def test_crear_vehiculo():
    """Test básico de creación de vehículo"""
    vehiculo = Vehiculo(
        marca="Toyota",
        modelo="Corolla",
        año=2020,
        tipo_motor=TipoMotor.GASOLINA,
        precio=15000,
        kilometraje=50000,
        ubicacion="Madrid"
    )
    
    assert vehiculo.marca == "Toyota"
    assert vehiculo.precio_formateado == "€15,000"
    assert vehiculo.estado == EstadoVehiculo.DISPONIBLE

def test_estado_vehiculos():
    """Test del estado de vehículos"""
    state = VehiculosState()
    
    # Test filtros iniciales
    assert state.filtro_marca == ""
    assert state.precio_min == 0
    assert state.precio_max == 100000
    
    # Test reseteo de filtros
    state.filtro_marca = "Toyota"
    state.resetear_filtros()
    assert state.filtro_marca == ""

# Casos de prueba manual para Justina:
"""
🔍 CASOS DE PRUEBA MANUALES:

1. Registro de Usuario:
   - Registrar con datos válidos ✓
   - Registrar con email duplicado (debe fallar) ✓
   - Registrar sin email (debe fallar) ✓

2. Login:
   - Login con credenciales correctas ✓
   - Login con credenciales incorrectas ✓
   - Persistencia de sesión ✓

3. Listado de Vehículos:
   - Cargar vehículos correctamente ✓
   - Aplicar filtros por marca ✓
   - Aplicar filtros por precio ✓
   - Resetear filtros ✓

4. Proceso de Compra:
   - Seleccionar vehículo ✓
   - Completar checkout ✓
   - Validar datos requeridos ✓
   - Confirmación final ✓

Ejecutar tests: python -m pytest backend_reflex/pruebas/ -v
"""

# Para ejecutar todos los tests
if __name__ == "__main__":
    pytest.main(["-v", "backend_reflex/pruebas/"])
```

## 📝 TAREAS INMEDIATAS POR ROL:

**Ibar:** 
1. Completar los modelos `transaccion.py` 
2. Configurar la base de datos inicial con `reflex db migrate`

**Daniela:** 
1. Probar el login/registro en la página
2. Agregar validaciones de seguridad adicionales

**JMB:** 
1. Crear las páginas faltantes (`/login`, `/registro`, `/listado`)
2. Conectar el layout con las rutas

**Alessandro:** 
1. Implementar la página de listado completa con filtros
2. Crear la página de detalle del vehículo

**Carlos:** 
1. Implementar la página de checkout completa
2. Conectar con el estado de autenticación

**JL:** 
1. Configurar el entorno de desarrollo
2. Crear docker-compose para toda la aplicación

**Justina:** 
1. Probar manualmente el flujo completo
2. Crear tests automatizados adicionales

