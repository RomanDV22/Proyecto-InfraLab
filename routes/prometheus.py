from fastapi import APIRouter, Response
from prometheus_client import CollectorRegistry, generate_latest, CONTENT_TYPE_LATEST

from services.prometheus_service import InfraLabCollector

router = APIRouter()


@router.get("/metrics")
def metrics():

    registry = CollectorRegistry()
    registry.register(InfraLabCollector())

    return Response(
        generate_latest(registry),
        media_type=CONTENT_TYPE_LATEST
    )
