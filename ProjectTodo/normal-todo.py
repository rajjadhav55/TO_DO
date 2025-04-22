

tasks=[]

def display_menu():
    print("-----TO-DO-----")
    print("  ")
    print("1. add task")
    print("2. remove task")
    print("3. view task")
    print("4. exit")

def view_task():
    if len(tasks) == 0:
        print("\nno task in your todo")
    else:
        print("\nyour tasks")
        i = 1
        for task in tasks:
            print(f"{i}:{task}")
            i+=1
        print("-"*20)

def add_task():
    task=input("enter your task: ")
    if len(task) > 0:
        tasks.append(task)
        print(f" task '{task}' added to the task ")
    else:
        print("task cannot be empty")

def remove_task():
    view_task()
    if len(tasks) > 0:
        index=int(input("enter the number of task to remove : "))
        if 1 <= index <= len(tasks):
            deleted_task= tasks.pop(index - 1)
            print(f" task '{deleted_task}' removed")
        else:
            print("invalid number")

def main():
    while True:
        display_menu()
        choice = int(input("enter your choise : "))
        if choice == 1:
            add_task()
        if choice == 2:
            remove_task()
        if choice == 3:
            view_task()
        if choice == 4:
            print("Exiting...")
            break

main()


    