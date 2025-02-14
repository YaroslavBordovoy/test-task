import csv
from pathlib import Path

from sqlalchemy.exc import SQLAlchemyError

from api_fetcher.database.models.posts import PostModel
from api_fetcher.database.settings import get_db


PATH_TO_CSV_FILE = Path("posts.csv")
HEADERS = [column.name for column in PostModel.__table__.columns]


def write_to_db(data: list[PostModel]) -> None:
    with get_db() as db:
        try:
            db.add_all(data)
            db.commit()
        except SQLAlchemyError as error:
            db.rollback()
            raise error


def write_to_csv(data: list[PostModel]) -> None:
    csv_file = PATH_TO_CSV_FILE.exists()

    with open(PATH_TO_CSV_FILE, "a", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)

        if not csv_file:
            writer.writerow(HEADERS)


        for post in data:
            writer.writerow([post.id, post.user_id, post.title, post.body])
