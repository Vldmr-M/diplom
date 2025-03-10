import pandas as pd

import EGA, Perebor, metrics,HillClimb,Task,numpy as np,time
from config import *
from Permutation import Permutation

def main():
    perebor_mass = np.arange(NUM_OF_EXPERIMENTS)
    hill_climb_mass = np.arange(NUM_OF_EXPERIMENTS)
    ega_mass = np.arange(NUM_OF_EXPERIMENTS)
    ega_modified_mass = np.arange(NUM_OF_EXPERIMENTS)


    ega_time=0
    modif_ega_time = 0
    for j in range(NUM_OF_EXPERIMENTS):
        tasks = Task.generate(COUNT_OF_TASKS, DESTINATION_TIME, DIREKTIV_TIME, EXECUTION_TIME)
        loss = metrics.Loss(tasks)
        # print("EGA - ",EGA.fit(tasks, COUNT_OF_GENERATIONS, POPULATION_SIZE, loss, REPLACE_COEF,MUTATION_COEF, ELITE_COEF,CHOOSE_RANDOM_CROSSOVER))
        # print("Hill Climb - ",Permutation(HillClimb.fit(tasks, loss)[0],loss))
        # print("Perebor - ",Permutation(Perebor.fullPerebor(tasks, loss)[0],loss))
        init_perm = [Permutation(list(x),loss) for x in HillClimb.fit(tasks, loss)[0]*5]



        ega_mass[j] = (EGA.fit(tasks, COUNT_OF_GENERATIONS, POPULATION_SIZE, loss, REPLACE_COEF,MUTATION_COEF, ELITE_COEF,
                               CHOOSE_RANDOM_PARENT_SELECTION)).loss
        print("ega - ",ega_mass[j])



        ega_modified_mass[j] = (EGA.fit(tasks, COUNT_OF_GENERATIONS, POPULATION_SIZE, loss, REPLACE_COEF,MUTATION_COEF, ELITE_COEF, 1,init_perm)).loss
        print("modified ega - ",ega_modified_mass[j])



        hill_climb_mass[j] = (HillClimb.fit(tasks, loss))[1]
        print("hill climb - ",hill_climb_mass[j])
        # time4 = time.time()
        # print("hill climb time - ", time4 - time3)
        perebor_mass[j] = (Perebor.fullPerebor(tasks, loss))[1]
        print("perebor - ",perebor_mass[j])
        # time5 = time.time()
        # print("perebor time - ", time5 - time4)
        # print("--------------")


    delta_hillclimb = ((hill_climb_mass - perebor_mass) / perebor_mass) * 100
    delta_ega = ((ega_mass - perebor_mass) / perebor_mass) * 100
    delta_ega_modified = ((ega_modified_mass - perebor_mass) / perebor_mass) * 100
    df = pd.DataFrame({"ega": delta_ega,"modif_ega":delta_ega_modified,"hill climb":delta_hillclimb})
    df.to_csv("experiment2.csv",index=False,sep='\t')
    print("ega mean - ",df["ega"].mean())
    print("modified ega mean - ",df["modif_ega"].mean())
    # print("ega mean time - ", ega_time/NUM_OF_EXPERIMENTS)
    # print("modified ega mean time - ", modif_ega_time/NUM_OF_EXPERIMENTS)
if __name__ == "__main__":
    main()