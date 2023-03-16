from alpesonline.seedwork.infraestructura.vistas import Vista
from alpesonline.modulos.ordenes.dominio.entidades import Orden
from alpesonline.config.db import db
from .dto import Orden as OrdenDTO

class VistaOrden(Vista):
    def obtener_todos(self):
        ordenes_dto = db.session.query(OrdenDTO).all()
        ordenes = list()

        for orden_dto in ordenes_dto:
            ordenes.append(Orden(id=orden_dto.id, 
                fecha_creacion=orden_dto.fecha_creacion, 
                fecha_actualizacion=orden_dto.fecha_actualizacion))
        
        return ordenes

    def obtener_por(self, id=None, estado=None, id_cliente=None, **kwargs) -> [Orden]:
        params = dict()

        if id:
            params['id'] = str(id)
        
        if estado:
            params['estado'] = str(estado)
        
        if id_cliente:
            params['id_cliente'] = str(id_cliente)
            
        # TODO Convierta OrdenDTO a Orden y valide que la consulta es correcta
        return db.session.query(OrdenDTO).filter_by(**params)
