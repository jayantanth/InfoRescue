#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
freqToProbCEM.py <path_to_freqCEM> <path_to_probCEM>

Converts the Frequency based Character Error Model to Probabilistic Character Error Model.
"""

import json
import sys
import codecs

if len(sys.argv) == 2 and sys.argv[1] == '-h':
	print("Usage: ./freqToProbCEM.py <freqCEM> <probCEM>")
	sys.exit()
elif len(sys.argv) != 3:
	print "Invalid number of arguments. Try './characterErrorModel.py -h'"
	sys.exit()

freqCEM = sys.argv[1]
probCEM = sys.argv[2]

modelDict = {}
with codecs.open(freqCEM, 'r', encoding='utf8') as output:
	modelDict = json.load(output)

for char in modelDict:
	total = 0
	for mappedChar in modelDict[char]:
		total += int(modelDict[char][mappedChar])
	for mappedChar in modelDict[char]:
		modelDict[char][mappedChar] = float(modelDict[char][mappedChar]) / total

with codecs.open(probCEM, 'w', encoding='utf8') as output:
		json.dump(modelDict, output, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)
