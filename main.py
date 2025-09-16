from fastapi import FastAPI

app = FastAPI()

vehiculos_db = [
    {"id": 1, "marca": "BMW", "modelo": "Serie 3", "precio": 25000},
    {"id": 2, "marca": "Mercedes", "modelo": "Clase A", "precio": 30000},
    {"id": 3, "marca": "Audi", "modelo": "A4", "precio": 28000}
]


@app.get("/")
def hola():
    return {"mensaje": "Mi primer mensaje con API"}



@app.get("/vehiculos")
def visualizar_vehiculos():
    return vehiculos_db


@app.get("/vehiculos/{mi_id}")
def obtener_vehiculo(vehiculo_id: int):
    for vehiculo in vehiculos_db:
        if vehiculo["id"]==vehiculo_id:
            return vehiculo
    return {"error": "Vehiculo no encontrado"}