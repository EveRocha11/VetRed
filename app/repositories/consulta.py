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
        """Obtener consultas de un empleado para una fecha específica con información del cliente"""
        try:
            # Primero determinar la sede del empleado
            from ..repositories.empleado import EmpleadoRepository
            empleado_repo = EmpleadoRepository()
            sede = empleado_repo.get_empleado_sede(idEmpleado)
            
            if not sede:
                logger.warning(f"No se pudo determinar la sede del empleado {idEmpleado}")
                return []
            
            consultas = []
            
            if sede == "Quito":
                # Buscar en base de datos de Quito - crear nueva conexión
                import pyodbc
                from ..config import ConfigQuito
                
                conn = pyodbc.connect(ConfigQuito.conn_str())
                cur = conn.cursor()
                
                query = """
                    SELECT 
                        c.idConsulta,
                        c.fecha,
                        c.hora,
                        c.motivo,
                        c.estado,
                        c.observaciones,
                        c.idEmpleado,
                        c.idMascota,
                        m.nombre as mascota_nombre,
                        m.especie as mascota_tipo,
                        'Cliente de ' + m.nombre as cliente_nombre
                    FROM Consulta_Quito c
                    LEFT JOIN Mascota m ON m.idMascota = c.idMascota
                    WHERE c.idEmpleado = ? AND c.fecha = ?
                    ORDER BY c.hora
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
                        "mascota_nombre": row[8] or f"Mascota {row[7]}",
                        "mascota_tipo": row[9] or "Desconocido",
                        "cliente_nombre": row[10] or "Cliente Desconocido",
                        "cliente_correo": ""
                    }
                    consultas.append(consulta)
                
                cur.close()
                conn.close()
                
            elif sede == "Guayaquil":
                # Buscar en base de datos de Guayaquil - crear nueva conexión
                import pyodbc
                from ..config import ConfigGuayaquil
                
                conn = pyodbc.connect(ConfigGuayaquil.conn_str())
                cur = conn.cursor()
                
                query = """
                    SELECT 
                        c.idConsulta,
                        c.fecha,
                        c.hora,
                        c.motivo,
                        c.estado,
                        c.observaciones,
                        c.idEmpleado,
                        c.idMascota,
                        m.nombre as mascota_nombre,
                        m.especie as mascota_tipo,
                        'Cliente de ' + m.nombre as cliente_nombre
                    FROM Consulta_Guayaquil c
                    LEFT JOIN Mascota m ON m.idMascota = c.idMascota
                    WHERE c.idEmpleado = ? AND c.fecha = ?
                    ORDER BY c.hora
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
                        "mascota_nombre": row[8] or f"Mascota {row[7]}",
                        "mascota_tipo": row[9] or "Desconocido",
                        "cliente_nombre": row[10] or "Cliente Desconocido",
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
        """Actualizar observaciones de una consulta"""
        try:
            # Intentar actualizar en Quito primero
            conn_quito = self.db_router.get_auth_db()
            cur = conn_quito.cursor()
            cur.execute(
                "UPDATE Consulta_Quito SET observaciones = ? WHERE idConsulta = ?",
                (observaciones, idConsulta)
            )
            rows_affected = cur.rowcount
            conn_quito.commit()
            cur.close()
            conn_quito.close()
            
            if rows_affected > 0:
                return True
            
            # Si no se actualizó en Quito, intentar en Guayaquil
            conn_guayaquil = self.db_router.get_cliente_contacto_db()
            cur = conn_guayaquil.cursor()
            cur.execute(
                "UPDATE Consulta_Guayaquil SET observaciones = ? WHERE idConsulta = ?",
                (observaciones, idConsulta)
            )
            rows_affected = cur.rowcount
            conn_guayaquil.commit()
            cur.close()
            conn_guayaquil.close()
            
            return rows_affected > 0
            
        except Exception as e:
            logger.error(f"Error actualizando observaciones de consulta {idConsulta}: {e}")
            return False

    def update_estado(self, idConsulta: int, estado: str) -> bool:
        """Actualizar estado de una consulta"""
        try:
            # Intentar actualizar en Quito primero
            conn_quito = self.db_router.get_auth_db()
            cur = conn_quito.cursor()
            cur.execute(
                "UPDATE Consulta_Quito SET estado = ? WHERE idConsulta = ?",
                (estado, idConsulta)
            )
            rows_affected = cur.rowcount
            conn_quito.commit()
            cur.close()
            conn_quito.close()
            
            if rows_affected > 0:
                return True
            
            # Si no se actualizó en Quito, intentar en Guayaquil
            conn_guayaquil = self.db_router.get_cliente_contacto_db()
            cur = conn_guayaquil.cursor()
            cur.execute(
                "UPDATE Consulta_Guayaquil SET estado = ? WHERE idConsulta = ?",
                (estado, idConsulta)
            )
            rows_affected = cur.rowcount
            conn_guayaquil.commit()
            cur.close()
            conn_guayaquil.close()
            
            return rows_affected > 0
            
        except Exception as e:
            logger.error(f"Error actualizando estado de consulta {idConsulta}: {e}")
            return False

# Instancia global del repositorio
consulta_repository = ConsultaRepository()
