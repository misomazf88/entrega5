import pulsar,_pulsar  
from pulsar.schema import *
import uuid
import time
import logging
import traceback
import datetime

from alpesonline.modulos.ordenes.infraestructura.schema.v1.eventos import EventoOrdenCreada
from alpesonline.modulos.ordenes.infraestructura.schema.v1.comandos import ComandoCrearOrden

from alpesonline.modulos.ordenes.aplicacion.comandos.crear_orden import CrearOrden
from alpesonline.seedwork.aplicacion.comandos import ejecutar_commando

from alpesonline.modulos.ordenes.infraestructura.proyecciones import ProyeccionOrdenesLista, ProyeccionOrdenesTotales
from alpesonline.seedwork.infraestructura.proyecciones import ejecutar_proyeccion
from alpesonline.seedwork.infraestructura import utils
from alpesonline.modulos.ordenes.aplicacion.dto import ItinerarioDTO

def suscribirse_a_eventos(app=None):
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://broker:6650')
        consumidor = cliente.subscribe('eventos-orden', consumer_type=_pulsar.ConsumerType.Shared,subscription_name='alpesonline-sub-eventos', schema=AvroSchema(EventoOrdenCreada))

        while True:
            mensaje = consumidor.receive()
            datos = mensaje.value().data
            print(f'Evento recibido: {datos}')
            
            # TODO Identificar el tipo de CRUD del evento: Creacion, actualización o eliminación.
            ejecutar_proyeccion(ProyeccionOrdenesTotales(datos.fecha_creacion, ProyeccionOrdenesTotales.ADD), app=app)
            ejecutar_proyeccion(ProyeccionOrdenesLista(datos.id_orden, datos.id_cliente, datos.estado, datos.fecha_creacion, datos.fecha_creacion), app=app)
            
            consumidor.acknowledge(mensaje)     

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos!')
        traceback.print_exc()
        if cliente:
            cliente.close()

def suscribirse_a_comandos(app=None):
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://broker:6650')
        consumidor = cliente.subscribe('comando-crear-orden', consumer_type=_pulsar.ConsumerType.Shared, subscription_name='alpesonline-sub-comando-crear-orden', schema=AvroSchema(ComandoCrearOrden))

        while True:
            mensaje = consumidor.receive()
            valor = mensaje.value()

            print(f'Comando recibido: {mensaje.value()}')
            
            fecha_creacion = utils.millis_a_datetime(valor.data.fecha_creacion).strftime('%Y-%m-%dT%H:%M:%SZ')
            id_orden = str(uuid.uuid4())
            itinerarios = [ItinerarioDTO(odos=[])]
            # TODO Debe poderse crear los itinerarios

            try:
                with app.app_context():
                    comando = CrearOrden(fecha_creacion, fecha_creacion, id_orden, itinerarios)
                    ejecutar_commando(comando)
            except:
                logging.error('ERROR: Procesando eventos!')
                traceback.print_exc()

            consumidor.acknowledge(mensaje)     
            
        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de comandos!')
        traceback.print_exc()
        if cliente:
            cliente.close()