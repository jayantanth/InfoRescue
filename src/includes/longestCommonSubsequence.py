#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import json
import codecs

THRESHOLD = 0.4
modelDict = {}
minProb = 1

def getCEM(CEMFile):
    global modelDict
    with codecs.open(CEMFile, 'r', encoding='utf8') as output:
        modelDict = json.load(output)
    for char in modelDict:
        for mappedChar in modelDict[char]:
           modelDict[char][mappedChar] = float(modelDict[char][mappedChar])

def getMinimumProbability():
    return min(min(mappedChars.values()) for mappedChars in modelDict.values())

def increaseProbability(minProb):
    for origChar in modelDict:
        for ocrChar in modelDict[origChar]:
            modelDict[origChar][ocrChar] += minProb

def prob_equals(ocrChar, origChar):
    try:
        if modelDict[origChar][ocrChar] >= THRESHOLD:
            return True
        return False
    except KeyError:
        return False

def getProb(ocrChar, origChar):
    try:
        return modelDict[origChar][ocrChar]
    except KeyError:
        return minProb

def printTable(table):
    for row in table:
        for column in row:
            print "%3s"%column,
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