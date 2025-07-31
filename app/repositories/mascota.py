from typing import List, Optional
from datetime import date
from ..database_router import DatabaseRouter
from ..models import Mascota
import logging

logger = logging.getLogger(__name__)

class MascotaRepository:
    def __init__(self):
        db_router = DatabaseRouter()
        # puedes elegir db_quito o db_guayaquil porque Mascota está replicada
        self.db = db_router.get_auth_db()

    def list_by_cliente(self, idCliente: int, correo: str) -> List[Mascota]:
        try:
            cur = self.db.cursor()
            cur.execute(
                "SELECT * FROM Mascota WHERE idCliente = ? AND correo = ?",
                (idCliente, correo)
            )
            cols = [c[0] for c in cur.description]
            rows = cur.fetchall()
            cur.close()
            return [Mascota(**dict(zip(cols, row))) for row in rows]
        except Exception as e:
            logger.error(f"Error listando mascotas para cliente {idCliente}, {correo}: {e}")
            return []

    def get_by_id(self, idMascota: int) -> Optional[Mascota]:
        try:
            cur = self.db.cursor()
            cur.execute("SELECT * FROM Mascota WHERE idMascota = ?", (idMascota,))
            row = cur.fetchone()
            cur.close()
            if row:
                cols = [c[0] for c in cur.description]
                return Mascota(**dict(zip(cols, row)))
            return None
        except Exception as e:
            logger.error(f"Error obteniendo mascota {idMascota}: {e}")
            return None

    def create(self, m: Mascota) -> Mascota:
        try:
            sql = """
            INSERT INTO Mascota
            (idMascota, nombre, especie, raza, sexo, fechaNacimiento, color, peso, idCliente, correo)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            cur = self.db.cursor()
            cur.execute(sql, (
                m.idMascota, m.nombre, m.especie, m.raza, m.sexo,
                m.fechaNacimiento, m.color, m.peso, m.idCliente, m.correo
            ))
            self.db.commit()
            cur.close()
            return m
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creando mascota: {e}")
            raise

    def update(self, m: Mascota) -> Mascota:
        try:
            sql = """
            UPDATE Mascota SET
            nombre=?, especie=?, raza=?, sexo=?, fechaNacimiento=?,
            color=?, peso=?
            WHERE idMascota=? AND idCliente=? AND correo=?
            """
            cur = self.db.cursor()
            cur.execute(sql, (
                m.nombre, m.especie, m.raza, m.sexo, m.fechaNacimiento,
                m.color, m.peso, m.idMascota, m.idCliente, m.correo
            ))
            self.db.commit()
            cur.close()
            return m
        except Exception as e:
            logger.error(f"Error actualizando mascota: {e}")
            raise

    def delete(self, idMascota: int):
        try:
            cur = self.db.cursor()
            cur.execute("DELETE FROM Mascota WHERE idMascota = ?", (idMascota,))
            self.db.commit()
            cur.close()
        except Exception as e:
            logger.error(f"Error eliminando mascota: {e}")
            raise

# Instancia global
mascota_repository = MascotaRepository()