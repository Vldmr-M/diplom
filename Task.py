import random, json

class Task:
    # StartTime = 0
    # EndTime = 0
    def __init__(self, number, destTime, time, direktiv):
        if type(time) is not tuple:
            self.num = number
            self.DestTime = destTime
            self.Time = time
            self.Direktiv = direktiv
        else:
            self.num = number
            self.DestTime = random.randrange(destTime[0], destTime[1])
            self.Time = random.randrange(time[0], time[1])
            self.Direktiv = random.randrange(direktiv[0], direktiv[1])

    def __str__(self):
        return (f"Number -      {self.num}\n"
                f"DesttTime - {self.DestTime}\n"
                f"Time - {self.Time}\n"
                f"Direktiv - {self.Direktiv}\n"
                # f"StartTime - {self.StartTime}\n"
                # f"EndTime - {self.EndTime}\n"
                f"------------------")


def generate(n: int, DestTime: tuple, Direktiv: tuple, Time: tuple):
    TaskList = []
    for i in range(n):
        TaskList.append(Task(i, (5, 10), (7, 12), (3, 9)))
    return TaskList

def write_tasks_to_json(tasks, filename):
    """
    Записывает массив объектов Task в файл JSON.

    :param tasks: Список объектов класса Task
    :param filename: Имя файла для записи данных
    """
    # Преобразуем объекты Task в словари
    tasks_data = []
    for task in tasks:
        task_dict = {
            "Number": task.num,
            "DestTime": task.DestTime,
            "Time": task.Time,
            "Direktiv": task.Direktiv,
        }
        tasks_data.append(task_dict)

    # Запись в файл JSON
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(tasks_data, file, ensure_ascii=False, indent=4)


def read_tasks_from_json(filename):
    """
    Считывает массив объектов Task из файла JSON.

    :param filename: Имя файла для чтения данных
    :return: Список объектов класса Task
    """
    with open(filename, 'r', encoding='utf-8') as file:
        tasks_data = json.load(file)

    # Преобразуем словари обратно в объекты Task
    tasks = []
    for task_dict in tasks_data:
        task = Task(
            number=task_dict["Number"],
            destTime=task_dict["DestTime"],  # Используем одно значение для диапазона
            time=task_dict["Time"],  # Используем одно значение для диапазона
            direktiv=task_dict["Direktiv"]  # Используем одно значение для диапазона
        )
        tasks.append(task)

    return tasks


# a=generate(10, (5, 10), (3, 9), (7, 12))
# write_tasks_to_json(a, "tasks.json")
# b= read_tasks_from_json("tasks.json")
# for i in b:
#     print(i)