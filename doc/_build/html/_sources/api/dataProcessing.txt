Data Processing
***************

renameFiles
-----------

renameFiles.py <Data>

Rename files to make two versions of data consistent.

*Parameters*:
	Data : Path to corpus

*Returns*:
	--

deleteCorpusFiles
-----------------

./deleteCorpusFiles.py <ocrData> <originalData>

This script will make the two data folder conssistent by deleting the extra files.

*Parameters*:
	ocrData : Path to ocred data

	originalData: path to ocered data

*Returns*:
	Name of all the deleted files.

ocr_orig_diff_stats
-------------------

ocr_orig_diff_stats.py <ocrData> <originalData>

Provide a comparison between two versions of data in terms of difference in purna Virams(।),
newlines, total words i.e. spaces for each file pair.

*Parameters*:
	ocerData : Path to ocred data
	
	originalData : Path to original Data

*Returns*:
	The difference for each file pair

cleanRisotBengali.sh
--------------------

. cleanRisotBengali.sh <dataPath>

Clean the corpus to remove all the puctuation, integers, non-language words.

*Parameters*:
	dataPath : Path to the data

*Returns*:
	--