#!/usr/bin/env python3
"""
This CGI script obtains all the entries from the BL layer and formats them for 
HTML display as a table
"""

# Add the bl sub-directory to the module path
# and the directory above to import the config file
import sys
sys.path.insert(0, "../bl/")
sys.path.insert(0, "../")

import blapi      # Import the Business Logic API
import htmlutils  # Import HTML utilities
import config     # Import configuration information (e.g. URLs)

entries = blapi.getAllEntries()
html    = htmlutils.header()

html += "<h1>List of all entries</h1>\n"
html += "  <table>\n"
html += "   <tr>"
html += "    <th>Accession</th>"
html += "    <th>GeneID</th>"
html += "    <th>Protein Product</th>"
html += "    <th>Locus</th>"
html += "   </tr>"

for entry in entries:
    html += "    <tr><td>"
    html += "<td><a href='" + config.searchurl + "?ac=" + entry['Accession'] + "'>" + entry['Accession'] + "</a></td>"         #Added keys to call specific data from the
    html += "<td><a href='" + config.searchurl + "?gi=" + entry['GeneID'] + "'>" + entry['GeneID'] + "</a></td>"            #entry object which is a dictionary          
    html += "<td><a href='" + config.searchurl + "?protein=" + entry['Product'] + "'>" + entry['Product'] + "</a></td>"
    html += "<td><a href='" + config.searchurl + "?loc=" + entry['Locus'] + "'>" + entry['Locus'] + "</a></td>"
    html += "</tr>\n"

    
html += "  </table>\n"
html += htmlutils.footer()

print(html)



