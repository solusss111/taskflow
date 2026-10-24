from datetime import date


class Task:
    ALLOWED_STATUSES = ("todo", "in_progress", "done")

    def __init__(
        self,
        task_id: int,
        title: str,
        due_date: date | None = None,
        status: str = "todo",
    ) -> None:
        title = title.strip()

        if not title:
            raise ValueError("Название задачи не может быть пустым")

        self.id = task_id
        self.title = title
        self.due_date = due_date

        self.set_status(status)

    @property
    def status(self) -> str:
        return self._status

    def set_status(self, status: str) -> None:
        if status not in self.ALLOWED_STATUSES:
            raise ValueError(
                "Допустимые статусы: todo, in_progress, done"
            )

        self._status = status

    def is_overdue(self, on_date: date) -> bool:
        return (
            self.due_date is not None
            and self.due_date < on_date
            and self.status != "done"
        )