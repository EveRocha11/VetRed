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
            self.db.cursor().execute(sql,
               e.idEmpleado, e.nombre, e.direccion, e.salario, e.fechaContratacion, e.idClinica)
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
        self.db.cursor().execute(sql,
           e.nombre, e.direccion, e.salario, e.fechaContratacion, e.idEmpleado, e.idClinica)
        return e

    def delete(self, idEmpleado: int, idClinica: int):
        sql = "DELETE FROM dbo.Empleado WHERE idEmpleado=? AND idClinica=?"
        self.db.cursor().execute(sql, idEmpleado, idClinica)
