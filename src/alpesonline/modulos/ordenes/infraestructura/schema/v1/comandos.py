from pulsar.schema import *
from dataclasses import dataclass, field
from alpesonline.seedwork.infraestructura.schema.v1.comandos import (ComandoIntegracion)
from alpesonline.seedwork.infraestructura.utils import time_millis
import uuid


class ComandoCrearOrdenPayload(ComandoIntegracion):
    id_usuario = String()
    id_correlacion = String()
    fecha_creacion = Long()
    # TODO Cree los records para itinerarios

class ComandoCrearOrden(ComandoIntegracion):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String()
    type = String()
    datacontenttype = String()
    service_name = String()
    data = ComandoCrearOrdenPayload()
