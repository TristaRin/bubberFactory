# 找出甘特圖的最長時間
def getMaxSpan(gantt) :
    maxSpan = 0
    for g in gantt :
        if g[-1] > maxSpan :
            maxSpan = g[-1]
    return maxSpan

# 計算生產線a產生的廢料
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

    # 將廢料情況回傳
    return scrapA    

# 給生產線b的計算用，用來找（此工作）如此的需求何時能被滿足
def findEnoughTime(start, resource, typeOfResource, require) :

    # 找哪個時段的廢料是夠的
    for i in range(start, len(resource[typeOfResource[0]])) :
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
            # print('this time is enough', i)
            # 回傳此時間
            return i
        # print('----')
    # 永遠沒有足夠的時候
    return -1

# 給生產線b的計算用，用來更新原料狀況
def updateResource(enoughTime, resource, typeOfResource, table, job, m) :
    # row 是時間
    for i in range(enoughTime, len(resource[typeOfResource[0]])) :
        # column 是原料種類
        for r in typeOfResource :
            resource[r][i] -= table[job][m]['require'][r]
    return resource

# 取得甘特圖，此函數給a以外的生產線（有考慮原料是否充足）用
def getGantt(jobBuf, macOrd, table, typeOfResource, resource) :
    gantt = list()
    
    # 每個 job
    for j in range(0, len(jobBuf)) :
        # 每台 machine
        for i in range(0, len(macOrd)) :
            # 當前是哪個 job 要在那台 machine 上工作多久時間（pt）
            job = jobBuf[j]
            m = macOrd[i]
            pt = table[job][m]['pt']
            # 工作所需的原料量
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
                # 將工作排入甘特圖
                gantt.append([enoughTime, enoughTime + pt])

            # 若是其他台機器的第一個工作
            elif j == 0 :
                # 開始時間要看上一台機器的結束時間
                start = gantt[i-1][2*i-1]

                # 從開始時間找原料足夠的時候
                enoughTime = findEnoughTime(start, resource, typeOfResource, require)
                # 永遠不夠別排了
                if enoughTime == -1 :
                    print('永遠不夠別排了2')
                    return gantt
                # 將工作排入甘特圖
                gantt.append([enoughTime, enoughTime + pt])

            # 若是第一台機器的其他工作
            elif i == 0 :
                # 開始時間要看這台機器前一個工作的結束時間
                start = gantt[0][2*j-1]
                
                # 從開始時間找原料足夠的時候
                enoughTime = findEnoughTime(start, resource, typeOfResource, require)
                # 永遠不夠別排了
                if enoughTime == -1 :
                    print('永遠不夠別排了3')
                    return gantt
                # 將工作排入甘特圖
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
                # 將工作排入甘特圖
                gantt[i] += [enoughTime, enoughTime + pt]

            # print(job, m, '開始', enoughTime, '結束', enoughTime+pt)
            # print('更新前')            
            # print(resource[typeOfResource[0]])
            # print(resource[typeOfResource[1]])

            # 若resource紀錄的時間長度不夠用,要補齊再去更新
            lenDrop = enoughTime + pt + 1 - len(resource[typeOfResource[0]])
            if lenDrop != 0 :
                for r in typeOfResource :
                    resource[r] += [resource[r][-1] for i in range(lenDrop)]
            # 更新原料狀況
            resource = updateResource(enoughTime, resource, typeOfResource, table, job, m)
            
            # print('更新後')            
            # print(resource[typeOfResource[0]])
            # print(resource[typeOfResource[1]])
            # print('-----------------------')
    # 將甘特圖結果回傳
    return gantt

