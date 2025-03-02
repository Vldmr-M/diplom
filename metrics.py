import Task



def Loss(tasks):
    """Принимает на вход массив объектов Task и перестановку
    возвращает перестановку с лучшим(меньшим) лоссом"""
    def loss(perm):
        loss = 0
        curr_time = 0
        for i in perm:
            if tasks[i].DestTime > curr_time:
                curr_time = tasks[i].DestTime
            else:
                curr_time += tasks[i].Time
            loss += curr_time - tasks[i].DestTime if curr_time > tasks[i].DestTime else 0
        return loss
    return loss


