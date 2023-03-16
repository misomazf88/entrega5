from alpesonline.seedwork.aplicacion.queries import Query, QueryHandler, QueryResultado
from alpesonline.seedwork.aplicacion.queries import ejecutar_query as query
from alpesonline.modulos.ordenes.infraestructura.repositorios import RepositorioOrdenes
from alpesonline.modulos.ordenes.dominio.entidades import Orden
from dataclasses import dataclass
from .base import OrdenQueryBaseHandler
from alpesonline.modulos.ordenes.aplicacion.mapeadores import MapeadorOrden
import uuid

@dataclass
class ObtenerOrden(Query):
    id: str

class ObtenerOrdenHandler(OrdenQueryBaseHandler):

    def handle(self, query: ObtenerOrden) -> QueryResultado:
        vista = self.fabrica_vista.crear_objeto(Orden)
        orden =  self.fabrica_vuelos.crear_objeto(vista.obtener_por(id=query.id)[0], MapeadorOrden())
        return QueryResultado(resultado=orden)

@query.register(ObtenerOrden)
def ejecutar_query_obtener_orden(query: ObtenerOrden):
    handler = ObtenerOrdenHandler()
    return handler.handle(query)