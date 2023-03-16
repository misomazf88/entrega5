from __future__ import annotations
from dataclasses import dataclass, field
import uuid
from alpesonline.seedwork.dominio.eventos import (EventoDominio)
from datetime import datetime

class EventoPago(EventoDominio):
    ...

@dataclass
class OrdenPagada(EventoPago):
    id_orden: uuid.UUID = None
    id_correlacion: str = None
    monto: float = None
    monto_vat: float = None
    fecha_actualizacion: datetime = None

@dataclass
class OrdenFallida(EventoPago):
    id_orden: uuid.UUID = None
    id_correlacion: str = None
    monto: float = None
    monto_vat: float = None
    fecha_actualizacion: datetime = None

@dataclass
class PagoRevertido(EventoPago):
    id_orden: uuid.UUID = None
    id_correlacion: str = None
    monto: float = None
    monto_vat: float = None
    fecha_actualizacion: datetime = None