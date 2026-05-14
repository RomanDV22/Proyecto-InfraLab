from fastapi import FastAPI
import psutil
import socket
import requests
import time

app = FastAPI()

@app.get("/")
def root():

    hostname = socket.gethostname()

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

    return {

        "servidor": hostname,

        "ip_local": ip_local,

        "internet": internet,

        "latencia_ms": latencia_ms,

        "cpu_porcentaje": cpu,

        "ram_porcentaje": ram.percent,

        "ram_usada_gb": round(ram.used / (1024 ** 3), 2),

        "ram_total_gb": round(ram.total / (1024 ** 3), 2)
    }