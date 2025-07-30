from typing import List
from ..db import db_guayaquil
from ..models import Empleado

class EmpleadoRepository:
    def __init__(self):
        self.db = db_guayaquil

    def list(self) -> List[Empleado]:
        try:
            cur = self.db.cursor()
            cur.execute("SELECT * FROM dbo.Empleado;")
            cols = [c[0] for c in cur.description]
            rows = cur.fetchall()
            cur.close()  # Cerrar el cursor
            return [Empleado(**dict(zip(cols, row))) for row in rows]
        except Exception as e:
            print(f"Error en list(): {e}")
            return []

    def create(self, e: Empleado) -> Empleado:
        try:
            sql = """
              INSERT INTO dbo.Empleado
                (idEmpleado,nombre,direccion,salario,fechaContratacion,idClinica)
              VALUES (?,?,?,?,?,?)
            """
            cur = self.db.cursor()
            cur.execute(sql,
               e.idEmpleado, e.nombre, e.direccion, e.salario, e.fechaContratacion, e.idClinica)
            cur.close()  # Cerrar el cursor
            return e
        except Exception as e:
            print(f"Error en create(): {e}")
            raise

    def update(self, e: Empleado) -> Empleado:
        sql = """
          UPDATE dbo.Empleado
             SET nombre=?, direccion=?, salario=?, fechaContratacion=?
           WHERE idEmpleado=? AND idClinica=?
        """
        cur = self.db.cursor()
        cur.execute(sql,
           e.nombre, e.direccion, e.salario, e.fechaContratacion, e.idEmpleado, e.idClinica)
        cur.close()  # Cerrar el cursor
        return e

    def delete(self, idEmpleado: int, idClinica: int):
        sql = "DELETE FROM dbo.Empleado WHERE idEmpleado=? AND idClinica=?"
        cur = self.db.cursor()
        cur.execute(sql, idEmpleado, idClinica)
        cur.close()  # Cerrar el cursor
