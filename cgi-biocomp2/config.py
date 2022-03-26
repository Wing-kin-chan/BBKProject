#!/usr/bin/python3
"""
...Comment header goes here...

All URLs and database connection parameters should appear in here.
"""

# The base (relative) URL for accessing your CGI scripts. At Birkbeck this
# will be something like:
#    cgiURL="/cgi-bin/cgiwrap/ab123"
# (where `ab123` is replaced by your username).
cgiURL="/cgi-bin/cgiwrap/cw001"

#Database connection details:
dbname = 'localhost'
dbhost = 'pandora'
port = 3306
dbuser = 'cw001'
dbpass = 'trp38ile'





#--------------------------------------------------------------------------
# You shouldn't need to touch anything below here for running the demo
searchurl  = cgiURL + "/biocomp2demo/cgi/search.cgi"
listallurl = cgiURL + "/biocomp2demo/cgi/listall.cgi"
