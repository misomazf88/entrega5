import typing
import strawberry
import uuid
import requests
import os

from datetime import datetime


ALPESONLINE_HOST = os.getenv("ALPESONLINE_ADDRESS", default="localhost")
FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'

def obtener_Ordenes(root) -> typing.List["Orden"]:
    Ordenes_json = requests.get(f'http://{ALPESONLINE_HOST}:5000/orden/orden').json()
    ordenes = []

    for orden in Ordenes_json:
        ordenes.append(
            Orden(
                fecha_creacion=datetime.strptime(orden.get('fecha_creacion'), FORMATO_FECHA), 
                fecha_actualizacion=datetime.strptime(orden.get('fecha_actualizacion'), FORMATO_FECHA), 
                id=orden.get('id'), 
                id_usuario=orden.get('id_usuario', '')
            )
        )

    return ordenes

@strawberry.type
class Itinerario:
    # TODO Completar objeto strawberry para incluir los itinerarios
    ...

@strawberry.type
class Orden:
    id: str
    id_usuario: str
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    #itinerarios: typing.List[Itinerario]

@strawberry.type
class OrdenRespuesta:
    mensaje: str
    codigo: int






