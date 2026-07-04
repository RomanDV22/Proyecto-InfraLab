from datetime import datetime, timedelta

import db
from services.agentes_service import obtener_agentes
from services.metricas_service import guardar_metrica
from tests.factories import metrica_dict


def test_obtener_agentes_devuelve_uno_por_servidor():
    guardar_metrica(metrica_dict("srv-a"))
    guardar_metrica(metrica_dict("srv-b"))

    agentes = obtener_agentes()

    servidores = {a["servidor"] for a in agentes}
    assert servidores == {"srv-a", "srv-b"}


def test_agente_recien_reportado_esta_online():
    guardar_metrica(metrica_dict("srv-a"))

    agentes = obtener_agentes()

    assert agentes[0]["online"] is True


def test_agente_sin_reportes_recientes_esta_offline():
    conexion = db.conectar_db()

    try:
        cursor = conexion.cursor()

        viejo = datetime.now() - timedelta(minutes=5)

        cursor.execute("""
            INSERT INTO metricas (
                servidor, ip_local, internet, latencia_ms, cpu_porcentaje,
                ram_porcentaje, ram_usada_gb, ram_total_gb, disco_porcentaje,
                disco_usado_gb, disco_total_gb, uptime_segundos, timestamp
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, ("srv-viejo", "127.0.0.1", "online", 1.0, 5.0, 5.0, 1.0, 8.0, 1.0, 1.0, 10.0, 10, viejo))

        conexion.commit()
        cursor.close()

    finally:
        db.liberar_db(conexion)

    agentes = obtener_agentes()
    agente = next(a for a in agentes if a["servidor"] == "srv-viejo")

    assert agente["online"] is False
