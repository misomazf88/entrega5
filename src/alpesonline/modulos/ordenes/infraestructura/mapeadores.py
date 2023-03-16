""" Mapeadores para la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará los diferentes mapeadores
encargados de la transformación entre formatos de dominio y DTOs

"""

from alpesonline.seedwork.dominio.repositorios import Mapeador
from alpesonline.seedwork.infraestructura.utils import unix_time_millis
from alpesonline.modulos.ordenes.dominio.objetos_valor import NombreAero, Odo, Leg, Segmento, Itinerario, CodigoIATA
from alpesonline.modulos.ordenes.dominio.entidades import Proveedor, Aeropuerto, Orden
from alpesonline.modulos.ordenes.dominio.eventos.ordenes import OrdenAprobada, OrdenCancelada, OrdenAprobada, OrdenPagada, OrdenCreada, EventoOrden

from .dto import Orden as OrdenDTO
from .dto import Itinerario as ItinerarioDTO
from .excepciones import NoExisteImplementacionParaTipoFabricaExcepcion
from pulsar.schema import *

class MapadeadorEventosOrden(Mapeador):

    # Versiones aceptadas
    versions = ('v1',)

    LATEST_VERSION = versions[0]

    def __init__(self):
        self.router = {
            OrdenCreada: self._entidad_a_orden_creada,
            OrdenAprobada: self._entidad_a_orden_aprobada,
            OrdenCancelada: self._entidad_a_orden_cancelada,
            OrdenPagada: self._entidad_a_orden_pagada
        }

    def obtener_tipo(self) -> type:
        return EventoOrden.__class__

    def es_version_valida(self, version):
        for v in self.versions:
            if v == version:
                return True
        return False

    def _entidad_a_orden_creada(self, entidad: OrdenCreada, version=LATEST_VERSION):
        def v1(evento):
            from .schema.v1.eventos import OrdenCreadaPayload, EventoOrdenCreada

            payload = OrdenCreadaPayload(
                id_orden=str(evento.id_orden), 
                id_cliente=str(evento.id_cliente), 
                estado=str(evento.estado), 
                fecha_creacion=int(unix_time_millis(evento.fecha_creacion))
            )
            evento_integracion = EventoOrdenCreada(id=str(evento.id))
            evento_integracion.id = str(evento.id)
            evento_integracion.time = int(unix_time_millis(evento.fecha_creacion))
            evento_integracion.specversion = str(version)
            evento_integracion.type = 'OrdenCreada'
            evento_integracion.datacontenttype = 'AVRO'
            evento_integracion.service_name = 'alpesonline'
            evento_integracion.data = payload

            return evento_integracion
                    
        if not self.es_version_valida(version):
            raise Exception(f'No se sabe procesar la version {version}')

        if version == 'v1':
            return v1(entidad)       

    def _entidad_a_orden_aprobada(self, entidad: OrdenAprobada, version=LATEST_VERSION):
        # TODO
        raise NotImplementedError
    
    def _entidad_a_orden_cancelada(self, entidad: OrdenCancelada, version=LATEST_VERSION):
        # TODO
        raise NotImplementedError
    
    def _entidad_a_orden_pagada(self, entidad: OrdenPagada, version=LATEST_VERSION):
        # TODO
        raise NotImplementedError

    def entidad_a_dto(self, entidad: EventoOrden, version=LATEST_VERSION) -> OrdenDTO:
        if not entidad:
            raise NoExisteImplementacionParaTipoFabricaExcepcion
        func = self.router.get(entidad.__class__, None)

        if not func:
            raise NoExisteImplementacionParaTipoFabricaExcepcion

        return func(entidad, version=version)

    def dto_a_entidad(self, dto: OrdenDTO, version=LATEST_VERSION) -> Orden:
        raise NotImplementedError


class MapeadorOrden(Mapeador):
    _FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'

    def _procesar_itinerario_dto(self, itinerarios_dto: list) -> list[Itinerario]:
        itin_dict = dict()
        
        for itin in itinerarios_dto:
            destino = Aeropuerto(codigo=itin.destino_codigo, nombre=None)
            origen = Aeropuerto(codigo=itin.origen_codigo, nombre=None)
            fecha_salida = itin.fecha_salida
            fecha_llegada = itin.fecha_llegada

            itin_dict.setdefault(str(itin.odo_orden),{}).setdefault(str(itin.segmento_orden), {}).setdefault(str(itin.leg_orden), Leg(fecha_salida, fecha_llegada, origen, destino))

        odos = list()
        for k, odos_dict in itin_dict.items():
            segmentos = list()
            for k, seg_dict in odos_dict.items():
                legs = list()
                for k, leg in seg_dict.items():
                    legs.append(leg)
                segmentos.append(Segmento(legs))
            odos.append(Odo(segmentos))

        return [Itinerario(odos)]

    def _procesar_itinerario(self, itinerario: any) -> list[ItinerarioDTO]:
        itinerarios_dto = list()

        for i, odo in enumerate(itinerario.odos):
            for j, seg in enumerate(odo.segmentos):
                for k, leg in enumerate(seg.legs):
                    itinerario_dto = ItinerarioDTO()
                    itinerario_dto.destino_codigo = leg.destino.codigo
                    itinerario_dto.origen_codigo = leg.origen.codigo
                    itinerario_dto.fecha_salida = leg.fecha_salida
                    itinerario_dto.fecha_llegada = leg.fecha_llegada
                    itinerario_dto.leg_orden = k
                    itinerario_dto.segmento_orden = j
                    itinerario_dto.odo_orden = i

                    itinerarios_dto.append(itinerario_dto)

        return itinerarios_dto

    def obtener_tipo(self) -> type:
        return Orden.__class__

    def entidad_a_dto(self, entidad: Orden) -> OrdenDTO:
        
        orden_dto = OrdenDTO()
        orden_dto.fecha_creacion = entidad.fecha_creacion
        orden_dto.fecha_actualizacion = entidad.fecha_actualizacion
        orden_dto.id = str(entidad.id)

        itinerarios_dto = list()
        
        for itinerario in entidad.itinerarios:
            itinerarios_dto.extend(self._procesar_itinerario(itinerario))

        orden_dto.itinerarios = itinerarios_dto

        return orden_dto

    def dto_a_entidad(self, dto: OrdenDTO) -> Orden:
        orden = Orden(dto.id, dto.fecha_creacion, dto.fecha_actualizacion)
        orden.itinerarios = list()

        itinerarios_dto: list[ItinerarioDTO] = dto.itinerarios

        orden.itinerarios.extend(self._procesar_itinerario_dto(itinerarios_dto))
        
        return orden