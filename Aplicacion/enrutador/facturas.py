from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from Aplicacion.conexion_bd import get_session
from Aplicacion.modelos.clientes import Cliente
from Aplicacion.modelos.facturas import Factura, FacturaCrear, FacturaEditar

router = APIRouter(prefix="/facturas", tags=["facturas"])


@router.get("", response_model=list[Factura])
async def listar_facturas(session: Session = Depends(get_session)):
    facturas = session.exec(select(Factura)).all()
    return facturas


@router.get("/{id}", response_model=Factura)
async def obtener_factura(id: int, session: Session = Depends(get_session)):
    factura = session.get(Factura, id)
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    return factura


@router.post("", response_model=Factura)
async def crear_factura(datos: FacturaCrear, session: Session = Depends(get_session)):
    cliente = session.get(Cliente, datos.cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    factura_nueva = Factura(**datos.model_dump())
    session.add(factura_nueva)
    session.commit()
    session.refresh(factura_nueva)
    return factura_nueva


@router.put("/{id}", response_model=Factura)
async def editar_factura(id: int, datos: FacturaEditar, session: Session = Depends(get_session)):
    factura = session.get(Factura, id)
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")

    factura.fecha = datos.fecha
    factura.cliente_id = datos.cliente_id
    factura.descripcion = datos.descripcion

    session.add(factura)
    session.commit()
    session.refresh(factura)
    return factura


@router.delete("/{id}")
async def eliminar_factura(id: int, session: Session = Depends(get_session)):
    factura = session.get(Factura, id)
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")

    session.delete(factura)
    session.commit()
    return {"mensaje": "Factura eliminada exitosamente", "factura": factura}