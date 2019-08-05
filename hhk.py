# -*- coding: utf-8 -*-
#python3
import random
import os
from tkinter import *
import tkinter.scrolledtext
from PIL import Image, ImageTk

def readfile(filename):
    mx = []
    with open(filename, 'r', encoding='utf-8') as f:
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
def getflag():
    with open("LF.CAL") as f:
        line = f.readline()
        line = line.strip().split(',')
    success = int(line[0])
    return success == 1
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
def Lrandom():
    mx = readfile("LF.L6")
    ratio = 5
    for i in range(len(mx)):
        mx[i][4] = random.random() * ratio
    writefile("LF.L6", mx)
#
def set0G():
    mx = readfile("LF.L5")
    name = 0
    ret = []
    for row, line in enumerate(mx):
        if line[2] != 0:
            tempold = mx[row][2]
            mx[row][2] = 0
            name = line[-1]
            writefile("LF.L5", mx)
            os.system("WMLFRTMsg")
            if getflag():
                ret.append([name, readslackval(readslack(),name)])
            mx[row][2] = tempold
            writefile("LF.L5", mx)
    return ret
#
#-----------------------------------------
    
    
def outputln( s):
    e.config(state="normal")
    e.insert("end", s)
    e.see("end")
    e.config(state="disabled")
def submit():
    r = inputw.get()
    outputln("your input: " + r + '\n')
    inputw.delete(0, "end")
    r = r.split()
    a = flag
    mess = "no operation! ^\n"
    if a == '3':
        mess = findinsql.searchrange(r, edges)
    outputln(mess)
    outputln(sline)
CALLBACKMEM = ''
def callback( a):
    global CALLBACKMEM
    flag = a
    if a == '1':
        sss = 0
        if sss == 1:
            Lrandom()
        else:
            line = None
            with open('errorseg.txt') as f:
                lines = f.readlines()
                line = list(eval(lines[0].strip()))
            ##
            mxL6 = readfile('LF.L6')
            rowsN = len(mxL6)
            for i in range(rowsN):
                mxL6[i][4] = line[i * 2]
                mxL6[i][5] = line[i * 2 + 1]
            writefile('LF.L6', mxL6)
            #
            line = None
            with open('originL5.txt') as f:
                lines = f.readlines()
                line = list(eval(lines[0].strip()))
            ##
            mxL5 = readfile('LF.L5')
            rowsN = len(mxL5)
            for i in range(rowsN):
                mxL5[i][3] = line[i * 2]
                mxL5[i][4] = line[i * 2 + 1]
            writefile('LF.L5', mxL5)
        outputln("已随机写入LF.L6\n")
    if a == '2':
        os.system("WMLFRTMsg")
        if getflag():
            outputln("计算成功!\n")
        else:
            outputln("计算不成功!\n")
        outputln(sline)
    if a == '3':
        outputln("搜索知识库...\n")
        mxL6 = readfile('LF.L6')
        parasL6 = []
        for i in mxL6:
            parasL6.append(i[4])
            parasL6.append(i[5])
        sol = None
        with open('errors.txt') as f:
            lines = f.readlines()
            lineN = -1
            for lineid, line in enumerate(lines):
                line = eval(line.strip())
                # print(line)
                equ = 1
                for iid, i in enumerate(line):
                    if i != parasL6[iid]:
                        equ = 0
                        break
                if equ == 1:
                    lineN = lineid
                    break
            if lineN != -1:
                sol = eval(lines[lineN + 1].strip())
        if sol != None:
            outputln("使用第 2 条知识: 修改有变动负荷附近发电机的出力\n")
            mxL5 = readfile('LF.L5')
            rowsN = len(mxL5)
            for i in range(rowsN):
                if mxL5[i][3] != sol[i * 2]:
                    outputln("建议修改:%s\nP:%s\tQ:%s\n" % (mxL5[i][-1], sol[i * 2], sol[i * 2 + 1]))
            CALLBACKMEM = sol
            return 
        outputln("正在使用第 1 条知识: 设置平衡机观察有功平衡情况\n")
        ret = set0G()
        outputln("建议修改:\n")
        for i in ret:
            outputln("%s: P:%s\tQ:%s\n" % (i[0], i[1][0], i[1][1]))
            CALLBACKMEM = ret[0]
            return 
    if a == '4':
        outputln(help + '\n')
    if a == '5':
        if CALLBACKMEM == '':
            callback('3')
        mxL5 = readfile('LF.L5')
        if type(CALLBACKMEM) == type([]):
            for lineid, line in enumerate(mxL5):
                if line[-1] == CALLBACKMEM[0]:
                    mxL5[lineid][3] = float(CALLBACKMEM[1][0])
                    mxL5[lineid][4] = float(CALLBACKMEM[1][1])
        else:
            rowsN = len(mxL5)
            for i in range(rowsN):
                mxL5[i][3] = CALLBACKMEM[i * 2]
                mxL5[i][4] = CALLBACKMEM[i * 2 + 1]
        writefile('LF.L5', mxL5)
        CALLBACKMEM = ''
        outputln("修改成功!\n")
    if a == '6':
        outputln("input student id:\n")
    if a == '7':
        outputln("input stu_id, book_id(split by blank):\n")
    if a == '8':
        outputln("input stu_id, book_id(split by blank):\n")
    if a == '9':
        mess = utils.allborrows(client, namespace)
        outputln("all books borrowed\n")
        outputln(mess)
        outputln(sline)
    if a == 'x':
        root.destroy()
