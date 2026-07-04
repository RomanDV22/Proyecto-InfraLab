from datetime import datetime

from db import conectar_db, liberar_db

COOLDOWN_SEGUNDOS = 300

UMBRALES = {
    "cpu_alto": ("cpu_porcentaje", 90, "Uso de CPU alto"),
    "ram_alta": ("ram_porcentaje", 90, "Uso de RAM alto"),
    "disco_alto": ("disco_porcentaje", 90, "Uso de disco alto"),
}


def evaluar_alertas(datos):

    conexion = conectar_db()

    try:
        cursor = conexion.cursor()

        for tipo, (campo, umbral, mensaje) in UMBRALES.items():

            valor = datos.get(campo)

            if valor is None or valor < umbral:
                continue

            cursor.execute("""
                SELECT timestamp
                FROM alertas
                WHERE servidor = %s AND tipo = %s
                ORDER BY timestamp DESC
                LIMIT 1
            """, (datos["servidor"], tipo))

            ultima = cursor.fetchone()

            if ultima and (datetime.now() - ultima[0]).total_seconds() < COOLDOWN_SEGUNDOS:
                continue

            cursor.execute("""
                INSERT INTO alertas (servidor, tipo, mensaje, valor)
                VALUES (%s, %s, %s, %s)
            """, (datos["servidor"], tipo, mensaje, valor))

        conexion.commit()

        cursor.close()

    finally:
        liberar_db(conexion)


def obtener_alertas():

    conexion = conectar_db()

    try:
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT servidor, tipo, mensaje, valor, timestamp
            FROM alertas
            ORDER BY timestamp DESC
            LIMIT 50
        """)

        filas = cursor.fetchall()

        cursor.close()

        return [
            {
                "servidor": fila[0],
                "tipo": fila[1],
                "mensaje": fila[2],
                "valor": fila[3],
                "timestamp": fila[4].strftime("%Y-%m-%d %H:%M:%S"),
            }
            for fila in filas
        ]

    finally:
        liberar_db(conexion)
