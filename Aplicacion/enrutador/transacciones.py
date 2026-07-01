from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from Aplicacion.conexion_bd import get_session
from Aplicacion.modelos.facturas import Factura
from Aplicacion.modelos.transacciones import (
    Transacciones,
    TransaccionesCrear,
    TransaccionesEditar,
)

router = APIRouter(prefix="/transacciones", tags=["transacciones"])


@router.get("", response_model=list[Transacciones])
async def listar_transacciones(session: Session = Depends(get_session)):
    return session.exec(select(Transacciones)).all()


@router.get("/{id}", response_model=Transacciones)
async def obtener_transaccion(id: int, session: Session = Depends(get_session)):
    transaccion = session.get(Transacciones, id)
    if not transaccion:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    return transaccion


@router.post("", response_model=Transacciones)
async def crear_transaccion(datos: TransaccionesCrear, session: Session = Depends(get_session)):
    factura = session.get(Factura, datos.factura_id)
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")

    nueva_transaccion = Transacciones(**datos.model_dump())
    session.add(nueva_transaccion)
    session.commit()
    session.refresh(nueva_transaccion)
    return nueva_transaccion


@router.put("/{id}", response_model=Transacciones)
async def editar_transaccion(id: int, datos: TransaccionesEditar, session: Session = Depends(get_session)):
    transaccion = session.get(Transacciones, id)
    if not transaccion:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")

    transaccion.cantidad = datos.cantidad
    transaccion.vr_unitario = datos.vr_unitario
    transaccion.descripcion = datos.descripcion
    transaccion.factura_id = datos.factura_id

    session.add(transaccion)
    session.commit()
    session.refresh(transaccion)
    return transaccion


@router.delete("/{id}")
async def eliminar_transaccion(id: int, session: Session = Depends(get_session)):
    transaccion = session.get(Transacciones, id)
    if not transaccion:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")

    session.delete(transaccion)
    session.commit()
    return {"mensaje": "Transacción eliminada", "transaccion": transaccion}


@router.get("/factura/{factura_id}", response_model=list[Transacciones])
async def obtener_transacciones_por_factura(factura_id: int, session: Session = Depends(get_session)):
    transacciones_factura = session.exec(select(Transacciones).where(Transacciones.factura_id == factura_id)).all()
    if not transacciones_factura:
        raise HTTPException(status_code=404, detail="No hay transacciones para esta factura")
    return transacciones_factura
