import requests
import allure
from .endpoint import Config

class GetMeme:
    url = Config.url

    @allure.step("Get meme by ID")
    def get_meme(self, meme_id):
        self.response = requests.get(
            f"{self.url}/{meme_id}",
            headers=Config.headers
        )
        return self.response

    @allure.step("Check response status code for GET")
    def check_response(self):
        assert self.response.status_code == 200, \
            f"Expected status code 200, but got {self.response.status_code}: {self.response.text}"

    @allure.step("Check content of the response")
    def check_response_content(self, expected_data):
        for key, value in expected_data.items():
            assert self.response.json().get(key) == value, \
                f"Expected '{key}' to be '{value}', but got '{self.response.json().get(key)}'"
