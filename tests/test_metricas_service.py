from services.metricas_service import guardar_metrica, obtener_metricas
from tests.factories import metrica_dict

# SELECT * en metricas devuelve columnas en el orden del schema:
# 0=id, 1=timestamp, 2=servidor, 3=ip_local, ..., 6=cpu_porcentaje
COL_SERVIDOR = 2
COL_CPU = 6


def test_guardar_y_obtener_metrica():
    guardar_metrica(metrica_dict("srv-a", cpu=15.0))

    filas = obtener_metricas()

    assert len(filas) == 1
    assert filas[0][COL_SERVIDOR] == "srv-a"
    assert filas[0][COL_CPU] == 15.0


def test_obtener_metricas_devuelve_mas_reciente_primero():
    guardar_metrica(metrica_dict("srv-a", cpu=10.0))
    guardar_metrica(metrica_dict("srv-a", cpu=20.0))

    filas = obtener_metricas()

    assert filas[0][COL_CPU] == 20.0
    assert filas[1][COL_CPU] == 10.0


def test_obtener_metricas_respeta_limite_de_10():
    for i in range(12):
        guardar_metrica(metrica_dict("srv-a", cpu=float(i)))

    filas = obtener_metricas()

    assert len(filas) == 10
