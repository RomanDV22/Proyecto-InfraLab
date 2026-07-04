from fastapi import APIRouter, Request

from fastapi.templating import Jinja2Templates

from services.alertas_service import obtener_alertas

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/alertas")
def alertas(request: Request):

    datos = obtener_alertas()

    return templates.TemplateResponse(

        request=request,

        name="alertas.html",

        context={
            "alertas": datos
        }

    )


@router.get("/api/alertas")
def alertas_api():

    return obtener_alertas()
