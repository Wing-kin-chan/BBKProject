Biocomputing II / cgi-biocomp2/db
=================================

This directory contains the code for the database access layer.

The dbapi.py is called by the business layer to access the database. 
It contains a symbolic link to dbapi_real.py

dbapi_real.py contains code for querying, and updating the database.

dbapi_dummy.py contains a dummy implementation of the code found in dbapi_real.py
and returns dummy data without connecting to, or querying the database
