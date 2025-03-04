import EGA, Perebor, metrics,HillClimb,Task
from config import *



if __name__ == "__main__":

    for j in range(NUM_OF_EXPERIMENTS):
        tasks = Task.generate(10, DESTINATION_TIME, DIREKTIV_TIME, EXECUTION_TIME)
        loss = metrics.Loss(tasks)
        print("hill-climbing - ", HillClimb.fit(tasks, loss))
        print("EGA - ", EGA.fit(tasks, COUNT_OF_GENERATIONS, POPULATION_SIZE,loss,REPLACE_COEF,ELITE_COEF,CHOOSE_RANDOM_CROSSOVER))
        print("perebor - ", Perebor.fullPerebor(tasks,loss))
        print("-----------------------")