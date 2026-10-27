import json
import os
from pathlib import Path

from board import TaskBoard
from models import Task

DEFAULT_PATH = Path(__file__).parent / "data" / "tasks.json"


def save_board(board: TaskBoard, path: Path = DEFAULT_PATH) -> None:
    payload = {
        "next_id": board.next_id,
        "tasks": [task.to_dict() for task in board.tasks],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(".tmp")
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    os.replace(tmp_path, path)


def load_board(path: Path = DEFAULT_PATH) -> TaskBoard:
    board = TaskBoard()
    if not path.exists():
        return board

    try:
        with open(path, encoding="utf-8") as f:
            payload = json.load(f)
        board.tasks = [Task.from_dict(item) for item in payload["tasks"]]
    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as e:
        raise ValueError(f"Не удалось прочитать файл {path}: {e}") from e

    max_id = max((t.id for t in board.tasks), default=0)
    board.next_id = max(payload.get("next_id", 1), max_id + 1)
    return board
