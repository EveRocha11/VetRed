from typing import List
from ..db import db_guayaquil
from ..models import ClienteContacto

class ClienteContactoRepository:
    def __init__(self):
        self.db = db_guayaquil

    def list(self) -> List[ClienteContacto]:
        try:
            cur = self.db.cursor()
            cur.execute("SELECT * FROM dbo.Cliente_Contacto;")
            cols = [c[0] for c in cur.description]
            rows = cur.fetchall()
            cur.close()  # Cerrar el cursor
            return [ClienteContacto(**dict(zip(cols, row))) for row in rows]
        except Exception as e:
            print(f"Error en list cliente_contacto: {e}")
            return []

    def create(self, cliente: ClienteContacto) -> ClienteContacto:
        try:
            sql = """
            INSERT INTO dbo.Cliente_Contacto
              (idCliente, correo, direccion, telefono)
            VALUES (?,?,?,?)
            """
            cur = self.db.cursor()
            cur.execute(sql,
                cliente.idCliente, cliente.correo, cliente.direccion, cliente.telefono
            )
            cur.close()  # Cerrar el cursor
            return cliente
        except Exception as e:
            print(f"Error creando cliente_contacto: {e}")
            raise

    def update(self, cliente: ClienteContacto) -> ClienteContacto:
        try:
            sql = """
            UPDATE dbo.Cliente_Contacto
               SET direccion=?, telefono=?
             WHERE idCliente=? AND correo=?
            """
            cur = self.db.cursor()
            cur.execute(sql,
                cliente.direccion, cliente.telefono, cliente.idCliente, cliente.correo
            )
            cur.close()  # Cerrar el cursor
            return cliente
        except Exception as e:
            print(f"Error actualizando cliente_contacto: {e}")
            raise

    def delete(self, idCliente: int, correo: str):
        try:
            sql = "DELETE FROM dbo.Cliente_Contacto WHERE idCliente=? AND correo=?"
            cur = self.db.cursor()
            cur.execute(sql, idCliente, correo)
            cur.close()  # Cerrar el cursor
        except Exception as e:
            print(f"Error eliminando cliente_contacto: {e}")
            raise
