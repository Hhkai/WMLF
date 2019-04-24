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
def con2dict(G):
    row_n = len(G)
    for i in G:
        assert(len(i)==row_n)
    G_dict = dict()
    for rowid, row in enumerate(G):
        G_dict[rowid+1] = dict()
        for colid in range(rowid, row_n):
            if colid == rowid:
                G_dict[rowid+1][colid+1] = row[colid]
            else:
                if row[colid] != 0:
                    G_dict[rowid+1][colid+1] = row[colid]
    #
    return G_dict
#
if __name__ == "__main__":
    mL5Col4(0.0,0.0,0.0,0.0,0.0,0.0,0.0)
