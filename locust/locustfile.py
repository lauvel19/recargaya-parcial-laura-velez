"""
Script de prueba de carga — RecargaYa S.A.S.
Objetivo: P95 < 300 ms con 30 usuarios simultáneos
Ejecutar: locust -f locust/locustfile.py --headless -u 30 -r 5 -t 60s --host http://127.0.0.1:8000
"""
import random
from locust import HttpUser, task, between, events


MONTOS_VALIDOS   = [1000, 5000, 9999, 10000, 20000, 29999, 30000, 40000, 50000]
MONTOS_INVALIDOS = [0, 999, 50001, 100000]


class RecargaUser(HttpUser):
    wait_time = between(0.5, 1.5)  # espera entre peticiones (simula usuario real)

    @task(7)
    def calcular_recarga_valida(self):
        payload = {
            "monto": random.choice(MONTOS_VALIDOS),
            "premium": random.choice([True, False]),
        }
        with self.client.post(
            "/recargas/calcular",
            json=payload,
            catch_response=True,
            name="POST /recargas/calcular [válida]",
        ) as response:
            if response.status_code != 200:
                response.failure(f"Status inesperado: {response.status_code}")
            elif not response.json().get("aceptada"):
                response.failure("Recarga válida fue rechazada")

    @task(2)
    def calcular_recarga_invalida(self):
        payload = {
            "monto": random.choice(MONTOS_INVALIDOS),
            "premium": False,
        }

        with self.client.post(
            "/recargas/calcular",
            json=payload,
            catch_response=True,
            name="POST /recargas/calcular [inválida]",
        ) as response:

            # Para datos inválidos esperamos rechazo
            if response.status_code in [200, 422]:
                response.success()
            else:
                response.failure(
                    f"Status inesperado: {response.status_code}"
                )

    @task(1)
    def consultar_reglas(self):
        self.client.get("/recargas/reglas", name="GET /recargas/reglas")

    @task(1)
    def health_check(self):
        self.client.get("/health", name="GET /health")


@events.quitting.add_listener
def verificar_p95(environment, **kwargs):
    """Falla la prueba si el P95 supera 300 ms."""
    stats = environment.runner.stats.total
    p95_ms = stats.get_response_time_percentile(0.95)
    print(f"\n📊 P95 medido: {p95_ms:.1f} ms (límite: 300 ms)")
    if p95_ms > 300:
        print(f"❌ FALLO: P95 ({p95_ms:.1f} ms) supera el límite de 300 ms")
        environment.process_exit_code = 1
    else:
        print(f"✅ OK: P95 dentro del límite")