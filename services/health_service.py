from datetime import datetime

from db import conectar_db, liberar_db


def obtener_health():
    resultado = {
        "status": "ok",
        "api": "ok",
        "database": "ok",
        "metricas": 0,
        "timestamp": datetime.now().isoformat(timespec="seconds"),
    }

    conexion = None

    try:
        conexion = conectar_db()
        cursor = conexion.cursor()

        cursor.execute("SELECT 1")
        cursor.fetchone()

        cursor.execute("SELECT COUNT(*) FROM metricas")
        resultado["metricas"] = cursor.fetchone()[0]

        cursor.close()

    except Exception as error:
        resultado["status"] = "degraded"
        resultado["database"] = "error"
        resultado["error"] = str(error)

    finally:
        if conexion is not None:
            liberar_db(conexion)

    return resultado
