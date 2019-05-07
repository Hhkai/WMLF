import os
import time
import random
def interval(a, b, origin_value):
    if a == 0 and b == 0:
        return origin_value + 5*random.random() - 0.5
    return (b - a) * random.random() + a
def generate():
    list_L1 = []
    with open("LF.L1") as f:
        tt = f.readlines()
        for i in tt:
            list_L1.append(eval(i.strip()))
    #
    list_L5 = []
    with open("LF.L5") as f:
        tt = f.readlines()
        for i in tt:
            list_L5.append(eval(i.strip()))
    line_n = len(list_L5)
    zero_line = int(random.random() * line_n)
    with open("LF.L5", "w") as f:
        count_n = 0
        for i in list_L5:
            templine = []
            for j in i:
                templine.append(j)
            _ = random.random()
            if templine[2] == 0:
                pass
            else:
                templine[3] = interval(templine[10], templine[9], templine[3])
                if templine[2] == 1 or templine[2] == -3:
                    templine[4] = interval(templine[8], templine[7], templine[4])
                if templine[2] == -1 or templine[2] == -2:
                    templine[5] = 0.95 + 0.1 * random.random()
            if templine[2] != 0 and templine[2] != 1 and templine[2] != -1 and templine[2] != -2 \
            and templine[2] != -3 :
                print "warning"
            for ind, iii in enumerate(templine):
                if type(iii) == type(0.0):
                    templine[ind] = round(iii, 6)
            f.write(str(templine)[1:-1] + ',\n')
    #
    list_L6 = []
    with open("LF.L6") as f:
        tt = f.readlines()
        for i in tt:
            list_L6.append(eval(i.strip()))
    with open("LF.L6", "w") as f:
        for i in list_L6:
            templine = []
            for j in i:
                templine.append(j)
            
            templine[4] = interval(templine[11], templine[10], templine[4])
            templine[5] = interval(templine[9], templine[8], templine[5])
            for ind, iii in enumerate(templine):
                if type(iii) == type(0.0):
                    templine[ind] = round(iii, 6)
            f.write(str(templine)[1:-1] + ',\n')
    #
    list_L3 = []
    with open("LF.L3") as f:
        tt = f.readlines()
        for i in tt:
            list_L3.append(eval(i.strip()))
    with open("LF.L3", "w") as f:
        for i in list_L3:
            templine = []
            for j in i:
                templine.append(j)
            _ = random.random()
            if templine[26] != 0:
                templine[31] = random.sample(range(templine[28], templine[27] + 1), 1)[0]
                v_jact = (1 - (templine[31] - templine[29]) * templine[30]) * templine[26]
                v_iact = templine[25]
                templine[6] = v_jact / list_L1[templine[2] - 1][1]
                if templine[1] > 0:
                    templine[6] = templine[6] / (v_iact / list_L1[templine[1] - 1][1])
                for ind, iii in enumerate(templine):
                    if type(iii) == type(0.0):
                        templine[ind] = round(iii, 6)
            f.write(str(templine)[1:-1] + ',\n')
    #
    '''
    list_L2 = []
    with open("LF.L2") as f:
        tt = f.readlines()
        for i in tt:
            list_L2.append(eval(i.strip()))
    with open("LF.L2", "w") as f:
        for i in list_L2:
            templine = []
            for j in i:
                templine.append(j)
            templine[0] = random.sample([0, 1, 2, 3], 1)[0]
            for ind, iii in enumerate(templine):
                if type(iii) == type(0.0):
                    templine[ind] = round(iii, 6)
            f.write(str(templine)[1:-1] + ',\n')
    #
    '''
if __name__ == "__main__":
    # name = str(time.time())[:10]
    generate()
    '''
    os.system("WMLFRTMsg")
    if check1() == True:
        name = name + 'y'
    else:
        name = name + 'n'
    os.mkdir(name)
    os.system('copy LF.CAL '+name)
    os.system('copy LF.L2 '+name)
    os.system('copy LF.L3 '+name)
    os.system('copy LF.L5 '+name)
    os.system('copy LF.L6 '+name)
    os.system('copy LF.LP1 '+name)
    os.system('copy LF.LP2 '+name)
    os.system('copy LF.LP3 '+name)
    os.system('copy LF.LP5 '+name)
    os.system('copy LF.LP6 '+name)
    '''
