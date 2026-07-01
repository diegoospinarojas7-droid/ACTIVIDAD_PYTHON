from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from Aplicacion.conexion_bd import get_session
from Aplicacion.modelos.clientes import Cliente, ClienteCrear, ClienteEditar

router = APIRouter(prefix="/clientes", tags=["clientes"])


@router.get("", response_model=List[Cliente])
async def listar_clientes(session: Session = Depends(get_session)):
    clientes = session.exec(select(Cliente)).all()
    return clientes


@router.get("/{id}", response_model=Cliente)
async def obtener_cliente(id: int, session: Session = Depends(get_session)):
    cliente = session.get(Cliente, id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente


@router.post("", response_model=Cliente)
async def crear_cliente(datos: ClienteCrear, session: Session = Depends(get_session)):
    nuevo_cliente = Cliente(**datos.model_dump())
    session.add(nuevo_cliente)
    session.commit()
    session.refresh(nuevo_cliente)
    return nuevo_cliente


@router.put("/{id}", response_model=Cliente)
async def editar_cliente(id: int, datos: ClienteEditar, session: Session = Depends(get_session)):
    cliente = session.get(Cliente, id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    cliente.nombre = datos.nombre
    cliente.email = datos.email
    cliente.descripcion = datos.descripcion
    session.add(cliente)
    session.commit()
    session.refresh(cliente)
    return cliente


@router.delete("/{id}")
async def eliminar_cliente(id: int, session: Session = Depends(get_session)):
    cliente = session.get(Cliente, id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    session.delete(cliente)
    session.commit()
    return {"mensaje": "Cliente eliminado exitosamente"}