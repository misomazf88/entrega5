"""Entidades del dominio de vuelos

En este archivo usted encontrará las entidades del dominio de vuelos

"""

from __future__ import annotations
from dataclasses import dataclass, field
import datetime
import uuid

import alpesonline.modulos.ordenes.dominio.objetos_valor as ov
from alpesonline.modulos.ordenes.dominio.eventos.ordenes import OrdenCreada, OrdenAprobada, OrdenCancelada, OrdenPagada
from alpesonline.seedwork.dominio.entidades import Locacion, AgregacionRaiz, Entidad

@dataclass
class Aeropuerto(Locacion):
    codigo: ov.Codigo = field(default_factory=ov.Codigo)
    nombre: ov.NombreAero = field(default_factory=ov.NombreAero)

    def __str__(self) -> str:
        return self.codigo.codigo.upper()

@dataclass
class Proveedor(Entidad):
    codigo: ov.Codigo = field(default_factory=ov.Codigo)
    nombre: ov.NombreAero = field(default_factory=ov.NombreAero)
    itinerarios: list[ov.Itinerario] = field(default_factory=list[ov.Itinerario])

    def obtener_itinerarios(self, odos: list[Odo], parametros: ParametroBusca):
        return self.itinerarios

@dataclass
class Pasajero(Entidad):
    clase: ov.Clase = field(default_factory=ov.Clase)
    tipo: ov.TipoPasajero = field(default_factory=ov.TipoPasajero)

@dataclass
class Orden(AgregacionRaiz):
    id_cliente: uuid.UUID = field(hash=True, default=None)
    estado: ov.EstadoOrden = field(default=ov.EstadoOrden.PENDIENTE)
    itinerarios: list[ov.Itinerario] = field(default_factory=list[ov.Itinerario])

    def crear_orden(self, orden: Orden):
        self.id_cliente = orden.id_cliente
        self.estado = orden.estado
        self.itinerarios = orden.itinerarios
        self.fecha_creacion = datetime.datetime.now()

        #self.agregar_evento(OrdenCreada(id_orden=self.id, id_cliente=self.id_cliente, estado=self.estado.name, fecha_creacion=self.fecha_creacion))
        # TODO Agregar evento de compensación

    def aprobar_orden(self):
        self.estado = ov.EstadoOrden.APROBADA
        self.fecha_actualizacion = datetime.datetime.now()

        self.agregar_evento(OrdenAprobada(self.id, self.fecha_actualizacion))
        # TODO Agregar evento de compensación

    def cancelar_orden(self):
        self.estado = ov.EstadoOrden.CANCELADA
        self.fecha_actualizacion = datetime.datetime.now()

        self.agregar_evento(OrdenCancelada(self.id, self.fecha_actualizacion))
        # TODO Agregar evento de compensación
    
    def pagar_orden(self):
        self.estado = ov.EstadoOrden.PAGADA
        self.fecha_actualizacion = datetime.datetime.now()

        self.agregar_evento(OrdenPagada(self.id, self.fecha_actualizacion))
        # TODO Agregar evento de compensación
