import sys
from board import TaskBoard
from tabulate import tabulate
from datetime import date
from models import Task


board = TaskBoard()

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
        due_date = date.fromisoformat(raw) 
        if due_date < date.today():
            due_date = None
            print("Задача будет бессрочной, так как указана прошедшая дата.")
        else:
            due_date = None
            print("Задача будет бессрочной, так как неверный формат даты.")
    except ValueError as e:
        print(f"Ошибка: {e}")
    else:
        board.create_task(title, due_date)
        print("Задача создана")

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
        print(tabulate(structured_data, headers="keys", tablefmt="plain", stralign="left"))
    else:
        print("Список задачи пусто.")

def change_task_status():
    show_tasks(title='Статус какой задачи хотите изменить?')
    tasks = board.tasks
    if tasks:
        try:
            task_id = int(input("\nВыберите ID задачи: "))
            print("\n1. todo\n2. in progress\n3. done")
            status = input("На какой статус вы хотите изменить?: ")
            match status:
                case "1":
                    status = "todo"
                case "2":
                    status = "in_progress"
                case "3":
                    status = "done"
                case _:
                    print("Статус задачи остался неизменным.")
                    return
            board.change_status(task_id=task_id, status=status)
            print(f"Статус задачи {board.get_task(task_id).title} успешно изменено на '{status}'")
        except (ValueError, LookupError) as e:
            print(f"Ошибка: {e}")
    else:
        print("Нет задачи для изменение статуса.")

def delete_task():
    show_tasks(title="Какую задачу хотите удалить?")
    tasks = board.tasks
    if tasks:
        try:
            task_id = int(input(("\nВыберите ID задачи которую вы хотите удалить: ")))
            task = board.get_task(task_id=task_id)
            confirm = input(f"Вы действительно хотите удалить задачу '{task.title}'? (да/нет): ")
            match confirm.strip().lower():
                case "да":
                    board.delete_task(task_id=task_id)
                case _:
                    print("Действие отменено.")
                    return
        except (ValueError, LookupError) as e:
            print(f"Ошибка: {e}")
        else:
            print(f"Задача с ID {task_id} успешно удалено.")
    else:
        print("Нет задачи для удалении.")

def show_tasks_by_status():
    label_choose_status = '''
========== Выберите статус ==========
'''
    clear_screen()
    print(f"{label_choose_status}\n1. todo\n2. in progress\n3. done")
    status = input("По какому статусу делать фильтр?: ")
    clear_screen()
    match status:
        case "1":
            show_tasks(board.filter_by_status("todo"))
        case "2":
            show_tasks(board.filter_by_status("in_progress"))
        case "3":
            show_tasks(board.filter_by_status("done"))
        case _:
            print("Пожалуйста, выберите один из 3 вариантов.")


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

    while True:
        clear_screen()
        print(label_main_menu)
        choice = input("Выберите действие: ")
        match choice:
            case "1":
                create_task()
                input("\nназад")
            case "2":
                show_tasks()
                input("\nназад")
            case "3":
                change_task_status()
                input("\nназад")
            case "4":
                delete_task()
                input("\nназад")
            case "5":
                show_tasks_by_status()
                input("\nназад")
            case "6":
                show_tasks(board.get_overdue(), title="Просроченные задачи")
                input("\nназад")
            case "0":
                break
            case _:
                print("Неизвестная команда")
                input("\nНажмите Enter...")
        
            
    print("Программа остановлена.")

if __name__ == "__main__":
    main()