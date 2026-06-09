from routes.dashboard import router as dashboard_router
from routes.api import router as api_router
from db import conectar_db
from fastapi import FastAPI, Request
import psutil
import socket
import requests
import time
import subprocess

#from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from routes.agentes import router as agentes_router
from routes.agente import router as agente_router

app = FastAPI()
app.include_router(dashboard_router)
app.include_router(api_router)
app.include_router(agentes_router)
app.include_router(agente_router)
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

