from services.alertas_service import evaluar_alertas, obtener_alertas
from tests.factories import metrica_dict


def test_evaluar_alertas_crea_alerta_por_cpu_alto():
    evaluar_alertas(metrica_dict("srv-a", cpu=95.0))

    alertas = obtener_alertas()

    assert len(alertas) == 1
    assert alertas[0]["servidor"] == "srv-a"
    assert alertas[0]["tipo"] == "cpu_alto"


def test_evaluar_alertas_no_dispara_bajo_el_umbral():
    evaluar_alertas(metrica_dict("srv-a", cpu=10.0, ram=10.0, disco=10.0))

    assert obtener_alertas() == []


def test_evaluar_alertas_respeta_cooldown():
    evaluar_alertas(metrica_dict("srv-a", cpu=95.0))
    evaluar_alertas(metrica_dict("srv-a", cpu=96.0))

    assert len(obtener_alertas()) == 1


def test_evaluar_alertas_dispara_varios_tipos_a_la_vez():
    evaluar_alertas(metrica_dict("srv-a", cpu=95.0, ram=95.0, disco=95.0))

    tipos = {a["tipo"] for a in obtener_alertas()}

    assert tipos == {"cpu_alto", "ram_alta", "disco_alto"}
