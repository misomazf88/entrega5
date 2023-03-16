from dataclasses import dataclass
from alpesonline.seedwork.aplicacion.queries import Query, QueryHandler, QueryResultado
from alpesonline.seedwork.aplicacion.queries import ejecutar_query as query
from alpesonline.modulos.ordenes.dominio.entidades import Orden
from alpesonline.modulos.ordenes.aplicacion.dto import OrdenDTO
from .base import OrdenQueryBaseHandler

@dataclass
class ObtenerTodasOrdenes(Query):
    ...

class ObtenerTodasOrdenesHandler(OrdenQueryBaseHandler):

    FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'

    def handle(self, query) -> QueryResultado:
        ordenes_dto = []
        vista = self.fabrica_vista.crear_objeto(Orden)
        ordenes = vista.obtener_todos()

        for orden in ordenes:
            dto = OrdenDTO(
                fecha_creacion=orden.fecha_creacion.strftime(self.FORMATO_FECHA),
                fecha_actualizacion=orden.fecha_actualizacion.strftime(self.FORMATO_FECHA),
                id = orden.id
            )
            ordenes_dto.append(dto)
        
        return QueryResultado(resultado=ordenes_dto)

@query.register(ObtenerTodasOrdenes)
def ejecutar_query_obtener_orden(query: ObtenerTodasOrdenes):
    handler = ObtenerTodasOrdenesHandler()
    return handler.handle(query)