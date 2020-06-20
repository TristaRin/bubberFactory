# 計算工作結束時產生的廢料
def calcuScrapA(ganttA) :
    for i in range(1, len(ganttA[0]), 2) :
        # 結束時間
        print(ganttA[1][i])
# 取得甘特圖
def getGanttA(jobBufA, macOrdA, tableA) :
    ganttA = list()
    # 初始化甘特圖第一台機器的第一個工作
    j1 = jobBufA[0]
    m1 = macOrdA[0]
    # 開始時間是零
    start = 0
    pt = tableA[j1][m1][0]
    ganttA.append([start, start + pt])
    
    # 初始化甘特圖第一台機器的剩下工作
    for j in range(1, len(jobBufA)) :
        job = jobBufA[j]
        # 開始時間要看這台機器前一個工作的結束時間
        start = ganttA[0][2*j-1]
        pt = tableA[job][m1][0]
        ganttA[0] += [start, start + pt]
    
    # 初始化甘特圖剩下機器的第一個工作
    for i in range(1, len(macOrdA)) :
        m = macOrdA[i]
        # 開始時間要看上一台機器的結束時間
        start = ganttA[i-1][2*i-1]
        pt = tableA[j1][m][0]
        ganttA.append([start, start + pt])
    
    # 填完剩下工作
    for i in range(1, len(macOrdA)) :
        for j in range(1, len(jobBufA)) :
            # 開始時間要看上一台機器的結束時間及這台機器前一個工作的結束時間
            start = max(ganttA[i-1][2*i-1], ganttA[i][2*j-1])
            job = jobBufA[j]
            m = macOrdA[i]
            pt = tableA[job][m][0]
            ganttA[i] += [start, start + pt]
    return ganttA

def main():
    tableA = {'J1': {'M1': [4, 3, 1], 'M2': [5, 3, 2]},
              'J2': {'M1': [5, 1, 3], 'M2': [2, 2, 2]},
              'J3': {'M1': [3, 2, 2], 'M2': [6, 1, 1]}}

    # tableB = {'j1': {'m1': [2, 0, 1], 'm2': [1, 1, 0]},
    #           'j2': {'m1': [3, 2, 2], 'm2': [2, 1, 1]},
    #           'j3': {'m1': [4, 7, 1], 'm2': [4, 1, 5]}}
    
    # 有幾台機器和幾個工作
    # mNum = 2
    # jobNum = 3

    # 生產線的代完成工作順序
    jobBufA = ['J1', 'J3', 'J2']
    # jobBufB = ['j1', 'j2', 'j3']

    # 生產工作必經的機器順序
    macOrdA = ['M1', 'M2']
    # macOrdB = ['m1', 'm2']

    # 甘特圖資料, 產生的廢料
    ganttA = getGanttA(jobBufA, macOrdA, tableA)
    print(ganttA)

    scrapA = calcuScrapA(ganttA)




main()