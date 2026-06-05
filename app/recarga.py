
MONTO_MINIMO = 1_000
MONTO_MAXIMO = 50_000

UMBRAL_BONIF_MEDIA = 10_000   
UMBRAL_BONIF_ALTA  = 30_000   

BONIF_MEDIA_PCT  = 10
BONIF_ALTA_PCT   = 25
BONIF_PREMIUM_PCT = 5


def calcular_recarga(monto: int | float, premium: bool = False) -> dict:
    # Validación de rango
    if monto < MONTO_MINIMO or monto > MONTO_MAXIMO:
        return {
            "aceptada": False,
            "mensaje": f"Monto rechazado. Debe estar entre "
                       f"${MONTO_MINIMO:,} y ${MONTO_MAXIMO:,}.",
            "monto": monto,
            "bonificacion_pct": 0,
            "datos_bonus_mb": 0,
        }

    # Bonificación base según monto
    if monto >= UMBRAL_BONIF_ALTA:
        bonif_base = BONIF_ALTA_PCT
    elif monto >= UMBRAL_BONIF_MEDIA:
        bonif_base = BONIF_MEDIA_PCT
    else:
        bonif_base = 0

    # Bonificación adicional premium
    bonif_extra = BONIF_PREMIUM_PCT if premium else 0
    bonif_total = bonif_base + bonif_extra

    datos_bonus = monto * bonif_total / 100

    return {
        "aceptada": True,
        "mensaje": "Recarga procesada exitosamente.",
        "monto": monto,
        "bonificacion_pct": bonif_total,
        "datos_bonus_mb": datos_bonus,
    }