# app/routers/consulta.py

from fastapi import APIRouter, HTTPException
from typing import List
from app.models import Consulta
from app.repositories.consulta import ConsultaRepository

# → Aquí se define el router que luego main.py incluye
router = APIRouter(
    prefix="/consultas",
    tags=["Consultas"],
)

# Instancia de tu repositorio
repo = ConsultaRepository()

@router.get("/", response_model=List[Consulta])
def get_consultas():
    return repo.list()

@router.post("/", response_model=Consulta, status_code=201)
def post_consulta(c: Consulta):
    try:
        repo.create(c)
        return c
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
