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

import blapi      # Import the Business Logic API
import htmlutils  # Import HTML utilities
import config     # Import configuration information (e.g. URLs)
cgitb.enable()

form = cgi.FieldStorage()
GenbankAccession = form.getvalue('ac')
GeneIdentifier = form.getvalue('gi')
ProteinProduct = form.getvalue('protein')
ChromosomalLocation = form.getvalue('loc')

#result = blapi_real.search

html = htmlutils.header()
html += "<head>"
html += "<title>Search Results</title>"
html += "</head>"
html += "<p /><b>Name: </b><p />"
html += "<b>Conformation: </b><p />"
html += "<b>Overhang: </b><p />"
html += "<b>Minimum Site Length: </b><p />"
html += "<b>Maximum Number of Cuts: </b><p />"
html += "<b>Included: </b><p />"
html += "<b>Noncutters: </b><p />"
html += "<table>"
html += "<thead align = 'center'>"
html += "<tr>"
html += "<th>Name"
html += "<th>Sequence"
html += "<th>Site Length"
html += "<th>Overhang"
html += "<th>Frequency"
html += "<th>Cut Positions"
html += "<tbody align = 'center'><TR align = 'center'>"
html += "<td>"
html += "<td>"
html += "<td>"
html += "<td>"
html += "<td>"
html += "<td></TABLE>"
html += htmlutils.footer()

print(html)




