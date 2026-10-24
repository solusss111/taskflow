import sys
from board import TaskBoard
from tabulate import tabulate


board = TaskBoard()

def create_task():
    label_create_task = '''
========== Создать задачу ==========
'''
    sys.stdout.write("\033[H\033[2J")
    print(label_create_task)
    try:
        title = input("Название: ")
        due_date = input("Срок выполнения (ГГГГ-ММ-ДД, Enter — без срока): ")
        
        board.create_task(title, due_date)
    except ValueError as e:
        print(f"Ошибка: {e}")


def show_all_tasks():
    label_show_tasks = '''
========== Все задачи ==========
'''
    sys.stdout.write("\033[H\033[2J")
    print(label_show_tasks)
    tasks = board.list_tasks
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
    show_all_tasks()
    tasks = board.list_tasks
    if tasks:
        try:
            task_id = int(input("\nВыберите ID задачи: "))
            board.get_task(task_id=task_id)
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
            print(f"Статус задачи {board.get_task(task_id).title} успешно изменено на {status}!")
        except LookupError as e:
            print(f"Ошибка: {e}")
    else:
        print("Нет задачи для изменение статуса.")

def delete_task():
    show_all_tasks()
    tasks = board.list_tasks
    if tasks:
        task_id = int(input(("\nВыберите ID задачи которую вы хотите удалить: ")))
        try:
            task = board.get_task(task_id=task_id)
            confirm = input(f"Вы действительно хотите удалить задачу '{task.title}'? (да/нет): ")
            match confirm:
                case "да":
                    board.delete_task(task_id=task_id)
                case _:
                    print("Действие отменено.")
                    return
        except LookupError as e:
            print(f"Ошибка: {e}")
        else:
            print(f"Задача с ID {task_id} успешно удалено.")
    else:
        print("Нет задачи для удалении.")





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
        sys.stdout.write("\033[H\033[2J")
        print(label_main_menu)
        choice = input("Выберите действие: ")
        match choice:
            case "1":
                create_task()
                input("\nназад")
            case "2":
                show_all_tasks()
                input("\nназад")
            case "3":
                
                change_task_status()
                input("\nназад")
            case "4":
                show_all_tasks()
                delete_task()
                input("\nназад")
            case "5":
                ...
            case "6":
                ...
            case _:
                break
        
            
    print("Программа остановлена.")

if __name__ == "__main__":
    main()