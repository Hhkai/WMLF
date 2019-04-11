def check():
    with open("LF.CAL") as f:
        line = f.readline()
        line = line.strip().split(',')
    success = int(line[0])
    if success != 1:
        print success, "not success"
        return False
    #
    with open("LF.LP1") as f:
        lines = f.readlines()
    for line in lines:
        _ = eval(line.strip())
        if len(_) > 2:
            x = float(_[1])
            if x < 0.95 or x > 1.05:
                print x
                return False
    ###
    dict_lp2 = dict()
    with open("LF.LP2") as f:
        lines = f.readlines()
    for i in lines:
        _ = eval(i.strip())
        dict_lp2[_[9]] = (_[3], _[4], _[5], _[6])
    dict_l2 = dict()
    with open("LF.L2") as f:
        lines = f.readlines()
    for i in lines:
        _ = eval(i.strip())
        dict_l2[_[17]] = (_[1], _[2], _[14])
    dict_l1 = dict()
    with open("LF.L1") as f:
        lines = f.readlines()
    for n, i in enumerate(lines):
        _ = eval(i.strip())
        dict_l1[n + 1] = _[1]
    for i in dict_lp2:
        if dict_l2[i][2] != 0:
            if dict_lp2[i][0] * dict_lp2[i][0] + dict_lp2[i][1] * dict_lp2[i][1] > \
            dict_l1[dict_l2[i][0]] * dict_l1[dict_l2[i][0]] * dict_l2[i][2] * dict_l2[i][2] or \
            dict_lp2[i][2] * dict_lp2[i][2] + dict_lp2[i][3] * dict_lp2[i][3] > \
            dict_l1[dict_l2[i][1]] * dict_l1[dict_l2[i][1]] * dict_l2[i][2] * dict_l2[i][2] :
                print "lp2"
                return False
    #
    ##
    dict_lp3 = dict()
    with open("LF.LP3") as f:
        lines = f.readlines()
    for i in lines:
        _ = eval(i.strip())
        dict_lp3[_[9]] = (_[3], _[4], _[5], _[6])
    dict_l3 = dict()
    with open("LF.L3") as f:
        lines = f.readlines()
    for i in lines:
        _ = eval(i.strip())
        dict_l3[_[24].strip()] = _[18]
    for i in dict_lp3:
        if dict_l3[i] != 0:
            if dict_lp2[i][0] * dict_lp2[i][0] + dict_lp2[i][1] * dict_lp2[i][1] > \
            dict_l3[i] * dict_l3[i] or \
            dict_lp2[i][2] * dict_lp2[i][2] + dict_lp2[i][3] * dict_lp2[i][3] > \
            dict_l3[i] * dict_l3[i] :
                print "LP3"
                return False
    #
    ##
    print "check generator"
    dict_lp5 = dict()
    with open("LF.LP5") as f:
        lines = f.readlines()
    for i in lines:
        _ = eval(i.strip())
        dict_lp5[_[4]] = (_[1], _[2])
    dict_l5 = dict()
    with open("LF.L5") as f:
        lines = f.readlines()
    for i in lines:
        _ = eval(i.strip())
        dict_l5[_[18]] = (_[10], _[9], _[8], _[7])
    for i in dict_lp5:
        if dict_lp5[i][0] > dict_l5[i][1] or dict_lp5[i][0] < dict_l5[i][0]:
            if dict_l5[i][1] != 0 and dict_l5[i][0] != 0:
                print "generator", i
                return False
        if dict_lp5[i][1] > dict_l5[i][3] or dict_lp5[i][1] < dict_l5[i][2]:
            if dict_l5[i][3] != 0 and dict_l5[i][2] != 0:
                print "generator", i
                return False
    #
    ##
    print "check load"
    dict_lp6 = dict()
    with open("LF.LP6") as f:
        lines = f.readlines()
    for i in lines:
        _ = eval(i.strip())
        dict_lp6[_[4]] = (_[2], _[3])
    dict_l6 = dict()
    with open("LF.L6") as f:
        lines = f.readlines()
    for i in lines:
        _ = eval(i.strip())
        dict_l6[_[18]] = (_[11], _[10], _[9], _[8])
    for i in dict_lp6:
        if dict_lp6[i][0] > dict_l6[i][1] or dict_lp6[i][0] < dict_l6[i][0]:
            if dict_l6[i][1] != 0 and dict_l6[i][0] != 0:
                print "load", i
                return False
        if dict_lp6[i][1] > dict_l6[i][3] or dict_lp6[i][1] < dict_l6[i][2]:
            if dict_l6[i][3] != 0 and dict_l6[i][2] != 0:
                print "load", i
                return False
    #
    return True
    
if __name__ == "__main__":
    print check()
