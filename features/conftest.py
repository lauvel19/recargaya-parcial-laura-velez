# features/conftest.py
import pytest
from pytest_bdd import given, when, then, parsers
from app.recarga import calcular_recarga


@pytest.fixture
def context():
    return {}


@given(parsers.re(r"que el usuario intenta recargar \$?(?P<monto>\d+) pesos"))
def step_monto(context, monto):
    context["monto"] = int(monto)


@given("el usuario no tiene plan premium")
def step_no_premium(context):
    context["premium"] = False


@given("el usuario tiene plan premium")
def step_premium(context):
    context["premium"] = True


@when("se procesa la recarga")
def step_procesar(context):
    context["resultado"] = calcular_recarga(
        monto=context["monto"],
        premium=context["premium"]
    )


@then("la recarga es rechazada")
def step_rechazada(context):
    assert context["resultado"]["aceptada"] is False


@then("la recarga es aceptada")
def step_aceptada(context):
    assert context["resultado"]["aceptada"] is True


@then("el mensaje indica que el monto está fuera del rango permitido")
def step_mensaje_rango(context):
    assert "rechazado" in context["resultado"]["mensaje"].lower()


@then(parsers.parse("la bonificación de datos es del {bonificacion:d}%"))
def step_bonificacion(context, bonificacion):
    assert context["resultado"]["bonificacion_pct"] == bonificacion


@then(parsers.parse("la recarga es {estado}"))
def step_estado_outline(context, estado):
    if estado == "aceptada":
        assert context["resultado"]["aceptada"] is True
    else:
        assert context["resultado"]["aceptada"] is False