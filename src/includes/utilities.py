#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This contain several common function specially relted to Character Error Model.

*Magic Numbers*:
    THRESHOLD : The threshold above which we consider that ocrChar charatcer can be the errorneous form of origChar. 
"""

import json
import codecs

THRESHOLD = 0.4
modelDict = {}
minProb = 1

def getCEM(CEMFile):
    """
    Read charatcer error model to store it in *modelDict*.

    *Parameters*:
        CEMFile : Path to CEM file.

    *Returns*:
        --
    """
    global modelDict
    with codecs.open(CEMFile, 'r', encoding='utf8') as output:
        modelDict = json.load(output)
    for char in modelDict:
        for mappedChar in modelDict[char]:
           modelDict[char][mappedChar] = float(modelDict[char][mappedChar])

def getMinimumProbability():
    """
    Returns the minimum probabiltiy in the Character Error Model.
    """
    return min(min(mappedChars.values()) for mappedChars in modelDict.values())

def increaseProbability(minProb):
    """
    Increase the each probability in the Character Error Model with minProb.

    *Parameters*:
        minProb : Probability to increase

    *Returns*:
        --
    """
    for origChar in modelDict:
        for ocrChar in modelDict[origChar]:
            modelDict[origChar][ocrChar] += minProb

def prob_equals(ocrChar, origChar):
    """
    Check whether the probability of origChar to be interpreted as ocrChar is greater than THRESHOLD or not.

    *Parameters*:
        ocrChar : Errorneous charatcer
        origChar : Original charatcer

    *Returns*:
        Boolean
    """
    try:
        if modelDict[origChar][ocrChar] >= THRESHOLD:
            return True
        return False
    except KeyError:
        return False

def getProb(ocrChar, origChar):
    """
    Return the probability of origChar to be interpreted as ocrChar.

    *Parameters*:
        ocrChar : Errorneous charatcer
        origChar : Original charatcer

    *Returns*:
        Probability of the pair and minProb if that pair doesnot exist in the Character Error Model
    
    """
    try:
        return modelDict[origChar][ocrChar]
    except KeyError:
        return minProb

def printTable(table):
    """
    Prints a 2D matrix or list of list.

    *Parameters*:
        table : 2D object

    *Returns*:
        --
    """
    for row in table:
        for column in row:
            print "%3s"%column,
        print