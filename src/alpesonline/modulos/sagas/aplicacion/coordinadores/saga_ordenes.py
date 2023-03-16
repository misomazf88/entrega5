from alpesonline.seedwork.aplicacion.sagas import CoordinadorOrquestacion, Transaccion, Inicio, Fin
from alpesonline.seedwork.aplicacion.comandos import Comando
from alpesonline.seedwork.dominio.eventos import EventoDominio, EventoIntegracion

from alpesonline.modulos.sagas.aplicacion.comandos.inventario import PagarOrden, RevertirPago
from alpesonline.modulos.sagas.aplicacion.comandos.logistica import ConfirmarOrden, RevertirConfirmacion
from alpesonline.modulos.ordenes.aplicacion.comandos.crear_orden import CrearOrden
from alpesonline.modulos.ordenes.aplicacion.comandos.aprobar_orden import AprobarOrden
from alpesonline.modulos.ordenes.aplicacion.comandos.cancelar_orden import CancelarOrden
from alpesonline.modulos.ordenes.dominio.eventos.ordenes import OrdenCreada, OrdenCancelada, OrdenAprobada, CreacionOrdenFallida, AprobacionOrdenFallida
from alpesonline.modulos.sagas.dominio.eventos.pagos import OrdenFallida, OrdenPagada, PagoRevertido
from alpesonline.modulos.sagas.dominio.eventos.logistica import OrdenLogisticaConfirmada, ConfirmacionLogisticaRevertida, ConfirmacionFallida


class CoordinadorOrdenes(CoordinadorOrquestacion):

    def inicializar_pasos(self):
        self.pasos = [
            Inicio(index=0, comando=CrearOrden, evento=OrdenCreada, error=CreacionOrdenFallida, compensacion=CancelarOrden),
            Transaccion(index=1, comando=PagarOrden, evento=OrdenPagada, error=OrdenFallida, compensacion=RevertirPago),
            Transaccion(index=2, comando=ConfirmarOrden, evento=OrdenLogisticaConfirmada, error=ConfirmacionFallida, compensacion=ConfirmacionLogisticaRevertida),
            Transaccion(index=3, comando=AprobarOrden, evento=OrdenAprobada, error=AprobacionOrdenFallida, compensacion=CancelarOrden),
            Fin(index=4)
        ]

    def iniciar(self):
        self.persistir_en_saga_log(self.pasos[0])
    
    def terminar(self):
        self.persistir_en_saga_log(self.pasos[-1])

    def persistir_en_saga_log(self, mensaje):
        ...

    def construir_comando(self, evento: EventoDominio, tipo_comando: type):
        ...

    def oir_mensaje(mensaje):
        from pydispatch import dispatcher
        from alpesonline.modulos.ordenes.aplicacion.handlers import HandlerOrdenIntegracion
        from alpesonline.modulos.ordenes.dominio.eventos.ordenes import OrdenCreada, OrdenCancelada, OrdenAprobada, OrdenPagada
        dispatcher.connect(HandlerOrdenIntegracion.handle_orden_creada, signal=f'{OrdenCreada.__name__}Integracion')
        dispatcher.connect(HandlerOrdenIntegracion.handle_orden_cancelada, signal=f'{OrdenCancelada.__name__}Integracion')
        dispatcher.connect(HandlerOrdenIntegracion.handle_orden_pagada, signal=f'{OrdenPagada.__name__}Integracion')
        dispatcher.connect(HandlerOrdenIntegracion.handle_orden_aprobada, signal=f'{OrdenAprobada.__name__}Integracion')
        if isinstance(mensaje, EventoIntegracion):
            coordinador = CoordinadorOrdenes()
            coordinador.procesar_evento(mensaje)
        else:
            raise NotImplementedError("El mensaje no es evento de Dominio")