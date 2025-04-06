import requests
import allure
from .base_endpoint import BaseEndpoint
from .endpoint import Config


class UpdateMeme(BaseEndpoint):
    url = Config.url

    @allure.step("Update meme by ID")
    def update_meme(self, meme_id, payload):
        self.response = requests.put(
            f"{self.url}/{meme_id}",
            json=payload,
            headers=Config.headers
        )
        return self.response

    @allure.step("Check response: status 200")
    def check_response_200(self):
        self.check_status_code(200)

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

    @allure.step("Verify that fields are updated correctly")
    def check_fields_updated_correctly(self, expected_data):
        response_json = self.response.json()

        assert response_json["text"] == expected_data["text"], (
            f"Expected 'text' to be {expected_data['text']}, but got {response_json['text']}"
        )
        assert response_json["url"] == expected_data["url"], (
            f"Expected 'url' to be {expected_data['url']}, but got {response_json['url']}"
        )
        assert response_json["tags"] == expected_data["tags"], (
            f"Expected 'tags' to be {expected_data['tags']}, but got {response_json['tags']}"
        )
        assert response_json["info"] == expected_data["info"], (
            f"Expected 'info' to be {expected_data['info']}, but got {response_json['info']}"
        )
