import requests

import socket

import psutil

import time



SERVER_URL = "http://172.28.37.80:8000/api/metricas"



while True:

    hostname = socket.gethostname()


    ip_local = socket.gethostbyname(hostname)


    cpu = psutil.cpu_percent(interval=1)


    ram = psutil.virtual_memory()


    datos = {

        "servidor": hostname,

        "ip_local": ip_local,

        "internet": "online",

        "latencia_ms": 0,

        "cpu_porcentaje": cpu,

        "ram_porcentaje": ram.percent,

        "ram_usada_gb": round(ram.used / (1024 ** 3), 2),

        "ram_total_gb": round(ram.total / (1024 ** 3), 2)

    }


    try:

        response = requests.post(

            SERVER_URL,

            json=datos

        )


        print(

            f"[OK] "

            f"{time.strftime('%H:%M:%S')} "

            f"{response.status_code}",

            flush=True
        )

    except Exception as e:

        print(

            f"[ERROR] "

            f"{time.strftime('%H:%M:%S')} "

            f"{e}",

            flush=True
        )

    time.sleep(5)
