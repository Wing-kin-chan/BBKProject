#!/usr/bin/env python3
"""
...Comment header goes here...

Simple script to generate the index.html file so that we can pick up
configuration information from the config file.
"""

# Add the CGI directory which is where the config file lives
import sys
sys.path.insert(0, "../cgi-biocomp2")
import config

print(
"""<!DOCTYPE html>
<html lang='en'>
  <head>
    <title>Chromosome 10 Genome Browser: Homepage</title>
    <meta charset='utf-8'>
    <meta name='description' content='Chromosome 10 Genome Browser for
    Birkbeck Biocomputing II Group 8 Coursework.'>
    <meta name='viewport' content='width=device-width,intial-scale=1'>
    <link rel='stylesheet' type='text/css' href='css/biocomp2.css' />
  </head>
  
  <body>
    <div class='content'>
    <header>
    <h1 style="text-align:center;">Chromosome 10 Genome Browser</h1>
    <p style="text-align:center;">A Chromosome 10 Genome Browser for Birkbeck Biocomputing II Group 8 Coursework</p>
</header>
<header id="header-background">
  <div class="banner"></div>
<div class="topnav">
<a href="index.html">Homepage</a>
<a href="geneoftheday.html">Gene of the Day</a>
<a href="feelinglucky.html">'I'm Feeling Lucky!'</a>
</div>
</header>
      <h1>Biocomputing II - framework</h1>
      <p>A simple demo of how the Biocomputing II project should work and
        be submitted. It shows how the API between the layers is organized.</p>
      
      <p>Most importantly, it shows how you how you are <b>strongly
        recommended</b> to organize your code in GitHub for
        marking. If you deviate from this, you must have a very good
        reason!
      </p>

      <p><b>Note</b> that the Genbank accession search is guaranteed to
         return zero or one entries; the other searches may return zero
         to many entries. Consequently the search by Genbank accession
         can take you to the detail page for that entry while the other
         searches should take you to a list of hits (just as you have
         when you list all entries).
      </p>
      
      <p>
        <a href='""" + config.listallurl + """'>List all entries</a>
      </p>
      
      <form action='""" + config.searchurl + """' method='get'>
        <p>Search by:</p>
        
        <table>
          <tr>
            <td>genbank accession</td>
            <td><input type='text' name='ac'/> (only this search box works in the demo)</td>
          </tr>
          <tr>
            <td>gene identifier</td>
            <td><input type='text' name='gi'/></td>
          </tr>
          <tr>
            <td>protein product</td>
            <td><input type='text' name='protein'/></td>
          </tr>
          <tr>
            <td>chromosomal location</td>
            <td><input type='text' name='loc'/></td>
          </tr>
        </table>

        <p><input type='Submit' value='Search' /></p>

      </form>
    </div> <!-- content -->
    
    <footer>
        <small>Copyright Wing, Tiina and Anthonia, Birkbeck 2022 &copy;<small>
        </footer>
  </body>
</html>
""")
