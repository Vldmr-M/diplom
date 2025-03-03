import itertools, pandas as pd,main
import Permutation

def fullPerebor(tasks,loss):
    """Принимает на вход лист с задачами
    Возвращает перестановку и лосс для нее"""
    # permutations = pd.DataFrame({"perm": itertools.permutations(range(len(tasks)))})
    # permutations['perm_losses'] = permutations.map(main.loss)
    # minid = permutations['perm_losses'].idxmin()
    # return permutations['perm'].iloc[minid], permutations['perm_losses'].iloc[minid]

    all_perms = [Permutation.Permutation(i,loss) for i in itertools.permutations(range(len(tasks)))]
    return sorted(all_perms, key = lambda x: x.loss)[0]