#!/usr/bin/env python3
"""
List of Python functions with HTML wrappers to generate components of webpages for each Genbank entry as well as 

Support code for generating HTML files
"""

def header():
    """
    ...Function comment header goes here...
    """
    html = "Content-Type: text/html\n\n"   # MIME-Type header
    html += "<!DOCTYPE html>"
    html += "<html>\n"
    html += "  <head>\n"
    html += "    <title>Biocomputing II - framework</title>\n"
    html += "    <link rel='stylesheet' type='text/css' href='css/biocomp2.css' />\n"
    html += "  </head>\n"
    html += "  \n"
    html += "  <body>\n"
    html += "    <div class='content'>\n"
    return(html)

def footer():
    """
    ...Function comment header goes here...
    """
    html = ""
    html += "    </div> <small>Copyright Wing, Tiina and Anthonia, Birkbeck 2022 &copy;<small>\n"
    html += "  </body>\n"
    html += "</html>\n"
    return(html)
