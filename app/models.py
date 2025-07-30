from pydantic import BaseModel
from datetime import date, time
from typing import Optional

class Empleado(BaseModel):
    idEmpleado:        int
    nombre:            str
    direccion:         Optional[str]
    salario:           Optional[float]
    fechaContratacion: date
    idClinica:         int

class Consulta(BaseModel):
    idConsulta:      int
    fecha:           date
    hora:            time
    motivo:          str
    estado:          str
    observaciones:   Optional[str] = None
    idClinica:       int
    idEmpleado:      int
    idMascota:       int

class ClienteContacto(BaseModel):
    idCliente:       int
    correo:          str
    direccion:       Optional[str] = None
    telefono:        Optional[str] = None

class ClienteInfo(BaseModel):
    idCliente:       int
    correo:          str
    nombre:          str

class LoginRequest(BaseModel):
    correo:          str
    password:        str

class RegisterRequest(BaseModel):
    idCliente:       int
    correo:          str
    nombre:          str
