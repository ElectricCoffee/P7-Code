#checks if it is possible to get from s0 to goal, a forward approch
def forwardDFS(st, s0, goal):
    if s0 == goal:
        return True
    elif not canTakeAnAction(st, s0):
        return False
    for x in allActions(st, s0):
        if forwardDFS(st, s0, x):
            return True
    return False


#checks if it is possible to take an action from s
def canTakeAnAction(st, s):
   for x in range(0, len(st[s])):
        if st[s][x] is not None:
            return True
   return False


#returns a list of every state s can go to
def allActions(st, s):
    act = []
    for x in range(0, len(st[s])):
        if st[s][x] is not None:
            act.append(x)
    return act


def backwardDFS(st, s0, goal):
    if s0 == goal:
        return True
    elif not thereExistAnAction(st, goal):
        return False
    for x in allPreState(st, goal):
        if backwardDFS(st, s0, x):
            return True
    return False


#checks if there exist an action to s in st
def thereExistAnAction(st, s):
    for x in range(0,len(st)):
        if st[x][s] is not None:
            return True
    return False

def allPreState(st, s):
    preState = []
    for x in range(0,len(st)):
        if st[x][s] is not None:
            preState.append(x)
    return preState