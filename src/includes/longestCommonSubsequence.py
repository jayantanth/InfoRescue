#!/usr/bin/env python

import copy

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

    lcs = ''
    def recon(i, j, lcs):
        if i == 0 or j == 0:
            return lcs
        elif x[i-1] == y[j-1]:
            if table[i-1, j] == table[i, j-1]:
                return recon(i-1, j-1, x[i-1] + lcs)
            elif table[i-1, j] > table[i, j-1]:
                return recon(i-1, j-1, x[i-1] + lcs) + ',' + recon(i-1, j, copy.copy(lcs))
            else:
                return recon(i-1, j-1, x[i-1] + lcs) + ',' + recon(i, j-1, copy.copy(lcs))
        elif table[i-1, j] == table[i, j-1]:
            return recon(i-1, j, lcs) + ',' + recon(i, j-1, copy.copy(lcs))
        elif table[i-1, j] > table[i, j-1]:
            return recon(i-1, j, lcs)
        else:
            return recon(i, j-1, lcs)
    return recon(n, m, lcs)


print lcs('ABCBDAB', 'BDCABA').split(',')