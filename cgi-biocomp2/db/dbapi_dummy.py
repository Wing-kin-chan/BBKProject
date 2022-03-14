#!/usr/bin/python3
"""
This is the database API - it needs to access the MySQL database using PyMySQL 
"""

# Add the directory above to the module path to import the config file
import sys
sys.path.insert(0, "../")

import config  # Import configuration information (e.g. database connection)

def getAllEntries():
    """
    ...Function comment header goes here...

    This is a dummy function that returns a list of entries. The real version would probably
    return a list of dictionaries and would access the MySQL database
    """

    return(['AB000123', 'AB000321', 'AC001564'])

def getAccessions():
    '''
    Dummy function to return all accession ID's that contain the query as a substring.
    For example, getAccessions(AB012) will return all accessions starting with AB012.
    If output is of length = 1 calls getAccession({query})
    '''
    
    return(['AB01234', 'AB012456', 'AB012876'])

def getAccession():
    '''
    Dummy function that will return the database entry for the GenBank accession that matches the query.
    For example getAccession(AB01234) will return all information on the GenBank accession AB01234.
    '''
    
    return(['Accession', 'Locus', 'Molecule type', 'Gene name', 'CDS', 'Sequnece', 'Protein product?', 'Intron/Exon boundaries'])

def getGeneID():
    '''
    Dummy function that will return the database entry for the ID that matches the query.
    For example getGeneID(TP53) will return all information on the TP53 gene.
    '''
    
    return(['Accession', 'Locus', 'Molecule type', 'Gene name', 'CDS', 'Sequnece', 'Protein product?', 'Intron/Exon boundaries'])

def getLocus():
    '''
    Dummy function that will
    '''