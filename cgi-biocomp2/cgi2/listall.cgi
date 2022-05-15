#!/usr/bin/env python3
"""
Program:   listall
File:      listall.cgi

Version:   v1.0
Date:      14.05.2022
Function:  A CGI script to obtain all entries from the business layer and formats them into an HTML table

Copyright: (c) Kyan W. T. Koranteng, Bioinformatics MSc student, Birkbeck UoL, 2022
Author:    Kyan Koranteng
----------------------------------------------------------------------------------------------------------
Description:
============
A CGI script to obtain all entries from the business layer and formats them into an HTML table
Each entry is represented by a row on the table.
There is a sperate column for the genbank accession, genbank id, protein name, and chromosomal location
The Header acts as a link to return to the index page
The Genbank accession acts as a link to the details page for that entry
----------------------------------------------------------------------------------------------------------
Revision History:
================
V1.0 14.05.2022
"""

import cgitb
cgitb.enable()

import sys
sys.path.insert(0, "../bl/")
sys.path.insert(0, "../")

import blapi      
import htmlutils  
import config     

entries = blapi.getAllEntries()

html = "Content-Type: text/html\n\n"
html += "<!DOCTYPE html>\n"
html += "<html lang='eng'>\n"
html += "  <head>\n"
html += "    <title>Chromosome 10 Genome Browser</title>\n"
html += "    <meta name='viewport' content='width=device-width, initial-scale=1.0'>\n"
html += "    <link rel='stylesheet' type='text/css' href='https://student.cryst.bbk.ac.uk/~kk004/biocomp2demo/css/biocomp2.css'/>\n"
html += "  </head>\n"    
html += "  <body>\n"

#Header with link to return to the index page
html += "    <div class='container'>\n"
html += "      <div class='topnav'>\n"
html += "        <a href='http://student.cryst.bbk.ac.uk/~kk004/biocomp2demo'>Chromosome 10 Genome Browser<br />Birkbeck Biocomputing II Group 8</a>\n"
html += "      </div>\n"

#First create the table with headers
html += "      <div>\n"
html += "        <table class='list_table'>\n"
html += "          <thead>\n"
html += "          <tr>\n"
html += "          <th class='list_cell_1'>Genbank accession</th>\n"
html += "          <th class='list_cell_2'>Gene identifier</th>\n"
html += "          <th class='list_cell_3'>Protein product name</th>\n"
html += "          <th class='list_cell_4'>Chromosomal location</th>\n"
html += "          </tr>\n"
html += "          </thead>\n"
html += "          <tbody>\n"

#Create a table row with the details for each entry
#The accession table cell acts as a link to details page for each entry
for entry in entries:
    html += "          <tr>\n"
    html += "          <td><a href='" + config.searchurl + "?search_by=ac&text_input=" + entry['Accession'] + "'>" + entry['Accession'] + "</a></td>\n" 
    html += "          <td>" + entry['GeneID'] + "</td>\n"                     
    html += "          <td>" + entry['Product'] + "</td>\n"
    html += "          <td>" + entry['Locus'] + "</td>\n"
    html += "          </tr>\n"

html += "          </tbody>\n"
html += "        </table>\n"
html += "      </div>\n"

html += "      <div class='footer'>\n"
html += "        <small>Copyright Wing, Tiina and Kyan, Birkbeck 2022 &copy;</small>\n"
html += "      </div>\n"
html += "    </div>\n"
html += "  </body>\n"
html += "</html>\n"

print(html)