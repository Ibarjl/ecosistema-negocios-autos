"""
Utilidades para vehículos
Funciones auxiliares y de conveniencia para el manejo de vehículos.
"""

from typing import List, Tuple, Optional
from ..modelos.vehiculo import Vehiculo, TipoMotor, TipoVehiculo
from .vehiculos_service import vehiculos_service

# Ejemplo de uso:
# resultado = crear_vehiculo_rapido(
#     marca="Toyota",
#     modelo="Corolla",
#     año=2020,
#     precio=15000.0,
#     vendedor_id=1
# )

def crear_vehiculo_rapido(marca: str, modelo: str, año: int, precio: float, 
                         vendedor_id: int, **kwargs) -> Tuple[bool, str, Optional[Vehiculo]]:
    """Función de utilidad para crear un vehículo rápidamente."""
    datos = {
        "marca": marca,
        "modelo": modelo,
        "año": año,
        "precio": precio,
        "tipo_motor": TipoMotor.GASOLINA,
        "tipo_vehiculo": TipoVehiculo.SEDAN,
        "kilometraje": 0,
        "ubicacion_ciudad": "Madrid",
        "ubicacion_provincia": "Madrid",
        **kwargs
    }
    
    return vehiculos_service.crear_vehiculo(datos, vendedor_id)

    # Ejemplo de uso:
    # lista = buscar_vehiculos_simples(marca="Toyota", precio_max=20000)
def buscar_vehiculos_simples(marca: str = None, precio_max: float = None) -> List[Vehiculo]:
    """Búsqueda simple de vehículos."""
    filtros = {}
    if marca:
        filtros["marca"] = marca
    if precio_max:
        filtros["precio"] = {"lte": precio_max}
    
    resultado = vehiculos_service.buscar_vehiculos(filtros)
    return resultado["vehiculos"]