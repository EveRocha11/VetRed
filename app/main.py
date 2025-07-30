from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="VetRed Admin")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR   = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

# 1) Sirve app/static bajo /static
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# 2) Raíz ➞ dashboard
@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/admin")

# 3) Panel estático
@app.get("/admin", include_in_schema=False)
def admin():
    return FileResponse(STATIC_DIR / "frontend" / "admin.html")

# 4) Tu API de empleados
from app.routers.empleado import router as empleado_router
app.include_router(empleado_router)

# 5) Tu API de consultas
# … ya tienes mount("/static") y la ruta /admin …
from app.routers.consulta import router as consulta_router
app.include_router(consulta_router)

