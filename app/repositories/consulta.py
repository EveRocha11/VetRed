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

    def list(self) -> List[Consulta]:
        try:
            db = self.get_consulta_db()
            cur = db.cursor()
            # Apunta a tu VIEW dbo.Consulta
            cur.execute("SELECT * FROM dbo.Consulta;")
            cols = [c[0] for c in cur.description]
            rows = cur.fetchall()
            cur.close()
            db.close()
            return [Consulta(**dict(zip(cols, row))) for row in rows]
        except Exception as e:
            logger.error(f"Error en list consultas: {e}")
            return []

    def get_by_empleado_fecha(self, idEmpleado: int, fecha: date) -> List[dict]:
        """Obtener consultas de un empleado para una fecha específica usando vistas unificadas"""
        try:
            # Primero determinar la sede del empleado
            from ..repositories.empleado import EmpleadoRepository
            empleado_repo = EmpleadoRepository()
            sede = empleado_repo.get_empleado_sede(idEmpleado)
            
            if not sede:
                logger.warning(f"No se pudo determinar la sede del empleado {idEmpleado}")
                return []
            
            consultas = []
            
            # Usar la vista unificada según la sede
            import pyodbc
            if sede == "Quito":
                from ..config import ConfigQuito
                conn = pyodbc.connect(ConfigQuito.conn_str())
            else:  # Guayaquil
                from ..config import ConfigGuayaquil
                conn = pyodbc.connect(ConfigGuayaquil.conn_str())
            
            cur = conn.cursor()
            
            # Query usando la vista unificada dbo.Consulta (usando solo columnas existentes)
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
            
            cur.execute(query, (idEmpleado, fecha))
            rows = cur.fetchall()
            
            for row in rows:
                consulta = {
                    "idConsulta": row[0],
                    "fecha": row[1].isoformat() if row[1] else None,
                    "hora": str(row[2]) if row[2] else None,
                    "motivo": row[3],
                    "estado": row[4],
                    "observaciones": row[5],
                    "idEmpleado": row[6],
                    "idMascota": row[7],
                    "mascota_nombre": f"Mascota {row[7]}",  # Placeholder
                    "mascota_tipo": "Desconocido",  # Placeholder
                    "cliente_nombre": "Cliente Desconocido",  # Placeholder
                    "cliente_correo": ""
                }
                consultas.append(consulta)
            
            cur.close()
            conn.close()
            
            logger.info(f"Encontradas {len(consultas)} consultas para empleado {idEmpleado} en {sede} para fecha {fecha}")
            return consultas
            
        except Exception as e:
            logger.error(f"Error obteniendo consultas del empleado {idEmpleado} para fecha {fecha}: {e}")
            return []

    def create(self, c: Consulta) -> Consulta:
        try:
            db = self.get_consulta_db()
            sql = """
            INSERT INTO dbo.Consulta
              (idConsulta, fecha, hora, motivo, estado, observaciones, idClinica, idEmpleado, idMascota)
            VALUES (?,?,?,?,?,?,?,?,?)
            """
            cur = db.cursor()
            cur.execute(sql,
                c.idConsulta, c.fecha, c.hora, c.motivo,
                c.estado, c.observaciones, c.idClinica,
                c.idEmpleado, c.idMascota
            )
            db.commit()
            cur.close()
            db.close()
            return c
        except Exception as e:
            logger.error(f"Error creando consulta: {e}")
            raise

    def update_observaciones(self, idConsulta: int, observaciones: str) -> bool:
        """Actualizar observaciones de una consulta usando la sede correcta"""
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
                tabla = "Consulta_Quito"
            else:  # Guayaquil
                from ..config import ConfigGuayaquil
                conn = pyodbc.connect(ConfigGuayaquil.conn_str())
                tabla = "Consulta_Guayaquil"
            
            cur = conn.cursor()
            cur.execute(
                f"UPDATE {tabla} SET observaciones = ? WHERE idConsulta = ?",
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
        """Actualizar estado de una consulta usando la sede correcta"""
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
                tabla = "Consulta_Quito"
            else:  # Guayaquil
                from ..config import ConfigGuayaquil
                conn = pyodbc.connect(ConfigGuayaquil.conn_str())
                tabla = "Consulta_Guayaquil"
            
            cur = conn.cursor()
            cur.execute(
                f"UPDATE {tabla} SET estado = ? WHERE idConsulta = ?",
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

    def _find_consulta_sede(self, idConsulta: int) -> Optional[str]:
        """Encontrar en qué sede está una consulta específica"""
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

# Instancia global del repositorio
consulta_repository = ConsultaRepository()