# 取得甘特圖，此函數只給生產線a（不考慮原料是否充足）用
def getGanttA(jobBufA, macOrdA, tableA) :
    ganttA = list()
    # 每個 job
    for j in range(0, len(jobBufA)) :
        # 每台 machine
        for i in range(0, len(macOrdA)) :
            # 當前是哪個 job 要在那台 machine 上工作多久時間（pt）
            job = jobBufA[j]
            m = macOrdA[i]
            pt = tableA[job][m]['pt']

            # 若是第一台機器的第一個工作
            if j == 0 and i == 0 :
                # 開始時間為零
                start = 0
                # 將工作排入甘特圖
                ganttA.append([start, start + pt])
            # 若是屬於第一個工作
            elif j == 0 :
                # 開始時間要看上一台機器的結束時間
                start = ganttA[i-1][2*i-1]
                # 將工作排入甘特圖
                ganttA.append([start, start + pt])

            # 若是第一台機器的工作
            elif i == 0 :
                # 開始時間要看這台機器前一個工作的結束時間
                start = ganttA[0][2*j-1]
                # 將工作排入甘特圖
                ganttA[0] += [start, start + pt]
            # 剩下的工作
            else :
                # 開始時間要看上一台機器的結束時間及這台機器前一個工作的結束時間
                start = max(ganttA[i-1][2*i-1], ganttA[i][2*j-1])
                # 將工作排入甘特圖
                ganttA[i] += [start, start + pt]

    # 將甘特圖結果回傳
    return ganttA
def useAPI(inputJobOrd) :
    # inputJobOrd = list(map(int, input().split()))
    jobBufA, jobBufB = list(), list()
    for x in inputJobOrd :
        job = 'j' + str(x%3+1)
        if x <= 2 :
            jobBufA.append(job)
        else :
            jobBufB.append(job)
    # 生產工作必經的機器順序
    macOrdA = ['M1', 'M2']
    macOrdB = ['m1', 'm2']
    # # 廢料種類
    typeOfRubberWaste = ['type1', 'type2']


    tableA = {'j1': {'M1': {'pt': 4, 'rubberWaste': {'type1': 3, 'type2': 1}}, 'M2': {'pt': 5, 'rubberWaste': {'type1': 3, 'type2': 2}}},
              'j2': {'M1': {'pt': 5, 'rubberWaste': {'type1': 1, 'type2': 3}}, 'M2': {'pt': 2, 'rubberWaste': {'type1': 2, 'type2': 2}}},
              'j3': {'M1': {'pt': 3, 'rubberWaste': {'type1': 2, 'type2': 2}}, 'M2': {'pt': 6, 'rubberWaste': {'type1': 1, 'type2': 1}}}
              }
 
    tableB = {'j1': {'m1': {'pt': 2, 'require': {'type1': 0, 'type2': 1}}, 'm2': {'pt': 1, 'require': {'type1': 1, 'type2': 0}}},
              'j2': {'m1': {'pt': 3, 'require': {'type1': 2, 'type2': 2}}, 'm2': {'pt': 2, 'require': {'type1': 1, 'type2': 1}}},
              'j3': {'m1': {'pt': 4, 'require': {'type1': 7, 'type2': 1}}, 'm2': {'pt': 4, 'require': {'type1': 1, 'type2': 5}}}
              }

    # 生產線A的甘特圖
    ganttA = getGanttA(jobBufA, macOrdA, tableA)
    # print(ganttA)

    # 生產線A產生的廢料
    scrapA = calcuScrapA(ganttA, jobBufA, macOrdA, tableA, typeOfRubberWaste)
    # print(scrapA[typeOfResource[0]])
    # print(scrapA[typeOfResource[1]])

    ganttB = getGantt(jobBufB, macOrdB, tableB, typeOfRubberWaste, scrapA)
    # print(ganttB)
    result = max(getMaxSpan(ganttA), getMaxSpan(ganttB))
    return result

