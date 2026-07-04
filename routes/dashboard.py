from fastapi import APIRouter, Request, WebSocket, WebSocketDisconnect

from fastapi.templating import Jinja2Templates

from services.dashboard_service import obtener_dashboard
from services.ws_manager import manager

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


@router.websocket("/ws/dashboard")
async def ws_dashboard(websocket: WebSocket):

    await manager.conectar(websocket)

    try:
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        manager.desconectar(websocket)

