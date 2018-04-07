def assignTargets(x):
    preyList = {}
    i = 0
    while i < len(x):
        preyList[x[i]] = x[i-1]
        i+=1
    return preyList
