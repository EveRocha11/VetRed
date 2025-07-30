from typing import Optional
from app.models import AdminQuito, AdminGuayaquil
from app.database_router import DatabaseRouter
import pyodbc
import logging

logger = logging.getLogger(__name__)

class AdministradorRepository:
    def __init__(self):
        self.db_router = DatabaseRouter()

    def authenticate_admin_quito(self, id_admin: int, nombre: str) -> Optional[AdminQuito]:
        """Autenticar administrador en la sede de Quito"""
        try:
            conn = self.db_router.get_auth_db()  # Conexión a Quito
            cursor = conn.cursor()
            
            query = """
                SELECT idAdmin, nombre, correo, idClinica 
                FROM Admin_Quito 
                WHERE idAdmin = ? AND nombre = ?
            """
            
            cursor.execute(query, (id_admin, nombre))
            row = cursor.fetchone()
            
            if row:
                return AdminQuito(
                    idAdmin=row[0],
                    nombre=row[1],
                    correo=row[2],
                    idClinica=row[3]
                )
            return None
            
        except Exception as e:
            logger.error(f"Error autenticando admin Quito: {e}")
            return None
        finally:
            if 'conn' in locals():
                conn.close()

    def authenticate_admin_guayaquil(self, id_admin: int, nombre: str) -> Optional[AdminGuayaquil]:
        """Autenticar administrador en la sede de Guayaquil"""
        try:
            conn = self.db_router.get_cliente_contacto_db()  # Conexión a Guayaquil
            cursor = conn.cursor()
            
            query = """
                SELECT idAdmin, nombre, correo, idClinica 
                FROM Admin_Guayaquil 
                WHERE idAdmin = ? AND nombre = ?
            """
            
            cursor.execute(query, (id_admin, nombre))
            row = cursor.fetchone()
            
            if row:
                return AdminGuayaquil(
                    idAdmin=row[0],
                    nombre=row[1],
                    correo=row[2],
                    idClinica=row[3]
                )
            return None
            
        except Exception as e:
            logger.error(f"Error autenticando admin Guayaquil: {e}")
            return None
        finally:
            if 'conn' in locals():
                conn.close()

    def authenticate_admin(self, id_admin: int, nombre: str, sede: str = None) -> Optional[dict]:
        """Autenticar administrador en cualquier sede"""
        if sede == "quito":
            admin = self.authenticate_admin_quito(id_admin, nombre)
            if admin:
                return {"admin": admin, "sede": "Quito", "tipo": "administrador"}
        elif sede == "guayaquil":
            admin = self.authenticate_admin_guayaquil(id_admin, nombre)
            if admin:
                return {"admin": admin, "sede": "Guayaquil", "tipo": "administrador"}
        else:
            # Buscar en ambas sedes
            admin_quito = self.authenticate_admin_quito(id_admin, nombre)
            if admin_quito:
                return {"admin": admin_quito, "sede": "Quito", "tipo": "administrador"}
            
            admin_guayaquil = self.authenticate_admin_guayaquil(id_admin, nombre)
            if admin_guayaquil:
                return {"admin": admin_guayaquil, "sede": "Guayaquil", "tipo": "administrador"}
        
        return None

# Instancia global del repositorio
administrador_repository = AdministradorRepository()
