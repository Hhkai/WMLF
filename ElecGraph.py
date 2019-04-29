import os
import copy

def myprint(a):
    with open("outlog.txt", "a") as f:
        f.write(a + '\n')
#

def read_matrix(filename):
    a = []
    with open(filename) as f:
        for line in f.readlines():
            _ = eval(line.strip())
            if type(_) == type(1):
                a.append([_])
            else:
                a.append(list(_))
    return a
#
class L6Load:
    def read_line(self, line):
        self.P = line[4]
        self.Q = line[5]
        self.name = line[-1]
#
class ElecGraph:
    def read_data(self, path):
        self.children = dict()
        self.name = path
        #
        self.L2 = read_matrix(path + "/LF.L2")
        self.L3 = read_matrix(path + "/LF.L3")
        self.L5 = read_matrix(path + "/LF.L5")
        self.L6 = read_matrix(path + "/LF.L6")
        # print self.L2
        self.log = read_matrix(path + "/checklog.txt")
        self.tag = True if len(self.log) == 0 or self.log[0][0] != -1 else False
        self.tensor = [self.L2, self.L3, self.L5, self.L6]
        self.loads = []
        for i in self.L2:
            _ = L6Load()
            _.read_line(i)
            self.loads.append(_)
        #
    def addChild_load(self, G):
        for id2, j in enumerate(self.L6):
            for id3, k in enumerate(j):
                if k != G.tensor[3][id2][id3]:
                    if (3, id2, id3) not in self.children:
                        self.children[(3, id2, id3)] = [G]
                    else:
                        self.children[(3, id2, id3)].append(G)
        #
    def addChild_gen(self, G):
        for id2, j in enumerate(self.L5):
            for id3, k in enumerate(j):
                if k != G.tensor[2][id2][id3]:
                    if (2, id2, id3) not in self.children:
                        self.children[(2, id2, id3)] = [G]
                    else:
                        self.children[(2, id2, id3)].append(G)
        #
    def findChild(self, G, mask):
        for id2, j in enumerate(self.L6):
            for id3, k in enumerate(j):
                if k != G.tensor[3][id2][id3]:
                    if (3, id2, id3) in mask:
                        continue
                    if (3, id2, id3) not in self.children:
                        return False
                    else:
                        return (3, id2, id3)
        return False
        #
    def write(self):
        with open("LF.L2", "w") as f:
            for i in self.L2:
                f.write(str(i)[1:-1] + '\n')
        with open("LF.L3", "w") as f:
            for i in self.L3:
                f.write(str(i)[1:-1] + '\n')
        with open("LF.L5", "w") as f:
            for i in self.L5:
                f.write(str(i)[1:-1] + '\n')
        with open("LF.L6", "w") as f:
            for i in self.L6:
                f.write(str(i)[1:-1] + '\n')
    def findans(self, key):
        if key == (2, 5, 3):
            myprint("负荷%s功率改变, 调整发电机%s" % (self.L6[0][-1], self.L5[5][-1]))
            val = -0.01
            max = 4.0
            success = 0
            while val < max:
                self.tensor[2][5][3] = val
                with open("LF.L5", "w") as f:
                    for i in self.L5:
                        f.write(str(i)[1:-1] + '\n')
                os.system("WMLFRTMsg")
                with open("LF.CAL") as f:
                    line = f.readline()
                    line = line.strip().split(',')
                success = int(line[0])
                if success == 1:
                    myprint("调整结束")
                    print("调整结束")
                    break
                val += 0.01
            if success == 0:
                print("failed")
            else:
                return True
        return False
    #
    def copytemp(self, temp, path):
        if path == (3, 0, 4):
            self.L6[0] = copy.deepcopy(temp.L6[0])
        if path == (2, 5, 3):
            self.L5[5] = copy.deepcopy(temp.L5[5])