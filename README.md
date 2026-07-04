# InfraLab

InfraLab es un proyecto personal de infraestructura y observabilidad construido con FastAPI y PostgreSQL.

El objetivo del proyecto es monitorear sistemas, recolectar métricas, visualizar datos históricos y experimentar con conceptos de backend, redes e infraestructura.

---

## Características

- Backend con FastAPI
- Base de datos PostgreSQL con pool de conexiones
- Dashboard en vivo actualizado por WebSockets
- Gráficos históricos
- Seguimiento de clientes
- Registro de requests
- Almacenamiento de métricas con validación Pydantic
- Alertas por umbral (CPU/RAM/disco)
- Autenticación por API key para los agentes
- Endpoint de healthcheck
- Endpoint de métricas para Prometheus
- Arquitectura modular

---

## Stack Tecnológico

- Python
- FastAPI
- PostgreSQL
- HTML
- CSS
- JavaScript
- Chart.js
- Uvicorn
- WSL2

---

## Instalación

Clonar el repositorio:

```bash
git clone https://github.com/RomanDV22/Proyecto-InfraLab.git
```

Entrar al proyecto:

```bash
cd Infralab
```

Crear el entorno virtual:

```bash
python3 -m venv venv
```

Activar el entorno:

```bash
source venv/bin/activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Crear el esquema de la base de datos PostgreSQL:

```bash
psql -U postgres -d infralab -f database/schema.sql
```

Más detalles disponibles en [docs/database.md](docs/database.md).

Guías útiles:

- [Guía de arranque](docs/runbook.md)
- [Documentación de la base de datos](docs/database.md)
- [Notas del laboratorio de red](docs/network-lab.md)
- [Prometheus y Grafana](docs/prometheus.md)
- [Cómo correr los tests](docs/testing.md)

---

## Levantar el Servidor

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

---

## Dashboard

Abrir en el navegador:

```text
http://SERVER_IP:8000/dashboard
```

Healthcheck:

```text
http://SERVER_IP:8000/health
```

Alertas:

```text
http://SERVER_IP:8000/alertas
```

Métricas de Prometheus:

```text
http://SERVER_IP:8000/metrics
```

Ver [docs/prometheus.md](docs/prometheus.md) para scrapearlo con Prometheus y armar un dashboard en Grafana.

---

## Capacidades Actuales

- Visualización de métricas
- Monitoreo histórico
- Seguimiento de requests
- Actualizaciones del dashboard en vivo
- Persistencia en base de datos

---

## Mejoras Futuras

- Soporte para Docker
- Monitoreo multi-agente
- Analítica avanzada
- Envío de alertas a Discord/Telegram/webhooks

---

## Arquitectura

```text
Cliente
   ↓
FastAPI
   ↓
Servicios
   ↓
PostgreSQL
```
