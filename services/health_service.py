from datetime import datetime

from db import conectar_db


def obtener_health():
    resultado = {
        "status": "ok",
        "api": "ok",
        "database": "ok",
        "metricas": 0,
        "timestamp": datetime.now().isoformat(timespec="seconds"),
    }

    try:
        conexion = conectar_db()
        cursor = conexion.cursor()

        cursor.execute("SELECT 1")
        cursor.fetchone()

        cursor.execute("SELECT COUNT(*) FROM metricas")
        resultado["metricas"] = cursor.fetchone()[0]

        cursor.close()
        conexion.close()

    except Exception as error:
        resultado["status"] = "degraded"
        resultado["database"] = "error"
        resultado["error"] = str(error)

    return resultado
