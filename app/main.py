from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator
from app.recarga import calcular_recarga, MONTO_MINIMO, MONTO_MAXIMO

app = FastAPI(
    title="RecargaYa API",
    description="Módulo de cálculo de recargas de celular — RecargaYa S.A.S.",
    version="1.0.0",
)


class RecargaRequest(BaseModel):
    monto: float
    premium: bool = False

    @field_validator("monto")
    @classmethod
    def monto_debe_ser_positivo(cls, v):
        if v <= 0:
            raise ValueError("El monto debe ser un número positivo.")
        return v


class RecargaResponse(BaseModel):
    aceptada: bool
    mensaje: str
    monto: float
    bonificacion_pct: int
    datos_bonus_mb: float


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "service": "RecargaYa API v1.0.0"}


@app.get("/health", tags=["Health"])
def health():
    return {"status": "healthy"}


@app.post("/recargas/calcular", response_model=RecargaResponse, tags=["Recargas"])
def calcular(request: RecargaRequest):
    """
    Calcula el resultado de una recarga.

    - **monto**: valor en pesos colombianos (entre $1.000 y $50.000)
    - **premium**: indica si el usuario tiene plan premium
    """
    resultado = calcular_recarga(monto=request.monto, premium=request.premium)
    return RecargaResponse(**resultado)


@app.get("/recargas/reglas", tags=["Recargas"])
def reglas():
    """Retorna las reglas de negocio vigentes."""
    return {
        "monto_minimo": MONTO_MINIMO,
        "monto_maximo": MONTO_MAXIMO,
        "bonificaciones": [
            {"desde": 10_000, "hasta": 29_999, "porcentaje": 10},
            {"desde": 30_000, "hasta": 50_000, "porcentaje": 25},
        ],
        "bonus_premium_pct": 5,
    }