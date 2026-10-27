from datetime import date, timedelta

import pytest

import main
import storage
from board import TaskBoard


@pytest.fixture(autouse=True)
def isolated_storage(monkeypatch, tmp_path):
    path = tmp_path / "tasks.json"
    monkeypatch.setattr(main, "save_board",
                        lambda board: storage.save_board(board, path))


def fake_input(answers):
    answers = iter(answers)
    return lambda prompt="": next(answers)


def test_create_task_with_past_date_is_rejected(monkeypatch):
    monkeypatch.setattr(main, "board", TaskBoard())
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    monkeypatch.setattr("builtins.input", fake_input(["Отчёт", yesterday]))

    main.create_task()

    assert main.board.tasks == []