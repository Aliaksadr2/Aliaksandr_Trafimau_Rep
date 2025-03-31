import pytest
import copy


TEST_DATA = [{
    "text": "Simple meme text",
    "url": "http://example.com/meme.jpg",
    "tags": ["simple", "example"],
    "info": {"author": "SimpleUser", "date": "2023-10-01"}
},
    {
        "text": "Simple meme text@2",
        "url": "http://example.com/meme.jpg",
        "tags": [
            "object_1",
            "object_2",
            "object_@#$",
            " ",
            None,
            False
        ],
        "info": {
            "name": [
                "name_1",
                "name_@#$",
                " ",
                None
            ],
            "description": [
                "description_1",
                "Description_@#$",
                "",
                False
            ]
        }

    }
    ]
INVALID_FIELDS = [
    ("text", []),
    ("text", None),
    ("url", ["test"]),
    ("url", None),
    ("url", ["test", ["test2"]]),
    ("tags", None),
    ("tags", ""),
    ("tags", 12345),
    ("tags", 'test'),
    ("tags", {"test1": 123, "test2": "value"}),
    ("info", ""),
    ("info", None),
    ("info", 12345)
]
INVALID_ID = [
    "text_123",
    "",
    "!@#$",
    "1234567854355676889578653435336878",
    None
]

@pytest.mark.parametrize('data', [TEST_DATA[0], TEST_DATA[1]])
def test_create_meme_valid_data(create_meme_endpoint, data, delete_meme_endpoint):
    create_meme_instance = create_meme_endpoint()
    response = create_meme_instance.new_meme(data)
    create_meme_instance.check_response()
    create_meme_instance.check_id_field()
    create_meme_instance.check_updated_by_field()
    meme_id = response.json().get("id")

    delete_meme_instance = delete_meme_endpoint()
    delete_meme_instance.delete_meme(meme_id)
    delete_meme_instance.check_response()


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
def test_update_meme_valid_data(create_meme_endpoint, update_meme_endpoint, delete_meme_endpoint, data):
    create_meme_instance = create_meme_endpoint()
    response_create = create_meme_instance.new_meme(data)
    meme_id = response_create.json().get("id")
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
    update_meme_instance.check_updated_by_field()

    delete_meme_instance = delete_meme_endpoint()
    delete_meme_instance.delete_meme(meme_id)
    delete_meme_instance.check_response()


@pytest.mark.parametrize('field, invalid_value', INVALID_FIELDS)
def test_update_meme_invalid_data(create_meme_endpoint, update_meme_endpoint, delete_meme_endpoint, field, invalid_value):
    create_meme_instance = create_meme_endpoint()
    response_create = create_meme_instance.new_meme(TEST_DATA[0])
    meme_id = response_create.json().get("id")

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

    delete_meme_instance = delete_meme_endpoint()
    delete_meme_instance.delete_meme(meme_id)
    delete_meme_instance.check_response()

def test_delete_meme(create_meme_endpoint, delete_meme_endpoint):
    create_meme_instance = create_meme_endpoint()
    response_create = create_meme_instance.new_meme(TEST_DATA[0])
    meme_id = response_create.json().get("id")

    delete_meme_instance = delete_meme_endpoint()
    delete_meme_instance.delete_meme(meme_id)
    delete_meme_instance.check_response()
    delete_meme_instance.check_cannot_delete_twice(meme_id)
    delete_meme_instance.check_meme_absence(meme_id)


@pytest.mark.parametrize("invalid_id", INVALID_ID)
def test_delete_nonexistent_meme(delete_meme_endpoint, invalid_id):
    delete_meme_instance = delete_meme_endpoint()
    delete_meme_instance.delete_meme(invalid_id)
    delete_meme_instance.check_nonexistent_id(invalid_id)


@pytest.mark.parametrize("data", [TEST_DATA[0], TEST_DATA[1]])
def test_get_meme(create_meme_endpoint, get_meme_endpoint, delete_meme_endpoint, data):
    create_meme_instance = create_meme_endpoint()
    response_create = create_meme_instance.new_meme(data)
    meme_id = response_create.json().get("id")

    get_meme_instance = get_meme_endpoint()
    get_meme_instance.get_meme(meme_id)
    get_meme_instance.check_response()
    get_meme_instance.check_response_content(data)

    delete_meme_instance = delete_meme_endpoint()
    delete_meme_instance.delete_meme(meme_id)
    delete_meme_instance.check_response()
