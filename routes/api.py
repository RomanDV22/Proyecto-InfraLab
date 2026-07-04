import os

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, Header, HTTPException
from fastapi.concurrency import run_in_threadpool

from schemas import MetricaIn
from services.alertas_service import evaluar_alertas
from services.dashboard_service import obtener_dashboard
from services.metricas_service import guardar_metrica
from services.ws_manager import manager

load_dotenv()

router = APIRouter()

API_KEY = os.getenv("API_KEY")


def verificar_api_key(x_api_key: str = Header(...)):
    if not API_KEY or x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="API key invalida")


@router.post("/api/metricas", dependencies=[Depends(verificar_api_key)])
async def recibir_metricas(datos: MetricaIn):

    payload = datos.model_dump()

    await run_in_threadpool(guardar_metrica, payload)
    await run_in_threadpool(evaluar_alertas, payload)

    dashboard_data = await run_in_threadpool(obtener_dashboard)
    await manager.broadcast(dashboard_data)

    return {
        "status": "ok"
    }
