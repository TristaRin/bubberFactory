
def main():
    ATable = {'J1':{'M1':[4, 3, 1], 'M2':[5, 3, 2]}, \
              'J2':{'M1':[5, 1, 3], 'M2':[2, 2, 2]}, \
              'J3':{'M1':[3, 2, 2], 'M2':[6, 1, 1]}}

    BTable = {'j1':{'m1':[2, 0, 1], 'm2':[1, 1, 0]}, \
              'j2':{'m1':[3, 2, 2], 'm2':[2, 1, 1]}, \
              'j3':{'m1':[4, 7, 1], 'm2':[4, 1, 5]}}

    mNum = 2
    jobNum = 3

    q1 = 0 # LineA 剩餘膠條
    q2 = 0 # LineA 剩餘膠粉
    
    r1 = 0 # LineB 剩餘膠條
    r2 = 0 # LineB 剩餘膠粉
    
    resource1 = 0 # 總剩餘膠條
    resource2 = 0 # 總剩餘膠粉

    AjobOrder = ['J1', 'J3', 'J2']
    BjobOrder = ['j1', 'j2', 'j3']

    ganttA = dict()
    ganttB = dict()

    # 按machine順序
    for m in ATable['J1']:
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
                    # 接續此machiney前一job的endtime 
                    ganttA[m][ AjobOrder[j] ] = [ ganttA[m][ AjobOrder[j-1] ][1], ganttA[m][ AjobOrder[j-1] ][1] + p ]
            # else (其他machine)
            else:
                # 若還未開始則start為前一machine第一個job的endtime
                if ganttA[m][ AjobOrder[0] ][1] == 0:
                    ganttA[m][ AjobOrder[j] ] = [ ganttA[premachine][ AjobOrder[0] ][1], ganttA[premachine][ AjobOrder[0] ][1] + p ]
                else:
                    # 若前一machine最後job的endtime > 現machine最後job的endtime
                    if ganttA[premachine][ AjobOrder[j] ][1] > ganttA[m][ AjobOrder[j-1] ][1]:
                        # startime = 前一machine最後job的endtime
                        ganttA[m][ AjobOrder[j] ] = [ ganttA[premachine][ AjobOrder[j] ][1], ganttA[premachine][ AjobOrder[j] ] [1] +p ]
                    # else (m1最後job的endtime < m2最後job的endtime)
                    else:
                        # startime = m2最後job的endtime
                        ganttA[m][ AjobOrder[j] ] = [ ganttA[m][ AjobOrder[j-1] ][1], ganttA[m][ AjobOrder[j-1] ][1] + p ]
        premachine = m

    CAmax = ganttA[ max(ganttA) ][ AjobOrder[-1] ][1]
    
    print(ganttA)
    print('CAmax: ', CAmax)

main()