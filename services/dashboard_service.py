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


    return {

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
