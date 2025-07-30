from typing import List, Optional
from ..database_router import DatabaseRouter
from ..models import Empleado, EmpleadoView
import logging

logger = logging.getLogger(__name__)

class EmpleadoRepository:
    def __init__(self):
        self.db_router = DatabaseRouter()

    def get_empleado_sede(self, idEmpleado: int) -> Optional[str]:
        """Determinar en qué sede trabaja un empleado usando las vistas unificadas"""
        try:
            # Verificar en Quito usando la vista dbo.Empleado
            import pyodbc
            from ..config import ConfigQuito, ConfigGuayaquil
            
            conn_quito = pyodbc.connect(ConfigQuito.conn_str())
            cursor_quito = conn_quito.cursor()
            
            cursor_quito.execute("SELECT idEmpleado FROM dbo.Empleado WHERE idEmpleado = ?", (idEmpleado,))
            quito_result = cursor_quito.fetchone()
            cursor_quito.close()
            conn_quito.close()
            
            if quito_result:
                return "Quito"  # Si se encuentra en Quito, es de Quito
            
            # Verificar en Guayaquil usando la vista dbo.Empleado
            conn_guayaquil = pyodbc.connect(ConfigGuayaquil.conn_str())
            cursor_guayaquil = conn_guayaquil.cursor()
            
            cursor_guayaquil.execute("SELECT idEmpleado FROM dbo.Empleado WHERE idEmpleado = ?", (idEmpleado,))
            guayaquil_result = cursor_guayaquil.fetchone()
            cursor_guayaquil.close()
            conn_guayaquil.close()
            
            if guayaquil_result:
                return "Guayaquil"  # Si se encuentra en Guayaquil, es de Guayaquil
            
            return None
            
        except Exception as e:
            logger.error(f"Error determinando sede del empleado {idEmpleado}: {e}")
            return None

    def get_empleado_db(self):
        """Por ahora usando la conexión de Quito para empleados"""
        return self.db_router.get_auth_db()

    def list(self) -> List[Empleado]:
        try:
            db = self.get_empleado_db()
            cur = db.cursor()
            cur.execute("SELECT * FROM dbo.Empleado;")
            cols = [c[0] for c in cur.description]
            rows = cur.fetchall()
            cur.close()
            db.close()
            return [Empleado(**dict(zip(cols, row))) for row in rows]
        except Exception as e:
            logger.error(f"Error en list(): {e}")
            return []

    def authenticate_empleado(self, id_empleado: int, nombre: str) -> Optional[dict]:
        """Autenticar empleado usando las vistas unificadas"""
        try:
            import pyodbc
            from ..config import ConfigQuito, ConfigGuayaquil
            
            # Intentar en Quito primero usando la vista dbo.Empleado
            conn_quito = pyodbc.connect(ConfigQuito.conn_str())
            cursor = conn_quito.cursor()
            
            query = """
                SELECT idEmpleado, nombre, direccion, salario, fechaContratacion, idClinica 
                FROM dbo.Empleado 
                WHERE idEmpleado = ? AND nombre = ?
            """
            
            cursor.execute(query, (id_empleado, nombre))
            row = cursor.fetchone()
            
            if row:
                empleado = EmpleadoView(
                    idEmpleado=row[0],
                    nombre=row[1],
                    direccion=row[2],
                    salario=row[3],
                    fechaContratacion=row[4],
                    idClinica=row[5],
                    sede="Quito"  # Hardcoded ya que estamos en la DB de Quito
                )
                
                cursor.close()
                conn_quito.close()
                
                return {
                    "empleado": empleado,
                    "sede": "Quito",
                    "tipo": "empleado",
                    "idClinica": row[5]
                }
            
            cursor.close()
            conn_quito.close()
            
            # Si no se encuentra en Quito, intentar en Guayaquil
            conn_guayaquil = pyodbc.connect(ConfigGuayaquil.conn_str())
            cursor = conn_guayaquil.cursor()
            
            cursor.execute(query, (id_empleado, nombre))
            row = cursor.fetchone()
            
            if row:
                empleado = EmpleadoView(
                    idEmpleado=row[0],
                    nombre=row[1],
                    direccion=row[2],
                    salario=row[3],
                    fechaContratacion=row[4],
                    idClinica=row[5],
                    sede="Guayaquil"  # Hardcoded ya que estamos en la DB de Guayaquil
                )
                
                cursor.close()
                conn_guayaquil.close()
                
                return {
                    "empleado": empleado,
                    "sede": "Guayaquil", 
                    "tipo": "empleado",
                    "idClinica": row[5]
                }
            
            cursor.close()
            conn_guayaquil.close()
            return None
            
        except Exception as e:
            logger.error(f"Error autenticando empleado: {e}")
            return None

    def create(self, e: Empleado) -> Empleado:
        try:
            db = self.get_empleado_db()
            sql = """
              INSERT INTO dbo.Empleado
                (idEmpleado,nombre,direccion,salario,fechaContratacion,idClinica)
              VALUES (?,?,?,?,?,?)
            """
            cur = db.cursor()
            cur.execute(sql,
               e.idEmpleado, e.nombre, e.direccion, e.salario, e.fechaContratacion, e.idClinica)
            cur.close()
            db.close()
            return e
        except Exception as e:
            logger.error(f"Error en create(): {e}")
            raise

    def update(self, e: Empleado) -> Empleado:
        try:
            db = self.get_empleado_db()
            sql = """
              UPDATE dbo.Empleado
                 SET nombre=?, direccion=?, salario=?, fechaContratacion=?
               WHERE idEmpleado=? AND idClinica=?
            """
            cur = db.cursor()
            cur.execute(sql,
               e.nombre, e.direccion, e.salario, e.fechaContratacion, e.idEmpleado, e.idClinica)
            cur.close()
            db.close()
            return e
        except Exception as e:
            logger.error(f"Error en update(): {e}")
            raise

    def delete(self, idEmpleado: int, idClinica: int):
        try:
            db = self.get_empleado_db()
            sql = "DELETE FROM dbo.Empleado WHERE idEmpleado=? AND idClinica=?"
            cur = db.cursor()
            cur.execute(sql, idEmpleado, idClinica)
            cur.close()
            db.close()
        except Exception as e:
            logger.error(f"Error en delete(): {e}")
            raise

# Instancia global del repositorio
empleado_repository = EmpleadoRepository()
