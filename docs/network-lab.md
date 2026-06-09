# Laboratorio de Red de InfraLab

InfraLab puede usarse como laboratorio para practicar backend, servidores y redes en una red local.

## Topologia Inicial

```text
Notebook con WSL
   -> ejecuta agente o dashboard

PC/Servidor
   -> ejecuta FastAPI
   -> ejecuta PostgreSQL

Red WiFi local
   -> conecta notebook y PC
```

Tambien se puede ejecutar todo en la misma maquina durante las primeras pruebas.

## Puertos Importantes

- `8000`: servidor FastAPI de InfraLab.
- `5432`: PostgreSQL, idealmente solo accesible desde la maquina servidor.

## Pruebas Basicas de Red

Ver IP local en Linux/WSL:

```bash
ip addr
```

Probar conectividad con el servidor:

```bash
ping IP_DEL_SERVIDOR
```

Probar que FastAPI responde:

```bash
curl http://IP_DEL_SERVIDOR:8000/health
```

Ver puertos escuchando en el servidor:

```bash
ss -tulpen
```

## Flujo de Datos

```text
Agente
   -> mide CPU, RAM, disco, internet y latencia
   -> envia POST /api/metricas

FastAPI
   -> recibe JSON
   -> guarda en PostgreSQL

Dashboard
   -> consulta PostgreSQL
   -> muestra metricas historicas
```

## Idea para Packet Tracer

Packet Tracer puede usarse para dibujar una version conceptual:

```text
Cliente/Agente -> Switch/AP -> Servidor InfraLab -> Base de Datos
```

Aunque Packet Tracer no ejecute FastAPI ni PostgreSQL reales, sirve para practicar:

- direccionamiento IP
- subredes
- puertos
- rutas
- diferencia entre cliente, servidor y base de datos
- flujo de paquetes entre dispositivos

## Proxima Meta de Red

Cuando el servidor y el agente funcionen en una sola maquina, mover el agente a otra maquina de la misma red:

```text
Notebook agente
   -> http://IP_PC_SERVIDOR:8000/api/metricas
   -> PC servidor
```

Ese paso convierte InfraLab en un laboratorio real de red local.
