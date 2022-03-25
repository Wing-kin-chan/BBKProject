#!/usr/bin/python3
"""
This CGI script obtains all the entries from the BL layer and formats them for 
HTML display as a table
"""

# Add the bl sub-directory to the module path
# and the directory above to import the config file
import sys
sys.path.insert(0, "../bl/")
sys.path.insert(0, "../")

import blapi_real      # Import the Business Logic API
import htmlutils  # Import HTML utilities
import config     # Import configuration information (e.g. URLs)

entries = blapi_real.getAllEntries()
html    = htmlutils.header()

html += "<h1>List of all entries</h1>\n"
html += "  <table>\n"

for entry in entries:
    html += "    <tr><td>"
    html += "<a href='" + config.searchurl + "?ac=" + entry + "'>"
    html += "<a href='" + config.searchurl + "?gi=" + entry + "'>"
    html += "<a href='" + config.searchurl + "?protein=" + entry + "'>"
    html += "<a href='" + config.searchurl + "?loc=" + entry + "'>"
    html += entry + "</a>"
    html += "</td></tr>\n"

    
html += "  </table>\n"
html += htmlutils.footer()

print(html)



