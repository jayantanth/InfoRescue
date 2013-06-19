#!/usr/bin/env python
# -*- coding: utf-8 -*-

#############
#Assumptions:
#punctuations is removed from the data

import sys
import os
import re
import json
import codecs

sys.path.insert(0, '../includes/')
import levenshteinDistance as ld

if len(sys.argv) == 2 and sys.argv[1] == '-h':
	print("Usage: ./characterErrorModel.py <ocrData> <originalData> <outputFile> <read the Model first y/n>")
	sys.exit()
elif len(sys.argv) != 5:
	print "Invalid number of arguments. Try './characterErrorModel.py -h'"
	sys.exit()

corpus_ocr = sys.argv[1]
corpus_orig = sys.argv[2]
outputFile = sys.argv[3]
readModel = sys.argv[4]

modelDict = {}
matras = ['া', 'ি', 'ী', 'ু', 'ূ', 'ে', 'ৈ', 'ো', 'ৌ', 'ৃ', 'ঁ', 'ং', 'ঃ', '়']
matras = [matra.decode('utf8') for matra in matras]
reportThisMap = False

#'n' this is the character showing nothing
def addStringToModelDict(ocr, orig): #these two string should be of the same size
	ocrLen = len(ocr)
	origLen = len(orig)
	if ocrLen <= origLen:
		ocr += 'n' * (origLen - ocrLen)
	else:
		orig += 'n' * (ocrLen - origLen)

	for origChar,ocrChar in zip(orig, ocr):
		addCharToModelDict(ocrChar, origChar)

def addCharToModelDict(ocrChar, origChar):
	if origChar in modelDict:
		if ocrChar in modelDict[origChar]:
			modelDict[origChar][ocrChar] += 1
		else:
			modelDict[origChar][ocrChar] = 1
	else:
		modelDict[origChar] = {ocrChar : 1}

def countMatras(string):
	cnt = 0
	for char in string:
		if char in matras:
			cnt += 1
	return cnt

def countChars(string):
	return len(string) - countMatras(string)

def getChars(string):
	chars = ''
	for char in string:
		if char not in matras:
			chars += char
	return chars

def getMatras(string):
	chars = ''
	for char in string:
		if char in matras:
			chars += char
	return chars

def mapCommonPeripherals(ocr, orig):
	ocrLen = len(ocr)
	origLen = len(orig)
	origCharF = 0
	ocrCharF = 0
	while ocrCharF < ocrLen and origCharF < origLen:
		if ocr[ocrCharF] == orig[origCharF]:
			addCharToModelDict(ocr[ocrCharF], orig[origCharF])
			origCharF += 1
			ocrCharF += 1
		else:
			break
	#after match ocr/origCharF if pointing to the char after match
	origCharB = -1
	ocrCharB = -1
	while ocrCharB >= -ocrLen + ocrCharF and origCharB >= -origLen + origCharF:
		if ocr[ocrCharB] == orig[origCharB]:
			addCharToModelDict(ocr[ocrCharB], orig[origCharB])
			origCharB -= 1
			ocrCharB -= 1
		else:
			break
	return ocr[ocrCharF : None if ocrCharB == -1 else ocrCharB + 1], orig[origCharF : None if origCharB == -1 else origCharB + 1]

def doIntelMapping(ocr, orig):
	reportThisMap = False
	ocrLen = len(ocr)
	origLen = len(orig)
	if ocrLen < origLen:
		origCharF,ocrCharF = 0,0
		diff = origLen - ocrLen
		for ocrChar in range(ocrLen):
			for origChar in range(origCharF, (origCharF + diff + 1) if (origCharF + diff) < origLen else origLen): #1 is added to cop with the behaviour of range, in condiditon check it is not there.
				if ocr[ocrChar] == orig[origChar]:
					addCharToModelDict(ocr[ocrChar], orig[origChar])
					addStringToModelDict(ocr[ocrCharF:ocrChar], orig[origCharF:origChar]) #adding the string before the current map which isn't matched
					diff = diff - origChar + origCharF #changing the diff accordingly, origChar (~ (origCharF, origCharF + diff)
					ocrCharF = ocrChar + 1
					origCharF = origChar + 1
	else:
		origCharF,ocrCharF = 0,0
		diff = ocrLen - origLen
		for ocrChar in range(ocrLen):
			for origChar in range(origCharF, origLen): #checking in complete orig for the case when some existing character are changed not just introduced
				if origChar - diff <= ocrChar <= origChar + diff and ocr[ocrChar] == orig[origChar]:
					if orig[origChar] not in orig[origChar+1:] or ocrChar <= orig.index(orig[origChar]) + diff:# check for the case when exists repeated character and the first occurence is get change and is get mapped to the second occurence
						addCharToModelDict(ocr[ocrChar], orig[origChar])
						addStringToModelDict(ocr[ocrCharF:ocrChar], orig[origCharF:origChar])
						diff = diff + origChar - ocrChar if ocrChar >= origChar else diff - origChar + ocrChar
						ocrCharF = ocrChar + 1
						origCharF = origChar + 1
	#if still some of the character remained then can't do anything, print info about this case
	if ocrCharF != ocrLen or origCharF != origLen:
		reportThisMap = True

