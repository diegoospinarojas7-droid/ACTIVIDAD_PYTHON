from pathlib import Path
import os

import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session


db_path = Path("test_facturas.db")
if db_path.exists():
    db_path.unlink()

os.environ["DATABASE_URL"] = f"sqlite:///{db_path}"

from main import app
from app.modelos.facturas import Factura
from conexion import engine


@pytest.fixture(autouse=True)
def setup_db():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    yield
    SQLModel.metadata.drop_all(engine)
    if db_path.exists():
        db_path.unlink()


def test_crear_y_listar_facturas():
    client = TestClient(app)

    response_cliente = client.post(
        "/clientes",
        json={"nombre": "Ana", "email": "ana@test.com", "descripcion": "Cliente prueba"},
    )
    assert response_cliente.status_code == 200
    cliente_id = response_cliente.json()["id"]

    response_factura = client.post(
        "/facturas",
        json={"cliente_id": cliente_id, "descripcion": "Factura prueba"},
    )
    assert response_factura.status_code == 200
    body = response_factura.json()
    assert body["cliente_id"] == cliente_id
    assert body["descripcion"] == "Factura prueba"

    response_lista = client.get("/facturas")
    assert response_lista.status_code == 200
    data = response_lista.json()
    assert len(data) == 1
    assert data[0]["descripcion"] == "Factura prueba"


def test_la_factura_expone_sus_relaciones_virtuales():
    client = TestClient(app)

    response_cliente = client.post(
        "/clientes",
        json={"nombre": "Luis", "email": "luis@test.com", "descripcion": "Cliente con factura"},
    )
    assert response_cliente.status_code == 200
    cliente_id = response_cliente.json()["id"]

    response_factura = client.post(
        "/facturas",
        json={"cliente_id": cliente_id, "descripcion": "Factura con relación"},
    )
    assert response_factura.status_code == 200
    factura_id = response_factura.json()["id"]

    response_transaccion = client.post(
        "/transacciones",
        json={"cantidad": 2, "vr_unitario": 15.5, "descripcion": "Producto", "factura_id": factura_id},
    )
    assert response_transaccion.status_code == 200

    with Session(engine) as session:
        factura = session.get(Factura, factura_id)
        assert factura is not None
        assert factura.cliente is not None
        assert factura.cliente.nombre == "Luis"
        assert len(factura.transacciones) == 1
        assert factura.transacciones[0].descripcion == "Producto"


def test_eliminar_cliente_con_facturas_y_transacciones():
    client = TestClient(app)

    response_cliente = client.post(
        "/clientes",
        json={"nombre": "Carlos", "email": "carlos@test.com", "descripcion": "Cliente con datos"},
    )
    assert response_cliente.status_code == 200
    cliente_id = response_cliente.json()["id"]

    response_factura = client.post(
        "/facturas",
        json={"cliente_id": cliente_id, "descripcion": "Factura para eliminar"},
    )
    assert response_factura.status_code == 200
    factura_id = response_factura.json()["id"]

    response_transaccion = client.post(
        "/transacciones",
        json={"cantidad": 1, "vr_unitario": 10.0, "descripcion": "Producto eliminado", "factura_id": factura_id},
    )
    assert response_transaccion.status_code == 200

    response_delete = client.delete(f"/clientes/{cliente_id}")
    assert response_delete.status_code == 200

    response_get = client.get("/clientes")
    assert response_get.status_code == 200
    assert all(item["id"] != cliente_id for item in response_get.json())b