import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "healthy"


def test_root():
    r = client.get("/")
    assert r.status_code == 200


def test_recarga_valida_sin_premium():
    r = client.post("/recargas/calcular", json={"monto": 10000, "premium": False})
    assert r.status_code == 200
    data = r.json()
    assert data["aceptada"] is True
    assert data["bonificacion_pct"] == 10
    assert data["datos_bonus_mb"] == 1000.0


def test_recarga_valida_con_premium():
    r = client.post("/recargas/calcular", json={"monto": 30000, "premium": True})
    assert r.status_code == 200
    data = r.json()
    assert data["aceptada"] is True
    assert data["bonificacion_pct"] == 30


def test_recarga_rechazada_monto_bajo():
    r = client.post("/recargas/calcular", json={"monto": 500, "premium": False})
    assert r.status_code == 200
    assert r.json()["aceptada"] is False


def test_recarga_rechazada_monto_alto():
    r = client.post("/recargas/calcular", json={"monto": 99999, "premium": False})
    assert r.status_code == 200
    assert r.json()["aceptada"] is False


def test_monto_negativo_validator():
    r = client.post("/recargas/calcular", json={"monto": -1000, "premium": False})
    assert r.status_code == 422


def test_reglas_endpoint():
    r = client.get("/recargas/reglas")
    assert r.status_code == 200
    data = r.json()
    assert data["monto_minimo"] == 1000
    assert data["monto_maximo"] == 50000