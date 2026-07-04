def metrica_dict(servidor, cpu=10.0, ram=20.0, disco=30.0, latencia=5.0, **overrides):

    datos = {
        "servidor": servidor,
        "ip_local": "127.0.0.1",
        "internet": "online",
        "latencia_ms": latencia,
        "cpu_porcentaje": cpu,
        "ram_porcentaje": ram,
        "ram_usada_gb": 1.0,
        "ram_total_gb": 8.0,
        "disco_porcentaje": disco,
        "disco_usado_gb": 10.0,
        "disco_total_gb": 100.0,
        "uptime_segundos": 60,
        "os": "Linux",
        "os_version": "test",
        "arquitectura": "x86_64",
        "usuario": "tester",
        "mac_address": "00:00:00:00:00:00",
        "python_version": "3.12",
    }

    datos.update(overrides)

    return datos
