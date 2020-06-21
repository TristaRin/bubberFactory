    

# 找出甘特圖的最長時間
def getMaxSpan(gantt) :
    maxSpan = 0
    for g in gantt :
        if g[-1] > maxSpan :
            maxSpan = g[-1]
    return maxSpan

# 計算工作結束時產生的廢料
def calcuScrapA(ganttA, jobBufA, macOrdA, tableA, typeOfRubberWaste) :
    maxSpan = getMaxSpan(ganttA)

    # 初始化此生產線每種廢料在每個時間的數量
    scrapA = dict()
    for rw in typeOfRubberWaste :
        # 初始化每種廢料數量, maxSpan要加1才能表示從零開始的每期
        scrapA[rw] = [0 for i in range(maxSpan+1)]
    
    # 根據甘特圖結束時間，將每項工作在何時產生廢料記錄下來
    for mIndex in range(len(ganttA)) :
        # 此台機器的時程
        aSchedule = ganttA[mIndex]
        for endIndex in range(1, len(aSchedule), 2) :
            # 此台機器上的結束時間點
            end = aSchedule[endIndex]
            # 這是哪個工作結束了
            job = jobBufA[int(endIndex/2)]
            # 這是哪台機器
            m = macOrdA[mIndex]
            for rw in typeOfRubberWaste :
                # 廢料數量 += 新產生的 
                scrapA[rw][end] += tableA[job][m]['rubberWaste'][rw] 
    
    # 廢料數量 += 之前留下來的 （未減用掉的）
    for rw in typeOfRubberWaste :
        # 假設第零期沒有前期留下來的
        scrapA[rw][0] += 0
        for time in range(1, maxSpan+1) :
            scrapA[rw][time] += scrapA[rw][time-1]

    return scrapA    

def findEnoughTime(start, resource, typeOfResource, require) :

    # 找哪個時段的廢料是夠的
    for i in range(start, len(resource['條'])) :
        isEnough = True

        # print('原料', '需求')
        # 檢查此時間的每種原料數量
        for r in typeOfResource :
            # print(resource[r][i] , require[r])
            # 只要其中一個原料不夠，這時間就不能做
            if resource[r][i] < require[r] :
                # print('不夠')
                isEnough = False
                break

        # 若此時間的原料足夠，則可替第一台機器安排第一項工作
        if isEnough == True :
            # print('yes', i)
            # 回傳此時間
            return i
        # print('----')
    # 永遠沒有足夠的時候
    return -1

def updateResource(enoughTime, resource, typeOfResource, table, job, m) :
    # print('enoughTime', enoughTime, resource['條'])
    for i in range(enoughTime, len(resource['條'])) :
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
            # 工作所需的原料
            require = table[job][m]['require']

            # 若是第一台機器的第一個工作
            if j == 0 and i == 0 :
                # 開始時間為零
                start = 0

                # 從開始時間找原料足夠的時候
                enoughTime = findEnoughTime(start, resource, typeOfResource, require)
                # 永遠不夠別排了
                if enoughTime == -1 :
                    print('永遠不夠別排了1')
                    return gantt
                
                gantt.append([enoughTime, enoughTime + pt])

            # 若是屬於第一個工作
            elif j == 0 :
                # 開始時間要看上一台機器的結束時間
                start = gantt[i-1][2*i-1]

                # 從開始時間找原料足夠的時候
                enoughTime = findEnoughTime(start, resource, typeOfResource, require)
                # 永遠不夠別排了
                if enoughTime == -1 :
                    print('永遠不夠別排了2')
                    return gantt
                
                gantt.append([enoughTime, enoughTime + pt])

            # 若是第一台機器的工作
            elif i == 0 :
                # 開始時間要看這台機器前一個工作的結束時間
                start = gantt[0][2*j-1]
                
                # 從開始時間找原料足夠的時候
                enoughTime = findEnoughTime(start, resource, typeOfResource, require)
                # 永遠不夠別排了
                if enoughTime == -1 :
                    print('永遠不夠別排了3')
                    return gantt

                gantt[0] += [enoughTime, enoughTime + pt]
            # 剩下的工作
            else :
                # 開始時間要看上一台機器的結束時間及這台機器前一個工作的結束時間
                start = max(gantt[i-1][-1], gantt[i][2*j-1])

                # 從開始時間找原料足夠的時候
                enoughTime = findEnoughTime(start, resource, typeOfResource, require)
                # 永遠不夠別排了
                if enoughTime == -1 :
                    print('永遠不夠別排了4')
                    return gantt

                gantt[i] += [enoughTime, enoughTime + pt]

            # print(job, m, '開始', enoughTime, '結束', enoughTime+pt)
            # print('更新前')            
            # print(resource['條'])
            # print(resource['粉'])
            # 若resource紀錄的時間長度不夠用,要補齊
            lenDrop = enoughTime + pt + 1 - len(resource['條'])
            if lenDrop != 0 :
                for r in typeOfResource :
                    resource[r] += [resource[r][-1] for i in range(lenDrop)]
            # 更新原料狀況
            resource = updateResource(enoughTime, resource, typeOfResource, table, job, m)
            # print('更新後')            
            # print(resource['條'])
            # print(resource['粉'])
            # print('-----------------------')
    return gantt

