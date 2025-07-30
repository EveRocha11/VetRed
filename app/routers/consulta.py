from fastapi import APIRouter
from typing import List
from ..models import Consulta
from ..repositories.consulta import ConsultaRepository

router = APIRouter(prefix="/api/consultas", tags=["Consultas"])
repo   = ConsultaRepository()

@router.get("/", response_model=List[Consulta])
def get_consultas():
    return repo.list()

@router.post("/", response_model=Consulta, status_code=201)
def post_consulta(c: Consulta):
    return repo.create(c)
