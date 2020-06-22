import sys

def printGantt(ganttname, gantt, Cmax):
    print(ganttname, gantt)
    print(Cmax)

def nextLine(BTable, BjobOrder, BmachineOrder, ATable, endtime):

    ganttB = dict()
    currentime = min(endtime) - 1
    reource = [0, 0] # 剩餘膠條、膠粉

    # 按BjobOrder依序放入
    for k in range(len(BjobOrder)):
        # 按machine'順序
        for mm in BmachineOrder:
            if mm not in ganttB:
                ganttB[mm] = dict()
            # 若job還未啟動
            if BjobOrder[k] not in ganttB[mm]:
                ganttB[mm][ BjobOrder[k] ] = [0, 0]
            
            # print(currentime)
            # print("resourse:", reource)
            # print("need: ", BTable[ BjobOrder[k] ][mm])
            
            # 當累積材料 < 現job所需材料，則不執行job
            while reource[0] < BTable[ BjobOrder[k] ][mm][1] or reource[1] < BTable[ BjobOrder[k] ][mm][2]:
                # currentime加一
                currentime +=1
                if currentime > max(endtime):
                    break
                # 若currentime 在 endtime
                if currentime in endtime:
                    # 累積當前剩餘材料
                    reource = [ reource[0] + endtime[currentime][0], reource[1] + endtime[currentime][1] ]
            # 若 LineA 已無產生廢料且當前累積材料 < 現所需材料
            if currentime > max(endtime) and (reource[0] < BTable[ BjobOrder[k] ][mm][1] or reource[1] < BTable[ BjobOrder[k] ][mm][2]):
                printGantt("LineB gantt:\n", ganttB)
                print("剩餘材料已不夠繼續")
                # 結束所有工作
                sys.exit(0)
          
            # print(currentime)
            # print("resourse:", reource)
            # print("need: ", BTable[ BjobOrder[k] ][mm])

            # 累積材料 >= 現job所需材料可以做
            pp = BTable[ BjobOrder[k] ][mm][0] # pp: job'處理時間
            # 若為machine 1
            if mm == 'm1':
                ganttB[mm][ BjobOrder[k] ] = [currentime, currentime + pp]
            # 其他machine
            else:
                # 若還未開始
                if ganttB[mm][ BjobOrder[0] ][1] == 0:
                    if ganttB[premachine2][ BjobOrder[0] ][1] > currentime:
                        while ganttB[premachine2][ BjobOrder[0] ][1] != currentime:
                            currentime +=1
                            # 若currentime增加後不在endtime中
                            if currentime in endtime:
                                # 累積當前剩餘材料
                                reource = [ reource[0] + endtime[currentime][0], reource[1] + endtime[currentime][1] ]
                        # 加入ganttB
                        ganttB[mm][ BjobOrder[k] ] = [ currentime, currentime + pp ]
                else:
                    # 若前一machine最後job的endtime > currentime
                    if ganttB[premachine2][ BjobOrder[k] ][1] > currentime:
                        # 直到若前一machine最後job的endtime = currentime
                        while ganttB[premachine2][ BjobOrder[k] ][1] != currentime:
                            currentime +=1
                            # 若currentime增加後在endtime中
                            if currentime in endtime:
                                # 累積當前剩餘材料
                                reource = [ reource[0] + endtime[currentime][0], reource[1] + endtime[currentime][1] ]
                        # 加入ganttB
                        ganttB[mm][ BjobOrder[k] ] = [ ganttB[premachine2][ BjobOrder[k] ][1], ganttB[premachine2][ BjobOrder[k] ][1] + pp ]
                    # else
                    else:
                        # startime = currentime
                        ganttB[mm][ BjobOrder[k] ] = [ currentime, currentime + pp ]
            # 扣除使用材料
            reource = [ reource[0] - BTable[ BjobOrder[k] ][mm][1], reource[1] - BTable[ BjobOrder[k] ][mm][2] ]
            # 記錄前一台machine
            premachine2 = mm

    CBmax = ganttB[ max(ganttB) ][ BjobOrder[-1] ][1]
    printGantt("LineB gantt:\n", ganttB, CBmax)
    
