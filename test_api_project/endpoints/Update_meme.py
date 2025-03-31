import requests
import allure
from .endpoint import Config

class UpdateMeme:
    url = Config.url

    @allure.step("Update meme by ID")
    def update_meme(self, meme_id, payload):
        self.response = requests.put(
            f"{self.url}/{meme_id}",
            json=payload,
            headers=Config.headers
        )
        return self.response

    @allure.step("Check response 200 after update")
    def check_response_200(self):
        assert self.response.status_code == 200, f"Expected status 200, but got {self.response.status_code}"

    @allure.step("Check response contains 'updated_by'")
    def check_updated_by_field(self):
        response_json = self.response.json()
        assert "updated_by" in response_json, "Field 'updated_by' is missing in the response."
        assert isinstance(response_json["updated_by"], str), "'updated_by' should be a string."

    @allure.step("Check update with invalid values")
    def check_update_invalid_values(self, meme_id, invalid_data):
        response = self.update_meme(meme_id, invalid_data)
        assert response.status_code == 400, (
            f"Expected status 400 for invalid value in field, but got {response.status_code}. "
            f"Response: {response.text}"
        )