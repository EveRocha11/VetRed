# app/main.py
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from app.repositories.consulta import ConsultaRepository  # ← importa tu repo

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent    # VetRed/app
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# crea una instancia de tu repositorio
repo_consulta = ConsultaRepository()

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    # obtén las consultas desde la BD
    consultas = repo_consulta.list()
    # pásalas al contexto de la plantilla
    return templates.TemplateResponse(
        "base.html",
        {
            "request": request,
            "consultas": consultas
        }
    )
