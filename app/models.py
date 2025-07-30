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
    tipo_usuario:    str  # "cliente", "empleado", "administrador"
    identificador:   str  # correo para clientes, idEmpleado para empleados, idAdmin para administradores
    nombre:          str  # nombre para validación

class RegisterRequest(BaseModel):
    idCliente:       int
    correo:          str
    nombre:          str

# Modelos para diferentes tipos de administradores
class AdminQuito(BaseModel):
    idAdmin:         int
    nombre:          str
    correo:          str
    idClinica:       int

class AdminGuayaquil(BaseModel):
    idAdmin:         int
    nombre:          str
    correo:          str
    idClinica:       int

# Modelo para vista unificada de empleados
class EmpleadoView(BaseModel):
    idEmpleado:      int
    nombre:          str
    direccion:       Optional[str]
    salario:         Optional[float]
    fechaContratacion: date
    idClinica:       int
    sede:            str  # "Quito" o "Guayaquil" determinado por idClinica
