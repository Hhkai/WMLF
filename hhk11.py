# -*- coding: utf-8 -*-
#python3

import os
import random
import math
import shutil


def readfile(filename, coding='utf-8'):
    mx = []
    with open(filename, 'r', encoding=coding) as f:
        lines = f.readlines()
        for line in lines:
            line = list(eval(line.strip()))
            mx.append(line)
    return mx


genDis = readfile('genDis.txt')
CUR_DIR = os.getcwd()


#
def writefile(filename, mx):
    with open(filename, "w", encoding='utf-8') as f:
        for i in mx:
            templine = []
            for j in i:
                templine.append(j)
            for ind, iii in enumerate(templine):
                if type(iii) == type(0.0):
                    templine[ind] = round(iii, 4)
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
    stdgen = load * 1.011
    r = stdgen / gen
    for i in range(len(mx2)):
        if mx2[i][2] == 1:
            mx2[i][3] = mx2[i][3] * r
            mx2[i][4] = mx2[i][4] * r
        if mx2[i][2] == -1:
            mx2[i][3] = mx2[i][3] * r
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
                if i[1] > val and (
                        i[0] in genList) and mx5[genList[i[0]]][3] > 0.1:
                    gen = genList[i[0]]
                    val = i[1]
        if gen == None:
            pass  ########## gao !!!!!!!!!!!!!!
        else:
            P = mx5[gen][3]
            r = (P - 0.5) / P
            if r < 0:
                r = 0.5
            mx5[gen][3] = mx5[gen][3] * r
            mx5[gen][4] = mx5[gen][4] * r
            writefile('LF.L5', mx5)
            print('1.15', gen)
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
        return (0, gen)  # line num
    if fixline in loadList:
        load = loadList[fixline]
        print(1, load)
        # return (1, load, fixnum > 1) # line num
        return (1, fixline, fixnum > 1)  # L1 id
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
    return 'xx', 'xx'


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
        P = readslackval(readslack(), name)
    else:
        return "fail"
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
def goonestep(genList, loadList, markList, lastLoad_list, genDis, mx5):
    os.system('WMLFRTMsg')
    if not getflag():
        # pau = input()
        return -1  #failure
    x = findLP1(genList, loadList, markList)
    if x[0] == -2:
        print('x[0] == -2, goonestep return 1')
        return 1  #continue, try once again
    if x[0] == -1:
        if getflag():
            return 0  # break, fixed, cur++
        else:
            return -1  # fail
    if x[0] == 0:
        ttt = setG(x[1])
        if ttt == "fail":
            return ttt
    if x[0] == 1:
        if x[1] == lastLoad_list[0]:
            lastLoad_list[1] = lastLoad_list[1] + 1
        else:
            lastLoad_list[0] = x[1]
            lastLoad_list[1] = 0
        if lastLoad_list[1] > 3:
            # xxxx
            ttt = setbyhand(lastLoad_list[0], x[2])
            if ttt == 1:
                markList.append(lastLoad_list[0])
            '''
            pau = input('set by hand %s:' % lastLoad)
            if pau == '1':
                markList.add(lastLoad)
            '''
            print('append', lastLoad_list[0])
            return 1  # continue, try again
        genid = genDis[lastLoad_list[0] - 1][lastLoad_list[1]]
        for ind, i in enumerate(mx5):
            if i[1] == genid:
                ttt = setG(ind)
                if ttt == "fail":
                    return ttt
                break
        if getflag():
            return 0  # break, fixed, cur++
        else:
            return -1  # fail
    print('error', x)
    # pau = input()


#
def go():
    global genDis
    if getflag():
        return "n_necessary"
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

    lastLoad = -1
    lastLoadN = 0
    lastLoad_list = [lastLoad, lastLoadN]
    step = 0.04
    markList = []
    nearflag = False
    while True:
        checkP()

        if nearflag == False and cur > 0.9:
            cur = 0.9
            nearflag = True
            continue

        b = cur / r
        r = cur
        changemx(b)

        goone = goonestep(genList, loadList, markList, lastLoad_list, genDis,
                          mx5)
        if goone == "fail":
            return False
        if goone == -1:  # fail
            cur -= step
            step *= 0.5
            if step < 0.002:
                return False
        if goone == 0:  # success
            if (r - 1) < 0.001 and (r - 1) > -0.001:
                print('success')
                break
            cur += step
            if cur > 1:
                cur = 1.0
            continue
        if goone == 1:  # unknown , continue
            print('goone==1')
            continue

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
    return getflag()


