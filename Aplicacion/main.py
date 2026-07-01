from fastapi import FastAPI
from sqlmodel import SQLModel

from Aplicacion.enrutador.clientes import router as clientes_router
from Aplicacion.enrutador.facturas import router as facturas_router
from Aplicacion.enrutador.transacciones import router as transacciones_router

from Aplicacion.modelos.clientes import Cliente
from Aplicacion.modelos.facturas import Factura
from Aplicacion.modelos.transacciones import Transacciones

from Aplicacion.conexion_bd import engine
app = FastAPI(
    title="API Gestión de Clientes",
    description="API para gestionar clientes, facturas y transacciones",
    version="1.0.0"
)

app.include_router(clientes_router)
app.include_router(facturas_router)
app.include_router(transacciones_router)


@app.on_event("startup")
def crear_tablas_inicio():
    SQLModel.metadata.create_all(engine)


@app.get("/")
async def root():
    return {
        "mensaje": "Bienvenido a la API de Gestión de Clientes",
        "versión": "1.0.0",
        "documentación": "/docs"
    }


@app.get("/health")
async def health_check():
    return {"estado": "La API está funcionando correctamente"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)