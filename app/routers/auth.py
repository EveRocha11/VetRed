from fastapi import APIRouter, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from app.models import LoginRequest, RegisterRequest, ClienteInfo
from app.repositories.cliente_info import cliente_info_repository
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/api/auth/login")
async def login(login_data: LoginRequest):
    """Validar credenciales de login"""
    try:
        # En este caso, usamos el correo como username y el idCliente como password
        # Esto es temporal hasta que tengas un sistema de passwords más robusto
        try:
            id_cliente = int(login_data.password)  # El password será el ID del cliente
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales inválidas"
            )
        
        # Validar que existe el cliente con ese ID y correo
        cliente = cliente_info_repository.get_by_id_and_email(id_cliente, login_data.correo)
        
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales inválidas"
            )
        
        return {
            "message": "Login exitoso",
            "user": {
                "idCliente": cliente.idCliente,
                "correo": cliente.correo,
                "nombre": cliente.nombre
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en login: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.post("/api/auth/register")
async def register(register_data: RegisterRequest):
    """Registrar nuevo cliente"""
    try:
        # Verificar si ya existe
        if cliente_info_repository.exists(register_data.idCliente, register_data.correo):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Cliente ya existe con ese ID y correo"
            )
        
        # Crear nuevo cliente
        nuevo_cliente = ClienteInfo(
            idCliente=register_data.idCliente,
            correo=register_data.correo,
            nombre=register_data.nombre
        )
        
        cliente_creado = cliente_info_repository.create(nuevo_cliente)
        
        return {
            "message": "Registro exitoso",
            "user": {
                "idCliente": cliente_creado.idCliente,
                "correo": cliente_creado.correo,
                "nombre": cliente_creado.nombre
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en registro: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )
