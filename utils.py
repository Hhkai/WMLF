def mL5Col4(*values):
    assert(len(values) == 7)
    # read file to memory
    data_list = []
    with open("LF.L5") as f:
        lines = f.readlines()
        for line in lines:
            data_list.append(list(eval(line.strip())))
    
    # modify the values 
    for row in range(1, 8):
        data_list[row][3] = values[row - 1]
    
    # write back
    with open("LF.L5", "w") as f:
        for line in data_list:
            f.write(str(line)[1:-1] + ',\n')
#
if __name__ == "__main__":
    mL5Col4(0.0,0.0,0.0,0.0,0.0,0.0,0.0)
