from datetime import date, datetime
from models import Task

class TaskBoard:
    def __init__(self) -> None:
        self.tasks: list[Task] = []
        self._next_id: int = 1

    def create_task(self, title: str, due_date: date | None) -> None:
        new_task = Task(self._next_id, title, due_date)
        self.tasks.append(new_task)
        self._next_id += 1

    def get_task(self, task_id: int) -> Task:
        for task in self.tasks:
            if task.id == task_id:
                return task
            
        raise LookupError(f"Задача с ID {task_id} не найдена")

    def change_status(self, task_id, status) -> None:
        task = self.get_task(task_id)
        task.set_status(status)

    def delete_task(self, task_id) -> None:
        task = self.get_task(task_id)
        self.tasks.remove(task)

    def filter_by_status(self, status) -> list[Task]:
        tasks_by_status = []
        for task in self.tasks:
            if task.status == status:
                tasks_by_status.append(task)
        return tasks_by_status

    def get_overdue(self) -> list[Task]:
        overdue_tasks = []
        for task in self.tasks:
            if task.is_overdue(date.today()):
                overdue_tasks.append(task)
        return overdue_tasks