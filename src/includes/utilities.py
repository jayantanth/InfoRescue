#!/usr/bin/env python
# -*- coding: utf-8 -*-

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