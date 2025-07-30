from fastapi import APIRouter, HTTPException
from typing import List
from ..models import ClienteContacto
from ..repositories.cliente_contacto import ClienteContactoRepository

router = APIRouter(prefix="/api/clientes", tags=["Clientes"])
repo = ClienteContactoRepository()

@router.get("/", response_model=List[ClienteContacto])
def get_clientes(sede_admin: str = "Quito"):
    """Obtener clientes filtrados por sede usando vista o tabla"""
    try:
        return repo.list(sede_admin=sede_admin)
    except Exception as e:
        print(f"Error en get_clientes: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.post("/", response_model=ClienteContacto, status_code=201)
def post_cliente(cliente: ClienteContacto):
    try:
        return repo.create(cliente)
    except Exception as e:
        print(f"Error en post_cliente: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.put("/", response_model=ClienteContacto)
def put_cliente(cliente: ClienteContacto):
    try:
        return repo.update(cliente)
    except Exception as e:
        print(f"Error en put_cliente: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.delete("/{idCliente}/{correo}", status_code=204)
def del_cliente(idCliente: int, correo: str):
    try:
        repo.delete(idCliente, correo)
    except Exception as e:
        print(f"Error en del_cliente: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")
