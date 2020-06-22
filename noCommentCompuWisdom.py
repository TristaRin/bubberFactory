def getMaxSpan(gantt) :
    maxSpan = 0
    for g in gantt :
        if g[-1] > maxSpan :
            maxSpan = g[-1]
    return maxSpan

def calcuScrapA(ganttA, jobBufA, macOrdA, tableA, typeOfRubberWaste) :
    maxSpan = getMaxSpan(ganttA)

    scrapA = dict()
    for rw in typeOfRubberWaste :
        scrapA[rw] = [0 for i in range(maxSpan+1)]
    
    for mIndex in range(len(ganttA)) :
        aSchedule = ganttA[mIndex]
        for endIndex in range(1, len(aSchedule), 2) :
            end = aSchedule[endIndex]
            job = jobBufA[int(endIndex/2)]
            m = macOrdA[mIndex]
            for rw in typeOfRubberWaste :
                scrapA[rw][end] += tableA[job][m]['rubberWaste'][rw] 
    
    for rw in typeOfRubberWaste :
        scrapA[rw][0] += 0
        for time in range(1, maxSpan+1) :
            scrapA[rw][time] += scrapA[rw][time-1]

    return scrapA    

def findEnoughTime(start, resource, typeOfResource, require) :

    for i in range(start, len(resource[typeOfResource[0]])) :
        isEnough = True

        for r in typeOfResource :
            if resource[r][i] < require[r] :
                isEnough = False
                break

        if isEnough == True :
            return i
    return -1

def updateResource(enoughTime, resource, typeOfResource, table, job, m) :
    for i in range(enoughTime, len(resource[typeOfResource[0]])) :
        for r in typeOfResource :
            resource[r][i] -= table[job][m]['require'][r]
    return resource

def getGantt(jobBuf, macOrd, table, typeOfResource, resource) :
    gantt = list()
    
    for j in range(0, len(jobBuf)) :
        for i in range(0, len(macOrd)) :
            job = jobBuf[j]
            m = macOrd[i]
            pt = table[job][m]['pt']
            require = table[job][m]['require']

            if j == 0 and i == 0 :
                start = 0

                enoughTime = findEnoughTime(start, resource, typeOfResource, require)
                if enoughTime == -1 :
                    return gantt, False
                gantt.append([enoughTime, enoughTime + pt])

            elif j == 0 :
                start = gantt[i-1][2*i-1]

                enoughTime = findEnoughTime(start, resource, typeOfResource, require)
                if enoughTime == -1 :
                    return gantt, False
                gantt.append([enoughTime, enoughTime + pt])

            elif i == 0 :
                start = gantt[0][2*j-1]
                
                enoughTime = findEnoughTime(start, resource, typeOfResource, require)
                if enoughTime == -1 :
                    return gantt, False
                gantt[0] += [enoughTime, enoughTime + pt]
            else :
                start = max(gantt[i-1][-1], gantt[i][2*j-1])

                enoughTime = findEnoughTime(start, resource, typeOfResource, require)
                if enoughTime == -1 :
                    return gantt, False
                gantt[i] += [enoughTime, enoughTime + pt]


            lenDrop = enoughTime + pt + 1 - len(resource[typeOfResource[0]])
            if lenDrop != 0 :
                for r in typeOfResource :
                    resource[r] += [resource[r][-1] for i in range(lenDrop)]
            resource = updateResource(enoughTime, resource, typeOfResource, table, job, m)

    return gantt, True

def getGanttA(jobBufA, macOrdA, tableA) :
    ganttA = list()
    for j in range(0, len(jobBufA)) :
        for i in range(0, len(macOrdA)) :
            job = jobBufA[j]
            m = macOrdA[i]
            pt = tableA[job][m]['pt']

            if j == 0 and i == 0 :
                start = 0
                ganttA.append([start, start + pt])
            elif j == 0 :
                start = ganttA[i-1][2*i-1]
                ganttA.append([start, start + pt])

            elif i == 0 :
                start = ganttA[0][2*j-1]
                ganttA[0] += [start, start + pt]
            else :
                start = max(ganttA[i-1][2*i-1], ganttA[i][2*j-1])
                ganttA[i] += [start, start + pt]

    return ganttA
    
def inputString(jobString) :
    inputJobOrd = list(map(int, jobString.split()))
    return useAPI(inputJobOrd)
def inputList(inputJobOrd) :
    return useAPI(inputJobOrd)

def useAPI(inputJobOrd) :
    jobBufA, jobBufB = list(), list()
    for x in inputJobOrd :
        job = 'j' + str(x%3+1)
        if x <= 2 :
            jobBufA.append(job)
        else :
            jobBufB.append(job)
    macOrdA = ['M1', 'M2']
    macOrdB = ['m1', 'm2']
    typeOfRubberWaste = ['type1', 'type2']


    tableA = {'j1': {'M1': {'pt': 4, 'rubberWaste': {'type1': 3, 'type2': 1}}, 'M2': {'pt': 5, 'rubberWaste': {'type1': 3, 'type2': 2}}},
              'j2': {'M1': {'pt': 5, 'rubberWaste': {'type1': 1, 'type2': 3}}, 'M2': {'pt': 2, 'rubberWaste': {'type1': 2, 'type2': 2}}},
              'j3': {'M1': {'pt': 3, 'rubberWaste': {'type1': 2, 'type2': 2}}, 'M2': {'pt': 6, 'rubberWaste': {'type1': 1, 'type2': 1}}}
              }
 
    tableB = {'j1': {'m1': {'pt': 2, 'require': {'type1': 0, 'type2': 1}}, 'm2': {'pt': 1, 'require': {'type1': 1, 'type2': 0}}},
              'j2': {'m1': {'pt': 3, 'require': {'type1': 2, 'type2': 2}}, 'm2': {'pt': 2, 'require': {'type1': 1, 'type2': 1}}},
              'j3': {'m1': {'pt': 4, 'require': {'type1': 7, 'type2': 1}}, 'm2': {'pt': 4, 'require': {'type1': 1, 'type2': 5}}}
              }

    ganttA = getGanttA(jobBufA, macOrdA, tableA)
    scrapA = calcuScrapA(ganttA, jobBufA, macOrdA, tableA, typeOfRubberWaste)
    ganttB, isEnough = getGantt(jobBufB, macOrdB, tableB, typeOfRubberWaste, scrapA)
    
    if isEnough == False :
        return -1

    result = max(getMaxSpan(ganttA), getMaxSpan(ganttB))
    return result



