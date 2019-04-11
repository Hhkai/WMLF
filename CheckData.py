# coding:utf-8
import numpy as np
import pandas as pd

global true_flag
true_flag = True

#是否收敛
def check_constriction():
    global true_flag
    cons_data = pd.read_csv('LF.CAL', header=None, sep=',', error_bad_lines=False)
    cons_flag = pd.to_numeric(cons_data[0][0])
    if cons_flag == 1:
        print("潮流计算收敛")
    else:
        print("潮流计算不收敛")

#母线
def check_bus_data():
    global true_flag
    bus_data = pd.read_csv('LF.LP1', skiprows=1, header=None, sep=',')
    #print(bus_data)
    bus_data[0] = pd.to_numeric(bus_data[0])
    bus_data[1] = pd.to_numeric(bus_data[1])

    print("-----------------------------")
    print("母线结果检验:")

    low_data = bus_data[(bus_data[1]<0.95)].index.tolist()
    for i in low_data:
        s = "母线" + str(bus_data[0][i]) + "数据低于下限"
        print(s)
        true_flag = False

    high_data = bus_data[(bus_data[1]>1.05)].index.tolist()
    for i in high_data:
        s = "母线" + str(bus_data[0][i]) + "数据高于上限"
        print(s)
        true_flag = False

    print("检验完成")
    print("-----------------------------")

#交流线
def check_ac_data():
    global true_flag
    ac_data = pd.read_csv('LF.LP2', header=None, sep=',')
    I_data = pd.read_csv('LF.L2', header=None, sep=',')
    U_data = pd.read_csv('LF.L1', header=None, sep=',')
    for i in [3,4,5,6]:
        ac_data[i] = pd.to_numeric(ac_data[i])
    for i in [1,2,14]:
        I_data[i] = pd.to_numeric(I_data[i])
    U_data[1] = pd.to_numeric(U_data[1])

    print("-----------------------------")
    print("交流线容量合理性结果检验:")
    for item in ac_data.index:
        indexs = []
        for line in ac_data.index:
            ac = str(ac_data[9][item])[1:-1]
            I_upper = str(I_data[17][line])[1:-1]
            if ac in I_upper:
                indexs.append(line)
        if indexs:
            i = indexs[0]
            I_i = I_data[14][i]

            if I_i == 0:
                s = str(ac_data[9][item]) + " 容量上限为0"
                print(s)
            else:
                p_i = ac_data[3][item]
                q_i = ac_data[4][item]
                p_j = ac_data[5][item]
                q_j = ac_data[6][item]

                u_i = U_data[1][int(I_data[1][i])]
                u_j = U_data[1][int(I_data[2][i])]
                #print((p_i,q_i,p_j,q_j,s_i))
                if p_i*p_i + q_i*q_i <= u_i*u_i*I_i*I_i and p_j*p_j + q_j*q_j <= u_j*u_j*I_i*I_i:
                    pass
                elif p_i*p_i + q_i*q_i <= u_i*u_i*I_i*I_i:
                    s = str(ac_data[9][item]) + " J侧容量超过上限"
                    print(s)
                    true_flag = False
                elif p_j*p_j + q_j*q_j <= u_j*u_j*I_i*I_i:
                    s = str(ac_data[9][item]) + " I侧容量超过上限"
                    print(s)
                    true_flag = False
                else:
                    s = str(ac_data[9][item]) + " 双侧容量超过上限"
                    print(s)
                    true_flag = False

    print("检验完成")
    print("-----------------------------")


