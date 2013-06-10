#!/usr/bin/env python

import sys
import os
import re

if len(sys.argv) == 2 and sys.argv[1] == '-h':
	print("Usage: ./makeTestData.py <%> <ocrData> <originalData>")
	sys.exit()
elif len(sys.argv) != 4:
	print "Invalid number of arguments. Try './makeTestData.py -h'"
	sys.exit()

ratio = int(sys.argv[1])
corpus_ocr = sys.argv[2]
corpus_orig = sys.argv[3]

pattern = re.compile("[a-zA-Z]+")
files_ocr = {}
for (dirpath, dirname, filenames) in os.walk(corpus_ocr):
	if pattern.match(dirpath.split("/")[-1]):
		files_ocr[dirpath.split("/")[-2][:4] + "-" + dirpath.split("/")[-1]] = filenames

files_orig = {}
for (dirpath, dirname, filenames) in os.walk(corpus_orig):
    if pattern.match(dirpath.split("/")[-1]):
	    files_orig[dirpath.split("/")[-2][:4] + "-" + dirpath.split("/")[-1]] = filenames

for i in files_ocr.keys():
	if len(files_ocr[i]) != len(files_orig[i]):
		print i + " Ocred>" + str(len(files_ocr[i]))+ " ______ " + " Original>" +str(len(files_orig[i]))
		if len(files_ocr[i]) < len(files_orig[i]):
			for j in range(len(files_ocr[i])):
				files_orig[i].remove(files_ocr[i][j])
			for f in files_orig[i]:
				print "Removing " + corpus_orig + i[:4] + "txt/" + i[5:] + "/" + f
				os.remove(corpus_orig + i[:4] + "txt/" + i[5:] + "/" + f)
		else:
			for j in range(len(files_orig[i])):
				files_ocr[i].remove(files_orig[i][j])
			for f in files_orig[i]:
				print "Removing " + corpus_ocr + i[:4] + "ocr/" + i[5:] + "/" + f
				os.remove(corpus_ocr + i[:4] + "ocr/" + i[5:] + "/" + f)