# 取得甘特圖
def getGanttA(jobBufA, macOrdA, tableA) :
    ganttA = list()

    for j in range(0, len(jobBufA)) :
        for i in range(0, len(macOrdA)) :
            job = jobBufA[j]
            m = macOrdA[i]
            pt = tableA[job][m]['pt']

            # 若是第一台機器的第一個工作
            if j == 0 and i == 0 :
                # 開始時間為零
                start = 0
                ganttA.append([start, start + pt])
            # 若是屬於第一個工作
            elif j == 0 :
                # 開始時間要看上一台機器的結束時間
                start = ganttA[i-1][2*i-1]
                ganttA.append([start, start + pt])

            # 若是第一台機器的工作
            elif i == 0 :
                # 開始時間要看這台機器前一個工作的結束時間
                start = ganttA[0][2*j-1]
                ganttA[0] += [start, start + pt]
            # 剩下的工作
            else :
                # 開始時間要看上一台機器的結束時間及這台機器前一個工作的結束時間
                start = max(ganttA[i-1][2*i-1], ganttA[i][2*j-1])
                ganttA[i] += [start, start + pt]

    return ganttA

def main():
    # tableA = {'J1': {'M1': [4, 3, 1], 'M2': [5, 3, 2]},
    #           'J2': {'M1': [5, 1, 3], 'M2': [2, 2, 2]},
    #           'J3': {'M1': [3, 2, 2], 'M2': [6, 1, 1]}
    #           }

    tableA = {'J1': {'M1': {'pt': 4, 'rubberWaste': {'條': 3, '粉': 1}}, 'M2': {'pt': 5, 'rubberWaste': {'條': 3, '粉': 2}}},
              'J2': {'M1': {'pt': 5, 'rubberWaste': {'條': 1, '粉': 3}}, 'M2': {'pt': 2, 'rubberWaste': {'條': 2, '粉': 2}}},
              'J3': {'M1': {'pt': 3, 'rubberWaste': {'條': 2, '粉': 2}}, 'M2': {'pt': 6, 'rubberWaste': {'條': 1, '粉': 1}}}
              }

    # tableB = {'j1': {'m1': [2, 0, 1], 'm2': [1, 1, 0]},
    #           'j2': {'m1': [3, 2, 2], 'm2': [2, 1, 1]},
    #           'j3': {'m1': [4, 7, 1], 'm2': [4, 1, 5]}}
    
    tableB = {'j1': {'m1': {'pt': 2, 'require': {'條': 0, '粉': 1}}, 'm2': {'pt': 1, 'require': {'條': 1, '粉': 0}}},
              'j2': {'m1': {'pt': 3, 'require': {'條': 2, '粉': 2}}, 'm2': {'pt': 2, 'require': {'條': 1, '粉': 1}}},
              'j3': {'m1': {'pt': 4, 'require': {'條': 7, '粉': 1}}, 'm2': {'pt': 4, 'require': {'條': 1, '粉': 5}}}
              }

    # 有幾個工作和幾台機器和幾種廢料
    # mNum = 2
    # jobNum = 3
    # rubburWasteNum = 2

    # 生產線的代完成工作順序
    jobBufA = ['J1', 'J3', 'J2']
    jobBufB = ['j3', 'j2', 'j1']

    # 生產工作必經的機器順序
    macOrdA = ['M1', 'M2']
    macOrdB = ['m1', 'm2']

    # 廢料種類
    typeOfRubberWaste = ['條', '粉']


    # 生產線A的甘特圖
    ganttA = getGanttA(jobBufA, macOrdA, tableA)
    # print(ganttA)

    # 生產線A產生的廢料
    scrapA = calcuScrapA(ganttA, jobBufA, macOrdA, tableA, typeOfRubberWaste)
    # print(scrapA['條'])
    # print(scrapA['粉'])

    ganttB = getGantt(jobBufB, macOrdB, tableB, typeOfRubberWaste, scrapA)
    print(ganttB)

main()