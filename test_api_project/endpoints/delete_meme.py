import requests
import allure
from .base_endpoint import BaseEndpoint
from .endpoint_config import Config


class DeleteMeme(BaseEndpoint):

    @allure.step("Delete meme by ID")
    def delete_meme(self, meme_id):
        self.response = requests.delete(
            f"{self.url}/{meme_id}",
            headers=Config.headers
        )
        return self.response

    @allure.step("Check if meme cannot be deleted twice")
    def check_cannot_delete_twice(self, meme_id):
        response_repeat_delete = requests.delete(
            f"{self.url}/{meme_id}",
            headers=Config.headers
        )
        assert response_repeat_delete.status_code == 404, (
            f"Expected status code 404 for second delete, but got {response_repeat_delete.status_code}: {response_repeat_delete.text}"
        )

    @allure.step("Check attempt to delete a non-existent meme")
    def check_nonexistent_id(self, meme_id):
        response = requests.delete(
            f"{self.url}/{meme_id}",
            headers=Config.headers
        )
        assert response.status_code == 404, (
            f"Expected status code 404 for non-existent ID, but got {response.status_code}: {response.text}"
        )
        if response.text:
            assert "not found" in response.text.lower(), (
                f"Expected 'not found' in the response for non-existent ID, but got response text: {response.text}"
            )
