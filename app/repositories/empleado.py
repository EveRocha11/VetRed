from typing import List, Optional
from ..database_router import DatabaseRouter
from ..models import Empleado, EmpleadoView
import logging

logger = logging.getLogger(__name__)

class EmpleadoRepository:
    def __init__(self):
        self.db_router = DatabaseRouter()

    def get_empleado_sede(self, idEmpleado: int) -> Optional[str]:
        """Determinar en qué sede trabaja un empleado usando las vistas dbo.Empleado"""
        try:
            import pyodbc
            from ..config import ConfigQuito, ConfigGuayaquil
            
            # Verificar en Quito usando la vista dbo.Empleado
            try:
                conn_quito = pyodbc.connect(ConfigQuito.conn_str())
                cursor_quito = conn_quito.cursor()
                
                cursor_quito.execute("SELECT idEmpleado FROM dbo.Empleado WHERE idEmpleado = ?", (idEmpleado,))
                quito_result = cursor_quito.fetchone()
                cursor_quito.close()
                conn_quito.close()
                
                if quito_result:
                    return "Quito"
            except Exception as e:
                logger.warning(f"Error consultando Quito para empleado {idEmpleado}: {e}")
            
            # Verificar en Guayaquil usando la vista dbo.Empleado
            try:
                conn_guayaquil = pyodbc.connect(ConfigGuayaquil.conn_str())
                cursor_guayaquil = conn_guayaquil.cursor()
                
                cursor_guayaquil.execute("SELECT idEmpleado FROM dbo.Empleado WHERE idEmpleado = ?", (idEmpleado,))
                guayaquil_result = cursor_guayaquil.fetchone()
                cursor_guayaquil.close()
                conn_guayaquil.close()
                
                if guayaquil_result:
                    return "Guayaquil"
            except Exception as e:
                logger.warning(f"Error consultando Guayaquil para empleado {idEmpleado}: {e}")
            
            return None
            
        except Exception as e:
            logger.error(f"Error determinando sede del empleado {idEmpleado}: {e}")
            return None

    def get_empleado_db(self):
        """Por ahora usando la conexión de Quito para empleados"""
        return self.db_router.get_auth_db()

    def list(self, sede_admin: str = None) -> List[Empleado]:
        """Listar empleados usando la vista dbo.Empleado con filtro por sede"""
        try:
            import pyodbc
            from ..config import ConfigQuito
            
            # Usar siempre la conexión de Quito (que tiene acceso a ambas sedes)
            conn = pyodbc.connect(ConfigQuito.conn_str())
            
            # Determinar el idClinica según la sede del admin
            if sede_admin == "Guayaquil":
                id_clinica_filter = 2  # Guayaquil = idClinica 2
            else:
                id_clinica_filter = 1  # Quito = idClinica 1 (por defecto)
            
            cursor = conn.cursor()
            
            # Usar la vista dbo.Empleado con filtro por idClinica
            query = "SELECT * FROM dbo.Empleado WHERE idClinica = ?"
            logger.info(f"Consultando empleados para sede {sede_admin} (idClinica={id_clinica_filter})")
            cursor.execute(query, (id_clinica_filter,))
            
            cols = [c[0] for c in cursor.description]
            rows = cursor.fetchall()
            
            logger.info(f"Encontrados {len(rows)} empleados para sede {sede_admin}")
            
            empleados = []
            for row in rows:
                empleado_data = dict(zip(cols, row))
                empleados.append(Empleado(**empleado_data))
            
            cursor.close()
            conn.close()
            
            return empleados
            
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
        """Crear empleado usando la vista dbo.Empleado"""
        conn = None
        cursor = None
        try:
            import pyodbc
            from ..config import ConfigQuito, ConfigGuayaquil
            # Determinar qué conexión usar según idClinica
            if e.idClinica == 2:  # Guayaquil
                conn = pyodbc.connect(ConfigGuayaquil.conn_str())
            else:  # Quito (idClinica == 1 o por defecto)
                conn = pyodbc.connect(ConfigQuito.conn_str())
            cursor = conn.cursor()
            # Activar XACT_ABORT para evitar errores con linked server
            cursor.execute("SET XACT_ABORT ON")
            # Insertar usando la vista dbo.Empleado
            sql = """
              INSERT INTO dbo.Empleado
                (idEmpleado, nombre, direccion, salario, fechaContratacion, idClinica)
              VALUES (?, ?, ?, ?, ?, ?)
            """
            logger.info(f"Creando empleado {e.idEmpleado} en sede {('Guayaquil' if e.idClinica == 2 else 'Quito')}")
            cursor.execute(sql, e.idEmpleado, e.nombre, e.direccion, e.salario, e.fechaContratacion, e.idClinica)
            conn.commit()
            logger.info(f"Empleado {e.idEmpleado} creado exitosamente")
            return e
        except Exception as e:
            logger.error(f"Error en create(): {e}")
            if conn:
                conn.rollback()
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def update(self, e: Empleado) -> Empleado:
        """Actualizar empleado usando la vista dbo.Empleado"""
        conn = None
        cursor = None
        try:
            import pyodbc
            from ..config import ConfigQuito, ConfigGuayaquil
            # Determinar qué conexión usar según idClinica
            if e.idClinica == 2:  # Guayaquil
                conn = pyodbc.connect(ConfigGuayaquil.conn_str())
            else:  # Quito (idClinica == 1 o por defecto)
                conn = pyodbc.connect(ConfigQuito.conn_str())
            cursor = conn.cursor()
            # Activar XACT_ABORT para evitar errores con linked server
            cursor.execute("SET XACT_ABORT ON")
            # Verificar si el empleado existe usando la vista
            cursor.execute("SELECT * FROM dbo.Empleado WHERE idEmpleado=? AND idClinica=?", e.idEmpleado, e.idClinica)
            existe = cursor.fetchone()
            logger.info(f"[DEBUG] Empleado existe en vista dbo.Empleado: {existe is not None}")
            # Actualizar usando la vista dbo.Empleado
            sql = """
              UPDATE dbo.Empleado
                 SET nombre=?, direccion=?, salario=?, fechaContratacion=?
               WHERE idEmpleado=? AND idClinica=?
            """
            logger.info(f"Actualizando empleado {e.idEmpleado} en sede {('Guayaquil' if e.idClinica == 2 else 'Quito')}")
            cursor.execute(sql, e.nombre, e.direccion, e.salario, e.fechaContratacion, e.idEmpleado, e.idClinica)
            # Verificar que se actualizó al menos una fila
            if cursor.rowcount == 0:
                raise Exception(f"No se encontró el empleado {e.idEmpleado} para actualizar")
            conn.commit()
            logger.info(f"Empleado {e.idEmpleado} actualizado exitosamente")
            return e
        except Exception as e:
            logger.error(f"Error en update(): {e}")
            if conn:
                conn.rollback()
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def delete(self, idEmpleado: int, idClinica: int):
        """Eliminar empleado usando la vista dbo.Empleado"""
        conn = None
        cursor = None
        try:
            import pyodbc
            from ..config import ConfigQuito, ConfigGuayaquil
            # Determinar qué conexión usar según idClinica
            if idClinica == 2:  # Guayaquil
                conn = pyodbc.connect(ConfigGuayaquil.conn_str())
            else:  # Quito (idClinica == 1 o por defecto)
                conn = pyodbc.connect(ConfigQuito.conn_str())
            cursor = conn.cursor()
            # Activar XACT_ABORT para evitar errores con linked server
            cursor.execute("SET XACT_ABORT ON")
            # Eliminar usando la vista dbo.Empleado
            sql = "DELETE FROM dbo.Empleado WHERE idEmpleado=? AND idClinica=?"
            logger.info(f"Eliminando empleado {idEmpleado} de sede {('Guayaquil' if idClinica == 2 else 'Quito')}")
            cursor.execute(sql, idEmpleado, idClinica)
            # Verificar que se eliminó al menos una fila
            if cursor.rowcount == 0:
                raise Exception(f"No se encontró el empleado {idEmpleado} para eliminar")
            conn.commit()
            logger.info(f"Empleado {idEmpleado} eliminado exitosamente")
        except Exception as e:
            logger.error(f"Error en delete(): {e}")
            if conn:
                conn.rollback()
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

# Instancia global del repositorio
empleado_repository = EmpleadoRepository()