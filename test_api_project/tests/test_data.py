# test_data.py

TEST_DATA = [
    {
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
