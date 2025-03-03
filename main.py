import EGA, Perebor, metrics,HillClimb
import  itertools, random, Task


loss = metrics.Loss(Task.tasks)

if __name__ == "__main__":

    for j in range(10):
        tasks = Task.generate(10, (5, 10), (7, 12), (3, 9))
        loss = metrics.Loss(tasks)
        print("hill-climbing - ", HillClimb.fit(tasks, loss=loss))
        print("EGA - ", EGA.fit(tasks, 30, 20))
        print("perebor - ", Perebor.fullPerebor(tasks))
        print("-----------------------")
        print(dir())