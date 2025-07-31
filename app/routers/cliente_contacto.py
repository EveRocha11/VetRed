from fastapi import APIRouter, HTTPException
from typing import List
from ..models import ClienteContacto
from ..repositories.cliente_contacto import ClienteContactoRepository
from ..repositories.cliente_info_repository import ClienteInfoRepository

router = APIRouter(prefix="/api/clientes", tags=["Clientes"])
repo = ClienteContactoRepository()
repo_info = ClienteInfoRepository()

@router.get("/", response_model=List[ClienteContacto])
def get_clientes():
    """Obtener clientes filtrados por sede usando vista o tabla"""
    try:
        return repo.list()
    except Exception as e:
        print(f"Error en get_clientes: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.get("/{idCliente}/{correo}", response_model=ClienteContacto)
def get_cliente_contacto(idCliente: int, correo: str):
    try:
        cliente = repo.get_by_id_and_correo(idCliente, correo)
        if cliente:
            return cliente
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    except Exception as e:
        print(f"Error en get_cliente_contacto: {e}")
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
        # Eliminar de ambas tablas usando el repositorio principal
        repo_info.delete(idCliente, correo)
    except Exception as e:
        print(f"Error en del_cliente: {e}")
        raise HTTPException(status_code=500, detail=str(e))
