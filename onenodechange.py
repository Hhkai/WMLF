import time
import MySQLdb
import os

def getflag():
    with open("LF.CAL") as f:
        line = f.readline()
        line = line.strip().split(',')
    success = int(line[0])
    return success
    
def readL6():
    mx = []
    with open("LF.L6") as f:
        for line in f.readlines():
            line = list(eval(line.strip()))
            mx.append(line)
    return mx
def readL5():
    mx = []
    with open("LF.L5") as f:
        for line in f.readlines():
            line = list(eval(line.strip()))
            mx.append(line)
    return mx
def writeL6(mx):
    with open("LF.L6", "w") as f:
        for i in mx:
            f.write(str(i)[1:-1] + '\n')
def writeL5(mx):
    with open("LF.L5", "w") as f:
        for i in mx:
            f.write(str(i)[1:-1] + '\n')
#
def savegraph(conn, mxL5, mxL6):
    paras = []
    for line in mxL5:
        if line[2] == 1:
            paras.append(line[3])
            paras.append(line[4])
        if line[2] == -1:
            paras.append(line[3])
            paras.append(line[5])
    for line in mxL6:
        paras.append(line[4])
        paras.append(line[5])
    sparas = ['%.6f' % i for i in paras]
    ind = str(time.time())[:10]
    cursor = conn.cursor()
    comd = "insert into graph values('%s', %s)" % (ind, str(sparas)[1:-1])
    # print comd
    cursor.execute(comd)
    cursor.close()
    conn.commit()
    time.sleep(1)
    return ind
def saveflag(conn, ind, flag):
    cursor = conn.cursor()
    comd = "insert into flag values('%s', '%s')" % (ind, flag)
    # print comd
    cursor.execute(comd)
    cursor.close()
    conn.commit()
    time.sleep(1)
    return ind
def saveedge(conn, u, v):
    cursor = conn.cursor()
    ind = str(time.time())[:10]
    comd = "insert into edge values('%s', '%s', '%s')" % (ind, u, v)
    # print comd
    cursor.execute(comd)
    cursor.close()
    conn.commit()
    time.sleep(1)
    return ind
    
conn = MySQLdb.connect(host = 'localhost', port = 3306, user = 'root', passwd = '1234', db = 'net36node')

for L6line in range(10):
    mx = readL6()
    L6p = mx[L6line][4]
    L6q = mx[L6line][5]
    oL6p = L6p
    oL6q = L6q
    if L6p != 0:
        bigp = 1.0
        if L6p < 1:
            bigp = 4.0
        else:
            bigp = 7.0
        r = bigp / L6p
        L6q *= r
        L6p *= r
    else:
        L6p = 3.7
        L6q = 1.893
    mx[L6line][4] = L6p
    mx[L6line][5] = L6q
    writeL6(mx)
    os.system("WMLFRTMsg")
    success = getflag()
    if success == 1:
        print "success", L6line, L6p, L6q
        mx[L6line][4] = oL6p
        mx[L6line][5] = oL6q
        writeL6(mx)
        continue
    ##### try to find the generator
    L5mx = readL5()
    rate = [i / 10.0 for i in range(40)]
    nosol = 1
    beforesaved = savegraph(conn, L5mx, mx)
    saveflag(conn, beforesaved, 0)
    for L5line in range(8):
        if L5mx[L5line][2] == 1:
            orip = L5mx[L5line][3]
            oriq = L5mx[L5line][4]
            for r in rate:
                newp = orip * r
                newq = oriq * r
                L5mx[L5line][3] = newp
                L5mx[L5line][4] = newq
                writeL5(L5mx)
                os.system("WMLFRTMsg")
                success = getflag()
                if success == 1:
                    print "find success: ", L6line, L5line
                    nosol = 0
                    # store
                    ind = savegraph(conn, L5mx, mx)
                    saveflag(conn, ind, 1)
                    saveedge(conn, beforesaved, ind)
                    break
            L5mx[L5line][3] = orip
            L5mx[L5line][4] = oriq
            writeL5(L5mx)
        if L5mx[L5line][2] == -1:
            orip = L5mx[L5line][3]
            for r in rate:
                newp = 0
                if orip < 0:
                    newp = orip + r
                else:
                    newp = orip * r
                L5mx[L5line][3] = newp
                writeL5(L5mx)
                os.system("WMLFRTMsg")
                success = getflag()
                if success == 1:
                    print "find success: ", L6line, L5line
                    nosol = 0
                    # store
                    ind = savegraph(conn, L5mx, mx)
                    saveflag(conn, ind, 1)
                    saveedge(conn, beforesaved, ind)
                    break
            L5mx[L5line][3] = orip
            writeL5(L5mx)
    if nosol == 1:
        print ">>>>>>>", L6line
        a = input()
    mx[L6line][4] = oL6p
    mx[L6line][5] = oL6q
    writeL6(mx)
#
conn.close()
exit()