from pydantic import BaseModel
from datetime import date, time
from typing import Optional

class Consulta(BaseModel):
    idConsulta:    int
    fecha:         date
    hora:          time
    motivo:        str
    estado:        Optional[str]
    observaciones: Optional[str]
    idClinica:     int
    idEmpleado:    int
    idMascota:     int
