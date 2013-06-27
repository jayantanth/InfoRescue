#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import sys

sys.path.insert(0, './')
from utilities import *

def removeDuplicate(lcss):
    setLcss = []
    for i in lcss:
        if i not in setLcss:
            setLcss.append(i)
    return setLcss

def lcs(ocr, orig):
    ocr, orig = ocr.decode('utf8'), orig.decode('utf8')
    m = len(ocr)
    n = len(orig)
    table = dict()

    for i in range(m+1):
        for j in range(n+1):
            if i == 0 or j == 0:
                table[i, j] = 0
            elif prob_equals(ocr[i-1], orig[j-1]):
                table[i, j] = table[i-1, j-1] + 1
            else:
                table[i, j] = max(table[i-1, j], table[i, j-1])

    # printTable(table)
    lcss = [[1,[]]]

    def lcssAppend(index):
        lcss.append(copy.deepcopy([lcss[index][0], lcss[index][1]]))

    def recon(i, j, index):
        if i == 0 or j == 0:
            return
        elif prob_equals(ocr[i-1], orig[j-1]):
            if table[i-1, j] > table[i-1, j-1]:
                lcssAppend(index)
                recon(i-1, j, len(lcss) - 1)
            if table[i, j-1] > table[i-1, j-1]:
                lcssAppend(index)
                recon(i, j-1, len(lcss) - 1)
            lcss[index][0] = lcss[index][0] * getProb(ocr[i-1], orig[j-1])
            # lcss[index][1].insert(0, (ocr[i-1], orig[j-1], i-1, j-1))
            lcss[index][1].insert(0, (i-1, j-1))
            recon(i-1, j-1, index)
        elif table[i-1, j] == table[i, j-1]:
            lcssAppend(index)
            newIndex = len(lcss) - 1
            recon(i-1, j, index)
            recon(i, j-1, newIndex)
        elif table[i-1, j] > table[i, j-1]:
            recon(i-1, j, index)
        else:
            recon(i, j-1, index)

    recon(m, n, 0)
    return removeDuplicate(lcss)

# print lcs('ABCBDAB', 'BDCABA')
# print lcs('AGCGA', 'CAGATAGAG')
getCEM('../features/characterErrorModelProbalistic.json')
minProb = getMinimumProbability()
increaseProbability(minProb)
# print lcs('চাহুর','রাহুর')
print lcs('চাহাচ','হচাচুচাচা')