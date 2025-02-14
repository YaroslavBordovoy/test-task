import json

import aiohttp
import asyncio

from api_fetcher.database.models.posts import PostModel
from api_fetcher.exceptions import (
    APITimeoutError,
    APIConnectionError,
    APIResponseError,
    APIDataError,
)
from api_fetcher.schemas import PostSchema
from pydantic import ValidationError
from api_fetcher.storages import write_to_db, write_to_csv
from sqlalchemy.exc import SQLAlchemyError


JSONPLACEHOLDER_URL = "https://jsonplaceholder.typicode.com/posts"


def validate_json(data: list[dict]) -> list[PostSchema]:
    validated_posts = []

    for post in data:
        try:
            validated_posts.append(PostSchema.model_validate(post))

        except ValidationError:
            raise ValidationError("An error occurred while validating json.")

    return validated_posts


def create_post_instances(data: list[dict]) -> list[PostModel]:
    validated_posts = validate_json(data)

    if not validated_posts:
        return []

    posts = [
        PostModel(
            user_id=schema.user_id,
            title=schema.title,
            body=schema.body
        )
        for schema in validated_posts
    ]

    return posts


async def get_posts(session: aiohttp.ClientSession) -> list[dict]:
    try:
        async with session.get(JSONPLACEHOLDER_URL) as response:
            if response.status == 200:
                try:
                    json_response = await response.json()

                    return json_response
                except json.JSONDecodeError:
                    raise APIDataError()

            raise APIResponseError(status_code=response.status)
    except aiohttp.ClientConnectionError:
        raise APIConnectionError()
    except asyncio.TimeoutError:
        raise APITimeoutError()


async def main():
    async with aiohttp.ClientSession() as session:
        posts = await get_posts(session)
        data_to_write = create_post_instances(posts)

        if data_to_write:
            try:
                write_to_db(data_to_write)
                write_to_csv(data_to_write)
            except SQLAlchemyError as error:
                raise SQLAlchemyError(f"Error while working with database: {error}")


if __name__ == "__main__":
    asyncio.run(main())
