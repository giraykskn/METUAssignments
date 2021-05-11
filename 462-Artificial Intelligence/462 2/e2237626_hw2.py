def eliminate(C, P1, P2):
    CC = []
    P11 = []
    P22 = []
    for i in C:
        if(i[0] == "!"):
            CC.append((i[1:],"negative"))
        else:
            CC.append((i,"positive"))
    for i in range(len(CC)):
        for j in range(len(CC)):
            if(i != j):
                (a,b) = CC[i]
                (c,d) = CC[j]
                if(unify(a,c) != [-1] and b != d):
                    return True
    for i in P1:
        if(i[0] == "!"):
            P11.append((i[1:],"negative"))
        else:
            P11.append((i,"positive"))
    for i in P2:
        if(i[0] == "!"):
            P22.append((i[1:],"negative"))
        else:
            P22.append((i,"positive"))
    count = 0
    for i in P11:
        for j in CC:
            (a,b) = i
            (c,d) = j
            isCapital = a.find("(") + 1
            isCapital2 = c.find("(") + 1
            if(len(C) >= len(P1) and b == d and unify(a,c) != [-1] and (a[isCapital].isupper() == False or (a[isCapital].isupper() == True and c[isCapital2].isupper() == True))):
                count += 1
                break
    if(count == len(P1)):
        return True

    count = 0
    for i in P22:
        for j in CC:
            (a,b) = i
            (c,d) = j
            isCapital = a.find("(") + 1
            isCapital2 = c.find("(") + 1
            if(len(C) >= len(P2) and b == d and unify(a,c) != [-1] and (a[isCapital].isupper() == False or (a[isCapital].isupper() == True and c[isCapital2].isupper() == True))):
                count += 1
                break
    if(count == len(P2)):
        return True
    return False

def split(str):
    output = []
    stack = ['OK']
    seperators = [-1]
    for i in range(len(str)):
        if(str[i] == "("):
            stack.append("(")
        elif(str[i] == ")"):
            stack.pop()
        if(str[i] == "," and stack[-1] == 'OK'):
            seperators.append(i)
    seperators.append(len(str))
    for i in range(len(seperators) - 1):
        output.append(str[seperators[i]+1:seperators[i+1]])
    return output

def substitue(str, s1, s2):
    l = str.rsplit(s1)
    if(len(l) == 1):
        return str
    else:
        output = l[0]
        for i in range(1,len(l)):
            output += s2
            output += l[i]
    return output

def unify(E1, E2):
    result = []
    if(E1.find('(') == -1 or E2.find('(') == -1):
        if(E1 == E2):
            return []
        if(E1[0].isupper() == False and E1.find('(') == -1):
            if(E2.find(E1) != -1):
                return [-1]
            else:
                return [[E1, E2]]
        elif(E2[0].isupper() == False and E2.find('(') == -1):
            if(E1.find(E2) != -1):
                return [-1]
            else:
                return [[E2, E1]]
        else:
            return [-1]
    start1 = E1.find('(')
    end1 = E1.rfind(')')
    start2 = E2.find('(')
    end2 = E2.rfind(')')
    name1 = E1[:start1]
    name2 = E2[:start2]
    if(name1 != name2):
        return [-1]
    newE1 = E1[start1+1:end1]
    newE2 = E2[start2+1:end2]
    E1list = split(newE1)
    E2list = split(newE2)
    if(len(E1list) != len(E2list)):
        return[-1]
    for i in range(len(E1list)):
        add = unify(E1list[i], E2list[i])
        if(add == [-1]):
            return [-1]
        if(add != []):
            for j in range(len(E1list)):
                E1list[j] = substitue(E1list[j], add[0][0], add[0][1])
                E2list[j] = substitue(E2list[j], add[0][0], add[0][1])
            result = result + add
    return result

def resolvable(C1, C2):
    L1 = []
    L2 = []
    for i in C1:
        if(i[0] == "!"):
            L1.append((i[1:],"negative"))
        else:
            L1.append((i,"positive"))
    for i in C2:
        if(i[0] == "!"):
            L2.append((i[1:],"negative"))
        else:
            L2.append((i,"positive"))

    for i in L1:
        for j in L2:
            (a,b) = i
            (c,d) = j
            if(b != d):
                output = unify(a,c)
                if(output != [-1]):
                    return output
    return [-1]

