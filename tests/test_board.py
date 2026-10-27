import pytest

from board import TaskBoard


@pytest.fixture
def board():
    return TaskBoard()

def test_ids_increase(board):
    first = board.create_task("A", None)
    second = board.create_task("B", None)

    assert first.id == 1
    assert second.id == 2


def test_id_is_not_reused_after_delete(board):
    board.create_task("A", None)
    board.delete_task(1)
    task = board.create_task("B", None)

    assert task.id == 2


def test_get_missing_task_raises_error(board):
    with pytest.raises(LookupError):
        board.get_task(42)


def test_filter_by_status(board):
    board.create_task("A", None)
    board.create_task("B", None)
    board.change_status(2, "done")

    assert [t.title for t in board.filter_by_status("done")] == ["B"]
