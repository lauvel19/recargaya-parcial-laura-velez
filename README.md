RecargaYa S.A.S. — Módulo de Recargas de Celular

Módulo backend para calcular el valor final de recargas de celular, construido con TDD + BDD, expuesto como API REST con FastAPI, con pruebas de carga en Locust y pipeline de integración continua en GitHub Actions.

---

Tabla de contenido

- Reglas de negocio
- Casos de prueba
- Estructura del proyecto
- Instalación
- Comandos de ejecución
- API Reference
- Pipeline CI/CD
- Ciclos TDD — Historial de commits
- Escenarios BDD
- Dependencias

---

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
- TC-01 — valor límite inferior - 1 — $999, sin premium — rechazada, 0% — CE1
- TC-02 — valor límite inferior exacto — $1.000, sin premium — aceptada, 0% — CE2
- TC-03 — partición equivalencia CE2 — $5.000, sin premium — aceptada, 0% — CE2
- TC-04 — valor límite superior CE2 — $9.999, sin premium — aceptada, 0% — CE2
- TC-05 — valor límite inferior CE3 — $10.000, sin premium — aceptada, 10% — CE3
- TC-06 — partición equivalencia CE3 — $20.000, sin premium — aceptada, 10% — CE3
- TC-07 — valor límite superior CE3 — $29.999, sin premium — aceptada, 10% — CE3
- TC-08 — valor límite inferior CE4 — $30.000, sin premium — aceptada, 25% — CE4
- TC-09 — partición equivalencia CE4 — $40.000, sin premium — aceptada, 25% — CE4
- TC-10 — valor límite superior exacto — $50.000, sin premium — aceptada, 25% — CE4
- TC-11 — valor límite superior + 1 — $50.001, sin premium — rechazada, 0% — CE5
- TC-12 — cero, borde extremo — $0, sin premium — rechazada, 0% — CE1
- TC-13 — negativo — -$500, sin premium — rechazada, 0% — CE1
- TC-14 — premium en límite CE3 — $10.000, con premium — aceptada, 15% — CE3
- TC-15 — premium en límite CE4 — $30.000, con premium — aceptada, 30% — CE4

---

Instalación

Prerrequisitos:
- Python 3.12 o superior
- pip

Pasos:

```bash
# Clonar el repositorio
git clone https://github.com/TU_USUARIO/recargaya.git
cd recargaya

# Crear entorno virtual (recomendado)
python -m venv venv

# Activar en Windows CMD
venv\Scripts\activate

# Activar en macOS o Linux
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

---

Comandos de ejecución

1. Tests unitarios — TDD

Ejecuta los 20 casos de prueba del módulo de lógica de negocio.

```bash
pytest tests/test_recarga.py -v
```

Salida esperada:
```
tests/test_recarga.py::test_monto_menor_minimo_rechazado   PASSED
tests/test_recarga.py::test_monto_cero_rechazado           PASSED
...
20 passed in 0.12s
```

2. Tests de integración — API

Verifica los endpoints de FastAPI con TestClient.

```bash
pytest tests/test_api.py -v
```

3. Tests BDD — Gherkin

Ejecuta los 5 escenarios definidos en `features/recarga.feature`, incluyendo el Scenario Outline con 7 ejemplos.

```bash
pytest features/ -v
```

4. Cobertura total

Corre todos los tests y genera el reporte de cobertura. Falla si la cobertura cae por debajo del 90%.

```bash
pip install pytest-cov

pytest tests/ features/ \
  --cov=app \
  --cov-report=term-missing \
  --cov-fail-under=90 \
  -v
```

5. Servidor local

```bash
uvicorn app.main:app --reload
```

Documentación interactiva disponible en:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

6. Prueba de carga — Locust

Modo headless, verifica P95 menor a 300 ms con 30 usuarios simultáneos:

```bash
# Terminal 1: iniciar la API
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Terminal 2: ejecutar la prueba de carga
locust -f locust/locustfile.py \
  --headless \
  -u 30 \
  -r 5 \
  -t 60s \
  --host http://127.0.0.1:8000
