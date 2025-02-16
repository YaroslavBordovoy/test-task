import asyncio
import json

import aiohttp
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from api_fetcher.database.models.posts import PostModel
from api_fetcher.exceptions import (
    APITimeoutError,
    APIConnectionError,
    APIResponseError,
    APIDataError,
)
from api_fetcher.schemas import PostSchema
from api_fetcher.storages import write_to_db, write_to_csv
from api_fetcher.logging import logger


JSONPLACEHOLDER_URL = "https://jsonplaceholder.typicode.com/posts"


def validate_json(data: list[dict]) -> list[PostSchema]:
    """
    Validates a list of post data dictionaries using the PostSchema.

    Args:
        data (list[dict]): A list of dictionaries representing raw post data.

    Returns:
        list[PostSchema]: A list of validated PostSchema instances.

    Raises:
        pydantic.ValidationError:
            If any of the input dictionaries fail schema validation.
    """
    validated_posts = []

    for post in data:
        try:
            validated_posts.append(PostSchema.model_validate(post))

        except ValidationError as error:
            raise error
    return validated_posts


def create_post_instances(data: list[dict]) -> list[PostModel]:
    """
    Creates a list of PostModel instances from validated JSON data.

    Args:
        data (list[dict]): A list of dictionaries containing raw post data.

    Returns:
        list[PostModel]:
            A list of PostModel instances if validation is successful.
            Returns an empty list if no valid posts are found.

    Raises:
        ValidationError: If the input data does not meet validation requirements.
    """
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
    """
    Asynchronous function for sending requests to API and receiving the necessary data.

    Args:
        session (aiohttp.ClientSession): An active aiohttp session used to send HTTP requests.

    Returns:
        list[dict]:
            A list of dictionaries, where each dictionary represents a post retrieved from the API.
            Each post typically contains keys such as 'id, 'userId', 'title', and 'body'.

    Raises:
        APITimeoutError: If the request times out.
        APIConnectionError: If there is a connection error.
        APIResponseError: If the API returns a non-200 status code.
        APIDataError: If the API response contains invalid JSON.

    """
    logger.info(f"Sending API request: {JSONPLACEHOLDER_URL}.")
    try:
        async with session.get(JSONPLACEHOLDER_URL) as response:
            if response.status == 200:
                try:
                    json_response = await response.json()
                    logger.info(f"Successful API response: {len(json_response)} records received.")

                    return json_response
                except json.JSONDecodeError:
                    logger.error("Error processing json response.", exc_info=True)
                    raise APIDataError()

            logger.warning(f"API returned error {response.status}")
            raise APIResponseError(status_code=response.status)
    except aiohttp.ClientConnectionError:
        logger.error("Error connecting to API.", exc_info=True)
        raise APIConnectionError()
    except asyncio.TimeoutError:
        logger.error("Response timeout exceeded.", exc_info=True)
        raise APITimeoutError()


async def main() -> None:
    """
    The main asynchronous function to fetch posts, process them,
    and save them to the database and CSV.

    Returns:
        None

    Raises:
        SQLAlchemyError: If an error occurred while writing to the database.
    """
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
