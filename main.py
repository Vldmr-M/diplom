import EGA
import Perebor
import metrics
import  itertools, random
import Task


def Loss(tasks):
    """Принимает на вход массив объектов Task и перестановку
    возвращает перестановку с лучшим(меньшим) лоссом"""
    def loss(perm):
        loss = 0
        curr_time = 0
        for i in perm:
            if tasks[i].DestTime > curr_time:
                curr_time = tasks[i].DestTime
            else:
                curr_time += tasks[i].Time
            loss += curr_time - tasks[i].DestTime if curr_time > tasks[i].DestTime else 0
        return loss
    return loss


loss = Loss(Task.tasks)

class HillClimbing():
    @staticmethod
    def generate_neighbours(perm):
        """returns a list of tuples"""
        neighbours = []
        for i in range(len(perm) - 1):
            temp = perm[0:i] + perm[i + 1:i + 2] + perm[i:i + 1] + perm[i + 2:]
            neighbours.append(temp)
        neighbours.append((perm[-1],) + perm[1:-1] + (perm[0],))
        return neighbours

    @staticmethod
    def fit(tasks, loss):
        """Принимает на вход массив объектов Task
        возвращает перестановку с лучшим(меньшим) лоссом"""
        curr_perm = random.choice([*itertools.permutations(range(len(tasks)))])
        # for _ in tasks:
        #     print(_)
        curr_loss = loss(curr_perm)

        while True:
            neighbours_losses = {}
            neighbours_perm = HillClimbing.generate_neighbours(curr_perm)
            for i in neighbours_perm:
                neighbours_losses[i] = loss(i)
            if min(neighbours_losses.values()) < curr_loss:
                curr_perm = min(neighbours_losses, key=neighbours_losses.get)
                curr_loss = min(neighbours_losses.values())
            else:
                break
        return curr_perm, curr_loss



if __name__ == "__main__":
    for j in range(100):
        a = Task.generate(10, (5, 10), (7, 12), (3, 9))
        loss = Loss(a)
        print("hill-climbing - ", HillClimbing.fit(a, loss=loss))
        print("EGA - ", EGA.fit(a,30,20))
        print("perebor - ", Perebor.fullPerebor(a))
        print("-----------------------")