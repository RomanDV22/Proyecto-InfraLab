from fastapi import APIRouter

from services.health_service import obtener_health


router = APIRouter()


@router.get("/health")
def health():
    return obtener_health()
