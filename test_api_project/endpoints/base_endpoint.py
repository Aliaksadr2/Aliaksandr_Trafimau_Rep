import allure
from .endpoint_config import Config


class BaseEndpoint:
    url = Config.url
    response = None

    @allure.step("Check response status 200")
    def check_response_200(self):
        self.check_status_code(200)

    @allure.step("Check response status 400")
    def check_response_400(self):
        self.check_status_code(400)

    @allure.step("Check response status 404")
    def check_response_404(self):
        self.check_status_code(404)

    @allure.step("Check response status code")
    def check_status_code(self, expected_code):
        assert self.response.status_code == expected_code, (
            f"Expected status code {expected_code}, but got {self.response.status_code}: {self.response.text}"
        )
