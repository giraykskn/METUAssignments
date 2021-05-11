import copy

#class
txt = "A->{A}\tB->{B}\tC->{C}\n"
class State:

    def __init__(self, ID,  parentID, List, g, h):
        self.ID = ID
        self.parentID = parentID
        self.List = copy.deepcopy(List)
        self.g = g
        self.h = h

    def p(self):
        print('ID: ', self.ID)
        print('ParentID: ', self.parentID)
        print('List: ', self.List)
        print('g value: ', self.g)
        print('h value: ', self.h)

    def outP(Self):
        print(txt.format(A = Self.List[0], B = Self.List[1], C = Self.List[2]))

#input
algorithm = input()
maxCost = int(input())
noOfDisks = int(input())
goalRod = input()
Ain = input()
Bin = input()
Cin = input()

if (Ain != ''):
    A = Ain.split(",")
    for i in range(len(A)):
        A[i] = int(A[i])
    A.sort(reverse = True)
else:
    A = []

if (Bin != ''):
    B = Bin.split(",")
    for i in range(len(B)):
        B[i] = int(B[i])
    B.sort(reverse = True)
else:
    B = []

if (Cin != ''):
    C = Cin.split(",")
    for i in range(len(C)):
        C[i] = int(C[i])
    C.sort(reverse = True)
else:
    C = []

def h(A, B, C):
    h = 0
    if (goalRod == 'A'):
        h += len(B)
        h += len(C)
        for i in A:
            smaller = False
            for j in B:
                if i<j:
                    smaller = True
            for j in C:
                if i<j:
                    smaller = True
            if smaller==True:
                h += 1
    elif (goalRod == 'B'):
        h += len(A)
        h += len(C)
        for i in B:
            smaller = False
            for j in A:
                if i<j:
                    smaller = True
            for j in C:
                if i<j:
                    smaller = True
            if smaller==True:
                h += 1
    else:
        h += len(B)
        h += len(A)
        for i in C:
            smaller = False
            for j in B:
                if i<j:
                    smaller = True
            for j in A:
                if i<j:
                    smaller = True
            if smaller==True:
                h += 1
    return h

Open = []
Closed = []
States = []
curr = []

def output(state):
    curState=state
    outp = [curState]
    while(curState.parentID != None):
        curState = copy.deepcopy(States[curState.parentID])
        outp.append(curState)
    outp.reverse()
    if(len(outp) > maxCost):
        print('FAILURE')
        return
    print('SUCCESS')
    print('\n', end='')
    first = True
    for i in outp:
        if(first):
            first = False
        else:
            print('\n', end='')
        i.outP()


def movable(state, fro, to):
    if (len(state.List[fro]) == 0):
        return False
    if (len(state.List[to]) == 0):
        return True
    if(state.List[fro][-1] < state.List[to][-1]):
        return True
    else:
        return False

def move(list, fro, to):
    list[to].append(list[fro].pop())

def AAlg(maxCost, noOfDisks, goalRod, A, B, C, Open, Closed, States):
    initial = State(0, None, [A,B,C], 0, h(A,B,C))
    Open.append(initial)
    States.append(initial)
    solution = []
    for i in range(noOfDisks):
        solution.append(i+1)
    solution.reverse()
    s = 0
    while(True):
        """print('***************************************** s = ',s)
        print('************ Open:')
        for i in Open:
            i.p()
        print('************ Closed:')
        for i in Closed:
            i.p()
        print('************ States:')
        for i in States:
            i.p()"""
        if (len(Open) == 0):
            print("FAILURE")
            break
        min = float('inf')
        index = -1
        for i in range(len(Open)):
            if (Open[i].g + Open[i].h < min):
                min = Open[i].g + Open[i].h
                index = i
        Closed.append(Open.pop(index))

        if(goalRod == 'A'):
            if(Closed[-1].List[0] == solution):
                output(Closed[len(Closed)-1])
                return
        elif(goalRod == 'B'):
            if(Closed[-1].List[1] == solution):
                output(Closed[len(Closed)-1])
                return
        else:
            if(Closed[-1].List[2] == solution):
                output(Closed[len(Closed)-1])
                return

        Successors = []
        closedState = copy.deepcopy(Closed[-1])
        if(movable(closedState, 0, 1)):
            newList = copy.deepcopy(closedState.List)
            move(newList, 0, 1)
            newState = State(len(States), closedState.ID, newList, closedState.g+1, h(newList[0],newList[1],newList[2]))
            States.append(newState)
            Successors.append(newState)

        if(movable(closedState, 0, 2)):
            newList = copy.deepcopy(closedState.List)
            move(newList, 0, 2)
            newState = State(len(States), closedState.ID, newList, closedState.g+1, h(newList[0],newList[1],newList[2]))
            States.append(newState)
            Successors.append(newState)

        if(movable(closedState, 1, 0)):
            newList = copy.deepcopy(closedState.List)
            move(newList, 1, 0)
            newState = State(len(States), closedState.ID, newList, closedState.g+1, h(newList[0],newList[1],newList[2]))
            States.append(newState)
            Successors.append(newState)

        if(movable(closedState, 1, 2)):
            newList = copy.deepcopy(closedState.List)
            move(newList, 1, 2)
            newState = State(len(States), closedState.ID, newList, closedState.g+1, h(newList[0],newList[1],newList[2]))
            States.append(newState)
            Successors.append(newState)

        if(movable(closedState, 2, 0)):
            newList = copy.deepcopy(closedState.List)
            move(newList, 2, 0)
            newState = State(len(States), closedState.ID, newList, closedState.g+1, h(newList[0],newList[1],newList[2]))
            States.append(newState)
            Successors.append(newState)

        if(movable(closedState, 2, 1)):
            newList = copy.deepcopy(closedState.List)
            move(newList, 2, 1)
            newState = State(len(States), closedState.ID, newList, closedState.g+1, h(newList[0],newList[1],newList[2]))
            States.append(newState)
            Successors.append(newState)

        for i in Successors:
            inOpen = False
            inClosed = False
            for j in Open:
                if(i.List == j.List):
                    inOpen = True
                    if(i.g + i.h < j.g + j.h):
                        j.parentID = closedState.ID

            if(len(Closed) != 0):
                for k in range(len(Closed)-1):
                    if(i.List == Closed[k].List):
                        inClosed = True
                        Closed.pop(k)
                        Open.append(i)

            if(not inOpen and not inClosed):
                Open.append(i)
        s+=1
    print('FAILURE')

