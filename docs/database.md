# Base de Datos de InfraLab

InfraLab usa PostgreSQL para guardar metricas enviadas por los agentes y para alimentar el dashboard web.

El archivo principal del esquema esta en:

```text
database/schema.sql
```

## Tablas

### metricas

Es la tabla central del proyecto. Cada fila representa un reporte enviado por un agente.

Campos principales:

- `servidor`: nombre del equipo que envia la metrica.
- `ip_local`: IP local detectada por el agente.
- `internet`: estado simple de conectividad.
- `latencia_ms`: latencia reportada en milisegundos.
- `cpu_porcentaje`: uso de CPU.
- `ram_porcentaje`: uso de RAM.
- `ram_usada_gb` y `ram_total_gb`: memoria usada y total.
- `disco_porcentaje`, `disco_usado_gb` y `disco_total_gb`: uso de disco.
- `uptime_segundos`: tiempo encendido del sistema.
- `os`, `os_version`, `arquitectura`, `usuario`, `mac_address`, `python_version`: datos del sistema.
- `timestamp`: fecha y hora en que PostgreSQL guarda la metrica.

### clientes

Tabla preparada para registrar clientes que acceden al servidor. Hoy el dashboard la usa para contar registros.

Campos actuales:

- `ip`: IP del cliente.
- `primer_acceso`: fecha y hora del primer registro.
- `mac_address`: direccion MAC si se logra detectar.

### requests

Tabla preparada para registrar requests HTTP. Hoy el dashboard la usa para contar registros.

Campos actuales:

- `ip_cliente`: IP que hizo el request.
- `endpoint`: ruta consultada.
- `metodo`: metodo HTTP.
- `timestamp`: fecha y hora del request.

### alertas

Guarda las alertas generadas automaticamente cuando una metrica supera un umbral (CPU, RAM o disco por encima de 90%). Hay un cooldown de 5 minutos por servidor y tipo de alerta para evitar spam.

Campos actuales:

- `servidor`: equipo que disparo la alerta.
- `tipo`: `cpu_alto`, `ram_alta` o `disco_alto`.
- `mensaje`: descripcion legible.
- `valor`: valor que disparo la alerta.
- `timestamp`: fecha y hora de la alerta.

Se consulta en `/alertas` (HTML) y `/api/alertas` (JSON).

Como la tabla la crea el usuario `postgres`, hay que otorgarle permisos al usuario de la aplicacion:

```sql
GRANT SELECT, INSERT, UPDATE ON alertas TO roman;
GRANT USAGE, SELECT ON SEQUENCE alertas_id_seq TO roman;
```

## Crear la Base desde Cero

Entrar a PostgreSQL:

```bash
psql -U postgres
```

Crear la base:

```sql
CREATE DATABASE infralab;
```

Salir de `psql`:

```sql
\q
```

Aplicar el esquema desde la raiz del proyecto:

```bash
psql -U postgres -d infralab -f database/schema.sql
```

Si se usa el usuario configurado en `.env`, ese usuario debe tener permisos para crear tablas en el esquema `public`. En el entorno actual, las tablas existentes pertenecen al usuario `postgres`.

## Variables de Entorno

El servidor lee la conexion desde `.env` usando estas variables:

```env
DB_HOST=localhost
DB_NAME=infralab
DB_USER=roman
DB_PASSWORD=tu_password
API_KEY=una_clave_larga_compartida
```

`API_KEY` la valida el servidor en cada `POST /api/metricas` (header `X-API-Key`). Generar una con:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

El agente lee la URL del servidor y la misma `API_KEY`:

```env
SERVER_URL=http://IP_DEL_SERVIDOR:8000/api/metricas
API_KEY=una_clave_larga_compartida
```

## Roles de PostgreSQL

En el entorno actual se usan dos roles con responsabilidades distintas:

- `postgres`: usuario administrador. Es el dueño de las tablas actuales y se usa para crear o modificar estructura.
- `roman`: usuario de la aplicacion. Se usa desde InfraLab para consultar e insertar datos.

Esta separacion es intencional. La aplicacion no necesita permisos para crear tablas, modificar columnas o crear indices durante su uso normal.

Cuando haya que aplicar cambios de estructura, usar `postgres`:

```bash
psql -U postgres -d infralab -f database/schema.sql
```

Cuando InfraLab se ejecuta normalmente, usa el usuario configurado en `.env`:

```env
DB_USER=roman
```

## Verificar Permisos y Tablas

Ver tablas existentes y sus dueños:

```sql
SELECT schemaname, tablename, tableowner
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY tablename;
```

Resultado esperado en el entorno actual:

```text
clientes  -> postgres
metricas  -> postgres
requests  -> postgres
```

## Probar que la Tabla Recibe Datos

Despues de ejecutar el agente, se puede verificar con:

```sql
SELECT id, servidor, ip_local, cpu_porcentaje, ram_porcentaje, timestamp
FROM metricas
ORDER BY id DESC
LIMIT 5;
```
