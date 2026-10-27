from datetime import date

import pytest

from board import TaskBoard
from storage import load_board, save_board


def test_save_and_load_roundtrip(tmp_path):
    path = tmp_path / "tasks.json"
    board = TaskBoard()
    board.create_task("Купить молоко", date(2030, 1, 1))
    second = board.create_task("Без срока", None)
    board.change_status(second.id, "done")
    board.delete_task(1)

    save_board(board, path)
    loaded = load_board(path)

    assert [t.to_dict() for t in loaded.tasks] == [t.to_dict() for t in board.tasks]
    assert loaded.create_task("Новая", None).id == 3


def test_load_missing_file_returns_empty_board(tmp_path):
    board = load_board(tmp_path / "missing.json")

    assert board.tasks == []
    assert board.next_id == 1


def test_load_broken_file_raises_error(tmp_path):
    path = tmp_path / "tasks.json"
    path.write_text("{ not json", encoding="utf-8")

    with pytest.raises(ValueError):
        load_board(path)
