def check(outlog = "checklog.txt"):
    outf = open(outlog, "w")
    with open("LF.CAL") as f:
        line = f.readline()
        line = line.strip().split(',')
    success = int(line[0])
    if success != 1:
        print success, "not success"
        outf.write("-1\n")
        outf.close()
        return False
    #
    with open("LF.LP1") as f:
        lines = f.readlines()
    for line in lines:
        _ = eval(line.strip())
        if len(_) > 2:
            x = float(_[1])
            if x < 0.95:
                mess = _[3], x, "L"
                print mess
                outf.write(str(mess)[1:-1] + "\n")
            if x > 1.05:
                mess = _[3], x, "H"
                print mess
                outf.write(str(mess)[1:-1] + "\n")
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
            dict_l1[dict_l2[i][0]] * dict_l1[dict_l2[i][0]] * dict_l2[i][2] * dict_l2[i][2] : 
                mess = "LP2", i, "IH"
                print mess
                outf.write(str(mess)[1:-1] + "\n")
            if dict_lp2[i][2] * dict_lp2[i][2] + dict_lp2[i][3] * dict_lp2[i][3] > \
            dict_l1[dict_l2[i][1]] * dict_l1[dict_l2[i][1]] * dict_l2[i][2] * dict_l2[i][2] :
                mess = "LP2", i, "JH"
                print mess
                outf.write(str(mess)[1:-1] + "\n")
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
            dict_l3[i] * dict_l3[i] :
                mess = "LP3", i, "IH"
                print mess
                outf.write(str(mess)[1:-1] + "\n")
            if dict_lp2[i][2] * dict_lp2[i][2] + dict_lp2[i][3] * dict_lp2[i][3] > \
            dict_l3[i] * dict_l3[i] :
                mess = "LP3", i, "JH"
                print mess
                outf.write(str(mess)[1:-1] + "\n")
    #
    ##
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
        if dict_lp5[i][0] > dict_l5[i][1] and dict_l5[i][1] != 0:
            mess = "generator", i, "PH"
            print mess
            outf.write(str(mess)[1:-1] + "\n")
        if dict_lp5[i][0] < dict_l5[i][0] and dict_l5[i][0] != 0:
            mess = "generator", i, "PL"
            print mess
            outf.write(str(mess)[1:-1] + "\n")
        if dict_lp5[i][1] > dict_l5[i][3] and dict_l5[i][3] != 0:
            mess = "generator", i, "QH"
            print mess
            outf.write(str(mess)[1:-1] + "\n")
        if dict_lp5[i][1] < dict_l5[i][2] and dict_l5[i][2] != 0:
            mess = "generator", i, "QL"
            print mess
            outf.write(str(mess)[1:-1] + "\n")
    #
    ##
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
        if dict_lp6[i][0] > dict_l6[i][1] and dict_l6[i][1] != 0:
            mess = "load", i, "PH"
            print mess
            outf.write(str(mess)[1:-1] + "\n")
        if dict_lp6[i][0] < dict_l6[i][0] and dict_l6[i][0] != 0:
            mess = "load", i, "PL"
            print mess
            outf.write(str(mess)[1:-1] + "\n")
        if dict_lp6[i][1] > dict_l6[i][3] and dict_l6[i][3] != 0:
            mess = "load", i, "QH"
            print mess
            outf.write(str(mess)[1:-1] + "\n")
        if dict_lp6[i][1] < dict_l6[i][2] and dict_l6[i][2] != 0:
            mess = "load", i, "QL"
            print mess
            outf.write(str(mess)[1:-1] + "\n")
    #
    return True
    
if __name__ == "__main__":
    print check()
