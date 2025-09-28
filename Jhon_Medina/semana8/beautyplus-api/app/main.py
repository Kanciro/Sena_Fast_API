from fastapi import FastAPI
from .routers.tipo_c_routers import router as tipo_c_router
from .routers.auth_routers import router as auth_router

app = FastAPI(
    title="API de Centro de Estética BeautyPlus",
    description="Gestión de servicios y perfiles de usuario",
    version="1.0.0"
)

app.include_router(auth_router, prefix="/api/v1/auth", tags=["Autenticación"])
app.include_router(tipo_c_router, prefix="/api/v1", tags=["Servicios de Usuario"])