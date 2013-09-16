Project
*******

Overview
========
Inforescue is a search engine which searches on erroneous data unlike general search engines which normally search on error free data.
The error in the data can be due to anything but Inforescue focuses errors particularily introduced by `OCR <http://en.wikipedia.org/wiki/Optical_character_recognition>`_. 

This project is done as a part of GSoC 2013 under Ankur India Organisation.

Objective/Plan
==============

1. Get the data *(Done)*

	Both the ocred and original version of same data with topics and qrels files.

2. Prepare the data *(Done)*

	Make both the versions of data consistent in terms of files present, file hierarchy, filenames.

3. Generate Character Error Model *(Done)*

	Make a model which will  represent the probability of a character to be wrongly recognized as any other character by OCR.

4. Make PLCS *(Done)*

	First Make a LCS (Longest Common Subsequence) which will return all the LCSs and then make it PLCS (Probabilistic LCS) using the character error model.

5. Make PLD *(Done)*

	Make a PLD (Probabilistic Levenshtein Distance) which will return PLD based on the character error model. 

6. Check for using Suffix Trees *(Done)*

	Study whether suffix trees can be used.

7. Make PLCS return associated probability *(Done)*

	Modify PLCS to return the probability of correctness with each LCS.

8. Make a complete Search System *(Doing)*

	A search engine which will use above mentioned schems with general search schemes.

9. Stemming Approach for searching *(Done)*

	To give more weight to stemming approach compared to PLCS and PLD.

10. Experimenting with the Search System (*Not Done Yet*)

	Get the best empirical values for all the magic numbers present above mentioned schemes.

11. Documentation *(Done for now)*

	Document everything.

Data
====

Data I am using is constcuted for `RISOT 2011 <http://www.isical.ac.in/~fire/risot/risot.html>`_.

I want to thank `Utpal Garain <https://plus.google.com/113165079765927893417>`_ who provide me the access to the data and `Prasenjit Majumdar <https://plus.google.com/100047743445084989719>`_ for contacting Utpal on hi behalf.

I have changed the data a little bit. To make files consistent in both version of the data I have to delete `some files <https://github.com/knoxxs/InfoRescue/blob/master/stats/filesDeleted>`_. Final stats about the files are `here <https://github.com/knoxxs/InfoRescue/blob/master/stats/corpusStats>`_.

`Here <https://github.com/knoxxs/InfoRescue/blob/master/stats/ocr_orig_diff_stats>`_ you can find about the different in two versions of data in terms of purna virams, newlines and words in two version of same file.

Lesson Learned
==============

- Character Error Model is one of the most important part for the correct working of InfoRescue.

- To consider all the possible LCSs.

- Modifying Lucene is very big for single person.

- Modify the schemes to use the hashed inverted index.