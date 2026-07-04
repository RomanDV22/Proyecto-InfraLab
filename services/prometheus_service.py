from datetime import datetime

from prometheus_client.core import GaugeMetricFamily

from db import conectar_db, liberar_db


class InfraLabCollector:

    def collect(self):

        conexion = conectar_db()

        try:
            cursor = conexion.cursor()

            cpu = GaugeMetricFamily(
                "infralab_cpu_porcentaje",
                "Uso de CPU por servidor (ultimo reporte)",
                labels=["servidor"]
            )
            ram = GaugeMetricFamily(
                "infralab_ram_porcentaje",
                "Uso de RAM por servidor (ultimo reporte)",
                labels=["servidor"]
            )
            disco = GaugeMetricFamily(
                "infralab_disco_porcentaje",
                "Uso de disco por servidor (ultimo reporte)",
                labels=["servidor"]
            )
            latencia = GaugeMetricFamily(
                "infralab_latencia_ms",
                "Latencia reportada por el agente hacia el servidor",
                labels=["servidor"]
            )
            agente_online = GaugeMetricFamily(
                "infralab_agente_online",
                "1 si el ultimo reporte llego hace menos de 30 segundos, 0 si no",
                labels=["servidor"]
            )

            cursor.execute("""
                SELECT DISTINCT ON (servidor)
                    servidor, cpu_porcentaje, ram_porcentaje, disco_porcentaje,
                    latencia_ms, timestamp
                FROM metricas
                ORDER BY servidor, timestamp DESC
            """)

            for servidor, cpu_v, ram_v, disco_v, latencia_v, timestamp in cursor.fetchall():
                if cpu_v is not None:
                    cpu.add_metric([servidor], float(cpu_v))

                if ram_v is not None:
                    ram.add_metric([servidor], float(ram_v))

                if disco_v is not None:
                    disco.add_metric([servidor], float(disco_v))

                if latencia_v is not None:
                    latencia.add_metric([servidor], float(latencia_v))

                online = (datetime.now() - timestamp).total_seconds() < 30
                agente_online.add_metric([servidor], 1.0 if online else 0.0)

            yield cpu
            yield ram
            yield disco
            yield latencia
            yield agente_online

            cursor.execute("SELECT COUNT(*) FROM metricas")
            metricas_total = GaugeMetricFamily(
                "infralab_metricas_total",
                "Cantidad total de metricas guardadas",
                value=cursor.fetchone()[0]
            )
            yield metricas_total

            alertas_total = GaugeMetricFamily(
                "infralab_alertas_total",
                "Cantidad total de alertas registradas por tipo",
                labels=["tipo"]
            )

            cursor.execute("SELECT tipo, COUNT(*) FROM alertas GROUP BY tipo")

            for tipo, cantidad in cursor.fetchall():
                alertas_total.add_metric([tipo], cantidad)

            yield alertas_total

            cursor.close()

        finally:
            liberar_db(conexion)
