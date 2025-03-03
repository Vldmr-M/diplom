import itertools, random
from copy import copy, deepcopy
from Permutation import Permutation


def cxPartialyMatched(par1, par2,loss):
    """Executes a partially matched crossover (PMX) on the input individuals.
    The two individuals are modified in place. This crossover expects
    :term:`sequence` individuals of indices, the result for any other type of
    individuals is unpredictable.

    :param ind1: The first individual participating in the crossover.
    :param ind2: The second individual participating in the crossover.
    :returns: A tuple of two individuals.

    Moreover, this crossover generates two children by matching
    pairs of values in a certain range of the two parents and swapping the values
    of those indexes. For more details see [Goldberg1985]_.

    This function uses the :func:`~random.randint` function from the python base
    :mod:`random` module.

    .. [Goldberg1985] Goldberg and Lingel, "Alleles, loci, and the traveling
       salesman problem", 1985.
    """
    ind1 = deepcopy(par1)
    ind2 = deepcopy(par2)
    size = min(len(ind1.perm), len(ind2.perm))
    p1, p2 = [0] * size, [0] * size

    # Initialize the position of each indices in the individuals
    for i in range(size):
        p1[ind1.perm[i]] = i
        p2[ind2.perm[i]] = i
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
        temp1 = ind1.perm[i]
        temp2 = ind2.perm[i]
        # Swap the matched value
        # print(ind1)
        ind1.perm[i], ind1.perm[p1[temp2]] = temp2, temp1
        ind2.perm[i], ind2.perm[p2[temp1]] = temp1, temp2
        # Position bookkeeping
        p1[temp1], p1[temp2] = p1[temp2], p1[temp1]
        p2[temp1], p2[temp2] = p2[temp2], p2[temp1]
    ind1 = Permutation(ind1.perm,loss)
    ind2 = Permutation(ind2.perm,loss)
    return ind1, ind2


def hamming(par1: Permutation, par2: Permutation):
    """
    calculate hamming distance between 2 Permutations
    :param par1: Permutation1
    :param par2: Permutation2
    :return: np.int64 distance
    """
    return par1 != par2


def generate_origin_population(size_of_population, tasks,loss):
    """returns list of Permutations where length of list = /size_of_population/ """
    perms = random.choices([*itertools.permutations(range(len(tasks)))], k=size_of_population)
    return [Permutation(list(i),loss) for i in perms]

def auto_breeding(population):
    """
    choosing the parents
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

def rand_choose(populaton):
    par1,par2 = random.choices(populaton,k=2)
    populaton.remove(par1)
    populaton.remove(par2)
    return par1,par2


def choose_parents(popolation,use_random_choose=0):
    if use_random_choose:
        return rand_choose(popolation)
    else:
        return auto_breeding(popolation)


def mutation(perm: Permutation, coef_of_mutation):
    if random.random() <= coef_of_mutation:
        mutant = deepcopy(perm)
        rand_indexes = random.choices(range(len(perm.perm)), k=2)
        mutant.perm[rand_indexes[0]], mutant.perm[rand_indexes[1]] = mutant.perm[rand_indexes[1]], mutant.perm[
            rand_indexes[0]]
        return [mutant]
    else:
        return []


def elite_selection(curr_population,childs,replace_coef=1,elite_coef=0.5):
    replace_size = round(len(curr_population)*replace_coef)
    elite_size = round(elite_coef * replace_size)
    next_gen = random.choices(curr_population,k=len(curr_population)-replace_size)
    population = sorted(deepcopy(childs+curr_population), key=lambda x: x.loss)


    #заполняем элитой
    for i in range(elite_size):
        next_gen += [population[i]]

    #вычисляем вероятности
    length_of_others = replace_size - elite_size
    mean_fit = sum([j.loss for j in childs]) / len(childs)
    weights = [1/j.loss for j in childs]

    #заполняем остальное
    next_gen += random.choices(childs, weights, k=length_of_others)
    return next_gen


def fit(tasks, count_of_generations, population_size,loss):
    curr_population = generate_origin_population(population_size, tasks,loss)


    for i in range(count_of_generations):

        childs = []
        # print("curr population - ")
        # for k in curr_population: print(k)
        population_copy = copy(curr_population)
        #выбираем родителей и воспроизводим потомков
        for j in range(population_size // 2):
            par1, par2 = choose_parents(population_copy)
            child1, child2 = cxPartialyMatched(par1, par2,loss)
            childs += [child1, child2]

        #добавляем мутантов к потомкам
        for j in range(len(childs)):
            childs += mutation(childs[j], 0.5)

        #заменяем популяцию
        curr_population = elite_selection(curr_population,childs,0.5,0.3)

    return sorted(curr_population, key=lambda x: x.loss)[0]


# a = fit(Task.tasks, 30, 20)
#
# print("final population - ")
# for i in a:
#     print(i)
