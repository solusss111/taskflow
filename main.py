import sys
from datetime import date

from tabulate import tabulate

from board import TaskBoard
from models import Task


board = TaskBoard()

STATUS_CHOICES = {"1": "todo", "2": "in_progress", "3": "done"}


def ask_status(question: str) -> str | None:
    print("\n1. todo\n2. in progress\n3. done")
    return STATUS_CHOICES.get(input(f"{question}: ").strip())


def clear_screen():
    sys.stdout.write("\033[H\033[2J")


def create_task():
    label_create_task = '''
========== Создать задачу ==========
'''
    clear_screen()
    print(label_create_task)
    try:
        title = input("Название: ")
        raw = input("Срок выполнения (ГГГГ-ММ-ДД, Enter — без срока): ").strip()
        due_date = date.fromisoformat(raw) if raw else None
        if due_date is not None and due_date < date.today():
            print("Срок не может быть в прошлом")
        created_task = board.create_task(title, due_date)
    except ValueError as e:
        print(f"Ошибка: {e}")
    else:
        print(f"Задача {created_task.id} создана")


def show_tasks(tasks: list[Task] | None = None, title: str = "Все задачи"):
    if tasks is None:
        tasks = board.tasks
    label_show_tasks = f'''
========== {title} ==========
'''
    clear_screen()
    print(label_show_tasks)
    if tasks:
        structured_data = [
            {
                "ID": task.id,
                "Название": task.title,
                "Статус": task.status,
                "Срок": task.due_date if task.due_date else "без срока"
            }
            for task in tasks
        ]
        print(tabulate(structured_data, headers="keys",
              tablefmt="plain", stralign="left"))
    else:
        print("Список задач пуст.")


def change_task_status():
    show_tasks(title="Список задач")
    if board.tasks:
        try:
            task_id = int(input("\nВыберите ID задачи: "))
            task = board.get_task(task_id)
            status = ask_status("На какой статус вы хотите изменить?")
            if status is None:
                print("Статус не изменён")
                return
            board.change_status(task_id=task_id, status=status)
            print(f"Статус задачи {task.title} успешно изменён на '{status}'")
        except (ValueError, LookupError) as e:
            print(f"Ошибка: {e}")
    else:
        print("Нет задач для изменения статуса.")


def delete_task():
    show_tasks(title="Какую задачу хотите удалить?")
    tasks = board.tasks
    if tasks:
        try:
            task_id = int(
                input(("\nВыберите ID задачи которую вы хотите удалить: ")))
            task = board.get_task(task_id=task_id)
            confirm = input(
                f"Вы действительно хотите удалить задачу '{task.title}'? (да/нет): ")
            match confirm.strip().lower():
                case "да":
                    board.delete_task(task_id=task_id)
                case _:
                    print("Действие отменено.")
                    return
        except (ValueError, LookupError) as e:
            print(f"Ошибка: {e}")
        else:
            print(f"Задача с ID {task_id} удалена.")
    else:
        print("Нет задач для удаления.")


def show_tasks_by_status():
    label_choose_status = '''
========== Выберите статус ==========
'''
    clear_screen()
    print(label_choose_status)
    status = ask_status("По какому статусу делать фильтр?")
    if status is None:
        print("Неверный выбор")
        return
    show_tasks(board.filter_by_status(status=status),
               f"Все задачи по статусу {status}")


def main():
    label_main_menu = '''
========== TaskFlow ==========

1. Создать задачу
2. Показать все задачи
3. Изменить статус задачи
4. Удалить задачу
5. Найти задачи по статусу
6. Показать просроченные задачи

0. Выйти
'''
    try:
        while True:
            clear_screen()
            print(label_main_menu)
            choice = input("Выберите действие: ").strip()
            match choice:
                case "1":
                    create_task()
                case "2":
                    show_tasks()
                case "3":
                    change_task_status()
                case "4":
                    delete_task()
                case "5":
                    show_tasks_by_status()
                case "6":
                    show_tasks(board.get_overdue(),
                               title="Просроченные задачи")
                case "0":
                    break
                case _:
                    print("Неизвестная команда")
            input("\nНажмите Enter, чтобы вернуться в меню")
    except (KeyboardInterrupt, EOFError):
        pass

    print("Программа остановлена.")


if __name__ == "__main__":
    main()
