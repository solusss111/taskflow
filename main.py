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
        input("\nназад")
    else:
        input("\nназад")


def show_all_tasks():
    label_create_task = '''
========== Все задачи ==========
'''
    sys.stdout.write("\033[H\033[2J")
    print(label_create_task)
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
    input("\nназад")


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
            case "2":
                show_all_tasks()
            case "3":
                ...
            case "4":
                ...
            case "5":
                ...
            case "6":
                ...
            case _:
                break
        
            
    print("Программа остановлена.")

if __name__ == "__main__":
    main()