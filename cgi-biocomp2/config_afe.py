#!/usr/bin/python3
"""
Database connection, and URLs for cgi scripts and website navigation
"""

#URLs:
cgiURL = "/cgi-bin/cgiwrap/kk004"
searchurl = cgiURL + "/biocomp2demo/cgi2/search.cgi"
listallurl = cgiURL + "/biocomp2demo/cgi2/listall.cgi"

#Database Connection
dbname = "cw001"
dbhost = "localhost"
port = 3306
dbuser = "cw001"
dbpass = "trp38ile"
