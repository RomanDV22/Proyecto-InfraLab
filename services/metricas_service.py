from db import conectar_db, liberar_db


def guardar_metrica(datos):

    conexion = conectar_db()

    try:
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
                ram_total_gb,
                disco_porcentaje,
                disco_usado_gb,
                disco_total_gb,
                uptime_segundos,
                os,
                os_version,
                arquitectura,
                usuario,
                mac_address,
                python_version

            )

            VALUES (
                %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s
            )

        """, (

            datos["servidor"],
            datos["ip_local"],
            datos["internet"],
            datos["latencia_ms"],
            datos["cpu_porcentaje"],
            datos["ram_porcentaje"],
            datos["ram_usada_gb"],
            datos["ram_total_gb"],
            datos["disco_porcentaje"],
            datos["disco_usado_gb"],
            datos["disco_total_gb"],
            datos["uptime_segundos"],
            datos.get("os"),
            datos.get("os_version"),
            datos.get("arquitectura"),
            datos.get("usuario"),
            datos.get("mac_address"),
            datos.get("python_version")

        ))

        conexion.commit()

        cursor.close()

    finally:
        liberar_db(conexion)


def obtener_metricas():

    conexion = conectar_db()

    try:
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT *
            FROM metricas
            ORDER BY id DESC
            LIMIT 10
        """)

        filas = cursor.fetchall()

        cursor.close()

        return filas

    finally:
        liberar_db(conexion)
