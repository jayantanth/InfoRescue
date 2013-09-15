#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This modules implement the Probabilistic Levenshtein Distance using the
Character Error Model for two words: one is erroneous and other is original
i.e. one is the word from the corpus (erroneous) and other is the query word
(original).
"""

import copy
import sys

sys.path.insert(0, './')
from utilities import *

def ld(ocr, orig):
	"""Calculate Probabilistic Levenshtein Distance between two words.

	Following three functions must be called prior to use this functions:

	1. :func:`infoRescue.includes.utilities.getCEM`
	2. :func:`infoRescue.includes.utilities.getMinimumProbability`
	3. :func:`infoRescue.includes.utilities.increaseProbability`

	*Parameters*:
		ocr : erroneous word
		orig : actual word

	*Returns*:
		Probabilistic Levenshtein Distance between two words.
	"""

	ocr, orig = ocr.decode('utf8'), orig.decode('utf8')
	l1 = len(ocr)
	l2 = len(orig)

	#l2 is no. of rows
	matrix = [range(l1 + 1)] * (l2 + 1)

	#writing maximum distance possible for each element
	for row in range(l2 + 1):
		matrix[row] = range(row,row + l1 + 1)

	# printTable(matrix)

	for row in range(l2):
		for column in range(l1):
			matrix[row+1][column+1] = min(matrix[row+1][column] + 1, matrix[row][column+1] + 1, matrix[row][column] + (0 if prob_equals(ocr[column], orig[row]) else 1))

	# printTable(matrix)
	return matrix[l2][l1]

# getCEM('../features/characterErrorModelProbalistic.json')
# minProb = getMinimumProbability()
# increaseProbability(minProb)
# print ld('চাহুর','রাহুর')