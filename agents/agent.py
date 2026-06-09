import platform
import getpass
import uuid
import socket
import time
import shutil
import requests
import psutil

import os
from dotenv import load_dotenv
from urllib.parse import urlparse

from datetime import datetime

#URL = "http://172.28.37.80:8000/api/metricas"
#URL = "http://192.168.0.139:8000/api/metricas"

load_dotenv()

URL = os.getenv("SERVER_URL")

if not URL:
    raise RuntimeError("SERVER_URL no esta definido en .env")


def obtener_ip_local():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as conexion:
            conexion.connect(("8.8.8.8", 80))
            return conexion.getsockname()[0]
    except OSError:
        return socket.gethostbyname(socket.gethostname())


def obtener_estado_internet():
    try:
        with socket.create_connection(("1.1.1.1", 53), timeout=2):
            return "online"
    except OSError:
        return "offline"


def medir_latencia_servidor(url):
    partes = urlparse(url)
    host = partes.hostname

    if not host:
        return 0

    if partes.port:
        port = partes.port
    elif partes.scheme == "https":
        port = 443
    else:
        port = 80

    inicio = time.perf_counter()

    try:
        with socket.create_connection((host, port), timeout=3):
            return round((time.perf_counter() - inicio) * 1000, 2)
    except OSError:
        return 0

while True:

    try:

        hostname = socket.gethostname()

        ip_local = obtener_ip_local()

        cpu = psutil.cpu_percent()

        ram = psutil.virtual_memory()

        disco = shutil.disk_usage("/")

        disco_total_gb = round(

            disco.total / (1024 ** 3), 2

        )


        disco_usado_gb = round(

            disco.used / (1024 ** 3), 2

        )


        disco_porcentaje = round(

            (disco.used / disco.total) * 100, 2

        )


        uptime_segundos = round(

            time.time() - psutil.boot_time()

        )

        sistema_operativo = platform.system()
        version_so = platform.release()
        arquitectura = platform.machine()
        usuario = getpass.getuser()

        mac = ':'.join([
            f'{(uuid.getnode() >> ele) & 0xff:02x}'
        
            for ele in range(0, 8 * 6, 8)
        
        ][::-1])

        python_version = platform.python_version()
        datos = {

            "servidor": hostname,

            "ip_local": ip_local,

            "internet": obtener_estado_internet(),

            "latencia_ms": medir_latencia_servidor(URL),

            "cpu_porcentaje": cpu,

            "ram_porcentaje": ram.percent,

            "ram_usada_gb": round(

                ram.used / (1024 ** 3), 2

            ),

            "ram_total_gb": round(

                ram.total / (1024 ** 3), 2

            ),

            "disco_porcentaje": disco_porcentaje,

            "disco_usado_gb": disco_usado_gb,

            "disco_total_gb": disco_total_gb,

            "uptime_segundos": uptime_segundos,

            "os": sistema_operativo,
            "os_version": version_so,
            "arquitectura": arquitectura,
            "usuario": usuario,
            "mac_address": mac, 
            "python_version": python_version
        }


        response = requests.post(
    	    
	    URL,
    	    json=datos,
            timeout=5
	)


        print(

            f"[OK] "

            f"{datetime.now().strftime('%H:%M:%S')} "

            f"{response.status_code}"

        )


    except Exception as e:

        print(

            f"[ERROR] "

            f"{datetime.now().strftime('%H:%M:%S')} "

            f"{e}"

        )


    time.sleep(10)