#变压器
def check_trans_data():
    global true_flag
    trans_data = pd.read_csv('LF.LP3', header=None, sep=',')
    U_data = pd.read_csv('LF.L3', header=None, sep=',')
    U_data[18] = pd.to_numeric(U_data[18])
    for i in [3,4,5,6]:
        trans_data[i] = pd.to_numeric(trans_data[i])

    print("-----------------------------")
    print("变压器容量合理性结果检验:")
    for item in trans_data.index:
        indexs = []
        for line in U_data.index:
            trans = str(trans_data[9][item])[1:-1]
            U = str(U_data[24][line])[1:-1]
            if trans in U:
                # print(str(trans_data[9][item]),str(U_data[24][line]))
                # print(line)
                indexs.append(line)
        if indexs:
            i = indexs[0]
            s_i = U_data[18][i]
            if s_i == 0:
                s = str(trans_data[9][item]) + " 容量上限为0"
                print(s)
            else:
                p_i = trans_data[3][item]
                q_i = trans_data[4][item]
                p_j = trans_data[5][item]
                q_j = trans_data[6][item]
                #print((p_i,q_i,p_j,q_j,s_i))
                if p_i*p_i + q_i*q_i <= s_i*s_i and p_j*p_j + q_j*q_j <= s_i*s_i:
                    pass
                elif p_i*p_i + q_i*q_i <= s_i*s_i:
                    s = str(trans_data[9][item]) + " J侧容量超过上限"
                    print(s)
                    true_flag = False
                elif p_j*p_j + q_j*q_j <= s_i*s_i:
                    s = str(trans_data[9][item]) + " I侧容量超过上限"
                    print(s)
                    true_flag = False
                else:
                    s = str(trans_data[9][item]) + " 双侧容量超过上限"
                    print(s)
                    true_flag = False

    print("检验完成")
    print("-----------------------------")



#发电机
def check_generator_data():
    global true_flag
    generator_data = pd.read_csv('LF.LP5', header=None, sep=',')
    generator_standard = pd.read_csv('LF.L5', header=None, sep=',')
    for i in [1,2]:
        generator_data[i] = pd.to_numeric(generator_data[i])
    for i in [8,9,10,11]:
        generator_standard[i] = pd.to_numeric(generator_standard[i])

    print("-----------------------------")
    print("发电机结果检验:")
    for i in generator_data.index:
        p_generator = generator_data[1][i]
        #print(p_generator)
        q_generator = generator_data[2][i]
        #print(q_generator)
        indexs = generator_standard[(generator_standard[18] == generator_data[4][i])].index.tolist()
        if indexs:
            i = indexs[0]
            p_min = generator_standard[10][i]
            p_max = generator_standard[9][i]
            q_min = generator_standard[8][i]
            q_max = generator_standard[7][i]

            if p_generator < p_min != 0:
                s = str(generator_data[4][i]) + "有功功率数据低于下限"
                print(s)
                true_flag = False
            if p_generator > p_max != 0:
                s = str(generator_data[4][i]) + "有功功率数据高于上限"
                print(s)
                true_flag = False
            if q_generator < q_min != 0:
                s = str(generator_data[4][i]) + "无功功率数据低于下限"
                print(s)
                true_flag = False
            if q_generator > q_max != 0:
                s = str(generator_data[4][i]) + "无功功率数据高于上限"
                print(s)
                true_flag = False
    print("检验完成")
    print("-----------------------------")

#负荷
def check_load_data():
    global true_flag
    load_data = pd.read_csv('LF.LP6', header=None, sep=',')
    load_standard = pd.read_csv('LF.L6', header=None, sep=',')
    for i in [2,3]:
        load_data[i] = pd.to_numeric(load_data[i])
    for i in [8,9,10,11]:
        load_standard[i] = pd.to_numeric(load_standard[i])

    print("-----------------------------")
    print("负荷结果检验:")
    for i in load_data.index:
        p_generator = load_data[2][i]
        #print(p_generator)
        q_generator = load_data[3][i]
        #print(q_generator)
        indexs = load_standard[(load_standard[18] == load_data[4][i])].index.tolist()
        if indexs:
            i = indexs[0]
            p_min = load_standard[11][i]
            p_max = load_standard[10][i]
            q_min = load_standard[9][i]
            q_max = load_standard[8][i]

            if p_generator < p_min != 0:
                s = str(load_data[4][i]) + "有功功率数据低于下限"
                print(s)
                true_flag = False
            if p_generator > p_max != 0:
                s = str(load_data[4][i]) + "有功功率数据高于上限"
                print(s)
                true_flag = False
            if q_generator < q_min != 0:
                s = str(load_data[4][i]) + "无功功率数据低于下限"
                print(s)
                true_flag = False
            if q_generator > q_max != 0:
                s = str(load_data[4][i]) + "无功功率数据高于上限"
                print(s)
                true_flag = False
    print("检验完成")
    print("-----------------------------")

if __name__ == "__main__":
    #true_flag = True
    check_constriction()
    check_load_data()
    check_generator_data()
    check_trans_data()
    check_ac_data()
    check_bus_data()
    if true_flag == True:
        print("潮流计算结果合理")
    else:
        print("潮流计算结果不合理")