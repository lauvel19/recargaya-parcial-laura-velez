RecargaYa S.A.S. — Módulo de Recargas de Celular

Reglas de negocio

Monto válido: entre $1.000 y $50.000 COP. Fuera de ese rango, la recarga es rechazada.

Bonificación de datos según monto:
- $1.000 a $9.999 — 0% de bonificación
- $10.000 a $29.999 — 10% de bonificación
- $30.000 a $50.000 — 25% de bonificación

Bonificación adicional por plan premium:
- El usuario premium recibe un 5% extra sobre cualquier bonificación base.

Ejemplos de cálculo:
- $5.000, estándar — 0%, sin datos bonus
- $10.000, estándar — 10%, 1.000 MB bonus
- $10.000, premium — 15%, 1.500 MB bonus
- $30.000, estándar — 25%, 7.500 MB bonus
- $30.000, premium — 30%, 9.000 MB bonus

---

Casos de prueba

Diseñados aplicando partición de equivalencia y análisis de valores límite sobre el campo `monto`.

Clases de equivalencia:
- CE1 — monto menor a $1.000 — inválida
- CE2 — $1.000 a $9.999 — válida, sin bonificación
- CE3 — $10.000 a $29.999 — válida, 10% bonificación
- CE4 — $30.000 a $50.000 — válida, 25% bonificación
- CE5 — monto mayor a $50.000 — inválida

Casos de prueba:
- TC-01 — valor límite inferior - 1 — $999, sin premium — CE1
- TC-02 — valor límite inferior exacto — $1.000, sin premium —  CE2
- TC-03 — partición equivalencia CE2 — $5.000, sin premium —  CE2
- TC-04 — valor límite superior CE2 — $9.999, sin premium — CE2
- TC-05 — valor límite inferior CE3 — $10.000, sin premium — CE3
- TC-06 — partición equivalencia CE3 — $20.000, sin premium —  CE3
- TC-07 — valor límite superior CE3 — $29.999, sin premium —  CE3
- TC-08 — valor límite inferior CE4 — $30.000, sin premium —  CE4
- TC-09 — partición equivalencia CE4 — $40.000, sin premium —  CE4
- TC-10 — valor límite superior exacto — $50.000, sin premium —  CE4
- TC-11 — valor límite superior + 1 — $50.001, sin premium —  CE5
- TC-12 — cero, borde extremo — $0, sin premium — CE1
- TC-13 — negativo — -$500, sin premium — CE1
- TC-14 — premium en límite CE3 — $10.000, con premium — CE3
- TC-15 — premium en límite CE4 — $30.000, con premium — CE4


Dependencias

```
fastapi==0.115.0
uvicorn==0.30.6
pytest==8.3.3
pytest-bdd==7.3.0
pytest-cov
httpx==0.27.2
locust==2.31.5
```

---

Autora

Laura Vélez — Ingeniería de Software, 5 semestre
Corporación Universitaria Alexander von Humboldt, Armenia, Quindío, Colombia
GitHub: https://github.com/lauvel19

---

