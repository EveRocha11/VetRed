from fastapi import APIRouter, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from app.models import LoginRequest, RegisterRequest, ClienteInfo
from app.repositories.cliente_info import cliente_info_repository
from app.repositories.empleado import empleado_repository
from app.repositories.administrador import administrador_repository
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/api/auth/login")
async def login(login_data: LoginRequest):
    """Validar credenciales de login según tipo de usuario"""
    try:
        tipo_usuario = login_data.tipo_usuario.lower()
        identificador = login_data.identificador
        nombre = login_data.nombre
        
        if tipo_usuario == "cliente":
            # Para clientes: identificador es correo, validar con nombre
            cliente = cliente_info_repository.get_by_email_and_name(identificador, nombre)
            
            if not cliente:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Credenciales inválidas"
                )
            
            return {
                "message": "Login exitoso",
                "user": {
                    "tipo": "cliente",
                    "idCliente": cliente.idCliente,
                    "correo": cliente.correo,
                    "nombre": cliente.nombre,
                    "redirect": "/usuario"
                }
            }
            
        elif tipo_usuario == "empleado":
            # Para empleados: identificador es idEmpleado, validar con nombre
            try:
                id_empleado = int(identificador)
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="ID de empleado inválido"
                )
            
            empleado_data = empleado_repository.authenticate_empleado(id_empleado, nombre)
            
            if not empleado_data:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Credenciales inválidas"
                )
            
            empleado = empleado_data["empleado"]
            return {
                "message": "Login exitoso",
                "user": {
                    "tipo": "empleado",
                    "idEmpleado": empleado.idEmpleado,
                    "nombre": empleado.nombre,
                    "sede": empleado_data["sede"],
                    "idClinica": empleado.idClinica,
                    "redirect": "/empleado"
                }
            }
            
        elif tipo_usuario == "administrador":
            # Para administradores: identificador es idAdmin, validar con nombre
            try:
                id_admin = int(identificador)
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="ID de administrador inválido"
                )
            
            admin_data = administrador_repository.authenticate_admin(id_admin, nombre)
            
            if not admin_data:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Credenciales inválidas"
                )
            
            admin = admin_data["admin"]
            return {
                "message": "Login exitoso",
                "user": {
                    "tipo": "administrador",
                    "idAdmin": admin.idAdmin,
                    "nombre": admin.nombre,
                    "correo": admin.correo,
                    "sede": admin_data["sede"],
                    "idClinica": admin.idClinica,
                    "redirect": "/admin"
                }
            }
        
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tipo de usuario inválido"
            )
        
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
