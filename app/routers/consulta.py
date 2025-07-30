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
