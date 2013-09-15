#!/usr/bin/env python

import sys
import os
import re

if len(sys.argv) == 2 and sys.argv[1] == '-h':
	print("Usage: ./renameFiles.py <Data>")
	sys.exit()
elif len(sys.argv) != 2:
	print "Invalid number of arguments. Try './renameFiles.py -h'"
	sys.exit()

corpus = sys.argv[1]

pattern = re.compile("[a-zA-Z]+")

for (dirpath, dirname, filenames) in os.walk(corpus):
	if pattern.match(dirpath.split("/")[-1]):
		for f in filenames:
			os.rename(dirpath + "/" + f,dirpath + "/" + f[:-7] + "txt")
