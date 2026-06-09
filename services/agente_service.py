from db import conectar_db


def obtener_agente(nombre):

    conexion = conectar_db()

    cursor = conexion.cursor()


    cursor.execute("""

        SELECT

            timestamp,
            cpu_porcentaje,
            ram_porcentaje,
            ip_local

        FROM metricas

        WHERE servidor = %s

        ORDER BY timestamp DESC

        LIMIT 20

    """, (nombre,))


    metricas = cursor.fetchall()


    metricas.reverse()

    if not metricas:

        cursor.close()
        conexion.close()

        return None
    
    ultima = metricas[-1]

    timestamps = []

    cpu = []

    ram = []


    for metrica in metricas:

        timestamps.append(

            metrica[0].strftime("%H:%M:%S")

        )

        cpu.append(metrica[1])

        ram.append(metrica[2])


    cursor.close()

    conexion.close()


    return {

        "servidor": nombre,

        "timestamps": timestamps,

        "cpu": cpu,

        "ram": ram,
        
        "ultima_cpu": ultima[1],

        "ultima_ram": ultima[2],

        "ultima_ip": ultima[3],

        "ultimo_timestamp": ultima[0]
    
    }
