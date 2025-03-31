import requests
import allure

from .endpoint import Config

class CreateMeme:
    url = Config.url
    response = None
    json = None

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

    @allure.step('Check_response')
    def check_response(self):
        assert self.response.status_code == 200

    @allure.step('Check_response_400')
    def check_response_400(self):
        assert self.response.status_code == 400, \
            f"Expected status code 400, but got {self.response.status_code}"

    @allure.step('Check response field: id')
    def check_id_field(self):
        assert "id" in self.json, "Missing 'id' key in JSON response"
        assert isinstance(self.json["id"], int), "'id' should be an integer"

    @allure.step('Check response field: updated_by')
    def check_updated_by_field(self):
        assert "updated_by" in self.json, "Missing 'updated_by' key in JSON response"
        assert isinstance(self.json["updated_by"], str), "'updated_by' should be a string"

    @allure.step('Check_response_404')
    def check_response_404(self):
        assert self.response.status_code == 404, \
            f"Expected status code 404, but got {self.response.status_code}: {self.response.text}"
