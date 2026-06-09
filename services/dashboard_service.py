from db import conectar_db


def obtener_dashboard():

    conexion = conectar_db()

    cursor = conexion.cursor()


    cursor.execute("SELECT COUNT(*) FROM clientes")

    total_clientes = cursor.fetchone()[0]


    cursor.execute("SELECT COUNT(*) FROM requests")

    total_requests = cursor.fetchone()[0]


    cursor.execute("SELECT COUNT(*) FROM metricas")

    total_metricas = cursor.fetchone()[0]


    cursor.execute("""

        SELECT servidor

        FROM metricas

        ORDER BY id DESC

        LIMIT 1

    """)

    ultimo_servidor_fila = cursor.fetchone()

    ultimo_servidor = ultimo_servidor_fila[0] if ultimo_servidor_fila else "Sin datos"


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

        cpu_historial.append(float(fila[0]))

        ram_historial.append(float(fila[1]))

        latencia_historial.append(float(fila[2]))


    cursor.close()

    conexion.close()


    return {

        "clientes": total_clientes,

        "requests": total_requests,

        "metricas": total_metricas,

        "ultimo_servidor": ultimo_servidor,

        "cpu": float(ultima_metrica[0]) if ultima_metrica else 0,

        "ram": float(ultima_metrica[1]) if ultima_metrica else 0,

        "latencia": float(ultima_metrica[2]) if ultima_metrica else 0,

        "cpu_historial": cpu_historial,

        "ram_historial": ram_historial,

        "latencia_historial": latencia_historial

    }
