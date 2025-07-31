from fastapi import APIRouter, HTTPException, Query
from typing import List
from ..models import Mascota
from ..repositories.mascota import MascotaRepository
router = APIRouter(prefix="/api/mascotas", tags=["Mascotas"])
repo = MascotaRepository()

# 1. Obtener todas las mascotas de un cliente
@router.get("/", response_model=List[Mascota])
def get_mascotas(idCliente: int, correo: str):
    try:
        return repo.list_by_cliente(idCliente, correo)
    except Exception as e:
        print(f"Error en get_mascotas: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

# 2. Obtener una mascota por ID
@router.get("/{idMascota}", response_model=Mascota)
def get_mascota_by_id(idMascota: int):
    mascota = repo.get_by_id(idMascota)
    if not mascota:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")
    return mascota

# 3. Crear una mascota
@router.post("/", response_model=Mascota, status_code=201)
def post_mascota(m: Mascota):
    try:
        return repo.create(m)
    except Exception as e:
        print(f"Error en post_mascota: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

# 4. Actualizar una mascota
@router.put("/", response_model=Mascota)
def put_mascota(m: Mascota):
    try:
        return repo.update(m)
    except Exception as e:
        print(f"Error en put_mascota: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

# 5. Eliminar una mascota
@router.delete("/{idMascota}", status_code=204)
def delete_mascota(idMascota: int):
    try:
        repo.delete(idMascota)
    except Exception as e:
        print(f"Error en delete_mascota: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")