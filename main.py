import ElecGraph
import os
import copy

def load_data():
    root = ElecGraph.ElecGraph()
    root.read_data("../data/origin")
    #
    child = ElecGraph.ElecGraph()
    child.read_data("../data/16H")
    root.addChild_load(child)
    child2 = ElecGraph.ElecGraph()
    child2.read_data("../data/16HO")
    child.addChild_gen(child2)
    #
    child = ElecGraph.ElecGraph()
    child.read_data("../data/16H1")
    root.addChild_load(child)
    child2 = ElecGraph.ElecGraph()
    child2.read_data("../data/16H1O")
    child.addChild_gen(child2)
    #
    child = ElecGraph.ElecGraph()
    child.read_data("../data/18H")
    root.addChild_load(child)
    child2 = ElecGraph.ElecGraph()
    child2.read_data("../data/18HO")
    child.addChild_gen(child2)
    return root
#
def read_temp():
    temp = ElecGraph.ElecGraph()
    temp.read_data(".")
    return temp
#
def find_end(root, temp, mask): 
    ElecGraph.myprint("搜索知识库...")
    path = root.findChild(temp, mask)
    mask.append(path)
    if path == False:
        print("no knowledge")
        ElecGraph.myprint("没有找到知识")
        return -1
    
    succ = 0
    for cur in root.children[path]:
        # different ways
        for key in cur.children: 
            # key is the solution pos
            for ans in cur.children[key]:
                if ans.tag == True:
                    print("找到解决方案, 尝试调整")
                    ElecGraph.myprint("找到解决方案, 尝试调整...")
                    print(path, key, ans.name)
                    #a = input("br")
                    ans.copytemp(temp, path)
                    ans.write()
                    res = ans.findans(key)
                    temp.write()
                    if res == True:
                        temp.copytemp(ans, key)
                        temp.write()
                        succ = 1
                        break
            if succ == 1:
                break
        if succ == 1:
            break
    return succ == 1
#
if __name__ == "__main__":
    ElecGraph.myprint("=============程序开始===========")
    ElecGraph.myprint("载入数据...")
    root = load_data()
    ElecGraph.myprint("载入完成")
    while True:
        a = input("continue?")
        ElecGraph.myprint(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        ElecGraph.myprint("读入输入文件...")
        temp = read_temp()
        mask = []
        while True: 
            res = find_end(root, temp, mask)
            if res == -1:
                break