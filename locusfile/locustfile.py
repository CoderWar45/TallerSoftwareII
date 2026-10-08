import time
import random
from locust import HttpUser, task, between

class LaravelLoadTestUser(HttpUser):
    # Simula un tiempo de espera aleatorio entre 1 y 5 segundos por usuario
    wait_time = between(1, 5)

    @task
    def test_bulk_store(self):
        # El JSON exacto con la estructura 'users' que creamos antes
        payload = {
            "users": [
                {
                    "name": "Usuario Prueba 1",
                    "email": "test1@loadtest.local",
                    "birth_date": "1990-01-01",
                    "password": "password"
                }
            ]
        }
        
        # Enviamos la petición POST al endpoint de Laravel
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        self.client.post("/api/users/bulk", json=payload, headers=headers)

    @task
    def Get_User(self):
        user_id = 1 
        self.client.get(f"/api/users/{user_id}")

    @task
    def Get_User_Emails(self):
        user_id = 1
        self.client.get(f"/api/users/{user_id}/emails")

    @task
    def test_get_over_twenty(self):
        headers = {"Accept": "application/json"}
        # Realiza la petición GET al nuevo endpoint
        with self.client.get("/api/users/over-twenty", headers=headers, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Falló con código: {response.status_code}")


    def test_post_bulk_users(self):
        unique_id = int(time.time() * 1000) + random.randint(1, 9999)
                payload = {
            "users": [
                {
                    "name": "Usuario Test A",
                    "email": f"user_a_{unique_id}@loadtest.local",
                    "birth_date": "1994-05-12",
                    "password": "password"
                },
                {
                    "name": "Usuario Test B",
                    "email": f"user_b_{unique_id}@loadtest.local",
                    "birth_date": "2010-11-23",
                    "password": "password"
                },
                {
                    "name": "Usuario Test C",
                    "email": f"user_c_{unique_id}@loadtest.local",
                    "birth_date": "2001-08-30",
                    "password": "password"
                }
            ]
        }

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        # Enviamos el POST esperando recibir el estado 201
        with self.client.post("/api/users/bulk", json=payload, headers=headers, catch_response=True) as response:
            if response.status_code == 201:
                response.success()
            else:
                response.failure(f"Error en BulkStore. Código recibido: {response.status_code}. Respuesta: {response.text}")