#
def paras():
    def submit():
        ttt = text.get("0.0", "end").split('\n')
        flag = 0
        row = 0
        for line in ttt:
            if len(line) == 0:
                continue
            if line[0] == '=':
                flag = -1
                continue
            if flag == -1:
                flag = -2
                continue
            if flag == -2:
                flag = 1
                continue
            if line[0] == '-':
                flag += 1
                row = 0
                continue
            if flag == 1:
                temp = line.split()
                mxL6[row][1] = int(temp[0])
                mxL6[row][2] = int(temp[1])
                mxL6[row][4] = float(temp[2])
                mxL6[row][5] = float(temp[3])
                mxL6[row][-1] = temp[4]
                row += 1
                continue
            if flag == 2:
                temp = line.split()
                mxL5[row][1] = int(temp[0])
                mxL5[row][2] = int(temp[1])
                mxL5[row][3] = float(temp[2])
                mxL5[row][4] = float(temp[3])
                mxL5[row][-1] = temp[4]
                row += 1
                continue
        #
        writefile("LF.L5", mxL5)
        writefile("LF.L6", mxL6)
        biu.destroy()
        return
    biu = Tk(className = 'paras')
    text = tkinter.scrolledtext.ScrolledText(biu, width = 80, height = 27)
    text.pack(padx=5)
    text.insert(0.0, "负荷\n")
    text.insert('end', "母线\t编号\tP\tQ\t名称\n----------------------------------\n")
    mxL6 = readfile("LF.L6")
    for i in mxL6:
        tpstr = str(i[1]) + '\t' + str(i[2]) + '\t' + str(i[4]) + '\t' + str(i[5]) + '\t' + str(i[-1]) + '\n'
        text.insert('end', tpstr)
    text.insert('end', "======================================\n发电机\n")
    text.insert('end', "母线\t类型\tP\tQ\t名称\n----------------------------------\n")
    mxL5 = readfile("LF.L5")
    for i in mxL5:
        tpstr = str(i[1]) + '\t' + str(i[2]) + '\t' + str(i[3]) + '\t' + str(i[4]) + '\t' + str(i[-1]) + '\n'
        text.insert('end', tpstr)
    Button(biu, text="确认",command=lambda: submit() , width = 10).pack()
    biu.mainloop()
#
def knowledgetext():
    biu = Tk(className = '知识文本')
    text = tkinter.scrolledtext.ScrolledText(biu, width = 80, height = 27)
    text.pack(padx=5)
    text.insert(0.0, "编号\t条件\t\t目的\t\t处理方法\t\t处理结果\n------------------------------------------------------------------------\n")
    txt = []
    num = 0
    with open("知识.txt") as f:
        lines = f.readlines()
        for line in lines:
            num += 1
            templine = line.strip().split()
            text.insert('end', str(num) + '\t')
            for i in templine:
                text.insert('end', i+'\t\t')
            text.insert('end', '\n')
    #print(text.get(0.0, 'end'))
    biu.mainloop()
if __name__ == "__main__":
    root = Tk(className = "LoadFlowCalculation Helper")
    welcome = '''
-----------------------------------------------
   welcome ~ 
-----------------------------------------------
                              HIT
-----------------------------------------------
'''
    help = '''  
'''
    sline = '-----------------------------------------------\n'
    # root.geometry("700x500")
    frame1 = Frame(root)
    frame1.grid(row = 0, column = 0)
    frame = Frame(root)
    frame.grid(row = 1, column = 1)
    Button(frame, text="随机负荷",command=lambda: callback('1') , width = 14).grid(row=0,column=0)
    Button(frame, text="潮流计算",command=lambda: callback('2') , width = 10).grid(row=0,column=1)
    Button(frame, text="搜索方案",command=lambda: callback('3') , width = 16).grid(row=0,column=2)
    Button(frame, text="help",command=lambda: callback('4') , width = 6).grid(row=0,column=3)
    Button(frame, text="exit",command=lambda: callback('x') , width = 10).grid(row=0,column=9)
    
    
    
    e = tkinter.scrolledtext.ScrolledText(frame1, width = 80, height = 27)
    e.pack(padx=5)
    
    
    w1 = Label(frame1,text="input text here: ")
    w1.pack()
    b = Button(frame1, text="submit",command=submit , width = 10)
    b.pack(side=RIGHT)
    v = StringVar()
    e1 = Entry(frame1, textvariable=v, width = 40)
    v.set("")
    inputw = e1
    v = v
    e1.pack()
    ##
    e.insert(0.0, welcome)
    e.insert("end", help)
    e.insert("end", "click a button now ~\n")
    e.insert("end", sline)
    e.config(state="disabled")
    #
    buttonsleft = Frame(frame1)
    buttonsleft.pack()
    Button(buttonsleft, text="查看/修改参数",command=lambda: paras() , width = 16).grid(row=0,column=1)
    Button(buttonsleft, text="查看知识库",command=lambda: knowledgetext() , width = 16).grid(row=0,column=2)
    Button(buttonsleft, text="自动修改",command=lambda: callback('5') , width = 16).grid(row=0,column=3)
    
    canvas = Canvas(root, width=650,height=450,bg='white')
    img = Image.open('9.bmp')  # 打开图片
    photo = ImageTk.PhotoImage(img)
    canvas.create_image(20,20,anchor=NW,image = photo)
    canvas.grid(row=0, column=1)
    
    root.mainloop()
    #Lrandom()
    #set0G()