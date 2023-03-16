import strawberry
import typing

from strawberry.types import Info
from bff_web import utils
from bff_web.despachadores import Despachador

from .esquemas import *

@strawberry.type
class Mutation:

    @strawberry.mutation
    async def crear_orden(self, id_usuario: str, id_correlacion: str, id_vendedor: str,id_entrega: str,total: str,status: str,info: Info) -> OrdenRespuesta:
        print(f"ID Usuario: {id_usuario}, ID Correlación: {id_correlacion}")
        payload = dict(
            id_usuario = id_usuario,
            id_correlacion = id_correlacion,
            fecha_creacion = utils.time_millis(),
            fecha_actualizacion=utils.time_millis(),
            id_vendedor=id_vendedor,
            id_entrega=id_entrega,
            fecha_entrega=utils.time_millis(),
            total=total,
            status=status
        )
        comando = dict(
            id = str(uuid.uuid4()),
            time=utils.time_millis(),
            specversion = "v1",
            type = "ComandoOrden",
            ingestion=utils.time_millis(),
            datacontenttype="AVRO",
            service_name = "BFF Web",
            data = payload
        )
        despachador = Despachador()
        info.context["background_tasks"].add_task(despachador.publicar_mensaje, comando, "comando-crear-orden", "public/default/comando-crear-orden")
        
        return OrdenRespuesta(mensaje="Procesando Mensaje", codigo=203)