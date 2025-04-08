import pytest
import requests

from endpoints.create_meme import CreateMeme
from endpoints.delete_meme import DeleteMeme
from endpoints.update_meme import UpdateMeme
from endpoints.get_meme import GetMeme
from endpoints.endpoint_config import Config
from endpoints.token_endpoint import TokenEndpoint


@pytest.fixture()
def token_endpoint():
    def _create_instance():
        return TokenEndpoint(base_url="http://167.172.172.115:52355")

    return _create_instance


@pytest.fixture()
def create_meme_endpoint():
    return CreateMeme


@pytest.fixture()
def delete_meme_endpoint():
    return DeleteMeme


@pytest.fixture()
def update_meme_endpoint():
    return UpdateMeme


@pytest.fixture()
def get_meme_endpoint():
    return GetMeme


@pytest.fixture(scope="session", autouse=True)
def ensure_token_once():
    response = requests.get(f"http://167.172.172.115:52355/authorize/{Config.headers['Authorization']}")
    if response.status_code == 401:
        auth_response = requests.post(
            f"http://167.172.172.115:52355/authorize",
            json={"username": "your_username", "password": "your_password"}
        )
        if auth_response.status_code == 200:
            Config.headers["Authorization"] = auth_response.json().get("token")
        else:
            raise Exception(f"Failed to update token: {auth_response.status_code}, {auth_response.text}")
    elif response.status_code != 200:
        raise Exception(f"Unexpected response while checking token: {response.status_code}, {response.text}")


@pytest.fixture
def create_and_delete_meme(create_meme_endpoint, delete_meme_endpoint):
    def _create(data):
        create_meme_instance = create_meme_endpoint()
        create_meme_instance.new_meme(payload=data)
        meme_id = create_meme_instance.response.json().get('id')

        yield meme_id

        delete_meme_instance = delete_meme_endpoint()
        delete_meme_instance.delete_meme(meme_id=meme_id)

    return _create