def main():
    # # lineNum = 2
    # # jobNum = 3
    # # mNum = 2
    # # rubburWasteNum = 2
    
    # # print('請輸入生產線個數')
    # # print('請輸入工作個數')
    # # print('請輸入機器個數')
    # # print('請輸入廢料種類個數')

    # # 生產線個數
    # lineNum = int(input())
    # # 工作個數
    # jobNum = int(input())
    # # 機器個數
    # mNum = int(input())
    # # 廢料種類個數
    # rubburWasteNum = int(input())

    # # 細節對照表，每條生產線的某工作在某機器的處理時間及廢料或原料資訊等等
    # table = list()

    # # 初始化細節對照表
    # for l in range(lineNum) :
    #     table.append(dict())
    #     table[l] = dict()

    #     for j in range(jobNum) :
    #         job = 'j' + str(j+1)
    #         table[l][job] = dict()

    #         for i in range(mNum) :
    #             m = 'm' + str(i+1)
    #             table[l][job][m] = dict()
    #             # 輸入處理時間
    #             # print('請輸入', l, '生產線上:', job, '在', m, '上的處理時間')
    #             table[l][job][m]['pt'] = int(input())
    #             table[l][job][m]['rubberWaste'] = dict()
    #             table[l][job][m]['require'] = dict()

    #             for r in range(rubburWasteNum) :
    #                 rw = 'type' + str(r+1)
    #                 if l == 0 :
    #                     # 輸入此種廢料數量
    #                     # print('請輸入廢料')
    #                     table[l][job][m]['rubberWaste'][rw] = int(input())
    #                 else :
    #                     # 輸入此種原料數量
    #                     # print('請輸入原料需求')
    #                     table[l][job][m]['require'][rw] = int(input())
                
    #             # print('生產線', l, '工作', job, '機器', m)
    #             # print(table[l][job][m])

    # 機器流程表（每條生產線的）
    # 廢料種類名稱表
    # 待辦工作順序（每條生產線的）
    # jobBuf = list()
    # macOrd = list()
    # for l in range(lineNum) :

    #     # print('請輸入生產線', l, '的工作順序')
    #     jobBuf.append(input().split())
    #     # print('請輸入生產線', l, '的機器順序')
    #     macOrd.append(input().split())

    # # print('請輸入廢料名稱')
    # typeOfRubberWaste = input().split()


    # # 生產線的代完成工作順序
    # # jobBufA = ['J1', 'J3', 'J2']
    # # jobBufB = ['j3', 'j2', 'j1']

    # macOrdA = macOrd[0]
    # macOrdB = macOrd[1]
    # tableA = table[0]
    # tableB = table[1]
    # //////////////////////////////////////////////////////////////////////////
    # jobBufA, jobBufB = list(), list()
    # inputJobOrd = list(map(int, input().split()))
    # for x in inputJobOrd :
    #     job = 'j' + str(x%3+1)
    #     if x <= 2 :
    #         jobBufA.append(job)
    #     else :
    #         jobBufB.append(job)

    # # 生產工作必經的機器順序
    # macOrdA = ['M1', 'M2']
    # macOrdB = ['m1', 'm2']
    # # # 廢料種類
    # typeOfRubberWaste = ['type1', 'type2']


    # tableA = {'j1': {'M1': {'pt': 4, 'rubberWaste': {'type1': 3, 'type2': 1}}, 'M2': {'pt': 5, 'rubberWaste': {'type1': 3, 'type2': 2}}},
    #           'j2': {'M1': {'pt': 5, 'rubberWaste': {'type1': 1, 'type2': 3}}, 'M2': {'pt': 2, 'rubberWaste': {'type1': 2, 'type2': 2}}},
    #           'j3': {'M1': {'pt': 3, 'rubberWaste': {'type1': 2, 'type2': 2}}, 'M2': {'pt': 6, 'rubberWaste': {'type1': 1, 'type2': 1}}}
    #           }
 
    # tableB = {'j1': {'m1': {'pt': 2, 'require': {'type1': 0, 'type2': 1}}, 'm2': {'pt': 1, 'require': {'type1': 1, 'type2': 0}}},
    #           'j2': {'m1': {'pt': 3, 'require': {'type1': 2, 'type2': 2}}, 'm2': {'pt': 2, 'require': {'type1': 1, 'type2': 1}}},
    #           'j3': {'m1': {'pt': 4, 'require': {'type1': 7, 'type2': 1}}, 'm2': {'pt': 4, 'require': {'type1': 1, 'type2': 5}}}
    #           }

    # # 生產線A的甘特圖
    # ganttA = getGanttA(jobBufA, macOrdA, tableA)
    # print(ganttA)

    # # 生產線A產生的廢料
    # scrapA = calcuScrapA(ganttA, jobBufA, macOrdA, tableA, typeOfRubberWaste)
    # # print(scrapA[typeOfResource[0]])
    # # print(scrapA[typeOfResource[1]])

    # ganttB = getGantt(jobBufB, macOrdB, tableB, typeOfRubberWaste, scrapA)
    # print(ganttB)
    print(useAPI([0, 2, 1, 5, 4, 3]))

