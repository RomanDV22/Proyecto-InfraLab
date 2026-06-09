from fastapi import APIRouter, Request

from fastapi.templating import Jinja2Templates

from services.dashboard_service import obtener_dashboard

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/")
def root():  

    return {
        "mensaje": "InfraLab Server Online"
    }

@router.get("/dashboard")

def dashboard(request: Request):

    datos = obtener_dashboard()

    return templates.TemplateResponse(

        request=request,

        name="dashboard.html",

        context=datos
    )

@router.get("/dashboard-data")

def dashboard_data():

    return obtener_dashboard()

