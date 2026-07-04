from db import conectar_db, liberar_db
from psycopg2.extras import RealDictCursor
from datetime import datetime

def obtener_agentes():

    conexion = conectar_db()

    try:
        cursor = conexion.cursor(
            cursor_factory=RealDictCursor
        )

        cursor.execute("""

            SELECT DISTINCT ON (servidor)

                servidor,
                internet,
                cpu_porcentaje,
                ram_porcentaje,
                ip_local,
                timestamp,
                os,
                usuario,
                python_version

            FROM metricas

            ORDER BY servidor, timestamp DESC

        """)


        agentes = cursor.fetchall()


        resultado = []


        for agente in agentes:

            diferencia = (

                datetime.now() - agente["timestamp"]

            ).total_seconds()

            online = diferencia < 30

            resultado.append({

                "servidor": agente["servidor"],

                "internet": agente["internet"],

                "cpu": agente["cpu_porcentaje"],

                "ram": agente["ram_porcentaje"],

                "ip": agente["ip_local"],

                "timestamp": agente["timestamp"],

                "os": agente["os"],

                "usuario": agente["usuario"],

                "python_version": agente["python_version"],

                "online": online

            })

        cursor.close()

        return resultado

    finally:
        liberar_db(conexion)
