from routes.dashboard import router as dashboard_router
from routes.api import router as api_router
from fastapi import FastAPI
import subprocess

from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from routes.agentes import router as agentes_router
from routes.agente import router as agente_router
from routes.health import router as health_router
from routes.metricas import router as metricas_router
from routes.alertas import router as alertas_router
from routes.prometheus import router as prometheus_router

app = FastAPI()
app.include_router(dashboard_router)
app.include_router(api_router)
app.include_router(agentes_router)
app.include_router(agente_router)
app.include_router(health_router)
app.include_router(metricas_router)
app.include_router(alertas_router)
app.include_router(prometheus_router)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
def obtener_mac(ip):

    try:

        resultado = subprocess.check_output(

        ["ip", "neigh"],

        text=True

        )

        for linea in resultado.splitlines():

            if ip in linea and "lladdr" in linea:

                partes = linea.split()

                indice = partes.index("lladdr")

                return partes[indice + 1]

    except:

        return None

