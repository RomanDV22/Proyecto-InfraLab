from fastapi import APIRouter

from db import conectar_db


router = APIRouter()


@router.post("/api/metricas")

def recibir_metricas(datos: dict):

    conexion = conectar_db()

    cursor = conexion.cursor()


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


    return {

        "status": "ok"

    }
