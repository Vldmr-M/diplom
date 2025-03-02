import itertools, numpy, pandas as pd


def loss(perm, tasks):
    """Принимает на вход массив объектов Task и перестановку
    возвращает перестановку с лучшим(меньшим) лоссом"""
    # print('perm type - ',type(perm))
    loss = 0
    curr_time = 0
    for i in perm:

        if tasks[i].DestTime > curr_time:
            curr_time = tasks[i].DestTime
        else:
            curr_time += tasks[i].Time
        loss += curr_time - tasks[i].DestTime if curr_time > tasks[i].DestTime else 0
    return loss


def fullPerebor(tasks):
    """Принимает на вход лист с задачами
    Возвращает перестановку и лосс для нее"""
    permutations = pd.DataFrame({"perm": itertools.permutations(range(len(tasks)))})
    permutations['perm_losses'] = permutations.map(loss, tasks=tasks)
    minid = permutations['perm_losses'].idxmin()
    return permutations['perm'].iloc[minid], permutations['perm_losses'].iloc[minid]
