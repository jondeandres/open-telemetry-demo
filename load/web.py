from locust import HttpUser, task, between


class WebUser(HttpUser):
    wait_time = between(0, 0.3)

    @task
    def home(self):
        self.client.get("/home")
        self.client.get("/home")

    @task
    def subscription(self):
        self.client.post('/subscription')
