from services.dashboard_service import obtener_dashboard
from services.metricas_service import guardar_metrica
from tests.factories import metrica_dict


def test_dashboard_sin_datos():
    datos = obtener_dashboard()

    assert datos["metricas"] == 0
    assert datos["ultimo_servidor"] == "Sin datos"
    assert datos["cpu"] == 0


def test_dashboard_cuenta_metricas_y_ultima_metrica():
    guardar_metrica(metrica_dict("srv-a", cpu=15.0))
    guardar_metrica(metrica_dict("srv-a", cpu=25.0))

    datos = obtener_dashboard()

    assert datos["metricas"] == 2
    assert datos["ultimo_servidor"] == "srv-a"
    assert datos["cpu"] == 25.0
    assert datos["cpu_historial"] == [25.0, 15.0]
