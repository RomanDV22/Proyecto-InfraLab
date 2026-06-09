from fastapi import APIRouter, Request

from fastapi.templating import Jinja2Templates

from services.agentes_service import obtener_agentes


router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/agentes")

def agentes(request: Request):

    datos = obtener_agentes()


    return templates.TemplateResponse(

        request=request,

        name="agentes.html",

        context={

            "agentes": datos

        }

    )
