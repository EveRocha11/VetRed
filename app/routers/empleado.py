from fastapi import APIRouter, HTTPException
from typing import List
from ..models import Empleado
from ..repositories.empleado import EmpleadoRepository

router = APIRouter(prefix="/api/empleados", tags=["Empleados"])
repo   = EmpleadoRepository()

@router.get("/", response_model=List[Empleado])
def get_empleados():
    try:
        return repo.list()
    except Exception as e:
        print(f"Error en get_empleados: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.post("/", response_model=Empleado, status_code=201)
def post_empleado(e: Empleado):
    return repo.create(e)

@router.put("/", response_model=Empleado)
def put_empleado(e: Empleado):
    return repo.update(e)

@router.delete("/{idEmpleado}/{idClinica}", status_code=204)
def del_empleado(idEmpleado: int, idClinica: int):
    repo.delete(idEmpleado, idClinica)
