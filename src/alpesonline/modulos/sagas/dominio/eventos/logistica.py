from __future__ import annotations
from dataclasses import dataclass, field
import uuid
from alpesonline.seedwork.dominio.eventos import (EventoDominio)
from datetime import datetime

class EventoLogistica(EventoDominio):
    ...

@dataclass
class OrdenLogisticaConfirmada(EventoLogistica):
    id_orden: uuid.UUID = None
    id_correlacion: str = None
    fecha_actualizacion: datetime = None

@dataclass
class ConfirmacionLogisticaRevertida(EventoLogistica):
    id_orden: uuid.UUID = None
    id_correlacion: str = None
    fecha_actualizacion: datetime = None

@dataclass
class ConfirmacionFallida(EventoLogistica):
    id_orden: uuid.UUID = None
    id_correlacion: str = None
    fecha_actualizacion: datetime = None