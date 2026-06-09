from fastapi import APIRouter, Request

from fastapi.templating import Jinja2Templates

from services.agente_service import obtener_agente

from fastapi import HTTPException

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/agente/{nombre}")

def agente(request: Request, nombre: str):

    datos = obtener_agente(nombre)

    if datos is None:

        raise HTTPException(
            status_code=404,
            detail="Agente no encontrado"
        ) 

    return templates.TemplateResponse(

        request=request,

        name="agente.html",

        context=datos

    )
