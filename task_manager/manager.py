from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from task_manager.database.models.task_manager import TaskManagerModel, TaskStatus
from task_manager.database.settings import get_db


class TaskManager:

    def __init__(self):
        self.db = next(get_db())

    @staticmethod
    def check_for_argument_existence(db: Session, task_id: int = None, title: str = None) -> TaskManagerModel:
        if task_id:
            task = db.scalar(select(TaskManagerModel).where(TaskManagerModel.id == task_id))
        elif title:
            task = db.scalar(select(TaskManagerModel).where(TaskManagerModel.title == title))
        else:
            raise ValueError("Either id or title must be provided.")

        if not task:
            raise ValueError("Task not found.")

        return task

    def add_task(self, title: str, description: str, due_date: str) -> None:
        date = datetime.strptime(due_date, "%Y-%m-%d").date()

        new_task = TaskManagerModel(
            title=title,
            description=description,
            due_date=date,
        )

        self.db.add(new_task)
        self.db.commit()

    def update_task_status(self, status: str, task_id: int = None, title: str = None) -> None:
        if status not in TaskStatus.__members__:
            raise ValueError("Invalid status.")

        task_to_update = self.check_for_argument_existence(self.db, task_id, title)

        task_to_update.status = status

        self.db.commit()

    def task_list(self) -> list:
        return list(self.db.scalars(select(TaskManagerModel).order_by(TaskManagerModel.due_date)))

    def delete_task(self, task_id: int = None, title: str = None) -> None:
        task_to_delete = self.check_for_argument_existence(self.db, task_id, title)

        self.db.delete(task_to_delete)
        self.db.commit()
