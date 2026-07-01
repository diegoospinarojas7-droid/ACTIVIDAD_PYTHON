from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from Aplicacion.modelos.clientes import Cliente
    from Aplicacion.modelos.transacciones import Transacciones


class FacturaBase(SQLModel):
    fecha: datetime = Field(default_factory=datetime.now)
    cliente_id: int = Field(sa_column_args=[ForeignKey("cliente.id", ondelete="CASCADE")])
    descripcion: str | None = None


class FacturaCrear(FacturaBase):
    pass


class FacturaEditar(FacturaBase):
    pass


class Factura(FacturaBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    cliente: Optional["Cliente"] = Relationship(back_populates="facturas")
    transacciones: list["Transacciones"] = Relationship(
        back_populates="factura",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )