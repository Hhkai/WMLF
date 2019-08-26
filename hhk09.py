# -*- coding: utf-8 -*-
#python3

import os
import random
import math
def readfile(filename, coding='utf-8'):
    mx = []
    with open(filename, 'r', encoding=coding) as f:
        lines = f.readlines()
        for line in lines:
            line = list(eval(line.strip()))
            mx.append(line)
    return mx
#
def writefile(filename, mx):
    with open(filename, "w", encoding='utf-8') as f:
        for i in mx:
            templine = []
            for j in i:
                templine.append(j)
            for ind, iii in enumerate(templine):
                if type(iii) == type(0.0):
                    templine[ind] = round(iii, 6)
            f.write(str(templine)[1:-1] + ',\n')
#
def checkload():
    mx = readfile('LF.L6')
    for i in range(len(mx)):
        P = mx[i][4]
        Q = mx[i][5]
        if P < Q:
            mx[i][4] = Q
    writefile('LF.L6', mx)
#
def Lrandom():
    mx = readfile("LF.L6")
    ratio = 5
    for i in range(len(mx)):
        mx[i][4] = random.random() * ratio
        mx[i][5] = random.random() * ratio
        if mx[i][5] > mx[i][4]:
            mx[i][5] = mx[i][4]
    writefile("LF.L6", mx)
def checkP():
    mx = readfile('LF.L6')
    load = 0
    for i in mx:
        load += i[4]
    mx2 = readfile('LF.L5')
    gen = 0
    for i in mx2:
        gen += i[3]
    if load * 1.01 - gen > 0:
        print('load>gen:success')
    else:
        print('gen too high')
        return 1
    if load * 1.02 - gen < 12:
        print('load<gen:success')
    else:
        print('gen too low')
        return 2
    return 0
#
def changemx(b):
    mx = readfile('LF.L6')
    for i in range(len(mx)):
        print(mx[i][4], type(mx[i][4]))
        mx[i][4] = mx[i][4] * b
        mx[i][5] = mx[i][5] * b
    writefile("LF.L6", mx)
    mx2 = readfile('LF.L5')
    for i in range(len(mx2)):
        mx2[i][3] = mx2[i][3] * b
    writefile('LF.L5', mx2)
#
def getflag():
    with open("LF.CAL") as f:
        line = f.readline()
        line = line.strip().split(',')
    success = int(line[0])
    return success == 1
#
# ----------------------------------------
def findLP1(genList, loadList, markList):
    lp1 = readfile('LF.LP1', coding='gb2312')
    n = 0
    loadsdown = []
    loadsup = []
    loadssum = 0
    abss = []
    for i in lp1:
        if len(i) == 4:
            loadssum += i[1]
            n += 1
    #
    gen = None
    val = 1
    mx5 = readfile('LF.L5')
    if n * 0.85 > loadssum:
        for i in lp1:
            if len(i) == 4:
                if i[1] < val and (i[0] in genList):
                    gen = genList[i[0]]
                    val = i[1]
        P = mx5[gen][3]
        r = (P + 0.5) / P
        if P < 0:
            r = -1
        mx5[gen][3] = mx5[gen][3] * r
        mx5[gen][4] = mx5[gen][4] * r
        writefile('LF.L5', mx5)
        print('0.85', gen)
        return (-2, 1)
    #
    gen = None
    val = 0
    if n * 1.15 < loadssum:
        for i in lp1:
            if len(i) == 4:
                if i[1] > val and (i[0] in genList) and mx5[genList[i[0]]][3] > 0.1:
                    gen = genList[i[0]]
                    val = i[1]
        P = mx5[gen][3]
        r = (P - 0.5) / P
        if r < 0:
            r = 0.5
        mx5[gen][3] = mx5[gen][3] * r
        mx5[gen][4] = mx5[gen][4] * r
        writefile('LF.L5', mx5)
        print('1.15',gen)
        return (-2, 1)
    #
    fixtype = -1
    fixline = 0
    fixnum = 1.0
    for i in lp1:
        if len(i) == 4:
            if abs(i[1] - 1) > 0.1:
                curtype = -2
                if i[0] in genList:
                    curtype = 1
                if i[0] in loadList:
                    curtype = 0
                    if i[0] in markList:
                        continue
                if curtype >= fixtype:
                    if abs(i[1] - 1) > abs(fixnum - 1):
                        fixline = i[0]
                        fixtype = curtype
                        fixnum = i[1]
            # 
    if fixtype == -1:
        return (-1, 1)
    if fixtype == -2:
        print('error')
        exit()
    if fixline in genList:
        gen = genList[fixline]
        print(0, gen)
        return (0, gen) # line num
    if fixline in loadList:
        load = loadList[fixline]
        print(1, load)
        # return (1, load, fixnum > 1) # line num
        return (1, fixline, fixnum > 1) # L1 id
    return (-3, 1)
#
def readslack():
    store = 0
    ret = []
    with open("lfreport.lis") as f:
        lines = f.readlines()
        for line in lines:
            templine = line.strip().split()
            if templine[0] == "Slack":
                store = 1
                continue
            if store == 1:
                ret.append(templine)
    return ret
#
def readslackval(slack, busname):
    for i in slack:
        # print('hhhhh', i[0], busname)
        if i[0] == busname:
            return i[1], i[2]
    return 'xx','xx'
def setG(linen):
    mx = readfile("LF.L5")
    name = 0
    P = (0.1, 0.1)

    oldtype = mx[linen][2]
    mx[linen][2] = 0
    name = mx[linen][-1]
    writefile("LF.L5", mx)
    os.system("WMLFRTMsg")
    if getflag():
        P = readslackval(readslack(),name)
    else:
        pass
    mx[linen][2] = oldtype
    mx[linen][3] = float(P[0][:4])
    mx[linen][4] = float(P[1][:4])
    
    writefile("LF.L5", mx)
    return
#
def setbyhand(x, toohigh):
    # open a -5 will make it higher
    mx = readfile('LF.L2')
    for i in range(len(mx)):
        if mx[i][1] == x and mx[i][2] == x:
            if toohigh:
                if mx[i][0] == 0 and mx[i][5] > 0:
                    mx[i][0] = 1
                    writefile('LF.L2', mx)
                    return 0
                if mx[i][0] == 1 and mx[i][5] < 0:
                    mx[i][0] = 0
                    writefile('LF.L2', mx)
                    return 0
            else:
                if mx[i][0] == 0 and mx[i][5] < 0:
                    mx[i][0] = 1
                    writefile('LF.L2', mx)
                    return 0
                if mx[i][0] == 1 and mx[i][5] > 0:
                    mx[i][0] = 0
                    writefile('LF.L2', mx)
                    return 0
    return 1
#
def go():
    r = 1.0
    cur = 0.3
    genList = dict()
    loadList = dict()
    mx5 = readfile('LF.L5')
    for ind, i in enumerate(mx5):
        if i[2] != 0:
            genList[i[1]] = ind
    mx6 = readfile('LF.L6')
    for ind, i in enumerate(mx6):
        loadList[i[1]] = ind
    genDis = readfile('genDis.txt')
    while True:
        if checkP() == 1:
            mx5 = readfile('LF.L5')
            for i in range(len(mx5)):
                if mx5[i][3] != 0:
                    mx5[i][3] = mx5[i][3] - 0.5
                    if mx5[i][3] < 0:
                        mx5[i][3] = (mx5[i][3] + 0.5) / 2
            writefile('LF.L5', mx5)
            continue
        if checkP() == 2:
            mx5 = readfile('LF.L5')
            for i in range(len(mx5)):
                if mx5[i][3] != 0:
                    mx5[i][3] = mx5[i][3] + 0.5
            writefile('LF.L5', mx5)
            continue
        #
        b = cur / r
        r = cur
        changemx(b)
        lastLoad = -1
        lastLoadN = 0
        step = 0.02
        markList = set()
        while True:
            os.system('WMLFRTMsg')
            if not getflag():
                cur -= 0.03
                print('cur--', cur)
                # pau = input()
                break
            x = findLP1(genList, loadList, markList)
            if x[0] == -2:
                continue
            if x[0] == -1:
                if getflag():
                    break
                else:
                    cur -= 0.03
                    break
            if x[0] == 0:
                setG(x[1])
            if x[0] == 1:
                if x[1] == lastLoad:
                    lastLoadN += 1
                else:
                    lastLoad = x[1]
                    lastLoadN = 0
                if lastLoadN > 3:
                    # xxxx
                    ttt = setbyhand(lastLoad, x[2])
                    if ttt == 1:
                        markList.add(lastLoad)
                    '''
                    pau = input('set by hand %s:' % lastLoad)
                    if pau == '1':
                        markList.add(lastLoad)
                    '''
                    continue
                genid = genDis[lastLoad - 1][lastLoadN]
                for ind, i in enumerate(mx5):
                    if i[1] == genid:
                        setG(ind)
                        break
            print(x)
            # pau = input()
        cur += 0.02
        if cur > 1:
            cur = 1
        print('++++++++ ', r)
        print(markList)
        # pau = input('clear?')
        # if pau == 'y':
        #    markList = set()
        if (r - 1) < 0.001 and (r - 1) > -0.001:
            break
        if r > 1:
            print('r>1')
            break
#
if __name__ == '__main__':
    c = readfile('LF.LP1', coding='gb2312')
    R = 1.0
    while True:
        a = input('func:')
        if a == '0':
            break
        if a == '1':
            Lrandom()
        if a == '2':
            checkP()
        if a == '3':
            b = input('ratio:')
            r = float(b)
            b = r / R 
            print('b=r/R=',r,'/',R,'=',r/R)
            R = r
            print('R:',R)
            changemx(b)
        if a == '4':
            os.system("WMLFRTMsg")
        if a == '5':
            go()
            