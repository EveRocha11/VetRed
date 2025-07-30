from fastapi import APIRouter, HTTPException
from typing import List
from ..models import Consulta
from ..repositories.consulta import ConsultaRepository

router = APIRouter(prefix="/api/consultas", tags=["Consultas"])
repo   = ConsultaRepository()

@router.get("/", response_model=List[Consulta])
def get_consultas(sede_admin: str = "Quito"):
    """Obtener consultas filtradas por sede usando vista dbo.Consulta"""
    try:
        return repo.list(sede_admin=sede_admin)
    except Exception as e:
        print(f"Error en get_consultas: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.post("/", response_model=Consulta, status_code=201)
def post_consulta(c: Consulta):
    try:
        return repo.create(c)
    except Exception as e:
        print(f"Error en post_consulta: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.get("/{idConsulta}/{idClinica}", response_model=Consulta)
def get_consulta_by_id(idConsulta: int, idClinica: int):
    """Obtener una consulta por su idConsulta e idClinica"""
    try:
        consulta = repo.get_by_id(idConsulta, idClinica)
        if not consulta:
            raise HTTPException(status_code=404, detail="Consulta no encontrada")
        return consulta
    except Exception as e:
        print(f"Error en get_consulta_by_id: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.put("/{idConsulta}/{idClinica}", response_model=Consulta)
def put_consulta(idConsulta: int, idClinica: int, c: Consulta):
    try:
        if c.idConsulta != idConsulta or c.idClinica != idClinica:
            raise HTTPException(status_code=400, detail="Los IDs no coinciden")
        return repo.update(c)
    except Exception as e:
        print(f"Error en put_consulta: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.delete("/{idConsulta}/{idClinica}", status_code=204)
def delete_consulta(idConsulta: int, idClinica: int):
    try:
        success = repo.delete(idConsulta, idClinica)
        if not success:
            raise HTTPException(status_code=404, detail="Consulta no encontrada")
        return None
    except Exception as e:
        print(f"Error en delete_consulta: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")
