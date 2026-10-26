from datetime import date

import pytest

from models import Task


def test_new_task_has_todo_status():
    task = Task(1, "Купить молоко")

    assert task.status == "todo"


def test_title_is_stripped():
    task = Task(1, "  Купить молоко  ")

    assert task.title == "Купить молоко"


def test_empty_title_raises_error():
    with pytest.raises(ValueError):
        Task(1, "   ")


def task_invalid_status_raises_error():
    task = Task(1, "Купить молоко")

    with pytest.raises(ValueError):
        task.set_status("finished")


def test_task_is_overdue_after_due_date():
    task = Task(1, "Отчёт", due_date=date(2026, 1, 10))

    assert task.is_overdue(date(2026, 1, 11)) is True


def test_task_not_overdue_on_due_date():
    task = Task(1, "Отчёт", due_date=date(2026, 1, 10))

    assert task.is_overdue(date(2026, 1, 10)) is False


def test_done_task_is_never_overdue():
    task = Task(1, "Отчёт", due_date=date(2026, 1, 10), status="done")

    assert task.is_overdue(date(2030, 1, 1)) is False


def test_task_without_due_date_is_never_overdue():
    task = Task(1, "Отчёт")

    assert task.is_overdue(date(2030, 1, 1)) is False