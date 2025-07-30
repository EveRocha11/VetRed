from fastapi import APIRouter, HTTPException
from typing import List
from ..models import Consulta
from ..repositories.consulta import ConsultaRepository

router = APIRouter(prefix="/api/consultas", tags=["Consultas"])
repo   = ConsultaRepository()

@router.get("/", response_model=List[Consulta])
def get_consultas():
    try:
        return repo.list()
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
