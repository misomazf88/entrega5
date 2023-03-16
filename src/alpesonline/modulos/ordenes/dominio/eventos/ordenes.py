from __future__ import annotations
from dataclasses import dataclass, field
import uuid
from alpesonline.seedwork.dominio.eventos import (EventoDominio)
from datetime import datetime

class EventoOrden(EventoDominio):
    ...


@dataclass
class OrdenCreada(EventoOrden):
    id_orden: uuid.UUID = None
    id_cliente: uuid.UUID = None
    estado: str = None
    fecha_creacion: datetime = None
    monto: float = None
    monto_vat: float = None
    
@dataclass
class CreacionOrdenFallida(EventoOrden):
    id_orden: uuid.UUID = None
    id_cliente: uuid.UUID = None
    estado: str = None
    fecha_creacion: datetime = None
    monto: float = None
    monto_vat: float = None

@dataclass
class OrdenCancelada(EventoOrden):
    id_orden: uuid.UUID = None
    fecha_actualizacion: datetime = None

@dataclass
class OrdenAprobada(EventoOrden):
    id_orden: uuid.UUID = None
    fecha_actualizacion: datetime = None

@dataclass
class OrdenPagada(EventoOrden):
    id_orden: uuid.UUID = None
    fecha_actualizacion: datetime = None

@dataclass
class AprobacionOrdenFallida(EventoOrden):
    id_orden: uuid.UUID = None
    fecha_actualizacion: datetime = None


