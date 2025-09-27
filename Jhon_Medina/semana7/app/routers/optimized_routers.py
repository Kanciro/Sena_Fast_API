# app/routers/optimized_routes.py
from fastapi import APIRouter
from ..cache.cache_decorators import cache_result
from ..cache.redis_config import cache_manager

router = APIRouter(prefix="/api/optimized", tags=["Genérico Optimizado"])

# Tipo A: Gestión de datos - Consultas frecuentes
@router.get("/entidad_principal/frecuentes")
@cache_result(ttl_type='tipo_a', key_prefix='frequent_queries')
async def get_frequent_data():
    """Ejemplo para datos frecuentemente consultados (Tipo A)"""
    # Lógica para obtener datos de la DB
    resultado = {"data": "datos de alta rotación"}
    return resultado

# Tipo C: Servicios de usuario - Datos estables
@router.get("/configuracion")
@cache_result(ttl_type='tipo_c', key_prefix='config')
async def get_stable_data():
    """Ejemplo para datos de configuración que cambian raramente (Tipo C)"""
    # Lógica para obtener configuración de la DB
    configuracion = {"settings": "configuracion estandar"}
    return configuracion

# Tipo D: Catálogo de elementos - Búsquedas complejas
@router.get("/catalogo/busqueda")
@cache_result(ttl_type='tipo_d', key_prefix='catalog_search')
async def search_catalog(query: str):
    """Ejemplo para búsquedas complejas (Tipo D)"""
    # Lógica para realizar búsqueda pesada en la DB
    search_results = {"results": f"Resultados para '{query}'"}
    return search_results

# Endpoint con invalidación de cache
@router.post("/entidad_principal/crear")
async def create_new_entity(data: dict):
    # Lógica para crear nueva entidad en la DB
    # ...
    # Invalida los caches que contienen datos de alta rotación
    cache_manager.invalidate_cache("cache:frequent_queries:*")
    return {"message": "Entidad creada y cache invalidado"}