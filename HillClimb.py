import random,itertools
from typing import Callable


def generate_neighbours(perm:list)->list[list]:

    neighbours = []
    for i in range(len(perm) - 1):
        temp = perm[0:i] + perm[i + 1:i + 2] + perm[i:i + 1] + perm[i + 2:]
        neighbours.append(temp)
    neighbours.append((perm[-1],) + perm[1:-1] + (perm[0],))
    return neighbours


def fit(tasks:list, loss:Callable):

    curr_perm = random.choice([*itertools.permutations(range(len(tasks)))])
    curr_loss = loss(curr_perm)

    while True:
        neighbours_losses = {}
        neighbours_perm = generate_neighbours(curr_perm)
        for i in neighbours_perm:
            neighbours_losses[i] = loss(i)
        if min(neighbours_losses.values()) < curr_loss:
            curr_perm = min(neighbours_losses, key=neighbours_losses.get)
            curr_loss = min(neighbours_losses.values())
        else:
            break
    return curr_perm, curr_loss