import time
from locust import HttpUser, task, between


class TickLoadTest(HttpUser):
    wait_time = between(1, 3)  # Simulate user wait time

    @task
    def post_tick(self):
        self.client.post(
            "/v1/ticks/",
            json={
                "instrument": "AAPL",
                "price": 150.0,
                "timestamp": int(time.time() * 1000.0),
            },
        )
