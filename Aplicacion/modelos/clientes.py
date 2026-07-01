from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from aplicacion.modelos.facturas import Factura


class ClienteBase(SQLModel):
    nombre: str
    email: str
    descripcion: str | None = None


class ClienteCrear(ClienteBase):
    pass


class ClienteEditar(ClienteBase):
    pass


class Cliente(ClienteBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    facturas: list["Factura"] = Relationship(
        back_populates="cliente",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )