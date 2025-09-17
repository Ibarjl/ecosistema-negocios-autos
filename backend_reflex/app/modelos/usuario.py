"""
Modelo Usuario

Contiene la definición y lógica del modelo Usuario para el ecosistema de negocios de autos.
"""
import reflex as rx
from typing import Optional
from datetime import datetime
from enum import Enum
from sqlmodel import Field

class TipoUsuario(Enum):
    PARTICULAR = "particular"
    ADMIN = "admin"

class Usuario(rx.Model, table=True):
    id: Optional[int] = Field(primary_key=True)
    email: str = Field(unique=True, max_length=255)
    password_hash: str = Field(max_length=255)
    nombre: str = Field(max_length=100)
    apellido: str = Field(max_length=100)
    telefono: Optional[str] = Field(max_length=20)
    tipo_usuario: TipoUsuario = TipoUsuario.PARTICULAR
    ciudad: str = Field(max_length=100)
    provincia: str = Field(max_length=100)
    
    # Gestión de cuenta
    activo: bool = True
    puede_publicar: bool = True
    
    # Estadísticas
    vehiculos_publicados: int = 0
    vehiculos_vendidos: int = 0
    
    # Fechas
    fecha_registro: datetime = Field(default_factory=datetime.now)
    fecha_actualizacion: Optional[datetime] = None
    
    @property
    def nombre_completo(self) -> str:
        return f"{self.nombre} {self.apellido}"
    
    def actualizar_estadisticas(self, vehiculo_vendido: bool = False):
        """Actualiza las estadísticas del usuario"""
        if vehiculo_vendido:
            self.vehiculos_vendidos += 1
        self.fecha_actualizacion = datetime.now()
