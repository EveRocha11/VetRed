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

# 2) Raíz ➞ login
@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/login")

# 3) Página de login
@app.get("/login", include_in_schema=False)
def login_page():
    return FileResponse(STATIC_DIR / "frontend" / "login.html")

# 4) Página de registro
@app.get("/register", include_in_schema=False)
def register_page():
    return FileResponse(STATIC_DIR / "frontend" / "register.html")

# 5) Panel estático (requiere autenticación)
@app.get("/admin", include_in_schema=False)
def admin():
    return FileResponse(STATIC_DIR / "frontend" / "admin.html")

# 6) Panel de empleados
@app.get("/empleado", include_in_schema=False)
def empleado():
    return FileResponse(STATIC_DIR / "frontend" / "empleado.html")

# 7) Panel de usuarios/clientes
@app.get("/usuario", include_in_schema=False)
def usuario():
    return FileResponse(STATIC_DIR / "frontend" / "usuario.html")

# 8) Panel de consultas
@app.get("/consultas", include_in_schema=False)
def consultas():
    return FileResponse(STATIC_DIR / "frontend" / "consultas.html")

# 9) Panel de clientes
@app.get("/clientes", include_in_schema=False)
def clientes():
    return FileResponse(STATIC_DIR / "frontend" / "clientes.html")

# 10) API de autenticación
from app.routers.auth import router as auth_router
app.include_router(auth_router)

# 11) Tu API de empleados
from app.routers.empleado import router as empleado_router
app.include_router(empleado_router)

# 12) Tu API de consultas
# … ya tienes mount("/static") y la ruta /admin …
from app.routers.consulta import router as consulta_router
app.include_router(consulta_router)

# 13) Tu API de clientes
from app.routers.cliente_contacto import router as cliente_router
app.include_router(cliente_router)

# 14) API de sistema (health check y conexiones)
from app.routers.system import router as system_router
app.include_router(system_router)

# 15) API de mascotas
from app.routers.mascota import router as mascota_router
app.include_router(mascota_router)

# 16) API de cliente_info
from app.routers.cliente_info import router as cliente_info_router
app.include_router(cliente_info_router)
