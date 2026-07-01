from sqlalchemy import inspect
from sqlmodel import SQLModel

from app.main import app
from app.modelos.facturas import Factura
from app.modelos.transacciones import Transacciones
from conexion import engine


def test_las_tablas_de_facturas_y_transacciones_existen():
    SQLModel.metadata.create_all(engine)
    inspector = inspect(engine)
    assert inspector.has_table(Factura.__tablename__)
    assert inspector.has_table(Transacciones.__tablename__)