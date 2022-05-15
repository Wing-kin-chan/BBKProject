#!/usr/bin/env python3
"""
Program:   index
File:      index.py

Version:   v1.0
Date:      14.05.2022
Function:  Prints the HTML for the index page

Copyright: (c) Kyan W. T. Koranteng, Bioinformatics MSc student, Birkbeck UoL, 2022
Author:    Kyan Koranteng
------------------------------------------------------------------------------------
Description:
============
This program prints the HTML for the index page. 
------------------------------------------------------------------------------------
Revision History:
================
V1.0 14.05.2022
"""

import sys
sys.path.insert(0, "../cgi-biocomp2")
import config

print(
"""
<!DOCTYPE html>
<html lang='eng'>

  <head>
    <title>Chromosome 10 Genome Browser</title>  
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel='stylesheet' type='text/css' href='https://student.cryst.bbk.ac.uk/~kk004/biocomp2demo/css/biocomp2.css' />
  </head>
  
  <body>
    <div class='container'>
      <div class='topnav'>
        <a href='http://student.cryst.bbk.ac.uk/~kk004/biocomp2demo'>Chromosome 10 Genome Browser<br />Birkbeck Biocomputing II Group 8</a>
      </div>
    
      <div class='listall_link'>
        <a href='""" + config.listallurl + """'>List of all entries</a>
      </div>
      
      <form action='""" + config.searchurl + """' method='get'>
        <table class='radio_table'>
          <thead>
          <tr>
            <th colspan="2">Search by:</th>
          </tr>
          </thead>
          <tbody>
          <tr>
            <td>
            <input type='radio' name='search_by' value='ac' id='ac' checked/>
            <label class='search_label' for='ac'>Genbank accession</label>
            </td>
            <td>
            <input type='radio' name='search_by' value='gi' id='gi'/>
            <label class='search_label' for='gi'>Gene identifier</label>
            </td>
          </tr>
          <tr>
            <td>
            <input type='radio' name='search_by' value='protein' id='protein'/>
            <label class='search_label' for='protein'>Protein product name</label>
            </td>
            <td>
            <input type='radio' name='search_by' value='loc' id='loc'/>
            <label class='search_label' for='loc'>Chromosomal location</label>
            </td>
          </tr>
          </tbody>
          <tfoot>
          <tr>
            <td colspan="2">
            <div class='search_bar'>
            <input type='text' placeholder="Search.." name='text_input'/><input class='button' type='Submit' value='Submit'/>
            </div>
            </td>
          </tr>
          </tfoot>
        </table>
      </form>
    
      <div class='footer'>
        <small>Copyright Wing, Tiina and Kyan, Birkbeck 2022 &copy;</small>
      </div>
    
    </div>
    
  </body>
  
</html>
""")