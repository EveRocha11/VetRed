from typing import List, Optional
from app.database_router import db_router
from app.models import ClienteInfo
import logging

logger = logging.getLogger(__name__)

class ClienteInfoRepository:
    def __init__(self):
        self.db = db_router.get_auth_db()
    
    def list(self) -> List[ClienteInfo]:
        """Obtener todos los clientes de Cliente_Info"""
        cursor = None
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT idCliente, correo, nombre FROM Cliente_Info")
            rows = cursor.fetchall()
            
            return [
                ClienteInfo(
                    idCliente=row[0],
                    correo=row[1],
                    nombre=row[2]
                ) for row in rows
            ]
            
        except Exception as e:
            logger.error(f"Error listando clientes info: {e}")
            raise
        finally:
            if cursor:
                cursor.close()

    def update(self, cliente: ClienteInfo) -> ClienteInfo:
        cursor = None
        try:
            cursor = self.db.cursor()
            cursor.execute(
                "UPDATE Cliente_Info SET nombre = ? WHERE idCliente = ? AND correo = ?",
                (cliente.nombre, cliente.idCliente, cliente.correo)
            )
            self.db.commit()
            return cliente
        except Exception as e:
            logger.error(f"Error actualizando cliente info: {e}")
            self.db.rollback()
            raise
        finally:
            if cursor:
                cursor.close()
    
    def get_by_email(self, correo: str) -> Optional[ClienteInfo]:
        """Obtener cliente por correo electrónico"""
        cursor = None
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT idCliente, correo, nombre FROM Cliente_Info WHERE correo = ?", (correo,))
            row = cursor.fetchone()
            
            if row:
                return ClienteInfo(
                    idCliente=row[0],
                    correo=row[1],
                    nombre=row[2]
                )
            return None
            
        except Exception as e:
            logger.error(f"Error obteniendo cliente por email {correo}: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
    
    def get_by_email_and_name(self, correo: str, nombre: str) -> Optional[ClienteInfo]:
        """Obtener cliente por correo y nombre (validación de login)"""
        cursor = None
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT idCliente, correo, nombre FROM Cliente_Info WHERE correo = ? AND nombre = ?", 
                         (correo, nombre))
            row = cursor.fetchone()
            
            if row:
                return ClienteInfo(
                    idCliente=row[0],
                    correo=row[1],
                    nombre=row[2]
                )
            return None
            
        except Exception as e:
            logger.error(f"Error validando cliente por correo y nombre {correo}, {nombre}: {e}")
            raise
        finally:
            if cursor:
                cursor.close()

    def get_by_id_and_email(self, idCliente: int, correo: str) -> Optional[ClienteInfo]:
        """Obtener cliente por ID y correo (validación de login)"""
        cursor = None
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT idCliente, correo, nombre FROM Cliente_Info WHERE idCliente = ? AND correo = ?", 
                         (idCliente, correo))
            row = cursor.fetchone()
            
            if row:
                return ClienteInfo(
                    idCliente=row[0],
                    correo=row[1],
                    nombre=row[2]
                )
            return None
            
        except Exception as e:
            logger.error(f"Error validando cliente {idCliente}, {correo}: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
    
    def create(self, cliente: ClienteInfo) -> ClienteInfo:
        """Crear nuevo cliente"""
        cursor = None
        try:
            cursor = self.db.cursor()
            cursor.execute(
                "INSERT INTO Cliente_Info (idCliente, correo, nombre) VALUES (?, ?, ?)",
                (cliente.idCliente, cliente.correo, cliente.nombre)
            )
            self.db.commit()
            return cliente
            
        except Exception as e:
            logger.error(f"Error creando cliente info: {e}")
            if cursor:
                self.db.rollback()
            raise
        finally:
            if cursor:
                cursor.close()
    
    def exists(self, idCliente: int, correo: str) -> bool:
        """Verificar si existe un cliente con ID y correo específicos"""
        cursor = None
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT COUNT(*) FROM Cliente_Info WHERE idCliente = ? AND correo = ?", 
                         (idCliente, correo))
            count = cursor.fetchone()[0]
            return count > 0
            
        except Exception as e:
            logger.error(f"Error verificando existencia de cliente: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
    

    def delete(self, idCliente: int, correo: str):
        cursor = None
        conn_gye = None
        cur_gye = None
        try:
            # Eliminar de Cliente_Info (Quito)
            cursor = self.db.cursor()
            cursor.execute(
                "DELETE FROM Cliente_Info WHERE idCliente = ? AND correo = ?",
                (idCliente, correo)
            )
            self.db.commit()

            # Eliminar de Cliente_Contacto (Guayaquil)
            import pyodbc
            from app.config import ConfigGuayaquil
            conn_gye = pyodbc.connect(ConfigGuayaquil.conn_str())
            cur_gye = conn_gye.cursor()
            cur_gye.execute(
                "DELETE FROM Cliente_Contacto WHERE idCliente = ? AND correo = ?",
                (idCliente, correo)
            )
            conn_gye.commit()

            logger.info(f"Cliente {idCliente} con correo {correo} eliminado de todas las tablas.")
        except Exception as e:
            logger.error(f"Error eliminando cliente info: {e}")
            try:
                if self.db:
                    self.db.rollback()
            except Exception as rb1:
                logger.warning(f"Error en rollback de db principal: {rb1}")
            try:
                if conn_gye:
                    conn_gye.rollback()
            except Exception as rb2:
                logger.warning(f"Error en rollback de Guayaquil: {rb2}")
            raise
        finally:
            if cursor:
                try:
                    cursor.close()
                except:
                    pass
            if cur_gye:
                try:
                    cur_gye.close()
                except:
                    pass
            if conn_gye:
                try:
                    conn_gye.close()
                except:
                    pass



# Instancia global
cliente_info_repository = ClienteInfoRepository()
