import enum
from datetime import datetime

from sqlalchemy import Integer, String, Date, Enum
from sqlalchemy.orm import Mapped, mapped_column

from task_manager.database.models.base import Base


class TaskStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class TaskManagerModel(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(127), nullable=False)
    description: Mapped[str] = mapped_column(String(511), nullable=False)
    due_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    status: Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus),
        nullable=False,
        default=TaskStatus.PENDING
    )

    def __repr__(self):
        return f"<TaskManager(id={self.id}, title={self.title}, due_date={self.due_date}, status={self.status})>"

    @classmethod
    def default_order_by(cls):
        return cls.due_date.asc()
