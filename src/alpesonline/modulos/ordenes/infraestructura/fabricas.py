""" Fábricas para la creación de objetos en la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos en la capa de infraestructura del dominio de vuelos

"""

from dataclasses import dataclass, field
from alpesonline.seedwork.dominio.fabricas import Fabrica
from alpesonline.seedwork.dominio.repositorios import Repositorio
from alpesonline.seedwork.infraestructura.vistas import Vista
from alpesonline.modulos.ordenes.infraestructura.vistas import VistaOrden
from alpesonline.modulos.ordenes.dominio.entidades import Orden
from alpesonline.modulos.ordenes.dominio.repositorios import RepositorioProveedores, RepositorioOrdenes, RepositorioEventosOrdenes
from .repositorios import RepositorioOrdenesSQLAlchemy, RepositorioProveedoresSQLAlchemy, RepositorioEventosOrdenSQLAlchemy
from .excepciones import ExcepcionFabrica

@dataclass
class FabricaRepositorio(Fabrica):
    def crear_objeto(self, obj: type, mapeador: any = None) -> Repositorio:
        if obj == RepositorioOrdenes:
            return RepositorioOrdenesSQLAlchemy()
        elif obj == RepositorioProveedores:
            return RepositorioProveedoresSQLAlchemy()
        elif obj == RepositorioEventosOrdenes:
            return RepositorioEventosOrdenSQLAlchemy()
        else:
            raise ExcepcionFabrica(f'No existe fábrica para el objeto {obj}')

@dataclass
class FabricaVista(Fabrica):
    def crear_objeto(self, obj: type, mapeador: any = None) -> Vista:
        if obj == Orden:
            return VistaOrden()
        else:
            raise ExcepcionFabrica(f'No existe fábrica para el objeto {obj}')