def mainLine(ATable, AjobOrder, AmachineOrder):

    ganttA = dict()
    endtime = dict()

    # 按machine順序
    for m in AmachineOrder:
        ganttA[m] = dict()
        # 按AjobOrder依序放入
        for j in range(len(AjobOrder)):
            ganttA[m][ AjobOrder[j] ] = [0, 0]
            p = ATable[ AjobOrder[j] ][m][0] # p: job處理時間
            # 若為machine 1
            if m == 'M1':
                # 若還未開始則start=0
                if ganttA[m][ AjobOrder[0] ][1] == 0:
                    ganttA[m][ AjobOrder[0] ] = [0, p]
                else:
                    # 接續此machine前一job的endtime
                    ganttA[m][ AjobOrder[j] ] = [ ganttA[m][ AjobOrder[j-1] ][1], ganttA[m][ AjobOrder[j-1] ][1] + p ]
            # 其他machine
            else:
                # 若還未開始則start為前一machine第一個job的endtime
                if ganttA[m][ AjobOrder[0] ][1] == 0:
                    ganttA[m][ AjobOrder[j] ] = [ ganttA[premachine][ AjobOrder[0] ][1], ganttA[premachine][ AjobOrder[0] ][1] + p ]
                else:
                    # 若前一machine最後job的endtime > 現machine最後job的endtime
                    if ganttA[premachine][ AjobOrder[j] ][1] > ganttA[m][ AjobOrder[j-1] ][1]:
                        # startime = 前一machine最後job的endtime
                        ganttA[m][ AjobOrder[j] ] = [ ganttA[premachine][ AjobOrder[j] ][1], ganttA[premachine][ AjobOrder[j] ] [1] + p ]
                    else:
                        # startime = m2最後job的endtime
                        ganttA[m][ AjobOrder[j] ] = [ ganttA[m][ AjobOrder[j-1] ][1], ganttA[m][ AjobOrder[j-1] ][1] + p ]
            # 紀錄job結束時間所產生廢料
            if ganttA[m][ AjobOrder[j] ][1] in endtime.keys():
                endtime[ ganttA[m][ AjobOrder[j] ][1] ][0] += ATable[ AjobOrder[j] ][m][1]
                endtime[ ganttA[m][ AjobOrder[j] ][1] ][1] += ATable[ AjobOrder[j] ][m][2]
            else:
                endtime[ ganttA[m][ AjobOrder[j] ][1] ] = [ ATable[ AjobOrder[j] ][m][1], ATable[ AjobOrder[j] ][m][2] ]
        # 紀錄前一machine
        premachine = m

    CAmax = ganttA[ max(ganttA) ][ AjobOrder[-1] ][1]
    printGantt("LineA gantt:\n", ganttA, CAmax)

    return endtime


def main():
    # test
    # ATable = {'J1':{'M1':[4, 3, 1], 'M2':[5, 3, 2]}, 'J2':{'M1':[5, 1, 3], 'M2':[2, 2, 2]}, 'J3':{'M1':[3, 2, 2], 'M2':[6, 1, 1]},'J4':{'M1':[5, 2, 3], 'M2':[3, 1, 1]}}
    # BTable = {'j1':{'m1':[2, 0, 1], 'm2':[1, 1, 0]}, 'j2':{'m1':[3, 2, 2], 'm2':[2, 1, 1]}, 'j3':{'m1':[4, 7, 1], 'm2':[4, 1, 5]}, 'j4':{'m1':[7, 7, 2], 'm2':[4, 4, 5]}}
    # AjobOrder = ['J1', 'J3', 'J2', 'J4']
    # BjobOrder = ['j3', 'j2', 'j1', 'j4']

    ATable = {'J1':{'M1':[4, 3, 1], 'M2':[5, 3, 2]},
              'J2':{'M1':[5, 1, 3], 'M2':[2, 2, 2]},
              'J3':{'M1':[3, 2, 2], 'M2':[6, 1, 1]}}

    AjobOrder = ['J1', 'J3', 'J2']
    AmachineOrder = ['M1', 'M2']

    BTable = {'j1':{'m1':[2, 0, 1], 'm2':[1, 1, 0]}, \
              'j2':{'m1':[3, 2, 2], 'm2':[2, 1, 1]}, \
              'j3':{'m1':[4, 7, 1], 'm2':[4, 1, 5]}}

    BjobOrder = ['j3', 'j2', 'j1']
    BmachineOrder = ['m1', 'm2']

    endtime = mainLine(ATable, AjobOrder, AmachineOrder)
    nextLine(BTable, BjobOrder, BmachineOrder, ATable, endtime)

    return 0

main()

