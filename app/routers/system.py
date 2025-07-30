from fastapi import APIRouter
from app.database_router import db_router

router = APIRouter()

@router.get("/api/system/health")
async def system_health():
    """Endpoint para verificar el estado del sistema y conexiones"""
    
    health = db_router.health_check()
    connections = db_router.get_available_connections()
    
    return {
        "status": "healthy" if health['total_connections'] > 0 else "degraded",
        "connections": health,
        "active_servers": connections,
        "routing": {
            "auth_database": "guayaquil",
            "cliente_contacto_database": "quito" if health['quito'] else "guayaquil",
            "failover_active": not health['quito']
        }
    }

@router.get("/api/system/connections")
async def get_connections():
    """Obtener información detallada de todas las conexiones"""
    return {
        "available_connections": db_router.get_available_connections(),
        "health_status": db_router.health_check()
    }
