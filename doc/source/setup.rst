System Setup & Simple Tutorial
******************************

Setting up python environment
=============================

This project is completely written in python. So to use it you must have python
pre-installed on your system. If you don't have it then please follow `this 
<http://askubuntu.com/questions/101591/how-do-i-install-python-2-7-2-on-ubuntu>`_

Getting the source code
=======================

You can clone the complete `repository <https://github.com/knoxxs/InfoRescue>`_
using this::

	git clone https://github.com/knoxxs/InfoRescue.git

Also if you want to clone only the latest code then use this::

	git clone https://github.com/knoxxs/InfoRescue.git -b dev

Getting the data
================

I have used the 
`RISOT 2011 data <http://www.isical.ac.in/~fire/risot/risot.html#0.1_data>`_ 
which is not publically available. You can request them and they will surely
share it with you.

Preparing the data
==================

You have to tune the data to make it more consistent so that both the versions
of data has same number of files with same file hierarchy and same file names.
Then you have to remove punctuations and any other exotic character. For this
you have to do the following things:

.. note:: Here I will be explaining everything w.r.t. Risot 2011 Bengali data.
   All the following script are written w.r.t. RISOT 2011 corpus.

Rename Files
++++++++++++

Rename all the files accordingly so that both the versions of data have same 
filenames. For RISOT 2011 both versions have different filenames. So we have to 
make them consistent. To do so I decided to change all the files names of 
origianl version of corpus to match to ocred version. Right now
all the files are named as filename.pc.utf8, this code will change that to
filename.txt::
	
	To do so you can use ``src/dataProcessing/renameFiles.py``.
	You have to pass the path to the corpus to it (i.e. patht o the original 
	version of data).

.. seealso:: `dataProcessing.renameFiles <api/dataProcessing.html#renamefiles>`_

Delete Files
++++++++++++

It may be possible that both versions of data don't have same files. So you have
to remove the extra files to make them consistent::

 	To do so you can use ``src\dataProcessing\deleteCorpusFiles.py``. You have
 	to pass two paths to it: path to ocred version of data and to origianl
 	version of data.

.. note:: You have to append a  **/** at the end of each path, else you will
   get an error.

.. seealso::
   `dataProcessing.deleteCorpusFiles <api/dataProcessing.html#deletecorpusfiles>`_

Clean Data
++++++++++

You have to clean the data to remove all the punctuations, numerals, and other
exotic characters::

	To do so you can use ``src\dataProcessing\cleanRisotBengali.py``.
	You have to pass the path of the corpus to it.

.. seealso::
   `dataProcessing.cleanRisotBengali <api/dataProcessing.html#cleanrisotbengali-sh>`_

Get Stats
+++++++++

This is optional. This will generate a file which will list the difference in
two versions of data for each file::

	To do so you can use ``src\dataProcessing\ocr_orig_diff_stats.py``.
	You have to pass the path of the both versions of data to it.

.. seealso::
   `dataProcessing.ocr_orig_diff_stats <api/dataProcessing.html#ocr-orig-diff-stats>`_

Generating Character Error Model
================================

Now we will generate the error model from the corpus. To generate the error
model use the following code::

	from characterErrorModel import CharacterModel

	a = CharacterModel()
	a.forCorpus('cleaned_ocredDataPath', 'cleaned_ocredDataPath')

This will store a .json file which will contain the error model. This file will
also print all those matches which it can't be able to match successfully.

.. note:: You have to place this file in the same directory of the
   characterErrorModel.py i.e. ``InfoRescue/src/features/``.

.. seealso::
   `features.characterErrorModel <api/features.html#charactererrormodel>`_

PLCS & PLD
==========

You can find these schemes at `src/includes/`.

.. seealso:: `includes.levenshteinDistance <api/includes.html#levenshteindistance>`_,
   `includes.longestCommonSubsequence <api/includes.html#longestcommonsubsequence>`_