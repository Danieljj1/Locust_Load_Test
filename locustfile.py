from locust import HttpUser, task, between 

class User(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def posts(self):
        self.client.get("/posts")

    @task(1)
    def post(self):
        self.client.get("/posts/1")