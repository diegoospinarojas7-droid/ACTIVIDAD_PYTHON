from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from Aplicacion.modelos.facturas import Factura


class TransaccionesBase(SQLModel):
    cantidad: int
    vr_unitario: float
    descripcion: str
    factura_id: int = Field(sa_column_args=[ForeignKey("factura.id", ondelete="CASCADE")])


class TransaccionesCrear(TransaccionesBase):
    pass


class TransaccionesEditar(TransaccionesBase):
    pass


class Transacciones(TransaccionesBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    factura: Optional["Factura"] = Relationship(back_populates="transacciones")