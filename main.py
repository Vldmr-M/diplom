import pandas as pd

import EGA, Perebor, metrics,HillClimb,Task,numpy as np,time
from config import *
from Permutation import Permutation

def prepare_mass():
    perebor_mass = np.arange(NUM_OF_EXPERIMENTS)
    hill_climb_mass = np.arange(NUM_OF_EXPERIMENTS)
    ega_mass = np.arange(NUM_OF_EXPERIMENTS)
    ega_modified_mass = np.arange(NUM_OF_EXPERIMENTS)
    return ega_mass, ega_modified_mass, hill_climb_mass, perebor_mass


def calculate_delta(ega_result_mass, hillClimb_result_mass, modifiedEga_result_mass, perebor_result_mass,file_name):
    delta_hillclimb = np.trunc(((hillClimb_result_mass - perebor_result_mass) / perebor_result_mass) * 100)
    delta_ega = np.trunc(((ega_result_mass - perebor_result_mass) / perebor_result_mass) * 100)
    delta_ega_modified = np.trunc(((modifiedEga_result_mass - perebor_result_mass) / perebor_result_mass) * 100)
    df_delta = pd.DataFrame({"ega": delta_ega, "modif_ega": delta_ega_modified, "hill climb": delta_hillclimb})
    df_delta.to_csv(file_name, index=False, sep='\t')
    print(df_delta.head(10))


def main():
    ega_result_mass, modifiedEga_result_mass, hillClimb_result_mass, perebor_result_mass = prepare_mass()


    for j in range(NUM_OF_EXPERIMENTS):
        tasks = Task.generate(COUNT_OF_TASKS, DESTINATION_TIME, DIREKTIV_TIME, EXECUTION_TIME)  #генерируем задачи
        loss = metrics.Loss(tasks)   #настраиваем лосс


        # print("EGA - ",EGA.fit(tasks, COUNT_OF_GENERATIONS, POPULATION_SIZE, loss, REPLACE_COEF,MUTATION_COEF, ELITE_COEF,CHOOSE_RANDOM_CROSSOVER))
        # print("Hill Climb - ",Permutation(HillClimb.fit(tasks, loss)[0],loss))
        # print("Perebor - ",Permutation(Perebor.fullPerebor(tasks, loss)[0],loss))
        #init_perm = [Permutation(list(x),loss) for x in HillClimb.fit(tasks, loss)[0]*5]   # генерируем с помощью HC хорошую перестановку

        ega_result_mass[j] = (EGA.fit(tasks, COUNT_OF_GENERATIONS, POPULATION_SIZE, loss, REPLACE_COEF,MUTATION_COEF, ELITE_COEF,
                               CHOOSE_RANDOM_PARENT_SELECTION)).loss
        print("ega - ",ega_result_mass[j])

        modifiedEga_result_mass[j] = (EGA.fit(tasks, COUNT_OF_GENERATIONS, POPULATION_SIZE, loss, REPLACE_COEF,MUTATION_COEF, ELITE_COEF,
                                              CHOOSE_RANDOM_PARENT_SELECTION)).loss
        print("modified ega - ",modifiedEga_result_mass[j])


        hillClimb_result_mass[j] = (HillClimb.fit(tasks, loss))[1]
        print("hill climb - ",hillClimb_result_mass[j])

        perebor_result_mass[j] = (Perebor.fullPerebor(tasks, loss))[1]
        print("perebor - ",perebor_result_mass[j])
        print("-----------")

    calculate_delta(ega_result_mass, hillClimb_result_mass, modifiedEga_result_mass, perebor_result_mass,"experiment2.csv")


if __name__ == "__main__":
    main()