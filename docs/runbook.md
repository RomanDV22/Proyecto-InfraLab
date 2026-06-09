# Guia de Arranque de InfraLab

Esta guia resume el flujo minimo para levantar InfraLab desde WSL.

## 1. Verificar PostgreSQL

Comprobar que PostgreSQL responde:

```bash
psql -U roman -d infralab -c "SELECT COUNT(*) FROM metricas;"
```

Si hay problemas de estructura, aplicar el esquema como administrador:

```bash
psql -U postgres -d infralab -f database/schema.sql
```

## 2. Revisar Variables de Entorno

El servidor necesita:

```env
DB_HOST=localhost
DB_NAME=infralab
DB_USER=roman
DB_PASSWORD=tu_password
```

El agente necesita:

```env
SERVER_URL=http://IP_DEL_SERVIDOR:8000/api/metricas
```

En una prueba local, puede ser:

```env
SERVER_URL=http://127.0.0.1:8000/api/metricas
```

## 3. Levantar el Servidor

Desde la raiz del proyecto:

```bash
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## 4. Probar el Healthcheck

Desde otra terminal:

```bash
curl http://127.0.0.1:8000/health
```

Respuesta esperada:

```json
{
  "status": "ok",
  "api": "ok",
  "database": "ok",
  "metricas": 2249
}
```

La cantidad de metricas puede variar.

## 5. Ejecutar el Agente

Desde otra terminal:

```bash
source venv/bin/activate
python agents/agent.py
```

El agente envia metricas cada 10 segundos.

## 6. Abrir el Dashboard

En el navegador:

```text
http://127.0.0.1:8000/dashboard
```

Vista de agentes:

```text
http://127.0.0.1:8000/agentes
```

## Checklist Rapido

- PostgreSQL responde.
- `.env` tiene credenciales correctas.
- FastAPI corre en el puerto `8000`.
- `/health` devuelve `status: ok`.
- El agente imprime respuestas `[OK]`.
- El dashboard muestra metricas.
