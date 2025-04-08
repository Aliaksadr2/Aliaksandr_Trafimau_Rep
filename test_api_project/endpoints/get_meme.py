import requests
import allure
from .base_endpoint import BaseEndpoint
from .endpoint_config import Config


class GetMeme(BaseEndpoint):

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

    @allure.step("Check if meme is deleted")
    def check_meme_absence(self, meme_id):
        response_check = requests.get(
            f"{self.url}/{meme_id}",
            headers=Config.headers
        )
        assert response_check.status_code == 404, (
            f"Expected status code 404 for deleted meme, but got {response_check.status_code}: {response_check.text}"
        )
