from datetime import datetime
from task_manager.logging import logger

from sqlalchemy import select
from sqlalchemy.orm import Session

from task_manager.cli import get_args
from task_manager.database.models.task_manager import TaskManagerModel, TaskStatus
from task_manager.database.settings import get_db


class TaskManager:
    """
    A class for managing tasks in the database.

    This class provides methods for adding, updating, retrieving, and deleting tasks.
    It interacts with the database via SQLAlchemy and logs all operations.

    Attributes:
        db (Session): The database session used for executing queries.

    Methods:
        add_task(title, description, due_date): Adds a new task to the database.
        update_task_status(status, task_id=None, title=None): Updates the status of a task.
        task_list(): Retrieves all tasks ordered by due date.
        delete_task(task_id=None, title=None): Deletes a task from the database.
    """

    def __init__(self):
        self.db = next(get_db())

    @staticmethod
    def check_for_argument_existence(db: Session, task_id: int = None, title: str = None) -> TaskManagerModel:
        if task_id:
            task = db.scalar(select(TaskManagerModel).where(TaskManagerModel.id == task_id))
        elif title:
            task = db.scalar(select(TaskManagerModel).where(TaskManagerModel.title == title))
        else:
            logger.error("Either id or title must be provided.")
            raise ValueError("Either id or title must be provided.")

        if not task:
            logger.warning("Task not found.")
            raise ValueError("Task not found.")

        return task

    def add_task(self, title: str, description: str, due_date: str) -> None:
        """
        Adds a new task to the database.

        Args:
            title (str): The title of the task.
            description (str): A brief description of the task.
            due_date (str): The due date in the format "DD-MM-YYYY".

        Raises:
            ValueError: If a task with the same title already exists.
        """
        title_exist = self.db.scalar(select(TaskManagerModel).where(TaskManagerModel.title == title))

        if title_exist:
            raise ValueError(f"A task named <{title}> already exists.")

        date = datetime.strptime(due_date, "%d-%m-%Y").date()

        new_task = TaskManagerModel(
            title=title,
            description=description,
            due_date=date,
            status=TaskStatus.PENDING,
        )

        self.db.add(new_task)
        self.db.commit()
        logger.info(
            f"New task added: ID={new_task.id}, title='{new_task.title}', "
            f"due={new_task.due_date}."
        )

    def update_task_status(self, status: str, task_id: int = None, title: str = None) -> None:
        """
        Update the task.

        Args:
            status (str): New status for the task.
            task_id (Optional[int]): The ID of the task.
            title (Optional[str]): The title of the task.
        """
        if status not in TaskStatus.__members__.values():
            logger.error(f"You cannot set the status <{status}>.")
            raise ValueError("Invalid status.")

        task_to_update = self.check_for_argument_existence(self.db, task_id, title)

        task_to_update.status = status

        self.db.commit()
        logger.info(
            f"The status of the task with the name <{task_to_update.title}> "
            f"has been updated: {task_to_update.status.value}."
        )

    def task_list(self) -> None:
        """
        Outputs a list of tasks to the terminal.

        Returns:
            None
        """
        logger.info(list(self.db.scalars(select(TaskManagerModel).order_by(TaskManagerModel.due_date))))

    def delete_task(self, task_id: int = None, title: str = None) -> None:
        """
        Delete the task.

        Args:
            task_id (Optional[int]): The ID of the task.
            title (Optional[str]): The title of the task.

        Returns:
            None
        """
        task_to_delete = self.check_for_argument_existence(self.db, task_id, title)

        self.db.delete(task_to_delete)
        self.db.commit()

        logger.info(f"Task with name <{task_to_delete.title}> deleted.")


def main() -> None:
    args = get_args()
    manager = TaskManager()

    if args.command == "add":
        manager.add_task(
            title=args.title,
            description=args.description,
            due_date=args.due_date,
        )

    elif args.command == "update":
        manager.update_task_status(
            status=args.status,
            task_id=args.task_id,
            title=args.title,
        )

    elif args.command == "list":
        manager.task_list()

    elif args.command == "delete":
        manager.delete_task(
            task_id=args.task_id,
            title=args.title,
        )


if __name__ == "__main__":
    main()
