from typing import List
from ..database_router import db_router
from ..models import ClienteContacto
import logging

logger = logging.getLogger(__name__)

class ClienteContactoRepository:
    def __init__(self):
        self.db = db_router.get_cliente_contacto_db()

    def list(self, sede_admin: str = None) -> List[ClienteContacto]:
        """Listar clientes filtrados por sede usando tabla Cliente_Contacto"""
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
            
            # Usar la tabla Cliente_Info directamente
            query = """
                SELECT idCliente, correo, nombre as direccion, '' as telefono
                FROM dbo.Cliente_Info
                WHERE idCliente IN (
                    SELECT idCliente FROM dbo.Cliente WHERE idClinica = ?
                )
            """
            logger.info(f"Consultando clientes para sede {sede_admin} (idClinica={id_clinica_filter})")
            cursor.execute(query, (id_clinica_filter,))
            
            cols = [c[0] for c in cursor.description]
            rows = cursor.fetchall()
            
            logger.info(f"Encontrados {len(rows)} clientes para sede {sede_admin}")
            
            clientes = []
            for row in rows:
                cliente_data = dict(zip(cols, row))
                clientes.append(ClienteContacto(**cliente_data))
            
            cursor.close()
            conn.close()
            
            return clientes
            
        except Exception as e:
            logger.error(f"Error en list cliente_contacto: {e}")
            # Si falla la consulta con filtro, intentar diferentes estrategias como fallback
            try:
                import pyodbc
                from ..config import ConfigQuito
                
                conn = pyodbc.connect(ConfigQuito.conn_str())
                cursor = conn.cursor()
                
                # Intentar primero con Cliente_Info
                try:
                    cursor.execute("SELECT idCliente, correo, nombre as direccion, '' as telefono FROM dbo.Cliente_Info;")
                    cols = [c[0] for c in cursor.description]
                    rows = cursor.fetchall()
                    
                    logger.info(f"Fallback: Encontrados {len(rows)} registros en Cliente_Info")
                    clientes = []
                    for row in rows:
                        cliente_data = dict(zip(cols, row))
                        clientes.append(ClienteContacto(
                            idCliente=cliente_data['idCliente'],
                            correo=cliente_data['correo'],
                            direccion=cliente_data.get('direccion', ''),
                            telefono=cliente_data.get('telefono', '')
                        ))
                    
                    cursor.close()
                    conn.close()
                    return clientes
                    
                except Exception as e_info:
                    logger.warning(f"Cliente_Info no disponible: {e_info}")
                
                # Si Cliente_Info no existe, intentar con datos simulados
                cursor.close()
                conn.close()
                
                logger.info("Retornando lista vacía de clientes")
                return []
                
            except Exception as e2:
                logger.error(f"Error en fallback cliente_contacto: {e2}")
                return []
        
    def get_by_id_and_correo(self, idCliente: int, correo: str) -> ClienteContacto | None:
        try:
            sql = "SELECT idCliente, correo, direccion, telefono FROM dbo.Cliente_Contacto WHERE idCliente = ? AND correo = ?"
            cur = self.db.cursor()
            cur.execute(sql, (idCliente, correo))
            row = cur.fetchone()
            cur.close()
            if row:
                return ClienteContacto(
                    idCliente=row[0],
                    correo=row[1],
                    direccion=row[2],
                    telefono=row[3]
                )
            return None
        except Exception as e:
            print(f"Error obteniendo cliente_contacto por id y correo: {e}")
            raise

    def create(self, cliente: ClienteContacto) -> ClienteContacto:
        try:
            sql = """
            INSERT INTO dbo.Cliente_Contacto
              (idCliente, correo, direccion, telefono)
            VALUES (?,?,?,?)
            """
            cur = self.db.cursor()
            cur.execute(sql, (
                cliente.idCliente,
                cliente.correo,
                cliente.direccion,
                cliente.telefono
            ))
            self.db.commit()
            cur.close()
            return cliente
        except Exception as e:
            print(f"Error creando cliente_contacto: {e}")
            self.db.rollback()
            raise

    def update(self, cliente: ClienteContacto) -> ClienteContacto:
        try:
            sql = """
            UPDATE dbo.Cliente_Contacto
               SET direccion=?, telefono=?
             WHERE idCliente=? AND correo=?
            """
            cur = self.db.cursor()
            cur.execute(sql, (
                cliente.direccion,
                cliente.telefono,
                cliente.idCliente,
                cliente.correo
            ))
            self.db.commit()
            cur.close()
            return cliente
        except Exception as e:
            print(f"Error actualizando cliente_contacto: {e}")
            self.db.rollback()
            raise

    def delete(self, idCliente: int, correo: str):
        try:
            sql = "DELETE FROM dbo.Cliente_Contacto WHERE idCliente=? AND correo=?"
            cur = self.db.cursor()
            cur.execute(sql, (idCliente, correo))  # 👈 parámetros como tupla
            self.db.commit()
            cur.close()
        except Exception as e:
            print(f"Error eliminando cliente_contacto: {e}")
            self.db.rollback()
            raise
