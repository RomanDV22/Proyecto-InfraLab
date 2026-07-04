from services.agente_service import obtener_agente
from services.metricas_service import guardar_metrica
from tests.factories import metrica_dict


def test_obtener_agente_inexistente_retorna_none():
    assert obtener_agente("no-existe") is None


def test_obtener_agente_devuelve_historial_ordenado():
    guardar_metrica(metrica_dict("srv-x", cpu=10.0, ram=11.0))
    guardar_metrica(metrica_dict("srv-x", cpu=20.0, ram=21.0))

    datos = obtener_agente("srv-x")

    assert datos["servidor"] == "srv-x"
    assert datos["cpu"] == [10.0, 20.0]
    assert datos["ram"] == [11.0, 21.0]
    assert datos["ultima_cpu"] == 20.0
    assert datos["ultima_ram"] == 21.0
