import random

class Task:
    # StartTime = 0
    # EndTime = 0
    def __init__(self, number, destTime, time, direktiv):
        self.num = number
        self.StartTime = 0
        self.EndTime = 0
        self.DestTime = random.randrange(destTime[0], destTime[1])
        self.Time = random.randrange(time[0], time[1])
        self.Direktiv = random.randrange(direktiv[0], direktiv[1])

    def __str__(self):
        return (f"Number -                 {self.num}\n"
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


tasks = generate(10, (5, 10), (7, 12), (3, 9))