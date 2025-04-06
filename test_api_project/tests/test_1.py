import pytest
import copy
from test_data import TEST_DATA, INVALID_ID, INVALID_FIELDS


@pytest.mark.parametrize('data', [TEST_DATA[0], TEST_DATA[1]])
def test_create_meme_valid_data(create_and_delete_meme, data):
    next(create_and_delete_meme(data))


@pytest.mark.parametrize('field, invalid_value', INVALID_FIELDS)
def test_create_meme_invalid_data(create_meme_endpoint, field, invalid_value):
    valid_data = copy.deepcopy(TEST_DATA[0])
    valid_data[field] = invalid_value
    create_meme_instance = create_meme_endpoint()
    create_meme_instance.new_meme(valid_data)
    create_meme_instance.check_response_400()


@pytest.mark.parametrize('data', [TEST_DATA[0]])
def test_create_meme_invalid_url(create_meme_endpoint, data):
    create_meme_instance = create_meme_endpoint()
    create_meme_instance.url = "http://167.172.172.115:52355/1"
    create_meme_instance.new_meme(data)
    create_meme_instance.check_response_404()


@pytest.mark.parametrize('data', [TEST_DATA[0]])
def test_update_meme_valid_data(create_and_delete_meme, update_meme_endpoint, data):
    meme_id = next(create_and_delete_meme(data))
    update_data = {
        "id": meme_id,
        "text": "Simple meme text_update",
        "url": "http://example_update.com/meme.jpg",
        "tags": ["simple", "example_2"],
        "info": {"author": "SimpleUser_2", "date": "2023-10-04"}
    }
    update_meme_instance = update_meme_endpoint()
    update_meme_instance.update_meme(meme_id, update_data)
    update_meme_instance.check_response_200()
    update_meme_instance.check_fields_updated_correctly(update_data)


@pytest.mark.parametrize('field, invalid_value', INVALID_FIELDS)
def test_update_meme_invalid_data(create_and_delete_meme, update_meme_endpoint, field, invalid_value):
    meme_id = next(create_and_delete_meme(TEST_DATA[0]))

    update_data = {
        "id": meme_id,
        "text": "Simple meme text_update",
        "url": "http://example_update.com/meme.jpg",
        "tags": ["simple", "example_2"],
        "info": {"author": "SimpleUser_2", "date": "2023-10-04"}
    }
    update_data[field] = invalid_value
    update_meme_instance = update_meme_endpoint()
    update_meme_instance.update_meme(meme_id, update_data)
    update_meme_instance.check_update_invalid_values(meme_id, update_data)


def test_delete_meme(create_and_delete_meme, delete_meme_endpoint):
    meme_id = next(create_and_delete_meme(TEST_DATA[0]))
    delete_meme_instance = delete_meme_endpoint()
    delete_meme_instance.delete_meme(meme_id)
    delete_meme_instance.check_status_code(200)
    delete_meme_instance.check_cannot_delete_twice(meme_id)
    delete_meme_instance.check_meme_absence(meme_id)


@pytest.mark.parametrize("invalid_id", INVALID_ID)
def test_delete_nonexistent_meme(delete_meme_endpoint, invalid_id):
    delete_meme_instance = delete_meme_endpoint()
    delete_meme_instance.delete_meme(invalid_id)
    delete_meme_instance.check_nonexistent_id(invalid_id)


@pytest.mark.parametrize("data", [TEST_DATA[0], TEST_DATA[1]])
def test_get_meme(create_and_delete_meme, get_meme_endpoint, data):
    meme_id = next(create_and_delete_meme(data))

    get_meme_instance = get_meme_endpoint()
    get_meme_instance.get_meme(meme_id)
    get_meme_instance.check_status_code(200)
    get_meme_instance.check_response_content(data)
