"""DTOs para la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará los DTOs (modelos anémicos) de
la infraestructura del dominio de vuelos

"""

from alpesonline.config.db import db
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, ForeignKey, Integer, Table

import uuid

Base = db.declarative_base()

# Tabla intermedia para tener la relación de muchos a muchos entre la tabla ordenes e itinerarios
ordenes_itinerarios = db.Table(
    "ordenes_itinerarios",
    db.Model.metadata,
    db.Column("orden_id", db.String(40), db.ForeignKey("ordenes.id")),
    db.Column("odo_orden", db.Integer),
    db.Column("segmento_orden", db.Integer),
    db.Column("leg_orden", db.Integer),
    db.Column("fecha_salida", db.DateTime),
    db.Column("fecha_llegada", db.DateTime),
    db.Column("origen_codigo", db.String(10)),
    db.Column("destino_codigo", db.String(10)),
    db.ForeignKeyConstraint(
        ["odo_orden", "segmento_orden", "leg_orden", "fecha_salida", "fecha_llegada", "origen_codigo", "destino_codigo"],
        ["itinerarios.odo_orden", "itinerarios.segmento_orden", "itinerarios.leg_orden", "itinerarios.fecha_salida", "itinerarios.fecha_llegada", "itinerarios.origen_codigo", "itinerarios.destino_codigo"]
    )
)

class Itinerario(db.Model):
    __tablename__ = "itinerarios"
    odo_orden = db.Column(db.Integer, primary_key=True, nullable=False)
    segmento_orden = db.Column(db.Integer, primary_key=True, nullable=False)
    leg_orden = db.Column(db.Integer, primary_key=True, nullable=False)
    fecha_salida = db.Column(db.DateTime, nullable=False, primary_key=True)
    fecha_llegada = db.Column(db.DateTime, nullable=False, primary_key=True)
    origen_codigo = db.Column(db.String(10), nullable=False, primary_key=True)
    destino_codigo= db.Column(db.String(10), nullable=False, primary_key=True)


class Orden(db.Model):
    __tablename__ = "ordenes"
    id = db.Column(db.String(40), primary_key=True)
    fecha_creacion = db.Column(db.DateTime, nullable=False)
    fecha_actualizacion = db.Column(db.DateTime, nullable=False)
    itinerarios = db.relationship('Itinerario', secondary=ordenes_itinerarios, backref='ordenes')

class EventosOrden(db.Model):
    __tablename__ = "eventos_orden"
    id = db.Column(db.String(40), primary_key=True)
    id_entidad = db.Column(db.String(40), nullable=False)
    fecha_evento = db.Column(db.DateTime, nullable=False)
    version = db.Column(db.String(10), nullable=False)
    tipo_evento = db.Column(db.String(100), nullable=False)
    formato_contenido = db.Column(db.String(10), nullable=False)
    nombre_servicio = db.Column(db.String(40), nullable=False)
    contenido = db.Column(db.Text, nullable=False)

class OrdenAnalitica(db.Model):
    __tablename__ = "analitica_ordenes"
    fecha_creacion = db.Column(db.Date, primary_key=True)
    total = db.Column(db.Integer, primary_key=True, nullable=False)