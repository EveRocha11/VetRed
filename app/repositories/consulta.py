from typing import List
from ..db import db_guayaquil
from ..models import Consulta

class ConsultaRepository:
    def __init__(self):
        self.db = db_guayaquil

    def list(self) -> List[Consulta]:
        cur = self.db.cursor()
        cur.execute("SELECT * FROM dbo.Consulta;")
        cols = [c[0] for c in cur.description]
        rows = cur.fetchall()
        return [Consulta(**dict(zip(cols, row))) for row in rows]

    def create(self, c: Consulta) -> Consulta:
        cur = self.db.cursor()
        cur.execute("""
            INSERT INTO dbo.Consulta
              (idConsulta, fecha, hora, motivo, estado, observaciones, idClinica, idEmpleado, idMascota)
            VALUES (?,?,?,?,?,?,?,?,?)
        """, 
        c.idConsulta, c.fecha, c.hora, c.motivo, c.estado, c.observaciones, c.idClinica, c.idEmpleado, c.idMascota)
        return c
