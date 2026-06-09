from fastapi import APIRouter
from services.metricas_service import guardar_metrica 

router = APIRouter()


@router.post("/api/metricas")
def recibir_metricas(datos: dict):

    guardar_metrica(datos)

    return {
        "status": "ok"
    }
