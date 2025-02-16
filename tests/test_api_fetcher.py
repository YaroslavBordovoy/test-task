from unittest.mock import AsyncMock

import aiohttp
import pytest
from pydantic import ValidationError
from pytest_mock import MockerFixture
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from api_fetcher.database.models.base import Base
from api_fetcher.database.models.posts import PostModel
from api_fetcher.fetch_data import (
    get_posts,
    validate_json,
    create_post_instances,
)
from api_fetcher.schemas import PostSchema
from api_fetcher.storages import write_to_db


TEST_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
test_connection = test_engine.connect()
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_connection)


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(test_engine)
    session = TestSessionLocal()

    yield session

    session.rollback()
    session.close()
    Base.metadata.drop_all(test_engine)


@pytest.mark.asyncio
async def test_get_posts(mocker: MockerFixture):
    mock_response = [
        {"id": 1, "userId": 1, "title": "first test title", "body": "first test body"},
        {"id": 2, "userId": 2, "title": "second test title", "body": "second test body"},
    ]

    mock_get = AsyncMock()
    mock_get.__aenter__.return_value.status = 200
    mock_get.__aenter__.return_value.json.return_value = mock_response

    mocker.patch("aiohttp.ClientSession.get", return_value=mock_get)

    async with aiohttp.ClientSession() as session:
        posts = await get_posts(session)

    assert len(posts) == 2
    assert posts[0]["id"] == 1
    assert posts[0]["userId"] == 1
    assert posts[0]["title"] == "first test title"
    assert posts[0]["body"] == "first test body"
    assert posts[1]["id"] == 2
    assert posts[1]["userId"] == 2
    assert posts[1]["title"] == "second test title"
    assert posts[1]["body"] == "second test body"


@pytest.mark.parametrize(
    "input_data, expected_result",
    [
        (
            [{"id": 1, "userId": 1, "title": "first test title", "body": "first test body"}],
            [PostSchema(userId=1, title="first test title", body="first test body")],
        ),
        (
            [{"id": 2, "userId": 2, "title": "second test title", "body": "second test body"}],
            [PostSchema(userId=2, title="second test title", body="second test body")],
        )
    ]
)
def test_validate_json_valid_data(input_data: list[dict], expected_result: list[PostSchema]):
    test_result = validate_json(input_data)

    assert test_result == expected_result


@pytest.mark.parametrize(
    "input_data, expected_result",
    [
        (
            [{"id": 1, "userId": 1, "title": "first test title"}],
            ValidationError,
        )
    ]
)
def test_validate_json_invalid_data(input_data: list[dict], expected_result: Exception):
    with pytest.raises(expected_result):
        validate_json(input_data)


@pytest.mark.parametrize(
    "input_data, expected_result",
    [
        (
            [
                {"id": 1, "userId": 1, "title": "first test title", "body": "first test body"},
                {"id": 2, "userId": 2, "title": "second test title", "body": "second test body"},
            ],
            [
                PostModel(user_id=1, title="first test title", body="first test body"),
                PostModel(user_id=2, title="second test title", body="second test body"),
            ],
        ),
        ([], []),
    ]
)
def test_create_post_instances(input_data: list[dict], expected_result: list[PostModel]):
    test_result = create_post_instances(input_data)

    assert len(test_result) == len(expected_result)


def test_write_to_db(mocker: MockerFixture, db_session: Session):
    mocker.patch("api_fetcher.storages.get_db", return_value=db_session)

    test_data = [
        PostModel(user_id=1, title="first test title", body="first test body"),
        PostModel(user_id=2, title="second test title", body="second test body"),
    ]

    write_to_db(test_data)

    stored_posts = db_session.query(PostModel).all()

    assert len(stored_posts) == 2
    assert stored_posts[0].title == "first test title"
    assert stored_posts[1].body == "second test body"
