# Prometheus y Grafana en InfraLab

InfraLab expone metricas en formato Prometheus en:

```text
http://SERVER_IP:8000/metrics
```

No requiere autenticacion (a diferencia de `/api/metricas`, que es para los agentes).

## Metricas expuestas

- `infralab_cpu_porcentaje{servidor="..."}`: ultimo uso de CPU reportado.
- `infralab_ram_porcentaje{servidor="..."}`: ultimo uso de RAM reportado.
- `infralab_disco_porcentaje{servidor="..."}`: ultimo uso de disco reportado.
- `infralab_latencia_ms{servidor="..."}`: ultima latencia reportada.
- `infralab_agente_online{servidor="..."}`: `1` si el ultimo reporte llego hace menos de 30 segundos, `0` si no.
- `infralab_metricas_total`: cantidad total de filas en la tabla `metricas`.
- `infralab_alertas_total{tipo="..."}`: cantidad de alertas registradas por tipo (`cpu_alto`, `ram_alta`, `disco_alto`).

Cada scrape consulta la base de datos en el momento (no hay estado en memoria), asi que los valores siempre reflejan el ultimo reporte guardado.

## Configurar Prometheus para scrapear InfraLab

En `prometheus.yml`:

```yaml
scrape_configs:
  - job_name: infralab
    scrape_interval: 15s
    static_configs:
      - targets: ["SERVER_IP:8000"]
```

Probar que Prometheus lo levanta:

```bash
curl http://SERVER_IP:8000/metrics
```

## Ver InfraLab en Grafana

1. Agregar Prometheus como data source en Grafana (URL del servidor de Prometheus).
2. Crear un dashboard nuevo con paneles usando estas queries de ejemplo:

```promql
infralab_cpu_porcentaje
infralab_ram_porcentaje
infralab_disco_porcentaje
infralab_latencia_ms
sum(infralab_agente_online) by (servidor)
increase(infralab_alertas_total[1h])
```

3. Para ver agentes offline, una alerta de Grafana o Prometheus Alertmanager puede dispararse con:

```promql
infralab_agente_online == 0
```

Esto complementa (no reemplaza) el sistema de alertas propio de InfraLab (`/alertas`): las alertas de Prometheus corren en un proceso externo y sobreviven aunque InfraLab este caido, mientras que las de `/alertas` dependen de que el propio servidor reciba metricas para evaluarlas.
