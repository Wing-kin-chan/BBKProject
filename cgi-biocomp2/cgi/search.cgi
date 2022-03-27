#!/usr/bin/python3
"""
This CGI script obtains all the entries from the BL layer and formats them for 
HTML display as a table
"""

# Add the bl sub-directory to the module path
# and the directory above to import the config file
import cgitb
import sys
sys.path.insert(0, "../bl/")
sys.path.insert(0, "../")

import cgi        # Import the CGI module

import blapi_real      # Import the Business Logic API
import htmlutils  # Import HTML utilities
import config     # Import configuration information (e.g. URLs)
cgitb.enable()

form = cgi.FieldStorage()
GenbankAccession = form.getvalue('ac')
GeneIdentifier = form.getvalue('gi')
ProteinProduct = form.getvalue('protein')
ChromosomalLocation = form.getvalue('loc')

#result = blapi_real.search

html    = htmlutils.header()
html += "<h1>Dummy search code</h1>\n"
html += "      <ul>\n"
html += "        <li>Result of search for '" + GenbankAccession + "'</li>\n"
html += "      </ul>\n"
html += htmlutils.footer()

print(html)