```

Modo con interfaz web:

```bash
locust -f locust/locustfile.py --host http://127.0.0.1:8000
# Abrir http://localhost:8089 y configurar: Users=30, Spawn rate=5
```

Criterio de aceptación: P95 menor a 300 ms. El script termina con código de salida 1 si no se cumple.

---

API Reference

POST /recargas/calcular

Calcula el resultado de una recarga.

Request body:
```json
{
  "monto": 10000,
  "premium": false
}
```

Response 200 OK:
```json
{
  "aceptada": true,
  "mensaje": "Recarga procesada exitosamente.",
  "monto": 10000,
  "bonificacion_pct": 10,
  "datos_bonus_mb": 1000.0
}
```

Response cuando el monto es inválido:
```json
{
  "aceptada": false,
  "mensaje": "Monto rechazado. Debe estar entre $1,000 y $50,000.",
  "monto": 500,
  "bonificacion_pct": 0,
  "datos_bonus_mb": 0
}
```

GET /recargas/reglas

Retorna las reglas de negocio vigentes.

```json
{
  "monto_minimo": 1000,
  "monto_maximo": 50000,
  "bonificaciones": [
    { "desde": 10000, "hasta": 29999, "porcentaje": 10 },
    { "desde": 30000, "hasta": 50000, "porcentaje": 25 }
  ],
  "bonus_premium_pct": 5
}
```

GET /health

Health check del servicio.

```json
{ "status": "healthy" }
```

---

Pipeline CI/CD

El pipeline se activa en cada push a cualquier rama y en Pull Requests a main.

Jobs configurados:
- unit-tests — pytest con cobertura mayor o igual al 90%, sin dependencias previas
- bdd-tests — escenarios Gherkin con pytest-bdd, depende de unit-tests
- load-tests — Locust con 30 usuarios y P95 menor a 300 ms, depende de unit-tests

Para verificar el estado del pipeline ir a:
https://github.com/TU_USUARIO/recargaya/actions

---

Ciclos TDD — Historial de commits

El desarrollo siguió estrictamente los ciclos Red, Green y Refactor:

- `test(RED): agrega tests TDD para módulo de recargas - todos fallan`
  Fase RED. Se escriben los 20 tests antes de existir implementación. Todos fallan.

- `feat(GREEN): implementa lógica de cálculo de recargas - todos los tests pasan`
  Fase GREEN. Se escribe la implementación mínima necesaria para que todos los tests pasen.

- `refactor: extrae funciones auxiliares, agrega validación de tipo y constantes nombradas`
  Fase REFACTOR. Se mejora la estructura interna sin cambiar el comportamiento. Los tests siguen pasando.

- `test(BDD): agrega escenarios Gherkin con Scenario Outline para partición de equivalencia`
  Se agregan los 5 escenarios BDD en español, incluyendo el Scenario Outline con 7 filas de ejemplos.

- `feat: agrega API REST con FastAPI y tests de integración`
  Se expone el módulo de negocio como API REST y se agregan los tests de integración correspondientes.

- `ci: agrega pipeline GitHub Actions, README y script Locust`
  Se conecta todo en un pipeline con 3 jobs y se documenta el proyecto.

---

Escenarios BDD

Definidos en `features/recarga.feature` usando Gherkin en español.

- Escenario 1 — Recarga rechazada por monto inferior al mínimo (Scenario)
- Escenario 2 — Recarga rechazada por monto superior al máximo (Scenario)
- Escenario 3 — Recarga mínima aceptada sin bonificación (Scenario)
- Escenario 4 — Usuario premium recibe bonificación adicional en recarga alta (Scenario)
- Escenario 5 — Bonificación según rango de monto para usuario estándar, con 7 ejemplos (Scenario Outline)

---

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

RecargaYa S.A.S. — Proyecto academico de pruebas de software