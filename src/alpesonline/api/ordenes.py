from alpesonline.seedwork.aplicacion.sagas import CoordinadorOrquestacion
import alpesonline.seedwork.presentacion.api as api
import json
from alpesonline.modulos.ordenes.aplicacion.dto import OrdenDTO
from alpesonline.seedwork.dominio.excepciones import ExcepcionDominio

from flask import redirect, render_template, request, session, url_for
from flask import Response
from alpesonline.modulos.ordenes.aplicacion.mapeadores import MapeadorOrdenDTOJson
from alpesonline.modulos.ordenes.aplicacion.comandos.crear_orden import CrearOrden
from alpesonline.modulos.ordenes.aplicacion.queries.obtener_orden import ObtenerOrden
from alpesonline.modulos.ordenes.aplicacion.queries.obtener_todas_ordenes import ObtenerTodasOrdenes
from alpesonline.seedwork.aplicacion.comandos import ejecutar_commando
from alpesonline.seedwork.aplicacion.queries import ejecutar_query

bp = api.crear_blueprint('orden', '/orden')

@bp.route('/crear', methods=('POST',))
def crear_orden_usando_comando():
    try:
        # NOTE Asignamos el valor 'pulsar' para usar la Unidad de trabajo de Pulsar y 
        # no la defecto de SQLAlchemy
        session['uow_metodo'] = 'pulsar'

        orden_dict = request.json

        map_orden = MapeadorOrdenDTOJson()
        orden_dto = map_orden.externo_a_dto(orden_dict)

        comando = CrearOrden(orden_dto.fecha_creacion, orden_dto.fecha_actualizacion, orden_dto.id, orden_dto.itinerarios)
        CoordinadorOrquestacion.inicializar_pasos()
        
        # TODO Reemplaze es todo código sincrono y use el broker de eventos para propagar este comando de forma asíncrona
        # Revise la clase Despachador de la capa de infraestructura
        ejecutar_commando(comando)
        
        return Response('{}', status=202, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')

@bp.route('/orden', methods=('GET',))
@bp.route('/orden/<id>', methods=('GET',))
def dar_orden_usando_query(id=None):
    map_orden = MapeadorOrdenDTOJson()

    if id:
        query_resultado = ejecutar_query(ObtenerOrden(id))
        return map_orden.dto_a_externo(query_resultado.resultado)
    else:
        query_resultado = ejecutar_query(ObtenerTodasOrdenes())
        resultados = []
        
        for orden in query_resultado.resultado:
            resultados.append(map_orden.dto_a_externo(orden))
        
        return resultados