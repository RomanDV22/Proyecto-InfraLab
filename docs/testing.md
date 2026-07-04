# Tests de InfraLab

Los tests son de integracion: corren contra una base de datos Postgres real (`infralab_test`), no contra mocks. Cada test se ejecuta sobre datos limpios porque `conftest.py` trunca las tablas despues de cada test.

## Preparar la base de datos de tests (una sola vez)

`infralab_test` debe existir y pertenecer al mismo usuario configurado en `.env` (`DB_USER`), para que los tests puedan crear/modificar tablas sin usar `postgres`:

```bash
sudo -u postgres psql -c "CREATE DATABASE infralab_test OWNER roman;"
```

El esquema (`database/schema.sql`) se aplica automaticamente al iniciar la sesion de tests, no hace falta correrlo a mano.

## Instalar dependencias de desarrollo

```bash
source venv/bin/activate
pip install -r requirements-dev.txt
```

## Correr los tests

Desde la raiz del proyecto:

```bash
python -m pytest -v
```

Usar `python -m pytest` (no solo `pytest`) para que la raiz del proyecto quede en el `sys.path` y los tests puedan importar `services`, `db` y `schemas` igual que la app.

## Como funciona

`conftest.py` en la raiz:

1. Fuerza `DB_NAME=infralab_test` antes de que `db.py` lea el `.env`, para que el pool de conexiones apunte a la base de tests y nunca a la de produccion.
2. Al iniciar la sesion, aplica `database/schema.sql` (es idempotente, usa `CREATE TABLE IF NOT EXISTS`).
3. Despues de cada test, hace `TRUNCATE` de `metricas`, `alertas`, `clientes` y `requests` para que el siguiente test arranque en blanco.

`tests/factories.py` tiene un helper `metrica_dict(servidor, ...)` para no repetir el payload de una metrica en cada test.
