"""
Sistema de enrutamiento de base de datos para VetRed
Determina qué base de datos usar para cada tipo de operación
"""
from .db import db_guayaquil, db_quito
import logging

logger = logging.getLogger(__name__)

class DatabaseRouter:
    """Enrutador para determinar qué base de datos usar"""
    
    @staticmethod
    def get_auth_db():
        """Base de datos para autenticación (Cliente_Info) - está en Quito"""
        if db_quito:
            return db_quito
        return db_guayaquil  # Fallback
    
    @staticmethod
    def get_cliente_contacto_db():
        """Base de datos para Cliente_Contacto - está en Guayaquil"""
        return db_guayaquil
    
    @staticmethod
    def get_empleado_db():
        """Base de datos para empleados"""
        return db_guayaquil
    
    @staticmethod
    def get_consulta_db():
        """Base de datos para consultas"""
        return db_guayaquil
    
    @staticmethod
    def get_available_connections():
        """Obtener información de conexiones disponibles"""
        connections = {}
        
        if db_guayaquil:
            guayaquil_info = db_guayaquil.test_connection()
            if guayaquil_info:
                connections['guayaquil'] = guayaquil_info
        
        if db_quito:
            quito_info = db_quito.test_connection()
            if quito_info:
                connections['quito'] = quito_info
        
        return connections
    
    @staticmethod
    def health_check():
        """Verificar estado de todas las conexiones"""
        status = {
            'guayaquil': False,
            'quito': False,
            'total_connections': 0
        }
        
        if db_guayaquil:
            try:
                info = db_guayaquil.test_connection()
                if info:
                    status['guayaquil'] = True
                    status['total_connections'] += 1
            except:
                pass
        
        if db_quito:
            try:
                info = db_quito.test_connection()
                if info:
                    status['quito'] = True
                    status['total_connections'] += 1
            except:
                pass
        
        return status

# Instancia global del router
db_router = DatabaseRouter()
