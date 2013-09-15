#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ocr_orig_diff_stats.py <ocrData> <originalData>

Provide a comparison between two versions of data in terms of difference in purna Virams(।),
newlines, total words i.e. spaces for each file pair.

*Parameters*:
	ocerData : Path to ocred data
	originalData : Path to original Data

*Returns*:
	The difference for each file pair
"""

import sys
import os
import re

sys.path.insert(0, '../includes/')
import levenshteinDistance as ld

if len(sys.argv) == 2 and sys.argv[1] == '-h':
	print("Usage: ./ocr_orig_diff_stats.py <ocrData> <originalData>")
	sys.exit()
elif len(sys.argv) != 3:
	print "Invalid number of arguments. Try './ocr_orig_diff_stats.py -h'"
	sys.exit()

corpus_ocr = sys.argv[1]
corpus_orig = sys.argv[2]

pattern = re.compile("[a-zA-Z]+")
files_ocr = {}

for (dirpath, dirname, filenames) in os.walk(corpus_ocr):
	if pattern.match(dirpath.split("/")[-1]):
		files_ocr[dirpath.split("/")[-2][:4] + ">" + dirpath.split("/")[-1]] = filenames

files_orig = {}
for (dirpath, dirname, filenames) in os.walk(corpus_orig):
    if pattern.match(dirpath.split("/")[-1]):
	    files_orig[dirpath.split("/")[-2][:4] + ">" + dirpath.split("/")[-1]] = filenames

print "##############################"
print "Format:(ocr, orig)"
print "Filename\nFileLengths\nNo. of purna Virams(।)\nno. of '\\n's\nno. of words i.e. spaces"
print "##############################\n\n"

for direc in files_ocr.keys():
	for fl in files_ocr[direc]:
		with open(corpus_ocr + direc.split('>')[0] + 'ocr/' + direc.split('>')[-1] + '/' + fl, 'r') as fl_ocr, open(corpus_orig + direc.split('>')[0] + 'txt/' + direc.split('>')[-1] + '/' + fl, 'r') as fl_orig:
			ocr = fl_ocr.read().strip().decode('utf8')
			orig = fl_orig.read().strip().decode('utf8')
			# ocr = re.sub(r"\n+", '', fl_ocr.read().strip().decode('utf8')).split()
			# orig = re.sub(r"\n+", '', fl_orig.read().strip().decode('utf8')).split()
			print direc.split('>')[0] + '/' + direc.split('>')[-1]+ '/' + fl
			print len(ocr), len(orig)
			print len(ocr.split('।'.decode('utf8'))), len(orig.split('।'.decode('utf8')))
			print len(ocr.split('\n')), len(orig.split('\n'))
			print len(ocr.split(' ')), len(orig.split(' '))
			print