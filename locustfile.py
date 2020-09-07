from locust import HttpUser, between, task
import logging
from datetime import datetime
import json

class WebsiteUser(HttpUser):
    wait_time = between(5, 15)

    def on_start(self):
        # Should be some test pre conditions
        pass

    @task
    def get_all_tours(self):
        login_payload = {
            "username": "user",
            "password": "pass"
        }
        headers = { "Content-Type": "application/json" }

        #response_login = self.client.post("api/Authentication/request", login_payload, headers)
        response_login = self.client.post("api/Authentication/request", json = login_payload)

        assert response_login.status_code is 200
        assert response_login.ok is True
        assert len(response_login.text) > 1, "Expected response length is less that 1"
        logging.info("token " + response_login.text)
        token = "Bearer " + response_login.text
        auth_payload = { "Authorization": token }

        self.client.get("api/tours/getAll", headers = auth_payload)
