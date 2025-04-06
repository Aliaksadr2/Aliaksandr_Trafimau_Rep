import requests
import allure
from .base_endpoint import BaseEndpoint
from .endpoint import Config


class GetMeme(BaseEndpoint):
    url = Config.url

    @allure.step("Get meme by ID")
    def get_meme(self, meme_id):
        self.response = requests.get(
            f"{self.url}/{meme_id}",
            headers=Config.headers
        )
        return self.response

    @allure.step("Check response content")
    def check_response_content(self, expected_data):
        response_json = self.response.json()
        for key, value in expected_data.items():
            assert response_json.get(key) == value, (
                f"Expected '{key}' to be '{value}', but got '{response_json.get(key)}'"
            )
