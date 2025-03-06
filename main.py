from matplotlib import pyplot as plt
import seaborn as sns
import EGA, Perebor, metrics,HillClimb,Task,numpy as np
from config import *
import pandas as pd


if __name__ == "__main__":

    perebor_mass = np.arange(NUM_OF_EXPERIMENTS)
    hill_climb_mass = np.arange(NUM_OF_EXPERIMENTS)
    ega_mass = np.arange(NUM_OF_EXPERIMENTS)
    ega_modified_mass = np.arange(NUM_OF_EXPERIMENTS)

    for j in range(NUM_OF_EXPERIMENTS):
        tasks = Task.generate(10, DESTINATION_TIME, DIREKTIV_TIME, EXECUTION_TIME)
        loss = metrics.Loss(tasks)
        # print("hill-climbing - ", HillClimb.fit(tasks, loss))
        # print("EGA - ", EGA.fit(tasks, COUNT_OF_GENERATIONS, POPULATION_SIZE,loss,REPLACE_COEF,ELITE_COEF,CHOOSE_RANDOM_CROSSOVER))
        # print("perebor - ", Perebor.fullPerebor(tasks,loss))
        # print("-----------------------")
        ega_mass[j]=(EGA.fit(tasks, COUNT_OF_GENERATIONS, POPULATION_SIZE,loss,REPLACE_COEF,ELITE_COEF,CHOOSE_RANDOM_CROSSOVER)).loss
        ega_modified_mass[j] = (EGA.fit(tasks, COUNT_OF_GENERATIONS, POPULATION_SIZE,loss,REPLACE_COEF,ELITE_COEF,1)).loss
        hill_climb_mass[j]=(HillClimb.fit(tasks, loss))[1]
        perebor_mass[j]=(Perebor.fullPerebor(tasks,loss))[1]

    # delta_hillclimb = ((hill_climb_mass - perebor_mass) / perebor_mass) * 100
    # delta_ega = ((ega_mass - perebor_mass) / perebor_mass) * 100
    # df = pd.DataFrame({"delta_ega": delta_ega, "delta_hillclimb": delta_hillclimb,"delta_ega_modified":ega_modified_mass})
    # df.to_csv("delta.csv",index=False,sep='\t')
    # sns.histplot(df, bins=10,multiple="dodge")
    # plt.show()