def movable2(X, Y):
    if (len(X) == 0):
        return False
    if (len(Y) == 0):
        return True
    if(X[-1] < Y[-1]):
        return True
    else:
        return False

def move2(X,Y):
    Y.append(X.pop())

def recursive(path, g ,h, curr, solution):
    def h2(A, B, C):
        h = 0
        if (goalRod == 'A'):
            h += len(B)
            h += len(C)
            for i in A:
                smaller = False
                for j in B:
                    if i<j:
                        smaller = True
                for j in C:
                    if i<j:
                        smaller = True
                if smaller==True:
                    h += 1
        elif (goalRod == 'B'):
            h += len(A)
            h += len(C)
            for i in B:
                smaller = False
                for j in A:
                    if i<j:
                        smaller = True
                for j in C:
                    if i<j:
                        smaller = True
                if smaller==True:
                    h += 1
        else:
            h += len(B)
            h += len(A)
            for i in C:
                smaller = False
                for j in B:
                    if i<j:
                        smaller = True
                for j in A:
                    if i<j:
                        smaller = True
                if smaller==True:
                    h += 1
        return h
    curr = path[-1]
    f = g + h2(curr[0], curr[1], curr[2])
    if (f > h):
        return f
    if (curr == solution):
        return -1;
    min = float('inf')
    Successors = []
    if(movable2(curr[0],curr[1])):
        newList = copy.deepcopy(curr)
        move2(newList[0],newList[1])
        Successors.append(newList)
    if(movable2(curr[0],curr[2])):
        newList = copy.deepcopy(curr)
        move2(newList[0],newList[2])
        Successors.append(newList)
    if(movable2(curr[1],curr[0])):
        newList = copy.deepcopy(curr)
        move2(newList[1],newList[0])
        Successors.append(newList)
    if(movable2(curr[1],curr[2])):
        newList = copy.deepcopy(curr)
        move2(newList[1],newList[2])
        Successors.append(newList)
    if(movable2(curr[2],curr[0])):
        newList = copy.deepcopy(curr)
        move2(newList[2],newList[0])
        Successors.append(newList)
    if(movable2(curr[2],curr[1])):
        newList = copy.deepcopy(curr)
        move2(newList[2],newList[1])
        Successors.append(newList)
    #print('***********************************************',Successors)
    for i in Successors:
        inPath = False
        for j in path:
            if (i==j):
                inPath = True
        if(inPath == False):
            path.append(i)
            #print('****************** ', path)
            h2 = recursive(path, g+1, h, curr, solution)
            if(h2 == -1):
                return -1
            if(h2 < min):
                min = h2
            path.pop()
    return min

def output2(path):
    if(len(path) > maxCost):
        print('FAILURE')
    else:
        print('SUCCESS')
        print('\n', end='')
        first = True
        for i in path:
            if(first == True):
                first = False
            else:
                print('\n', end='')
            print(txt.format(A = i[0], B = i[1], C = i[2]))

def IDAAlg(maxCost, noOfDisks, goalRod, A, B, C, curr):
    def h(A, B, C):
        h = 0
        if (goalRod == 'A'):
            h += len(B)
            h += len(C)
            for i in A:
                smaller = False
                for j in B:
                    if i<j:
                        smaller = True
                for j in C:
                    if i<j:
                        smaller = True
                if smaller==True:
                    h += 1
        elif (goalRod == 'B'):
            h += len(A)
            h += len(C)
            for i in B:
                smaller = False
                for j in A:
                    if i<j:
                        smaller = True
                for j in C:
                    if i<j:
                        smaller = True
                if smaller==True:
                    h += 1
        else:
            h += len(B)
            h += len(A)
            for i in C:
                smaller = False
                for j in B:
                    if i<j:
                        smaller = True
                for j in A:
                    if i<j:
                        smaller = True
                if smaller==True:
                    h += 1
        return h
    path = []
    hx = h(A,B,C)
    path.append([A,B,C])

    soln = []
    for i in range(noOfDisks):
        soln.append(i+1)
    soln.reverse()
    if(goalRod == 'A'):
        solution = [soln,[],[]]
    elif(goalRod == 'B'):
        solution = [[],soln,[]]
    else:
        solution = [[],[],soln]

    while (True):
        #print(path)
        h2 = recursive(path, 0, hx, curr, solution)
        if (h2 == -1):
            output2(path)
            return
        elif (h2 == float('inf')):
            print('FAILURE')
            return
        hx = h2


if (algorithm == "A*"):
    AAlg(maxCost, noOfDisks, goalRod, A, B, C, Open, Closed, States)
elif (algorithm == "IDA*"):
    IDAAlg(maxCost, noOfDisks, goalRod, A, B, C, curr)
else:
    pass
