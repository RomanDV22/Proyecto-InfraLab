CREATE TABLE IF NOT EXISTS clientes (
    id SERIAL PRIMARY KEY,
    ip TEXT,
    primer_acceso TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    mac_address TEXT
);

CREATE TABLE IF NOT EXISTS requests (
    id SERIAL PRIMARY KEY,
    ip_cliente TEXT,
    endpoint TEXT,
    metodo TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS metricas (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    servidor TEXT,
    ip_local TEXT,
    internet TEXT,
    latencia_ms REAL,
    cpu_porcentaje REAL,
    ram_porcentaje REAL,
    ram_usada_gb REAL,
    ram_total_gb REAL,
    disco_porcentaje REAL,
    disco_usado_gb REAL,
    disco_total_gb REAL,
    uptime_segundos BIGINT,
    os TEXT,
    os_version TEXT,
    arquitectura TEXT,
    usuario TEXT,
    mac_address TEXT,
    python_version TEXT
);

CREATE INDEX IF NOT EXISTS idx_metricas_servidor_timestamp
ON metricas (servidor, timestamp DESC);

CREATE INDEX IF NOT EXISTS idx_metricas_timestamp
ON metricas (timestamp DESC);