def addToModel(ocr, orig):
	ocrLen = len(ocr)
	origLen = len(orig)
	if ocrLen == origLen:
		addStringToModelDict(ocr, orig)
	else:
		ocr, orig = mapCommonPeripherals(ocr, orig)
		ocrLen, origLen = len(ocr), len(orig)
		if ocrLen == 0: #ocr complete
			addStringToModelDict(origLen * 'n', orig)
		elif origLen == 0: #orig complete
			addStringToModelDict(ocr, ocrLen * 'n')
		elif countChars(ocr) == countChars(orig) and countChars(ocr) > 0: #2nd condition to check the case when there is no chars at all, only matras
			addStringToModelDict(getChars(ocr), getChars(orig))
			addToModel(getMatras(ocr), getMatras(orig))
		elif countMatras(ocr) == countMatras(orig) and countMatras(ocr) > 0:
			addStringToModelDict(getMatras(ocr), getMatras(orig))
			addToModel(getChars(ocr), getChars(orig))
		else:
			doIntelMapping(ocr, orig)

def dumpModelDict():
	with codecs.open(outputFile, 'w', encoding='utf8') as output:
		json.dump(modelDict, output, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)

def readStoredModel():
	with codecs.open(outputFile, 'r', encoding='utf8') as output:
		modelDict = json.load(output)

def forPair(ocr, orig):
	ocr, orig = ocr.decode('utf8'), orig.decode('utf8')
	print ocr.encode('utf8'), orig.encode('utf8')
	addToModel(ocr, orig)
	if reportThisMap == True:
		#reporting the info
		print "File: " + direc.split('>')[0] + direc.split('>')[-1] + '/' + fl + "\n" + ocr[i] + "  " + orig[j] + "\n"
	dumpModelDict()

def forCorpus():
	pattern = re.compile("[a-zA-Z]+")
	files_ocr = {}

	if readModel == 'y':
		readStoredModel()

	for (dirpath, dirname, filenames) in os.walk(corpus_ocr):
		if pattern.match(dirpath.split("/")[-1]):
			files_ocr[dirpath.split("/")[-2][:4] + ">" + dirpath.split("/")[-1]] = filenames

	files_orig = {}
	for (dirpath, dirname, filenames) in os.walk(corpus_orig):
	    if pattern.match(dirpath.split("/")[-1]):
		    files_orig[dirpath.split("/")[-2][:4] + ">" + dirpath.split("/")[-1]] = filenames

	for direc in files_ocr.keys():
		print direc
		for fl in files_ocr[direc]:
			with open(corpus_ocr + direc.split('>')[0] + 'ocr/' + direc.split('>')[-1] + '/' + fl, 'r') as fl_ocr, open(corpus_orig + direc.split('>')[0] + 'txt/' + direc.split('>')[-1] + '/' + fl, 'r') as fl_orig:
				ocr = re.sub(r"\n+", '', fl_ocr.read().strip().decode('utf8')).split()
				orig = re.sub(r"\n+", '', fl_orig.read().strip().decode('utf8')).split()
				i,j = 0,0
				origLen = len(orig)
				while i < len(ocr) and j < origLen:
					if(len(ocr[i]) > 3):
						minLDist = 1000
						for k in range(10 if origLen - j >= 10 else origLen - j):
							lDist = ld.levenshtein(ocr[i], orig[j + k])
							if lDist < minLDist:
								minLDist = lDist
								jInc = k

						if minLDist <= 6:
							j += jInc
							reportThisMap = False
							addToModel(ocr[i], orig[j])
							if reportThisMap == True:
								#reporting the info
								print "File: " + direc.split('>')[0] + direc.split('>')[-1] + '/' + fl + "\n" + ocr[i] + "  " + orig[j] + "\n"
							# print ocr[i].encode('utf8'), orig[j].encode('utf8')
					i += 1
				# sys.exit()
	dumpModelDict()

forCorpus()
# forPair('বজেঢ', 'বাজেট')