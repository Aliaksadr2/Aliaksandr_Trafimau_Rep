import requests
import allure
from .base_endpoint import BaseEndpoint
from .endpoint import Config


class CreateMeme(BaseEndpoint):
    url = Config.url

    @allure.step('Create new meme')
    def new_meme(self, payload):
        self.response = requests.post(
            self.url,
            json=payload,
            headers=Config.headers
        )
        self.json = None
        if self.response.ok:
            self.json = self.response.json()
        return self.response

    @allure.step('Check response: status 200')
    def check_response_200(self):
        self.check_status_code(200)

    @allure.step('Check response: status 400')
    def check_response_400(self):
        self.check_status_code(400)

    @allure.step('Check response: status 404')
    def check_response_404(self):
        self.check_status_code(404)

    @allure.step('Check response field: id')
    def check_id_field(self):
        assert "id" in self.json, "Missing 'id' key in JSON response"
        assert isinstance(self.json["id"], int), "'id' should be an integer"

    @allure.step('Check response field: updated_by')
    def check_updated_by_field_is_str(self):
        assert "updated_by" in self.json, "Missing 'updated_by' key in JSON response"
        assert isinstance(self.json["updated_by"], str), "'updated_by' should be a string"
