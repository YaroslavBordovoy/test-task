from datetime import datetime
from unittest.mock import patch

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, Session

from task_manager.database.models.base import Base
from task_manager.database.models.task_manager import TaskManagerModel, TaskStatus
from task_manager.manager import main


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


def test_add_task(db_session: Session):
    test_args = [
        "task_manager.manager",
        "add",
        "test task",
        "test description",
        "15-02-2025",
    ]

    with patch("sys.argv", test_args), patch("task_manager.manager.get_db", return_value=iter([db_session])):
        main()

    task = db_session.scalar(select(TaskManagerModel).where(TaskManagerModel.title == "test task"))

    assert task is not None
    assert task.description == "test description"
    assert task.due_date == datetime.strptime("15-02-2025", "%d-%m-%Y").date()
    assert task.status == TaskStatus.PENDING

    test_args_2 = [
        "task_manager.manager",
        "add",
        "test task",
        "new test description",
        "15-02-2025",
    ]

    with patch("sys.argv", test_args_2), patch("task_manager.manager.get_db", return_value=iter([db_session])):
        with pytest.raises(ValueError):
            main()


@pytest.mark.parametrize(
    "test_args, expected_result",
    [
        (["task_manager.manager", "update", "completed", "--task-id", "1",], TaskStatus.COMPLETED),
        (["task_manager.manager", "update", "pending", "--title", "test task",], TaskStatus.PENDING),
    ],
)
def test_update_task(db_session: Session, test_args: list[str], expected_result: TaskStatus):
    new_task = [
        "task_manager.manager",
        "add",
        "test task",
        "test description",
        "15-05-2025",
    ]

    with patch("sys.argv", new_task), patch("task_manager.manager.get_db", return_value=iter([db_session])):
        main()

    task = db_session.scalar(select(TaskManagerModel).where(TaskManagerModel.title == "test task"))

    assert task is not None

    with patch("sys.argv", test_args), patch("task_manager.manager.get_db", return_value=iter([db_session])):
        main()

    updated_task = db_session.scalar(select(TaskManagerModel).where(TaskManagerModel.title == "test task"))

    assert updated_task is not None
    assert updated_task.status == expected_result


@pytest.mark.parametrize(
    "test_args, expected_result",
    [
        (["task_manager.manager", "update", "new status", "--task-id", "1"], ValueError),
        (["task_manager.manager", "update", "completed", "--title", "some title"], ValueError),
        (["task_manager.manager", "update", "completed"], ValueError),
    ],
)
def test_invalid_update_task(db_session: Session, test_args: list[str], expected_result: Exception):
    new_task = [
        "task_manager.manager",
        "add",
        "test task",
        "test description",
        "15-05-2025",
    ]

    with patch("sys.argv", new_task), patch("task_manager.manager.get_db", return_value=iter([db_session])):
        main()

    task = db_session.scalar(select(TaskManagerModel).where(TaskManagerModel.title == "test task"))

    assert task is not None

    with patch("sys.argv", test_args), patch("task_manager.manager.get_db", return_value=iter([db_session])):
        with pytest.raises(expected_result):
            main()


@pytest.mark.parametrize(
    "test_args",
    [
        ["task_manager.manager", "add", "title 1", "description 1", "20-05-2025"],
        ["task_manager.manager", "add", "title 2", "description 2", "20-05-2025"],
        ["task_manager.manager", "add", "title 3", "description 3", "20-05-2025"],
    ],
)
def test_task_list(db_session: Session, test_args: list[str]):
    with patch("sys.argv", test_args), patch("task_manager.manager.get_db", return_value=iter([db_session])):
        main()

    tasks = db_session.scalars(select(TaskManagerModel))

    assert tasks is not None
    assert len(list(tasks)) > 0

    task_list = [
        "task_manager.manager",
        "list",
    ]

    with patch("sys.argv", task_list), patch("task_manager.manager.get_db", return_value=iter([db_session])):
        main()


def test_delete_task(db_session: Session):
    new_task = [
        "task_manager.manager",
        "add",
        "test task",
        "test description",
        "15-05-2025",
    ]

    with patch("sys.argv", new_task), patch("task_manager.manager.get_db", return_value=iter([db_session])):
        main()

    task = db_session.scalar(select(TaskManagerModel).where(TaskManagerModel.title == "test task"))

    assert task is not None

    delete_task = [
        "task_manager.manager",
        "delete",
        "--title",
        "test task",
    ]

    with patch("sys.argv", delete_task), patch("task_manager.manager.get_db", return_value=iter([db_session])):
        main()

    task = db_session.scalar(select(TaskManagerModel).where(TaskManagerModel.title == "test task"))

    assert task is None
