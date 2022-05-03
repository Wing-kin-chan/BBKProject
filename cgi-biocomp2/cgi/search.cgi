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
Resultslen = 100
SearchBy = ''

if GenbankAccession:
    query = GenbankAccession
    results = blapi.getByAccession(GenbankAccession, Resultslen)
    SearchBy = 'Accession'
if GeneIdentifier:
    query = GeneIdentifier
    results = blapi.getByGeneID(GeneIdentifier, Resultslen)
    SearchBy = 'GeneID'
if ProteinProduct:
    query = ProteinProduct
    results = blapi.getByProtein(ProteinProduct, Resultslen)
    SearchBy = 'Gene Product'
if ChromosomalLocation:
    query = ChromosomalLocation
    results = blapi.getByLocus(ChromosomalLocation, Resultslen)
    SearchBy = 'Locus'

highlighted_CDS_source = blapi.coding_region(results['Accession'])
highlighted_CDS = highlighted_CDS_source.replace('{', '<span style="background-color: #FFFF00>'.replace('}', '</span>'))

html = htmlutils.header()

if results == 'No results found':
    html += "<h1>" + results + " for: " + query + "</h1>"
    html += htmlutils.footer()
    
if type(results) == list:
    html += "<head>"
    html += "<h1>Searching By " + SearchBy + ": " + query + "</h1>"
    html += "</head>"
    html += "  <table>\n"
    html += "   <tr>"
    html += "    <th>Accession</th>"
    html += "    <th>GeneID</th>"
    html += "    <th>Protein Product</th>"
    html += "    <th>Locus</th>"
    html += "   </tr>"
    
    for entry in results:
        html += "<tr>"
        html += "<td><a href='" + config.searchurl + "?ac=" + entry['Accession'] + "'>" + entry['Accession'] + "</a></td>"         
        html += "<td><a href='" + config.searchurl + "?gi=" + entry['GeneID'] + "'>" + entry['GeneID'] + "</a></td>"            
        html += "<td><a href='" + config.searchurl + "?protein=" + entry['Product'] + "'>" + entry['Product'] + "</a></td>"
        html += "<td><a href='" + config.searchurl + "?loc=" + entry['Locus'] + "'>" + entry['Locus'] + "</a></td>"
        html += "</tr>\n"

if type(results) == dict:
    html += "<head>"
    html += "<title>" + results['Product'] + "</title>"
    html += "</head>"
    html += "<h1>" + results['Product'] + "</h1>"
    html += "<div class='summary'>"
    html += "<h2>Record Summary</h2>" 
    html += "<p /><b>Accession: " + results['Accession'] + "</b><p />"
    html += "<p /><b>GeneID: " + results['GeneID'] + "</b><p />"
    html += "<p/><b>Locus: " + results['Locus'] + "</b><p />"
    html += "</div>"
    html += "</div class='record-description'>"
    html += "<h2>Description</h2>"
    html += "<p /><b>" + results['Description'] + "</b><p />"
    html += "</div>"
    html += "<div class='sequence'>"
    html += "<h2>Sequence:</h2>"
    html += "<p /><b>" + highlighted_CDS + "</b><p />"
    html += "</div>"
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




