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

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../includes/')
import levenshteinDistance as ld

class CharacterModel():
	modelDict , matras, reportThisMap = None, None, None

	def __init__(self):
		self.modelDict = {}
		matras = ['া', 'ি', 'ী', 'ু', 'ূ', 'ে', 'ৈ', 'ো', 'ৌ', 'ৃ', 'ঁ', 'ং', 'ঃ', '়']
		self.matras = [matra.decode('utf8') for matra in matras]
		self.reportThisMap = False

	#'n' this is the character showing nothing
	def addStringToModelDict(self, ocr, orig): #these two string should be of the same size
		ocrLen = len(ocr)
		origLen = len(orig)
		if ocrLen <= origLen:
			ocr += 'n' * (origLen - ocrLen)
		else:
			orig += 'n' * (ocrLen - origLen)

		for origChar,ocrChar in zip(orig, ocr):
			self.addCharToModelDict(ocrChar, origChar)

	def addCharToModelDict(self, ocrChar, origChar):
		if origChar in self.modelDict:
			if ocrChar in self.modelDict[origChar]:
				self.modelDict[origChar][ocrChar] += 1
			else:
				self.modelDict[origChar][ocrChar] = 1
		else:
			self.modelDict[origChar] = {ocrChar : 1}

	def countMatras(self, string):
		cnt = 0
		for char in string:
			if char in self.matras:
				cnt += 1
		return cnt

	def countChars(self, string):
		return len(string) - self.countMatras(string)

	def getChars(self, string):
		chars = ''
		for char in string:
			if char not in self.matras:
				chars += char
		return chars

	def getMatras(self, string):
		chars = ''
		for char in string:
			if char in self.matras:
				chars += char
		return chars

	def mapCommonPeripherals(self, ocr, orig):
		ocrLen = len(ocr)
		origLen = len(orig)
		origCharF = 0
		ocrCharF = 0
		while ocrCharF < ocrLen and origCharF < origLen:
			if ocr[ocrCharF] == orig[origCharF]:
				self.addCharToModelDict(ocr[ocrCharF], orig[origCharF])
				origCharF += 1
				ocrCharF += 1
			else:
				break
		#after match ocr/origCharF if pointing to the char after match
		origCharB = -1
		ocrCharB = -1
		while ocrCharB >= -ocrLen + ocrCharF and origCharB >= -origLen + origCharF:
			if ocr[ocrCharB] == orig[origCharB]:
				self.addCharToModelDict(ocr[ocrCharB], orig[origCharB])
				origCharB -= 1
				ocrCharB -= 1
			else:
				break
		return ocr[ocrCharF : None if ocrCharB == -1 else ocrCharB + 1], orig[origCharF : None if origCharB == -1 else origCharB + 1]

	def doIntelMapping(self, ocr, orig):
		self.reportThisMap = False
		ocrLen = len(ocr)
		origLen = len(orig)
		if ocrLen < origLen:
			origCharF,ocrCharF = 0,0
			diff = origLen - ocrLen
			for ocrChar in range(ocrLen):
				for origChar in range(origCharF, (origCharF + diff + 1) if (origCharF + diff) < origLen else origLen): #1 is added to cop with the behaviour of range, in condiditon check it is not there.
					if ocr[ocrChar] == orig[origChar]:
						self.addCharToModelDict(ocr[ocrChar], orig[origChar])
						self.addStringToModelDict(ocr[ocrCharF:ocrChar], orig[origCharF:origChar]) #adding the string before the current map which isn't matched
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
							self.addCharToModelDict(ocr[ocrChar], orig[origChar])
							self.addStringToModelDict(ocr[ocrCharF:ocrChar], orig[origCharF:origChar])
							diff = diff + origChar - ocrChar if ocrChar >= origChar else diff - origChar + ocrChar
							ocrCharF = ocrChar + 1
							origCharF = origChar + 1
		#if still some of the character remained then can't do anything, print info about this case
		if ocrCharF != ocrLen or origCharF != origLen:
			self.reportThisMap = True

	def addToModel(self, ocr, orig):
		ocrLen = len(ocr)
		origLen = len(orig)
		if ocrLen == origLen:
			self.addStringToModelDict(ocr, orig)
		else:
			ocr, orig = self.mapCommonPeripherals(ocr, orig)
			ocrLen, origLen = len(ocr), len(orig)
			if ocrLen == 0: #ocr complete
				self.addStringToModelDict(origLen * 'n', orig)
			elif origLen == 0: #orig complete
				self.addStringToModelDict(ocr, ocrLen * 'n')
			elif self.countChars(ocr) == self.countChars(orig) and self.countChars(ocr) > 0: #2nd condition to check the case when there is no chars at all, only self.matras
				self.addStringToModelDict(self.getChars(ocr), self.getChars(orig))
				self.addToModel(self.getMatras(ocr), self.getMatras(orig))
			elif self.countMatras(ocr) == self.countMatras(orig) and self.countMatras(ocr) > 0:
				self.addStringToModelDict(self.getMatras(ocr), self.getMatras(orig))
				self.addToModel(self.getChars(ocr), self.getChars(orig))
			else:
				self.doIntelMapping(ocr, orig)

	def dumpModelDict(self, fileName):
		with codecs.open(fileName, 'w', encoding='utf8') as output:
			json.dump(self.modelDict, output, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)

	def readStoredModel(self, fileName):
		with codecs.open(fileName, 'r', encoding='utf8') as output:
			self.modelDict = json.load(output)

	def forPair(self, ocr, orig):
		ocr, orig = ocr.decode('utf8'), orig.decode('utf8')
		print ocr.encode('utf8'), orig.encode('utf8')
		self.addToModel(ocr, orig)
		if self.reportThisMap == True:
			#reporting the info
			print "File: " + direc.split('>')[0] + direc.split('>')[-1] + '/' + fl + "\n" + ocr[i] + "  " + orig[j] + "\n"
		self.dumpModelDict('characterErrorModelForPair')

	def forCorpus(self, corpus_ocr, corpus_orig, readModelFileName):
		pattern = re.compile("[a-zA-Z]+")
		files_ocr = {}

		if readModelFileName:
			self.readStoredModel(readModelFileName)

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
								self.reportThisMap = False
								self.addToModel(ocr[i], orig[j])
								if self.reportThisMap == True:
									#reporting the info
									print "File: " + direc.split('>')[0] + direc.split('>')[-1] + '/' + fl + "\n" + ocr[i] + "  " + orig[j] + "\n"
								# print ocr[i].encode('utf8'), orig[j].encode('utf8')
						i += 1
					# sys.exit()
		self.dumpModelDict('characterErrorModel')

# forPair('বজেঢ', 'বাজেট')
a = CharacterModel()
# a.readStoredModel('characterErrorModel.json')
a.forPair('বজেঢ', 'বাজেট')