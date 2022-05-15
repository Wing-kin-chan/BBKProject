#!/usr/bin/python3
"""
Program:   search
File:      search.cgi

Version:   v1.0
Date:      14.05.2022
Function:  A CGI script to handle search queries 
           Produces a results page for multiple results
           Produces a details page for each entry

Copyright: (c) Kyan W. T. Koranteng, Bioinformatics MSc student, Birkbeck UoL, 2022
Author:    Kyan Koranteng
-------------------------------------------------------------------------------------------------------------------------
Description:
============
A CGI script to handle search queries
Produces a results page for multiple results
Each entry is represented by a row on the table.
There is a sperate column for the genbank accession, genbank id, protein name, and chromosomal location
Produces a details page for each entry
A table with genbank accession, genbank id, protein name, and chromosomal location for the entry is at the top of the page
Four tabs for the dna sequence, coding region, amino acid sequence, and restriction enzymes are in the middle of the page
The chromosome frequency table is at the bottom of the page with horizontal scrolling.

--------------------------------------------------------------------------------------------------------------------------
Revision History:
================
V1.0 14.05.2022
"""

import cgitb
cgitb.enable()

import sys
sys.path.insert(0, "../bl/")
sys.path.insert(0, "../")

import cgi
import blapi
import businesslayer as bl
import htmlutils 
import config     

form = cgi.FieldStorage()
radio_value = form.getvalue('search_by')
form_input = form.getvalue('text_input')

results_len = 500

if radio_value == 'ac':
    search_results = blapi.getByAccession(form_input, results_len)
if radio_value == 'gi':
    search_results = blapi.getByGeneID(form_input, results_len)
if radio_value == 'protein':
    search_results = blapi.getByProtein(form_input, results_len)
if radio_value == 'loc':
    search_results = blapi.getByLocus(form_input, results_len)

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

#Results table for multiple search results
if type(search_results) == list:
    html += "      <div class='search_table_div'>\n"
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
    for entry in search_results:
        html += "    <tr>\n"
        html += "      <td><a href='" + config.searchurl + "?search_by=ac&text_input=" + entry['Accession'] + "'>" + entry['Accession'] + "</a></td>\n" 
        html += "      <td>" + entry['GeneID'] + "</td>\n"                     
        html += "      <td>" + entry['Product'] + "</td>\n"
        html += "      <td>" + entry['Locus'] + "</td>\n"
        html += "    </tr>\n" 
    html += "          </tbody>\n"
    html += "        </table>\n"
    html += "      </div>\n"

#Details page for a single entry
if type(search_results) == dict:
    html += "      <div class='search_table_div'>\n"
    html += "        <table class='search_table'>\n"
    html += "          <thead>\n"
    html += "          <tr>\n"
    html += "          <th class='list_cell_1'>Genbank accession</th>\n"
    html += "          <th class='list_cell_2'>Gene identifier</th>\n"
    html += "          <th class='list_cell_3'>Protein product name</th>\n"
    html += "          <th class='list_cell_4'>Chromosomal location</th>\n"
    html += "          </tr>\n"
    html += "          </thead>\n"
    html += "          <tbody>\n"
    html += "          <tr>\n"
    html += "          <td>" + search_results['Accession'] + "</td>\n"
    html += "          <td>" + search_results['GeneID'] + "</td>\n"
    html += "          <td>" + search_results['Product'] + "</td>\n"
    html += "          <td>" + search_results['Locus'] + "</td>\n"
    html += "          </tr>\n"
    html += "          </tbody>\n"
    html += "        </table>\n"
    html += "      </div>\n"
    
#Accessing the business layer for sequence information
    dna_seq = bl.coding_region(search_results['Accession'])
    coding_reg_hl = dna_seq[0].replace("{", "<mark>").replace("}", "</mark>")
    
    aa_zip = bl.aa_nt(search_results['Accession'])
    aa_list = []
    s1 = ''
    for aa in aa_zip[0]:
        aa_list.append(aa[1])
        aa_str = s1.join(aa_list)
        
#Organising sequence information into tabs
    html += "      <div class='seqtabs'>\n"
    html += "        <input type='radio' id='dna' name='seqtabs' checked='checked'/>\n"
    html += "        <label for='dna'>DNA sequence with highlighted coding regions</label>\n"
    html += "        <div class='tab'>\n"
    html += "          <p>" + coding_reg_hl + "</p>\n"
    html += "        </div>\n"
    html += "        <input type='radio' id='coding' name='seqtabs'/>\n"
    html += "        <label for='coding'>Coding DNA sequence</label>\n"
    html += "        <div class='tab'>\n"
    html += "          <p>" + dna_seq[1] + "</p>\n"
    html += "        </div>\n"
    html += "        <input type='radio' id='aa' name='seqtabs'/>\n"
    html += "        <label for='aa'>Amino acid sequence</label>\n"
    html += "        <div class='tab'>\n"
    html += "          <p>" + aa_str + "</p>\n"
    html += "        </div>\n"
    html += "        <input type='radio' id='enz' name='seqtabs'/>\n"
    html += "        <label for='enz'>Restriction Enzymes</label>\n"
    html += "        <div class='tab'>\n"
    html += "          <p>Restriction enzyme feature not currently available.</p>\n"
    html += "        </div>\n"
    html += "      </div>\n"

#Creating a horizontally orientated codon frequency table from information from the business layer
    html += "      <div class='table_title'><h>Codon frequency table</h></div>\n"
    codon_freq = bl.codonFreq_entry(search_results['Accession'])
    codon_dict = codon_freq[0]
    html += "      <div class='codon_table'>\n"
    html += "        <table>\n"
    html += "          <tr>\n"
    html += "          <th>Codon</th>\n"
    for k, v in codon_dict.items():
        html += "          <td>" + k + "</td>\n"
    html += "          </tr>\n"
    html += "          <tr>\n"
    html += "          <th>AA</th>\n"
    for k, v in codon_dict.items():
        html += "          <td>" + v[0] + "</td>\n"
    html += "          </tr>\n"
    html += "          <tr>\n"
    html += "          <th>Frequency per entry</th>\n"
    for k, v in codon_dict.items():
        html += "          <td>" + str(v[1]) + "</td>\n"
    html += "          </tr>\n"
    html += "          <tr>\n"
    html += "          <th>Frequency per chromosome</th>\n"
    for k, v in codon_dict.items():
        html += "          <td>" + str(v[2]) + "</td>\n"
    html += "          </tr>\n"
    html += "        </table>\n"
    html += "      </div>"

html += "      <div class='footer'>\n"
html += "        <small>Copyright Wing, Tiina and Kyan, Birkbeck 2022 &copy;</small>\n"
html += "      </div>\n"
html += "    </div>\n"
html += "  </body>\n"
html += "</html>\n"

print(html)