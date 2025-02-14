from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from api_fetcher.database.models.base import Base


class PostModel(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String(127), nullable=False)
    body: Mapped[str] = mapped_column(String(511), nullable=False)

    def __repr__(self):
        return f"<PostModel(id={self.id}, user_id={self.user_id}, title={self.title}, body={self.body[:50]})>"

    @classmethod
    def default_order_by(cls):
        return cls.id.asc()