def resolve(C1, C2):
    L1 = []
    L2 = []
    pos1 = -1
    pos2 = -1
    for i in C1:
        if(i[0] == "!"):
            L1.append((i[1:],"negative"))
        else:
            L1.append((i,"positive"))
    for i in C2:
        if(i[0] == "!"):
            L2.append((i[1:],"negative"))
        else:
            L2.append((i,"positive"))
    breakSignal = False
    for i in range(len(L1)):
        if(breakSignal):
            break
        for j in range(len(L2)):
            (a,b) = L1[i]
            (c,d) = L2[j]
            if(b != d):
                soln = unify(a,c)
                if(soln != [-1]):
                    pos1 = i
                    pos2 = j
                    breakSignal = True
                    break


    output = C1+C2
    output.pop(pos1)
    output.pop(len(C1)+pos2-1)
    for i in range(len(output)):
        for j in soln:
            output[i] = substitue(output[i],j[0],j[1])
    return output

def reparse(parsed):
    first = True
    str = ""
    for j in parsed:
        if(first):
            str = j
            first = False
        else:
            str += "+"
            str += j
    return str

def parse(original):
    output = []
    for i in original:
        sep1 = i.rsplit('+')
        output.append(sep1)
    return output

def theorem_prover(KB, N):
    original = KB + N
    parsed = parse(original)
    popped = []
    proccessed = []
    solution = []
    leng = len(parsed)
    haveResolution = False
    currResolution = ""
    while(True):
        resCopy = currResolution
        chainBroken = False
        if(haveResolution):
            chosenParent = -1
            i = 0
            while(i <= leng):
                if(i == leng):
                    haveResolution = False
                    chainBroken = True
                    break
                isPopped = False
                for j in popped:
                    if(i == j):
                        isPopped = True
                if(isPopped):
                    i += 1
                    continue
                solution = resolvable(resCopy, parsed[i])
                if(solution != [-1]):
                    popped.append(i)
                    chosenParent = i
                    break
                else:
                    i += 1
            if(chainBroken):
                continue
            nextResolution = resolve(resCopy, parsed[chosenParent])
            breakSignal = False
            for i in range(len(nextResolution)):
                if(breakSignal):
                    break
                for j in range(len(nextResolution)):
                    if(i != j and nextResolution[i] == nextResolution[j]):
                        nextResolution.pop(j)
                        breakSignal = True
                        break
            if(nextResolution == []):
                proccessed.append(reparse(currResolution)+"$"+original[chosenParent]+"$"+"empty")
                return ("yes", proccessed)
            if(eliminate(nextResolution, resCopy, parsed[chosenParent])):
                haveResolution = False
            else:
                proccessed.append(reparse(currResolution)+"$"+original[chosenParent]+"$"+reparse(nextResolution))
                currResolution = nextResolution
                haveResolution = True
        else:
            parent1 = -1
            parent2 = -1
            i = 0
            while(i <= leng):
                if(i == leng):
                    return ('no', proccessed)
                isPopped = False
                for k in popped:
                    if(k == i):
                        isPopped = True
                if(isPopped):
                    i += 1
                    continue
                j = i + 1
                isFound = False
                while(j < leng):
                    isPopped2 = False
                    for k in popped:
                        if(k == j):
                            isPopped2 = True
                    if(isPopped2):
                        j += 1
                        continue
                    solution = resolvable(parsed[i], parsed[j])
                    if(solution != [-1]):
                        popped.append(i)
                        popped.append(j)
                        parent1 = i
                        parent2 = j
                        isFound = True
                        break
                    else:
                        j += 1
                if(isFound):
                    break
                else:
                    i += 1
            nextResolution = resolve(parsed[parent1], parsed[parent2])
            breakSignal = False
            for i in range(len(nextResolution)):
                if(breakSignal):
                    break
                for j in range(len(nextResolution)):
                    if(i != j and nextResolution[i] == nextResolution[j]):
                        nextResolution.pop(j)
                        breakSignal = True
                        break
            if(nextResolution == []):
                proccessed.append(original[parent1]+"$"+original[parent2]+"$"+"empty")
                return ("yes", proccessed)
            if(eliminate(nextResolution, parsed[parent1], parsed[parent2])):
                haveResolution = False
            else:
                proccessed.append(original[parent1]+"$"+original[parent2]+"$"+reparse(nextResolution))
                currResolution = nextResolution
                haveResolution = True


print(theorem_prover(["p(A,f(t))", "q(z)+!p(z,f(B))", "!q(y)+r(y)"],["!r(A)"]))
