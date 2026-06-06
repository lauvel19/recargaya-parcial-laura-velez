import pytest
from app.recarga import calcular_recarga


# ── Casos inválidos (partición de equivalencia y valores límite) ──

def test_monto_menor_minimo_rechazado():
    resultado = calcular_recarga(monto=999, premium=False)
    assert resultado["aceptada"] is False
    assert "rechazado" in resultado["mensaje"].lower()

def test_monto_cero_rechazado():
    resultado = calcular_recarga(monto=0, premium=False)
    assert resultado["aceptada"] is False

def test_monto_negativo_rechazado():
    resultado = calcular_recarga(monto=-500, premium=False)
    assert resultado["aceptada"] is False

def test_monto_mayor_maximo_rechazado():
    resultado = calcular_recarga(monto=50001, premium=False)
    assert resultado["aceptada"] is False

# ── Clase 1: [1000, 9999] — sin bonificación ──

def test_monto_minimo_aceptado():
    resultado = calcular_recarga(monto=1000, premium=False)
    assert resultado["aceptada"] is True
    assert resultado["bonificacion_pct"] == 0

def test_monto_medio_clase1():
    resultado = calcular_recarga(monto=5000, premium=False)
    assert resultado["aceptada"] is True
    assert resultado["bonificacion_pct"] == 0

def test_limite_superior_clase1():
    resultado = calcular_recarga(monto=9999, premium=False)
    assert resultado["aceptada"] is True
    assert resultado["bonificacion_pct"] == 0

# ── Clase 2: [10000, 29999] — 10% bonificación ──

def test_limite_inferior_clase2():
    resultado = calcular_recarga(monto=10000, premium=False)
    assert resultado["aceptada"] is True
    assert resultado["bonificacion_pct"] == 10

def test_monto_medio_clase2():
    resultado = calcular_recarga(monto=20000, premium=False)
    assert resultado["aceptada"] is True
    assert resultado["bonificacion_pct"] == 10

def test_limite_superior_clase2():
    resultado = calcular_recarga(monto=29999, premium=False)
    assert resultado["aceptada"] is True
    assert resultado["bonificacion_pct"] == 10

# ── Clase 3: [30000, 50000] — 25% bonificación ──

def test_limite_inferior_clase3():
    resultado = calcular_recarga(monto=30000, premium=False)
    assert resultado["aceptada"] is True
    assert resultado["bonificacion_pct"] == 25

def test_monto_medio_clase3():
    resultado = calcular_recarga(monto=40000, premium=False)
    assert resultado["aceptada"] is True
    assert resultado["bonificacion_pct"] == 25

def test_monto_maximo_aceptado():
    resultado = calcular_recarga(monto=50000, premium=False)
    assert resultado["aceptada"] is True
    assert resultado["bonificacion_pct"] == 25

# ── Premium: +5% adicional ──

def test_premium_clase1_sin_bonificacion_extra():
    resultado = calcular_recarga(monto=5000, premium=True)
    assert resultado["aceptada"] is True
    assert resultado["bonificacion_pct"] == 5

def test_premium_clase2_bonificacion():
    resultado = calcular_recarga(monto=10000, premium=True)
    assert resultado["aceptada"] is True
    assert resultado["bonificacion_pct"] == 15

def test_premium_clase3_bonificacion():
    resultado = calcular_recarga(monto=30000, premium=True)
    assert resultado["aceptada"] is True
    assert resultado["bonificacion_pct"] == 30

# ── Cálculo de datos de bonificación ──

def test_datos_bonificacion_calculados_correctamente():
    resultado = calcular_recarga(monto=10000, premium=False)
    assert resultado["datos_bonus_mb"] == 1000  # 10% de 10000

def test_datos_bonificacion_premium():
    resultado = calcular_recarga(monto=10000, premium=True)
    assert resultado["datos_bonus_mb"] == 1500  # 15% de 10000