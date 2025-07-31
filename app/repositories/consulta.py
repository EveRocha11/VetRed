from typing import List, Optional
from datetime import date
from ..database_router import DatabaseRouter
from ..models import Consulta
import logging

logger = logging.getLogger(__name__)

class ConsultaRepository:
    def __init__(self):
        self.db_router = DatabaseRouter()

    def get_consulta_db(self):
        """Por ahora usando la conexión de Quito para consultas"""
        return self.db_router.get_auth_db()

    def list(self, sede_admin: str = None) -> List[Consulta]:
        """Listar consultas usando la vista dbo.Consulta con filtro por sede"""
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
            
            # Usar la vista dbo.Consulta con filtro por idClinica
            query = "SELECT * FROM dbo.Consulta WHERE idClinica = ?"
            logger.info(f"Consultando consultas para sede {sede_admin} (idClinica={id_clinica_filter})")
            cursor.execute(query, (id_clinica_filter,))
            
            cols = [c[0] for c in cursor.description]
            rows = cursor.fetchall()
            
            logger.info(f"Encontradas {len(rows)} consultas para sede {sede_admin}")
            
            consultas = []
            for row in rows:
                consulta_data = dict(zip(cols, row))
                consultas.append(Consulta(**consulta_data))
            
            cursor.close()
            conn.close()
            
            return consultas
            
        except Exception as e:
            logger.error(f"Error en list consultas: {e}")
            return []

    def get_by_empleado_fecha(self, idEmpleado: int, fecha: date) -> List[dict]:
        """Obtener consultas de un empleado para una fecha específica usando vista dbo.Consulta"""
        try:
            # Primero determinar la sede del empleado
            from ..repositories.empleado import EmpleadoRepository
            empleado_repo = EmpleadoRepository()
            sede = empleado_repo.get_empleado_sede(idEmpleado)
            
            if not sede:
                logger.warning(f"No se pudo determinar la sede del empleado {idEmpleado}")
                return []
            
            consultas = []
            
            # Usar la vista dbo.Consulta según la sede
            import pyodbc
            try:
                if sede == "Quito":
                    from ..config import ConfigQuito
                    conn = pyodbc.connect(ConfigQuito.conn_str())
                else:  # Guayaquil
                    from ..config import ConfigGuayaquil
                    conn = pyodbc.connect(ConfigGuayaquil.conn_str())
                
                cursor = conn.cursor()
                
                # Query usando la vista dbo.Consulta
                query = """
                    SELECT 
                        idConsulta,
                        fecha,
                        hora,
                        motivo,
                        estado,
                        observaciones,
                        idEmpleado,
                        idMascota
                    FROM dbo.Consulta
                    WHERE idEmpleado = ? AND fecha = ?
                    ORDER BY hora
                """
                
                cursor.execute(query, (idEmpleado, fecha))
                rows = cursor.fetchall()
                
                for row in rows:
                    consulta_dict = {
                        'idConsulta': row[0],
                        'fecha': row[1].strftime('%Y-%m-%d') if row[1] else None,
                        'hora': str(row[2]) if row[2] else None,
                        'motivo': row[3],
                        'estado': row[4],
                        'observaciones': row[5],
                        'idEmpleado': row[6],
                        'idMascota': row[7]
                    }
                    consultas.append(consulta_dict)
                
                cursor.close()
                conn.close()
                
            except Exception as e:
                logger.error(f"Error consultando vista dbo.Consulta en {sede}: {e}")
                return []
            
            return consultas
            
        except Exception as e:
            logger.error(f"Error obteniendo consultas del empleado {idEmpleado}: {e}")
            return []

    def create(self, c: Consulta) -> Consulta:
        """Crear consulta usando la vista dbo.Consulta"""
        conn = None
        cursor = None
        try:
            import pyodbc
            from ..config import ConfigQuito, ConfigGuayaquil
            
            # Determinar qué conexión usar según idClinica
            if c.idClinica == 2:  # Guayaquil
                conn = pyodbc.connect(ConfigGuayaquil.conn_str())
            else:  # Quito (idClinica == 1 o por defecto)
                conn = pyodbc.connect(ConfigQuito.conn_str())
            
            cursor = conn.cursor()

            # Habilitar XACT_ABORT para evitar transacciones anidadas
            cursor.execute("SET XACT_ABORT ON")
            # Insertar usando la vista dbo.Consulta
            sql = """
              INSERT INTO dbo.Consulta
                (idConsulta, fecha, hora, motivo, estado, observaciones, idClinica, idEmpleado, idMascota)
              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            
            logger.info(f"Creando consulta {c.idConsulta} en sede {('Guayaquil' if c.idClinica == 2 else 'Quito')}")
            cursor.execute(sql, c.idConsulta, c.fecha, c.hora, c.motivo,
                         c.estado, c.observaciones, c.idClinica,
                         c.idEmpleado, c.idMascota)
            
            conn.commit()
            logger.info(f"Consulta {c.idConsulta} creada exitosamente")
            
            return c
            
        except Exception as e:
            logger.error(f"Error creando consulta: {e}")
            if conn:
                conn.rollback()
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def update_observaciones(self, idConsulta: int, observaciones: str) -> bool:
        """Actualizar observaciones de una consulta usando la vista dbo.Consulta"""
        try:
            # Primero encontrar en qué sede está la consulta
            sede = self._find_consulta_sede(idConsulta)
            if not sede:
                logger.warning(f"No se pudo encontrar la consulta {idConsulta} en ninguna sede")
                return False
            
            import pyodbc
            if sede == "Quito":
                from ..config import ConfigQuito
                conn = pyodbc.connect(ConfigQuito.conn_str())
            else:  # Guayaquil
                from ..config import ConfigGuayaquil
                conn = pyodbc.connect(ConfigGuayaquil.conn_str())
            
            cur = conn.cursor()
            # Habilitar XACT_ABORT para evitar transacciones anidadas
            cursor.execute("SET XACT_ABORT ON")
            # Usar la vista dbo.Consulta en lugar de las tablas base
            cur.execute(
                "UPDATE dbo.Consulta SET observaciones = ? WHERE idConsulta = ?",
                (observaciones, idConsulta)
            )
            rows_affected = cur.rowcount
            conn.commit()
            cur.close()
            conn.close()
            
            if rows_affected > 0:
                logger.info(f"Observaciones actualizadas en {sede} para consulta {idConsulta}")
                return True
            else:
                logger.warning(f"No se encontró la consulta {idConsulta} para actualizar")
                return False
            
        except Exception as e:
            logger.error(f"Error actualizando observaciones de consulta {idConsulta}: {e}")
            return False

    def update_estado(self, idConsulta: int, estado: str) -> bool:
        """Actualizar estado de una consulta usando la vista dbo.Consulta"""
        try:
            # Primero encontrar en qué sede está la consulta
            sede = self._find_consulta_sede(idConsulta)
            if not sede:
                logger.warning(f"No se pudo encontrar la consulta {idConsulta} en ninguna sede")
                return False
            
            import pyodbc
            if sede == "Quito":
                from ..config import ConfigQuito
                conn = pyodbc.connect(ConfigQuito.conn_str())
            else:  # Guayaquil
                from ..config import ConfigGuayaquil
                conn = pyodbc.connect(ConfigGuayaquil.conn_str())
            
            cur = conn.cursor()
            # Habilitar XACT_ABORT para evitar transacciones anidadas
            cur.execute("SET XACT_ABORT ON")
            # Usar la vista dbo.Consulta en lugar de las tablas base
            cur.execute(
                "UPDATE dbo.Consulta SET estado = ? WHERE idConsulta = ?",
                (estado, idConsulta)
            )
            rows_affected = cur.rowcount
            conn.commit()
            cur.close()
            conn.close()
            
            if rows_affected > 0:
                logger.info(f"Estado actualizado en {sede} para consulta {idConsulta}: {estado}")
                return True
            else:
                logger.warning(f"No se encontró la consulta {idConsulta} para actualizar")
                return False
            
        except Exception as e:
            logger.error(f"Error actualizando estado de consulta {idConsulta}: {e}")
            return False

    def update(self, c: Consulta) -> Consulta:
        """Actualizar consulta completa usando la vista dbo.Consulta"""
        conn = None
        cursor = None
        try:
            import pyodbc
            from ..config import ConfigQuito, ConfigGuayaquil
            
            # Determinar qué conexión usar según idClinica
            if c.idClinica == 2:  # Guayaquil
                conn = pyodbc.connect(ConfigGuayaquil.conn_str())
            else:  # Quito (idClinica == 1 o por defecto)
                conn = pyodbc.connect(ConfigQuito.conn_str())
            
            cursor = conn.cursor()
            # Habilitar XACT_ABORT para evitar transacciones anidadas
            cursor.execute("SET XACT_ABORT ON")
            # Actualizar usando la vista dbo.Consulta
            sql = """
              UPDATE dbo.Consulta
                 SET fecha=?, hora=?, motivo=?, estado=?, observaciones=?, idEmpleado=?, idMascota=? 
               WHERE idConsulta=? AND idClinica=?
            """
            
            logger.info(f"Actualizando consulta {c.idConsulta} en sede {('Guayaquil' if c.idClinica == 2 else 'Quito')}")
            cursor.execute(sql, c.fecha, c.hora, c.motivo, c.estado, c.observaciones,
                         c.idEmpleado, c.idMascota, c.idConsulta, c.idClinica)
            
            # Verificar que se actualizó al menos una fila
            if cursor.rowcount == 0:
                raise Exception(f"No se encontró la consulta {c.idConsulta} para actualizar")
            
            conn.commit()
            logger.info(f"Consulta {c.idConsulta} actualizada exitosamente")
            
            return c
            
        except Exception as e:
            logger.error(f"Error actualizando consulta: {e}")
            if conn:
                conn.rollback()
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def delete(self, idConsulta: int, idClinica: int) -> bool:
        """Eliminar consulta usando la vista dbo.Consulta"""
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
            
            # Activar XACT_ABORT para evitar problemas con transacciones anidadas
            cursor.execute("SET XACT_ABORT ON")
            
            # Primero, verificar que la consulta existe
            query_check = "SELECT COUNT(*) FROM dbo.Consulta WHERE idConsulta = ? AND idClinica = ?"
            cursor.execute(query_check, (idConsulta, idClinica))
            exists = cursor.fetchone()[0]

            if exists == 0:
                logger.error(f"Consulta {idConsulta} no encontrada para eliminar.")
                return False  # No se encontró la consulta
            
            # Eliminar usando la vista dbo.Consulta
            sql = "DELETE FROM dbo.Consulta WHERE idConsulta=? AND idClinica=?"
            cursor.execute(sql, idConsulta, idClinica)
            
            # Verificar que se eliminó al menos una fila
            if cursor.rowcount == 0:
                return False  # No se encontró la consulta para eliminar
            
            conn.commit()
            logger.info(f"Consulta {idConsulta} eliminada exitosamente")
            return True
        except Exception as e:
            logger.error(f"Error eliminando consulta: {e}")
            if conn:
                conn.rollback()
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def _find_consulta_sede(self, idConsulta: int) -> Optional[str]:
        """Encontrar en qué sede está una consulta específica usando la vista dbo.Consulta"""
        try:
            import pyodbc
            from ..config import ConfigQuito, ConfigGuayaquil
            
            # Buscar en Quito primero
            try:
                conn_quito = pyodbc.connect(ConfigQuito.conn_str())
                cur = conn_quito.cursor()
                cur.execute("SELECT idConsulta FROM dbo.Consulta WHERE idConsulta = ?", (idConsulta,))
                if cur.fetchone():
                    cur.close()
                    conn_quito.close()
                    return "Quito"
                cur.close()
                conn_quito.close()
            except Exception as e:
                logger.error(f"Error buscando en Quito: {e}")
            
            # Buscar en Guayaquil
            try:
                conn_guayaquil = pyodbc.connect(ConfigGuayaquil.conn_str())
                cur = conn_guayaquil.cursor()
                cur.execute("SELECT idConsulta FROM dbo.Consulta WHERE idConsulta = ?", (idConsulta,))
                if cur.fetchone():
                    cur.close()
                    conn_guayaquil.close()
                    return "Guayaquil"
                cur.close()
                conn_guayaquil.close()
            except Exception as e:
                logger.error(f"Error buscando en Guayaquil: {e}")
            
            return None
            
        except Exception as e:
            logger.error(f"Error determinando sede de consulta {idConsulta}: {e}")
            return None

    def get_by_id(self, idConsulta: int, idClinica: int) -> Optional[Consulta]:
        """Obtener una consulta por idConsulta e idClinica usando la vista dbo.Consulta"""
        try:
            import pyodbc
            from ..config import ConfigQuito, ConfigGuayaquil
            # Determinar qué conexión usar según idClinica
            if idClinica == 2:
                conn = pyodbc.connect(ConfigGuayaquil.conn_str())
            else:
                conn = pyodbc.connect(ConfigQuito.conn_str())
            cursor = conn.cursor()
            query = "SELECT * FROM dbo.Consulta WHERE idConsulta = ? AND idClinica = ?"
            cursor.execute(query, (idConsulta, idClinica))
            row = cursor.fetchone()
            if row:
                cols = [c[0] for c in cursor.description]
                consulta_data = dict(zip(cols, row))
                consulta = Consulta(**consulta_data)
            else:
                consulta = None
            cursor.close()
            conn.close()
            return consulta
        except Exception as e:
            logger.error(f"Error en get_by_id: {e}")
            return None

# Instancia global del repositorio
consulta_repository = ConsultaRepository()
