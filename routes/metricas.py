from fastapi import APIRouter

from services.metricas_service import obtener_metricas

router = APIRouter()


@router.get("/metricas")
def metricas():

    return obtener_metricas()
