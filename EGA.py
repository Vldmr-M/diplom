import itertools, random
from typing import Callable
from copy import copy, deepcopy
from Permutation import Permutation


def cxPartialyMatched(par1:Permutation, par2:Permutation,loss:Callable)->tuple:
    """Executes a partially matched crossover (PMX) on the input individuals.
    The two individuals are modified in place. This crossover expects
    :term:`sequence` individuals of indices, the result for any other type of
    individuals is unpredictable.

    :param ind1: The first individual participating in the crossover.
    :param ind2: The second individual participating in the crossover.
    :returns: A tuple of two individuals.
    """
    ind1 = deepcopy(par1.perm)
    ind2 = deepcopy(par2.perm)
    size = min(len(ind1), len(ind2))
    p1, p2 = [0] * size, [0] * size

    # Initialize the position of each indices in the individuals
    for i in range(size):
        p1[ind1[i]] = i
        p2[ind2[i]] = i
    # print(p1,p2)
    # Choose crossover points
    cxpoint1 = random.randint(0, size)
    cxpoint2 = random.randint(0, size - 1)
    if cxpoint2 >= cxpoint1:
        cxpoint2 += 1
    else:  # Swap the two cx points
        cxpoint1, cxpoint2 = cxpoint2, cxpoint1
    # print(cxpoint1,cxpoint2)

    # Apply crossover between cx points
    for i in range(cxpoint1, cxpoint2):
        # Keep track of the selected values
        temp1 = ind1[i]
        temp2 = ind2[i]
        # Swap the matched value
        # print(ind1)
        ind1[i], ind1[p1[temp2]] = temp2, temp1
        ind2[i], ind2[p2[temp1]] = temp1, temp2
        # Position bookkeeping
        p1[temp1], p1[temp2] = p1[temp2], p1[temp1]
        p2[temp1], p2[temp2] = p2[temp2], p2[temp1]
    ind1 = Permutation(ind1,loss)
    ind2 = Permutation(ind2,loss)
    return ind1, ind2


def hamming(par1: Permutation, par2: Permutation) ->int:
    return par1 != par2


def generate_origin_population(size_of_population:int, tasks:list,loss:Callable) ->list:

    perms = random.choices([*itertools.permutations(range(len(tasks)))], k=size_of_population)
    return [Permutation(list(i),loss) for i in perms]

def auto_breeding(population:list)->tuple:
    """
    chooses the parents with max Hamming distance
    :param population: array_like of Permutation
    :return: tuple with 2 parents
    """

    par1 = population[0]
    par2 = population[1]
    max_hamm = 0
    for i in range(len(population)):
        for j in range(len(population)):
            if hamming(population[i], population[j]) > max_hamm:
                par1 = population[i]
                par2 = population[j]
    population.remove(par1)
    population.remove(par2)
    return par1, par2

def rand_choose(population:list)->tuple:
    """
    chooses parents randomly
    :param population:
    :return:
    """
    # for i in population:
    #     print(i)
    # print("--------------")
    par1,par2 = random.sample(population,k=2)
    # print(par1)
    # print(par2)
    population.remove(par1)
    population.remove(par2)
    return par1,par2


def choose_parents(population:list,use_random_choose:int=0)->tuple:
    if use_random_choose:
        return rand_choose(population)
    else:
        return auto_breeding(population)


def mutation(perm: Permutation, coef_of_mutation:float)->list[Permutation] | list[None]:

    if random.random() <= coef_of_mutation:
        mutant = deepcopy(perm)
        rand_indexes = random.choices(range(len(perm.perm)), k=2)
        mutant.perm[rand_indexes[0]], mutant.perm[rand_indexes[1]] = mutant.perm[rand_indexes[1]], mutant.perm[
            rand_indexes[0]]
        return [mutant]
    else:
        return []


def elite_selection(curr_population:list[Permutation],childs:list[Permutation],replace_coef:float=1,elite_coef:float=0.5)->list[Permutation]:
    """
    selects the best individuals from reproductive population and returns it.


    chooses part of population by elite selection algorithm,
    rest of population is replaced by Fitness proportionate selection algorithm
    from childs

    :param curr_population:
    :param childs:
    :param replace_coef:
    :param elite_coef:
    :return:
    """
    replace_size = round(len(curr_population)*replace_coef)
    elite_size = round(elite_coef * replace_size)
    next_gen = random.choices(curr_population,k=len(curr_population)-replace_size)
    population = sorted(deepcopy(childs+curr_population), key=lambda x: x.loss)

    #заполняем элитой
    for i in range(elite_size):
        next_gen += [population[i]]

    #вычисляем вероятности
    length_of_others = replace_size - elite_size
    # mean_fit = sum([j.loss for j in childs]) / len(childs)
    weights = [1/j.loss for j in childs]

    #заполняем остальное
    next_gen += random.choices(childs, weights, k=length_of_others)
    return next_gen


def fit(tasks:list, count_of_generations:int, population_size:int,loss,replace_coef:float,
        mutation_coef:float,elite_coef:float,choose_random_parents:int,init_population:list=None)->Permutation:
    gens_without_imp=0
    if init_population:
        curr_population = init_population
    else:
        curr_population = generate_origin_population(population_size, tasks,loss)
    best_loss = sorted(curr_population, key=lambda x: x.loss)[0].loss

    for i in range(count_of_generations):


        if gens_without_imp >= 10:
            break
        childs = []
        # print("curr population - ")
        # for k in curr_population: print(k)
        population_copy = copy(curr_population)
        #выбираем родителей и воспроизводим потомков
        for j in range(population_size // 2):
            par1, par2 = choose_parents(population_copy,choose_random_parents)
            child1, child2 = cxPartialyMatched(par1, par2,loss)
            childs += [child1, child2]

        #добавляем мутантов к потомкам
        for j in range(len(childs)):
            childs += mutation(childs[j], mutation_coef)

        #заменяем популяцию
        curr_population = elite_selection(curr_population,childs,replace_coef,elite_coef)

        #условие остановки
        temp = sorted(curr_population, key=lambda x: x.loss)[0].loss
        if temp < best_loss:
            best_loss = temp
            gens_without_imp = 0
        else:
            gens_without_imp+=1

    return sorted(curr_population, key=lambda x: x.loss)[0]


# a = fit(Task.tasks, 30, 20)
#
# print("final population - ")
# for i in a:
#     print(i)
