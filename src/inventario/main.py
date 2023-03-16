from fastapi import FastAPI
# from cliente.config.api import app_configs, settings
# from cliente.api.v1.router import router as v1

# from cliente.modulos.infraestructura.consumidores import suscribirse_a_topico
# from .eventos import EventoUsuario, UsuarioValidado, UsuarioDesactivado, UsuarioRegistrado, TipoCliente

# from cliente.modulos.infraestructura.despachadores import Despachador
# from cliente.seedwork.infraestructura import utils

import asyncio
import time
import traceback
import uvicorn

from pydantic import BaseSettings
from typing import Any

from .eventos import EventoPago, PagoRevertido, OrdenPagada
from .comandos import ComandoPagarOrden, ComandoRevertirPago, RevertirPagoPayload, PagarOrdenPayload
from .consumidores import suscribirse_a_topico
from .despachadores import Despachador

from . import utils

class Config(BaseSettings):
    APP_VERSION: str = "1"

settings = Config()
app_configs: dict[str, Any] = {"title": "Pagos AlpesOnline"}

app = FastAPI(**app_configs)
tasks = list()

@app.on_event("startup")
async def app_startup():
    global tasks
    task1 = asyncio.ensure_future(suscribirse_a_topico("evento-pago", "sub-pagos", EventoPago))
    #task2 = asyncio.ensure_future(suscribirse_a_topico("comando-pagar-orden", "sub-com-pagos-ordenr", ComandoPagarOrden))
    #task3 = asyncio.ensure_future(suscribirse_a_topico("comando-revertir-pago", "sub-com-pagos-revertir", ComandoRevertirPago))
    tasks.append(task1)
    #tasks.append(task2)
    #tasks.append(task3)

@app.on_event("shutdown")
def shutdown_event():
    global tasks
    for task in tasks:
        task.cancel()