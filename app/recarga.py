"""
Módulo de cálculo de recargas — RecargaYa S.A.S.
Versión refactorizada: constantes nombradas, validación de tipo,
función auxiliar de bonificación base desacoplada.
"""
from __future__ import annotations

MONTO_MINIMO      = 1_000
MONTO_MAXIMO      = 50_000
UMBRAL_BONIF_MEDIA = 10_000
UMBRAL_BONIF_ALTA  = 30_000
BONIF_MEDIA_PCT   = 10
BONIF_ALTA_PCT    = 25
BONIF_PREMIUM_PCT = 5


def _bonificacion_base(monto: float) -> int:
    """Retorna el porcentaje de bonificación base según el monto."""
    if monto >= UMBRAL_BONIF_ALTA:
        return BONIF_ALTA_PCT
    if monto >= UMBRAL_BONIF_MEDIA:
        return BONIF_MEDIA_PCT
    return 0


def _es_monto_valido(monto: float) -> bool:
    return MONTO_MINIMO <= monto <= MONTO_MAXIMO


def calcular_recarga(monto: int | float, premium: bool = False) -> dict:
    """
    Calcula el resultado de una recarga de celular.

    Reglas de negocio
    -----------------
    * Monto válido : $1.000 – $50.000 COP
    * ≥ $10.000    : +10 % datos de bonificación
    * ≥ $30.000    : +25 % datos de bonificación
    * Premium      : +5 % adicional sobre cualquier bonificación

    Returns
    -------
    dict(aceptada, mensaje, monto, bonificacion_pct, datos_bonus_mb)
    """
    try:
        monto = float(monto)
    except (TypeError, ValueError):
        return {
            "aceptada": False,
            "mensaje": "El monto debe ser un número.",
            "monto": monto,
            "bonificacion_pct": 0,
            "datos_bonus_mb": 0,
        }

    if not _es_monto_valido(monto):
        return {
            "aceptada": False,
            "mensaje": (
                f"Monto rechazado. Debe estar entre "
                f"${MONTO_MINIMO:,.0f} y ${MONTO_MAXIMO:,.0f}."
            ),
            "monto": monto,
            "bonificacion_pct": 0,
            "datos_bonus_mb": 0,
        }

    bonif_total = _bonificacion_base(monto) + (BONIF_PREMIUM_PCT if premium else 0)
    datos_bonus = monto * bonif_total / 100

    return {
        "aceptada": True,
        "mensaje": "Recarga procesada exitosamente.",
        "monto": monto,
        "bonificacion_pct": bonif_total,
        "datos_bonus_mb": datos_bonus,
    }