def compare_result(l2_before, l2_after, l5_before, l5_after, l6_before,
                   l6_after, l1, lfreport_file, outfile):
    # dic = ["有效", "无效"]
    with open(l6_before,
              "r", encoding="utf-8") as f1, open(l6_after,
                                                 "r",
                                                 encoding="utf-8") as f2:
        i = 1
        for row1, row2 in zip(f1, f2):
            row1 = row1.strip().split(",")
            row2 = row2.strip().split(",")
            active_power1 = float(row1[4].strip())
            active_power2 = float(row2[4].strip())
            reactive_power1 = float(row1[5].strip())
            reactive_power2 = float(row2[5].strip())
            if not (abs(active_power1 - active_power2) < 1e-3
                    and abs(active_power1 - active_power2) < 1e-3):
                return ("l6_" + str(i) + "error")
            i += 1

    bus_set = []
    with open(l1, "r", encoding="utf-8") as f:
        for row in f:
            bus_name = row.strip().split(",")[0][1:-1].strip()
            bus_set.append(bus_name)
    # print(bus_set)
    res = []
    res.append("发电机:")
    with open(l5_before,
              "r", encoding="utf-8") as f1, open(l5_after,
                                                 "r",
                                                 encoding="utf-8") as f2:
        for row1, row2 in zip(f1, f2):
            row1 = row1.strip().split(",")
            row2 = row2.strip().split(",")
            bus_name = row1[-2].strip()[1:-1]
            node_type = int(eval(row1[2].strip()))
            active_power1 = float(row1[3].strip())
            active_power2 = float(row2[3].strip())
            reactive_power1 = float(row1[4].strip())
            reactive_power2 = float(row2[4].strip())
            if node_type not in [0, 1, -1]:
                return "l5_node_type_error"
            elif node_type == 1:
                if active_power1 != active_power2 or reactive_power1 != reactive_power2:
                    res.append(bus_name + ": " + "%.3f" % active_power1 +
                               " + " + "%.3f" % reactive_power1 + "j --> " +
                               "%.3f" % active_power2 + " + " +
                               "%.3f" % reactive_power2 + "j")

            elif node_type == -1:
                if active_power1 != active_power2:
                    res.append(bus_name + ": " + "%.3f" % active_power1 +
                               " + " + " --> " + "%.3f" % active_power2)
    with open(l2_before,
              "r", encoding="utf-8") as f1, open(l2_after,
                                                 "r",
                                                 encoding="utf-8") as f2:
        i = 1
        res.append("电容电抗器:")
        for row1, row2 in zip(f1, f2):
            row1 = row1.split(",")[:3]
            row2 = row2.split(",")[:3]
            valid1 = int(eval(row1[0].strip()))
            valid2 = int(eval(row2[0].strip()))
            if row1[1] == row1[2]:
                if valid1 != valid2:
                    # res.append(
                    #     str(i) + ": " + dic[int(valid1)] + "改为" +
                    #     dic[int(valid2)])
                    # print(i)
                    res.append(bus_set[int(row1[1].strip()) - 1] + ": " +
                               str(valid1) + " --> " + str(valid2))
            i += 1

    res.append("潮流计算结果:")
    with open(lfreport_file, "r", encoding="gbk") as f:
        res.append(f.read())
    with open(outfile, "a", encoding="utf-8") as f:
        # with open(outfile, "w", encoding="utf-8") as f:
        for row in res:
            f.write(row + "\n")


# compare_result("LF.L2", "LF1.L2", "LF.L5", "LF1.L5", "LF.L6", "LF1.L6",
#                "LF.L1", "lfreport.lis", "result.txt")


def test(test_dir, ith):
    fail_list = []
    origin_fail_list = []
    fail_and_acpower_greater_than_9_list = []  # acpower > 9
    new_dir = os.path.join(test_dir, str(ith))
    old_dir = os.path.join(test_dir, str(ith) + "_old")
    for i in range(1, 40):
        cur_dir = os.path.join(new_dir, str(i))
        cur_old_dir = os.path.join(old_dir, str(i))
        os.chdir(cur_dir)
        print(os.getcwd())
        if not getflag():
            origin_fail_list.append(str(ith) + "_" + str(i))
        flag = go()
        os.chdir(CUR_DIR)
        if flag == "n_necessary":
            continue
        # flag= random.random() > 0.5

        if not flag:
            fail_list.append(str(ith) + "_" + str(i))
            with open(os.path.join(cur_old_dir, "LF.L6"),
                      "r",
                      encoding="utf-8") as f:
                row = f.readline()
                row = row.strip().split(",")
                active_power = float(row[4].strip())
                if active_power >= 9:
                    fail_and_acpower_greater_than_9_list.append(
                        str(ith) + "_" + str(i))
        else:
            with open(os.path.join(CUR_DIR, "result.txt"),
                      "a",
                      encoding="utf-8") as f:
                f.write(str(ith) + "_" + str(i) + ":\n")
            compare_result(os.path.join(cur_old_dir, "LF.L2"),
                           os.path.join(cur_dir, "LF.L2"),
                           os.path.join(cur_old_dir, "LF.L5"),
                           os.path.join(cur_dir, "LF.L5"),
                           os.path.join(cur_old_dir, "LF.L6"),
                           os.path.join(cur_dir, "LF.L6"),
                           os.path.join(cur_old_dir, "LF.L1"),
                           os.path.join(cur_dir, "lfreport.lis"),
                           os.path.join(CUR_DIR, "result.txt"))
    print("xxxxxx")
    with open(os.path.join(CUR_DIR, "conv_result.txt"), "a") as f:
        f.write(str(ith) + ":\n")
        f.write("不收敛样本："+str(origin_fail_list) + "\n")
        f.write("调整失败样本："+str(fail_list) + "\n")
        f.write("调整失败样本中某个有功功率大于9的样本："+str(fail_and_acpower_greater_than_9_list) + "\n")
    print("xxxxxx")


def copy_folder(ith):
    shutil.copytree("36data/" + str(ith), "data/" + str(ith))
    shutil.copytree("36data/" + str(ith), "data/" + str(ith) + "_old")


if __name__ == '__main__':
    for i in range(151, 201):
        copy_folder(i)
        test("data", i)

# #
# if __name__ == '__main__':
#     R = 1.0
#     while True:
#         a = input('func:')
#         if a == '0':
#             break
#         if a == '1':
#             Lrandom()
#         if a == '2':
#             checkP()
#         if a == '3':
#             b = input('ratio:')
#             r = float(b)
#             b = r / R
#             print('b=r/R=', r, '/', R, '=', r / R)
#             R = r
#             print('R:', R)
#             changemx(b)
#         if a == '4':
#             os.system("WMLFRTMsg")
#         if a == '5':
#             go()
