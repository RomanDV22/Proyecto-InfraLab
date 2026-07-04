from services.health_service import obtener_health


def test_health_ok_cuando_bd_disponible():
    resultado = obtener_health()

    assert resultado["status"] == "ok"
    assert resultado["api"] == "ok"
    assert resultado["database"] == "ok"
    assert "error" not in resultado
