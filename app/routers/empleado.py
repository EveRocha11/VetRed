from fastapi import APIRouter, HTTPException
from typing import List
from datetime import date
from ..models import Empleado
from ..repositories.empleado import EmpleadoRepository
from ..repositories.consulta import ConsultaRepository

router = APIRouter(prefix="/api/empleados", tags=["Empleados"])
repo = EmpleadoRepository()
consulta_repo = ConsultaRepository()

@router.get("/", response_model=List[Empleado])
def get_empleados():
    try:
        return repo.list()
    except Exception as e:
        print(f"Error en get_empleados: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.get("/{idEmpleado}/consultas/{fecha}")
def get_consultas_empleado(idEmpleado: int, fecha: str):
    """Obtener consultas de un empleado para una fecha específica"""
    try:
        # Convertir string a date
        fecha_obj = date.fromisoformat(fecha)
        consultas = consulta_repo.get_by_empleado_fecha(idEmpleado, fecha_obj)
        return {"consultas": consultas}
    except Exception as e:
        print(f"Error obteniendo consultas del empleado {idEmpleado}: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.get("/{idEmpleado}/consultas-hoy")
def get_consultas_empleado_hoy(idEmpleado: int):
    """Obtener consultas de hoy para un empleado específico"""
    try:
        from datetime import date
        hoy = date.today()
        consultas = consulta_repo.get_by_empleado_fecha(idEmpleado, hoy)
        return {"consultas": consultas, "fecha": hoy.isoformat()}
    except Exception as e:
        print(f"Error obteniendo consultas de hoy del empleado {idEmpleado}: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.put("/consultas/{idConsulta}/observaciones")
def update_observaciones_consulta(idConsulta: int, data: dict):
    """Actualizar observaciones de una consulta"""
    try:
        observaciones = data.get("observaciones", "")
        success = consulta_repo.update_observaciones(idConsulta, observaciones)
        if success:
            return {"message": "Observaciones actualizadas exitosamente"}
        else:
            raise HTTPException(status_code=400, detail="Error actualizando observaciones")
    except Exception as e:
        print(f"Error actualizando observaciones: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.put("/consultas/{idConsulta}/estado")
def update_estado_consulta(idConsulta: int, data: dict):
    """Actualizar estado de una consulta"""
    try:
        estado = data.get("estado", "")
        success = consulta_repo.update_estado(idConsulta, estado)
        if success:
            return {"message": "Estado actualizado exitosamente"}
        else:
            raise HTTPException(status_code=400, detail="Error actualizando estado")
    except Exception as e:
        print(f"Error actualizando estado: {e}")
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
