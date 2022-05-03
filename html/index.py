#!/usr/bin/env python3
import sys
sys.path.insert(0, "../cgi-biocomp2")
import config

print(
"""
<!DOCTYPE html>
<html lang='en'>
  <head>
    <title>Chromosome 10 Genome Browser: Homepage</title>
    <meta charset='utf-8'>
    <meta name='description' content= 'Chromosome 10 Genome Browser for Birkbeck Biocomputing II Group 8 Coursework.'>
    <meta name='viewport' content='width=device-width,intial-scale=1'>
    <link rel='stylesheet' type='text/css' href='biocomp2.css' />
  </head>
  

  <body>
    
    <div class='content'>
<header>
    <h1 style="text-align:center;">Chromosome 10 Genome Browser</h1>
    <p style="text-align:center;">A Chromosome 10 Genome Browser for Birkbeck Biocomputing II Group 8 Coursework</p>
</header>

<header>
<ul class="topnav">
<li><a href="index.html">Homepage</a></li>
</ul>
</header>

        <a href='""" + config.listallurl + """'>List all entries</a>
      </p>
      
      <form action='""" + config.searchurl + """'method='post'>
        <p>Search by:</p>
       
        <div align="center">
        <table>
          <tr>
            <td>Genbank Accession</td>
            <td><input type='text' name='ac'/></td>
          </tr>
          <tr>
            <td>Gene Identifier</td>
            <td><input type='text' name='gi'/></td>
          </tr>
          <tr>
            <td>Protein Product</td>
            <td><input type='text' name='protein'/></td>
          </tr>
          <tr>
            <td>Chromosomal Location</td>
            <td><input type='text' name='loc'/></td>
          </tr>
        </table>

        <p><input type='Submit' value='Search' /></p>
        </div>
      </form>
    </div> <!-- content -->

    <div class="footer">
    <footer><small>Copyright Wing, Tiina and Anthonia, Birkbeck 2022 &copy;</small></footer>
        </div>
  </body>
</html>
""")
