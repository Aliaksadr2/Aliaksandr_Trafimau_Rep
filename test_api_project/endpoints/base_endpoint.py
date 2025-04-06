import allure


class BaseEndpoint:
    response = None

    @allure.step("Check response status code")
    def check_status_code(self, expected_code):
        assert self.response.status_code == expected_code, (
            f"Expected status code {expected_code}, but got {self.response.status_code}: {self.response.text}"
        )
