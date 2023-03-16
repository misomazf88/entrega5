from alpesonline.seedwork.aplicacion.comandos import Comando
from alpesonline.modulos.ordenes.aplicacion.dto import ItinerarioDTO, OrdenDTO
from .base import CrearOrdenBaseHandler
from dataclasses import dataclass, field
from alpesonline.seedwork.aplicacion.comandos import ejecutar_commando as comando

from alpesonline.modulos.ordenes.dominio.entidades import Orden
from alpesonline.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from alpesonline.modulos.ordenes.aplicacion.mapeadores import MapeadorOrden
from alpesonline.modulos.ordenes.infraestructura.repositorios import RepositorioOrdenes, RepositorioEventosOrdenes

from pydispatch import dispatcher

@dataclass
class CrearOrden(Comando):
    fecha_creacion: str
    fecha_actualizacion: str
    id: str
    itinerarios: list[ItinerarioDTO]


class CrearOrdenHandler(CrearOrdenBaseHandler):
    
    def handle(self, comando: CrearOrden):
        orden_dto = OrdenDTO(
                fecha_actualizacion=comando.fecha_actualizacion
            ,   fecha_creacion=comando.fecha_creacion
            ,   id=comando.id
            ,   itinerarios=comando.itinerarios)

        orden: Orden = self.fabrica_vuelos.crear_objeto(orden_dto, MapeadorOrden())
        orden.crear_orden(orden)

        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioOrdenes)
        repositorio_eventos = self.fabrica_repositorio.crear_objeto(RepositorioEventosOrdenes)

        from alpesonline.config.db import db

        # TODO Debido al uso de multi-thread el uso de sesiones Flask no es permitido. ¿Como cree que podría implementarse
        # una UnidadDeTrabajo en este caso?
        #UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, orden, repositorio_eventos_func=repositorio_eventos.agregar)
        #UnidadTrabajoPuerto.commit()
        repositorio.agregar(orden)

        for evento in orden.eventos:
            dispatcher.send(signal=f'{type(evento).__name__}Integracion', evento=evento)
            
        db.session.commit()


@comando.register(CrearOrden)
def ejecutar_comando_crear_orden(comando: CrearOrden):
    handler = CrearOrdenHandler()
    handler.handle(comando)
    