main()
# 輸入測資
# 2
# 3
# 2
# 2
# 4
# 3
# 1
# 5
# 3
# 2
# 5
# 1
# 3
# 2
# 2
# 2
# 3
# 2
# 2
# 6
# 1
# 1
# 2
# 0
# 1
# 1
# 1
# 0
# 3
# 2
# 2
# 2
# 1
# 1
# 4
# 7
# 1
# 4
# 1
# 5
# 輸出範例
# [[0, 4, 4, 7, 7, 12], [4, 9, 9, 15, 15, 17]]
# [[9, 13, 15, 18, 18, 20], [13, 17, 18, 20, 20, 21]]


    # for l in range(lineNum) :
    #     for j in range(jobNum) :
    #         job = jobBuf[0][j]
    #         # print(table[l][job])
    #         for i in range(mNum) :
    #             m = macOrd[l][i]
    #             # print(table[l][job][m])
    #             # print(table[l][job][m]['pt'])
    #             for r in range(rubburWasteNum) :
    #                 rw = typeOfRubberWaste[r]
    #                 # print(table[l][job][m]['rubberWaste'][rw])
    #                 # print(table[l][job][m]['require'][rw])


    # # 初始化對照表們
    # for l in range(lineNum) :
    #     jobBuf.append(list())
    #     macOrd.append(list())
    #     table.append(dict())
    #     # 初始化工作名稱表
    #     for j in range(jobNum) :
    #         jobBuf[l].append('j' + str(j+1))
    #     #  初始化機器名稱表
    #     for i in range(mNum) :
    #         macOrd[l].append('m' + str(i+1))
    # # 初始化廢料種類名稱表
    # for r in range(rubburWasteNum) :
    #     typeOfRubberWaste.append('type' + str(r+1))




    # # 初始化細節對照表
    # for l in range(lineNum) :

    #     table[l] = dict()
    #     for j in range(jobNum) :
    #         job = jobBuf[l][j]

    #         table[l][job] = dict()
    #         for i in range(mNum) :
    #             m = macOrd[l][i]
    #             table[l][job][m] = dict()
    #             # 輸入處理時間
    #             print('請輸入', l, '生產線上:', job, '在', m, '上的處理時間')
    #             table[l][job][m]['pt'] = int(input())

    #             table[l][job][m]['rubberWaste'] = dict()
    #             table[l][job][m]['require'] = dict()
    #             for r in range(rubburWasteNum) :
    #                 rw = typeOfRubberWaste[r]
    #                 if l == 0 :
    #                     # 輸入此種廢料數量
    #                     print('請輸入廢料')
    #                     table[l][job][m]['rubberWaste'][rw] = int(input())
    #                 else :
    #                     # 輸入此種原料數量
    #                     print('請輸入原料需求')
    #                     table[l][job][m]['require'][rw] = int(input())
                
    #             # print('生產線', l, '工作', job, '機器', m)
    #             # print(table[l][job][m])


