from fastapi import APIRouter, HTTPException
from typing import List
from ..models import ClienteInfo
from ..repositories.cliente_info import ClienteInfoRepository

router = APIRouter(prefix="/api/cliente-info", tags=["Cliente Info"])
repo = ClienteInfoRepository()

@router.get("/", response_model=List[ClienteInfo])
def get_clientes_info():
    try:
        return repo.list()
    except Exception as e:
        print(f"Error en get_clientes: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{idCliente}/{correo}", response_model=ClienteInfo)
def get_cliente_info(idCliente: int, correo: str):
    cliente = repo.get_by_id_and_email(idCliente, correo)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente

@router.post("/", response_model=ClienteInfo, status_code=201)
def post_cliente_info(cliente: ClienteInfo):
    try:
        return repo.create(cliente)
    except Exception as e:
        print(f"Error en post_cliente: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/", response_model=ClienteInfo)
def put_cliente_info(cliente: ClienteInfo):
    try:
        return repo.update(cliente)
    except Exception as e:
        print(f"Error en put_cliente: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{idCliente}/{correo}", status_code=204)
def del_cliente_info(idCliente: int, correo: str):
    try:
        repo.delete(idCliente, correo)
    except Exception as e:
        print(f"Error en del_cliente: {e}")
        raise HTTPException(status_code=500, detail=str(e))
