Biocomputing II / cgi-biocomp2/bl
=================================

This directory contains the code for the business logic layer.

It imports the `dbapi.py` module from the `../db` directory.

Business logic layer code files in this directory:
	`blapi_real.py` contains the API for the FE
	`blapi.py` has symbolic link to `blapi_real.py`
	`businesslayer.py` contains the code that is used by the `blapi.py`
	`sub_bl.py` contains sub-code that is used within the BL (to create static text files for example)

This directory also contains a static .txt file `overallcodonfreqs.txt` that
is pre-calculated and derived from all the database entries using the `codonFreq_chromosome10` function in the business layer `sub_bl.py` code.

This directory also contains a static .txt file `getallcodingregions.txt` that
is pre-calculated and derived from all the database entries using the `getAllCodingRegions` function in the business layer `sub_bl.py` code.

For more details please read `bl_code_documentation.txt` in the `docs` directory.


