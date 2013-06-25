#!/usr/bin/env python

import copy

def printTable(table, n, m):
    for i in range(n+1):
        for j in range(m+1):
            print table[i,j],
        print

def lcs(x, y):
    n = len(x)
    m = len(y)
    table = dict()

    for i in range(n+1):
        for j in range(m+1):
            if i == 0 or j == 0:
                table[i, j] = 0
            elif x[i-1] == y[j-1]:
                table[i, j] = table[i-1, j-1] + 1
            else:
                table[i, j] = max(table[i-1, j], table[i, j-1])

    # printTable(table, n, m)
    lcss = [[]]
    def recon(i, j, index):
        if i == 0 or j == 0:
            return
        elif x[i-1] == y[j-1]:
            if table[i-1, j] > table[i-1, j-1]:
                lcss.append(copy.deepcopy(lcss[index]))
                recon(i-1, j, len(lcss) - 1)
            if table[i, j-1] > table[i-1, j-1]:
                lcss.append(copy.deepcopy(lcss[index]))
                recon(i, j-1, len(lcss) - 1)
            # lcss[index].insert(0, (x[i-1],i-1, j-1))
            lcss[index].insert(0, (i-1, j-1))
            recon(i-1, j-1, index)
        elif table[i-1, j] == table[i, j-1]:
            lcss.append(copy.deepcopy(lcss[index]))
            newIndex = len(lcss) - 1
            recon(i-1, j, index)
            recon(i, j-1, newIndex)
        elif table[i-1, j] > table[i, j-1]:
            recon(i-1, j, index)
        else:
            recon(i, j-1, index)

    recon(n, m, 0)
    return lcss

# print lcs('ABCBDAB', 'BDCABA')
# print lcs('AGCGA', 'CAGATAGAG')