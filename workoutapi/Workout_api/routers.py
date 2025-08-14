from fastapi import APIRouter
from Workout_api.atleta.controller import router as atleta_router
from Workout_api.categorias.controller import router as categoria_router
from Workout_api.centro_treinamento.controller import router as centro_treinamento_router

api_router = APIRouter()
api_router.include_router(atleta_router, prefix="/atletas", tags=["Atletas"])
api_router.include_router(categoria_router, prefix="/categorias", tags=["categorias"])
api_router.include_router(centro_treinamento_router, prefix="/centros_treinamento", tags=["centros_treinamento"])