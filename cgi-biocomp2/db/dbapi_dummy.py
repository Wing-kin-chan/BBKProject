#!/usr/bin/python3
"""
This is the database API for querying and returning data for searches
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

    return([
        {'GeneID': 'TP53', 'Protein': 'Tumour Protein 53', 'Accession': 'AB120004', 'Locus': '10q23'},
        {'.Other entries with accession similar to query.'},
        {'.Other entries with accession similar to query.'},
    ])

def getByAccessions(accession: str):
    '''
    Dummy function to return all genes that contain the query as a substring in their accession number.
    For example, getAccessions(AB012) will return all genes whose accession starts with with AB012.
    If output is of length = 1 calls getAccession({query})
    '''
    
    return([
        {'GeneID': 'TP53', 'Protein': 'Tumour Protein 53', 'Accession': 'AB120004', 'Locus': '10q23'},
        {'.Other entries with accession similar to query.'},
        {'.Other entries with accession similar to query.'},
    ])

def getAccession(accession: str):
    '''
    Dummy function that will return the database entry for the GenBank accession that matches the query.
    For example getAccession(AB01234) will return all information on the GenBank accession AB01234. This
    will be the function called when accessing a single entry.
    '''
    
    return({
        'Accession': 'AB023432',
        'Date': '19-SEP-2005',
        'Locus': '10q21',
        'GeneID': '3642345',
        'ProteinProduct': 'Angiotensin Receptor II',
        'Description': 'Human angiotensin receptor II full CDS',
        'Sources': 'Homo sapiens (human)',
        'Sequence': 'atgcatgctagcgatgcgatcacgtagcgatgcttcaggtgtcggtagtcgttgagtcgtagcatgcgcgtgtagcggtagctgggtgacatcgacgagcggcgtgagcgtatcgactgaugctagcgatc',
        'Translation': 'MTHAVTRRAHPHAILATHCTAHTERRGPQQMELIPVATR',
        'Coding Regions': {
            'Region 1':'1:30',
            'Region 2': '62:252'
        }
    })

def getByGeneID(geneID: str):
    '''
    Dummy function that will return the database entry for the ID that matches the query.
    For example getGeneID(TP53) will return all information on the TP53 gene.
    '''
    
    return([
        {'GeneID': '3642345', 'Protein': 'Tumour Protein 53', 'Accession': 'AB120004', 'Locus': '10q23'},
        {'...'},
        {'...'},
    ])

def getByLocus(locus: str):
    '''
    Dummy function that will return all gene entries (list of tuples) in a locus
    '''
    
    return([
    {'GeneID': '3642345', 'Protein': 'Tumour Protein 53', 'Accession': 'AB120004', 'Locus': '10q23'},
    {'.Another gene in 10q23.'},
    {'.Another gene in 10q23.'},
])

def getByProtein(protein: str):
    '''
    Dummy function that will return gene entries (list of tuples) related to the queried protein product 
    '''
    
    return([
    {'GeneID': '3642345', 'Protein': 'Tumour Protein 53', 'Accession': 'AB120004', 'Locus': '10q23'},
    {'.Other tumour proteins.'},
    {'.Other tumour proteins.'},
])
