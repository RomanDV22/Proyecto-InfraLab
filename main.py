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


app = FastAPI()
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

@app.get("/")
def root(request: Request):

    hostname = socket.gethostname()
    
    ip_cliente = request.client.host
    
    mac_address = obtener_mac(ip_cliente)
    
    print(ip_cliente)
    mac_address = obtener_mac(ip_cliente)
    print(mac_address)

    endpoint = request.url.path

    metodo = request.method
    
    cpu = psutil.cpu_percent(interval=1)

    ram = psutil.virtual_memory()

    ip_local = socket.gethostbyname(hostname)

    internet = "offline"

    latencia_ms = None

    try:

        inicio = time.time()

        requests.get("https://www.google.com", timeout=3)

        fin = time.time()

        latencia_ms = round((fin - inicio) * 1000, 2)

        internet = "online"

    except:
        internet = "offline"

    datos = {

        "servidor": hostname,

        "ip_local": ip_local,

        "internet": internet,

        "latencia_ms": latencia_ms,

        "cpu_porcentaje": cpu,

        "ram_porcentaje": ram.percent,

        "ram_usada_gb": round(ram.used / (1024 ** 3), 2),

        "ram_total_gb": round(ram.total / (1024 ** 3), 2)
    }

    conexion = conectar_db()

    cursor = conexion.cursor()
   
    cursor.execute("""

        INSERT INTO clientes (
            ip,
            mac_address
        )

        VALUES (%s, %s)

        ON CONFLICT (ip) DO NOTHING

    """, (ip_cliente, mac_address))

    cursor.execute("""

        INSERT INTO requests (

        ip_cliente,
        endpoint,
        metodo

        )

        VALUES (%s,%s,%s)

    """, (

        ip_cliente,
        endpoint,
        metodo

    ))

    cursor.execute("""

        INSERT INTO metricas (

            servidor,
            ip_local,
            internet,
            latencia_ms,
            cpu_porcentaje,
            ram_porcentaje,
            ram_usada_gb,
            ram_total_gb

        )

        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)

    """, (

        datos["servidor"],
        datos["ip_local"],
        datos["internet"],
        datos["latencia_ms"],
        datos["cpu_porcentaje"],
        datos["ram_porcentaje"],
        datos["ram_usada_gb"],
        datos["ram_total_gb"]

    ))

    conexion.commit()

    cursor.close()

    conexion.close()

    return datos

@app.get("/metricas")
def obtener_metricas():

    conexion = conectar_db()

    cursor = conexion.cursor()

    cursor.execute("""

        SELECT *

        FROM metricas

        ORDER BY id DESC

        LIMIT 10

    """)

    filas = cursor.fetchall()

    cursor.close()

    conexion.close()

    return filas

@app.get("/dashboard")
def dashboard(request: Request):

    conexion = conectar_db()

    cursor = conexion.cursor()

    cursor.execute("""

        SELECT COUNT(*)

        FROM clientes

    """)

    total_clientes = cursor.fetchone()[0]

    cursor.execute("""

        SELECT COUNT(*)

        FROM requests

    """)

    total_requests = cursor.fetchone()[0]

    cursor.execute("""

        SELECT COUNT(*)

        FROM metricas

    """)

    total_metricas = cursor.fetchone()[0]

    cursor.execute("""

        SELECT servidor

        FROM metricas

        ORDER BY id DESC

        LIMIT 1

    """)

    ultimo_servidor = cursor.fetchone()[0]

    cursor.execute("""

        SELECT

            cpu_porcentaje,
            ram_porcentaje,
            latencia_ms

        FROM metricas

        ORDER BY id DESC

        LIMIT 1

    """)

    ultima_metrica = cursor.fetchone()
    
    cursor.execute("""

        SELECT

            cpu_porcentaje,
            ram_porcentaje,
            latencia_ms

        FROM metricas

        ORDER BY id DESC

        LIMIT 10

    """)

    historico = cursor.fetchall()
    
    cpu_historial = []

    ram_historial = []

    latencia_historial = []

    for fila in historico:
        cpu_historial.append(fila[0])

        ram_historial.append(fila[1])

        latencia_historial.append(fila[2])

    cursor.close()

    conexion.close()

    return templates.TemplateResponse(

        request=request,

        name="dashboard.html",

        context={

            "clientes": total_clientes,

            "requests": total_requests,

            "metricas": total_metricas,

            "ultimo_servidor": ultimo_servidor,

            "cpu": ultima_metrica[0],

            "ram": ultima_metrica[1],

            "latencia": ultima_metrica[2],
            
            "cpu_historial": cpu_historial,

            "ram_historial": ram_historial,

            "latencia_historial": latencia_historial
        }
   )

@app.get("/dashboard-data")
def dashboard_data():

    conexion = conectar_db()

    cursor = conexion.cursor()
    cursor.execute("SELECT COUNT(*) FROM clientes")

    total_clientes = cursor.fetchone()[0]


    cursor.execute("SELECT COUNT(*) FROM requests")

    total_requests = cursor.fetchone()[0]


    cursor.execute("SELECT COUNT(*) FROM metricas")

    total_metricas = cursor.fetchone()[0]

    cursor.execute("""

        SELECT

            cpu_porcentaje,
            ram_porcentaje,
            latencia_ms

        FROM metricas

        ORDER BY id DESC

        LIMIT 10

    """)

    historico = cursor.fetchall()

    cpu_historial = []

    ram_historial = []

    latencia_historial = []

    for fila in historico:

        cpu_historial.append(fila[0])

        ram_historial.append(fila[1])

        latencia_historial.append(fila[2])

    cursor.close()

    conexion.close()

    return {

        "clientes": total_clientes,

        "requests": total_requests,

        "metricas": total_metricas,

        "cpu_historial": cpu_historial,

        "ram_historial": ram_historial,

        "latencia_historial": latencia_historial

    }
