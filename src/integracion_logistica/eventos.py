from pulsar.schema import *
from .utils import time_millis
import uuid

class OrdenConfirmada(Record):
    id = String(),
    id_correlacion = String(),
    orden_id = String()
    fecha_confirmacion = Long()
 
class ConfirmacionRevertida(Record):
    id = String()
    id_correlacion = String()
    orden_id = String()
    fecha_actualizacion = Long()

class EventoConfirmacionLogistica(Record):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String(default="v1")
    type = String(default="EventoConfirmacionLogistica")
    datacontenttype = String()
    service_name = String(default="logistica.alpesonline")
    confirmacion_revertida = ConfirmacionRevertida
    orden_confirmada = OrdenConfirmada

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
