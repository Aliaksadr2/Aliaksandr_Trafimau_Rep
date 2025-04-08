import requests
import allure


class TokenEndpoint:
    def __init__(self, base_url):
        self.base_url = base_url
        self.response = None
        self.json = None
        self.text = None

    @allure.step("Generate a new token")
    def generate_token(self, name):
        payload = {"name": name}
        headers = {"Content-Type": "application/json"}
        self.response = requests.post(
            f"{self.base_url}/authorize",
            json=payload,
            headers=headers
        )
        self._process_response()
        return self.response

    @allure.step("Verify a token's freshness")
    def verify_token(self, token):
        self.response = requests.get(f"{self.base_url}/authorize/{token}")
        self._process_response_text()
        return self.response

    def _process_response(self):
        if self.response.ok:
            try:
                self.json = self.response.json()
            except ValueError:
                self.json = None

    def _process_response_text(self):
        self.text = self.response.text if self.response.ok else None

    @allure.step("Check response status code")
    def check_status_code(self, expected_code):
        assert self.response.status_code == expected_code, (
            f"Expected status code {expected_code}, but got {self.response.status_code}: {self.response.text}"
        )

    @allure.step("Validate token generation response")
    def check_token_response(self):
        assert "token" in self.json, "Response missing 'token' key"
        assert isinstance(self.json["token"], str), "'token' should be a string"
        assert "user" in self.json, "Response missing 'user' key"
        assert isinstance(self.json["user"], str), "'user' should be a string"

    @allure.step("Validate token freshness response")
    def check_token_freshness_response(self, expected_username):
        assert self.response.status_code == 200, f"Expected status code 200, got {self.response.status_code}"
        assert f"Token is alive. Username is {expected_username}" in self.text, \
            f"Unexpected response text: {self.text}"

    @allure.step("Check token is expired")
    def check_token_expired(self):
        assert self.response.status_code == 404, f"Expected status 404, got {self.response.status_code}"
