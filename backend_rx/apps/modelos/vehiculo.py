"""
Modelo Vehiculo

Contiene la definición y lógica del modelo Vehiculo para el ecosistema de negocios de autos.
"""
# Aquí va la definición del modelo Vehiculo.


"""
Modelo Vehiculo
Contiene la definición y lógica del modelo Vehiculo para el ecosistema de negocios de autos.
"""
import reflex as rx
from typing import Optional
from datetime import datetime
from enum import Enum
from sqlmodel import Field

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

class TipoVehiculo(Enum):
    SEDAN = "sedan"
    SUV = "suv"
    HATCHBACK = "hatchback"
    COUPE = "coupe"
    PICKUP = "pickup"
    BERLINA = "berlina"
    MONOVOLUMEN = "monovolumen"
    FURGONETA = "furgoneta"

class Vehiculo(rx.Model, table=True):
    id: Optional[int] = Field(primary_key=True)
    marca: str = Field(max_length=50)
    modelo: str = Field(max_length=100)
    año: int = Field(ge=1900, le=2030)
    tipo_motor: TipoMotor
    tipo_vehiculo: TipoVehiculo
    precio: float = Field(ge=0)
    precio_negociable: bool = True
    kilometraje: int = Field(ge=0)
    descripcion: Optional[str] = Field(max_length=1000)
    caracteristicas_extras: Optional[str] = Field(max_length=500)
    color_exterior: Optional[str] = Field(max_length=50)
    color_interior: Optional[str] = Field(max_length=50)
    
    # Ubicación
    ubicacion_ciudad: str = Field(max_length=100)
    ubicacion_provincia: str = Field(max_length=100)
    
    # Estado y gestión
    estado: EstadoVehiculo = EstadoVehiculo.DISPONIBLE
    activo: bool = True
    destacado: bool = False
    vistas: int = 0
    
    # Vendedor
    vendedor_id: int = Field(foreign_key="usuario.id")
    
    # Fechas
    fecha_creacion: datetime = Field(default_factory=datetime.now)
    fecha_actualizacion: Optional[datetime] = None
    
    # Opciones adicionales
    disponible_financiacion: bool = False
    acepta_parte_pago: bool = False
    motivo_inactivo: Optional[str] = None

    @property
    def precio_formateado(self) -> str:
        return f"€{self.precio:,.0f}"
    
    def incrementar_vistas(self):
        """Incrementa el contador de vistas"""
        self.vistas += 1

    def marcar_como_vendido(self):
        """Marca el vehículo como vendido"""
        self.estado = EstadoVehiculo.VENDIDO
        self.fecha_actualizacion = datetime.now()

    def activar_destacado(self):
        """Marca el vehículo como destacado"""
        self.destacado = True
        self.fecha_actualizacion = datetime.now()