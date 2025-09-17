"""
Validaciones de modelos
Contiene las funciones de validación para los modelos del ecosistema de autos.
"""
from typing import Dict, Any, Tuple
from datetime import datetime
import re

def validar_datos_vehiculo(datos: Dict[str, Any]) -> Tuple[bool, str]:
    """Valida los datos de un vehículo antes de crearlo"""
    
    # Campos obligatorios
    campos_requeridos = ["marca", "modelo", "año", "precio", "kilometraje", "ubicacion_ciudad", "ubicacion_provincia"]
    for campo in campos_requeridos:
        if not datos.get(campo):
            return False, f"El campo {campo} es obligatorio"
    
    # Validar año
    año_actual = datetime.now().year
    if datos["año"] < 1900 or datos["año"] > año_actual + 1:
        return False, f"Año debe estar entre 1900 y {año_actual + 1}"
    
    # Validar precio
    if datos["precio"] <= 0:
        return False, "El precio debe ser mayor a 0"
    
    # Validar kilometraje
    if datos["kilometraje"] < 0:
        return False, "El kilometraje no puede ser negativo"
    
    # Validar marca y modelo (solo letras, números y espacios)
    if not re.match(r'^[a-zA-Z0-9\s\-]+$', datos["marca"]):
        return False, "La marca contiene caracteres no válidos"
    
    if not re.match(r'^[a-zA-Z0-9\s\-]+$', datos["modelo"]):
        return False, "El modelo contiene caracteres no válidos"
    
    return True, "Validación exitosa"