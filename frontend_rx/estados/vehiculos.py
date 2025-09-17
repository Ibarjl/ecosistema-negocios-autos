"""
Estado Vehículos

Maneja el estado y datos de los vehículos en el marketplace.
"""
import reflex as rx

class VehiculosState(rx.State):
    """Estado para manejo de vehículos y filtros."""
    
    # Datos de vehículos (simulados)
    vehiculos: list[dict] = [
        {"id": 1, "marca": "BMW", "modelo": "Serie 3", "precio": 25000, "año": 2020, "tipo": "sedan"},
        {"id": 2, "marca": "Mercedes", "modelo": "Clase A", "precio": 30000, "año": 2021, "tipo": "hatchback"},
        {"id": 3, "marca": "Audi", "modelo": "A4", "precio": 28000, "año": 2019, "tipo": "sedan"},
        {"id": 4, "marca": "Toyota", "modelo": "Corolla", "precio": 22000, "año": 2022, "tipo": "sedan"},
        {"id": 5, "marca": "Volkswagen", "modelo": "Golf", "precio": 24000, "año": 2020, "tipo": "hatchback"},
    ]
    
    # Filtros
    filtro_marca: str = ""
    filtro_precio_max: str = "50000"
    filtro_tipo: str = ""
    
    def get_vehiculos_filtrados(self) -> list[dict]:
        """Retorna los vehículos filtrados según los criterios actuales."""
        resultado = self.vehiculos
        
        if self.filtro_marca:
            resultado = [v for v in resultado if self.filtro_marca.lower() in v["marca"].lower()]
        
        if self.filtro_precio_max and self.filtro_precio_max.isdigit():
            precio_max = int(self.filtro_precio_max)
            resultado = [v for v in resultado if v["precio"] <= precio_max]
        
        if self.filtro_tipo:
            resultado = [v for v in resultado if v["tipo"] == self.filtro_tipo]
        
        return resultado
    
    def limpiar_filtros(self):
        """Limpia todos los filtros aplicados."""
        self.filtro_marca = ""
        self.filtro_precio_max = "50000"
        self.filtro_tipo = ""