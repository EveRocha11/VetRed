from fastapi import APIRouter, HTTPException
from typing import List
from app.models import ClienteInfo
from app.repositories.cliente_info_repository import cliente_info_repository

router = APIRouter(prefix="/api/clientes", tags=["Clientes"])

@router.get("/", response_model=List[ClienteInfo])
def get_clientes(sede_admin: str = "Quito"):
    """Obtiene todos los clientes"""
    try:
        return cliente_info_repository.list()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al obtener clientes")

@router.post("/", response_model=ClienteInfo, status_code=201)
def post_cliente(cliente: ClienteInfo):
    """Crea un nuevo cliente"""
    try:
        return cliente_info_repository.create(cliente)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al crear cliente")

@router.delete("/{idCliente}/{correo}", status_code=200)
def delete_cliente(idCliente: int, correo: str):
    """Elimina un cliente por idCliente y correo"""
    try:
        # Verificar si el cliente existe antes de eliminar
        if not cliente_info_repository.exists(idCliente, correo):
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        
        # Eliminar el cliente
        cliente_info_repository.delete(idCliente, correo)
        
        # Retornar una respuesta JSON válida
        return {"message": "Cliente eliminado exitosamente", "idCliente": idCliente, "correo": correo}
    except HTTPException:
        raise  # Re-lanzar HTTPExceptions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar cliente: {str(e)}")

