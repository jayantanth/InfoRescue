#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import json
import codecs

THRESHOLD = 0.02
modelDict = {}

def getCEM(CEMFile):
    global modelDict
    with codecs.open(CEMFile, 'r', encoding='utf8') as output:
        modelDict = json.load(output)
    for char in modelDict:
        for mappedChar in modelDict[char]:
           modelDict[char][mappedChar] = float(modelDict[char][mappedChar])

def prob_equals(ocrChar, origChar):
    if modelDict[origChar][ocrChar] >= THRESHOLD:
        return True
    return False

def printTable(table, m, n):
    for i in range(m+1):
        for j in range(n+1):
            print table[i,j],
        print

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

    # printTable(table, m, n)
    lcss = [[]]
    def recon(i, j, index):
        if i == 0 or j == 0:
            return
        elif prob_equals(ocr[i-1], orig[j-1]):
            if table[i-1, j] > table[i-1, j-1]:
                lcss.append(copy.deepcopy(lcss[index]))
                recon(i-1, j, len(lcss) - 1)
            if table[i, j-1] > table[i-1, j-1]:
                lcss.append(copy.deepcopy(lcss[index]))
                recon(i, j-1, len(lcss) - 1)
            # lcss[index].insert(0, (ocr[i-1],i-1, j-1))
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

    recon(m, n, 0)
    return removeDuplicate(lcss)

# print lcs('ABCBDAB', 'BDCABA')
# print lcs('AGCGA', 'CAGATAGAG')
# getCEM('../features/characterErrorModelProbalistic.json')
# print lcs('চাহুর','রাহুর')