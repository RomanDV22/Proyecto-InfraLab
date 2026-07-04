import pytest
from pydantic import ValidationError

from schemas import MetricaIn
from tests.factories import metrica_dict


def test_metrica_valida_con_campos_opcionales_ausentes():
    datos = metrica_dict("srv-test")

    for campo in ("os", "os_version", "arquitectura", "usuario", "mac_address", "python_version"):
        del datos[campo]

    metrica = MetricaIn(**datos)

    assert metrica.servidor == "srv-test"
    assert metrica.os is None


def test_metrica_falla_sin_campo_requerido():
    datos = metrica_dict("srv-test")
    del datos["cpu_porcentaje"]

    with pytest.raises(ValidationError):
        MetricaIn(**datos)
