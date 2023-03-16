from pulsar.schema import *
from .utils import time_millis
import uuid

class ConfirmarOrdenPayload(Record):
    id_correlacion = String(),
    orden_id = String(),
 
class RevertirConfirmacionPayload(Record):
    id = String()
    id_correlacion = String()
    orden_id = String()

class ComandoConfirmarOrden(Record):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String(default="v1")
    type = String(default="ConfirmarOrden")
    datacontenttype = String()
    service_name = String(default="logistica.alpesonline")
    data = ConfirmarOrdenPayload

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class ComandoRevertirConfirmacion(Record):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String(default="v1")
    type = String(default="RevertirConfirmacion")
    datacontenttype = String()
    service_name = String(default="logistica.alpesonline")
    data = RevertirConfirmacionPayload

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
