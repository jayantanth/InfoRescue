#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import re

sys.path.insert(0, '../includes/')
import levenshteinDistance as ld

if len(sys.argv) == 2 and sys.argv[1] == '-h':
	print("Usage: ./characterErrorModel.py <ocrData> <originalData> <outputFile>")
	sys.exit()
elif len(sys.argv) != 4:
	print "Invalid number of arguments. Try './characterErrorModel.py -h'"
	sys.exit()

corpus_ocr = sys.argv[1]
corpus_orig = sys.argv[2]
outputFile = sys.argv[3]

pattern = re.compile("[a-zA-Z]+")
files_ocr = {}

for (dirpath, dirname, filenames) in os.walk(corpus_ocr):
	if pattern.match(dirpath.split("/")[-1]):
		files_ocr[dirpath.split("/")[-2][:4] + "-" + dirpath.split("/")[-1]] = filenames

files_orig = {}
for (dirpath, dirname, filenames) in os.walk(corpus_orig):
    if pattern.match(dirpath.split("/")[-1]):
	    files_orig[dirpath.split("/")[-2][:4] + "-" + dirpath.split("/")[-1]] = filenames

for direc in files_ocr.keys():
	for fl in files_ocr[direc]:
		with open(corpus_ocr + direc.split('-')[0] + 'ocr/' + direc.split('-')[-1] + '/' + fl, 'r') as fl_ocr, open(corpus_orig + direc.split('-')[0] + 'txt/' + direc.split('-')[-1] + '/' + fl, 'r') as fl_orig:
			ocr = re.sub(r"\n+", '', fl_ocr.read().strip().decode('utf8')).split()
			orig = re.sub(r"\n+", '', fl_orig.read().strip().decode('utf8')).split()
			# print direc.split('-')[0] + '/' + direc.split('-')[-1]+ '/' + fl
			# print len(ocr), len(orig)
			# print len(ocr.split('।'.decode('utf8'))), len(orig.split('।'.decode('utf8')))
			# print len(ocr.split('\n')), len(orig.split('\n'))
			# print len(ocr.split(' ')), len(orig.split(' '))
			# print
			i,j = 0,0
			while i < len(ocr) and j < len(orig) - 20:
				if(len(ocr[i]) > 4):
					minLDist = 1000
					for k in range(10):
						lDist = ld.levenshtein(ocr[i], orig[j + k])
						if lDist < minLDist:
							minLDist = lDist
							jInc = k

					if minLDist <= 2:
						j += jInc
						print ocr[i].encode('utf8'), orig[j].encode('utf8')
				i += 1
			sys.exit()