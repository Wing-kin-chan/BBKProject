#!/usr/bin/python3
"""
Business layer APIs
List of function definitions to parse, and perform operations on Genbank entries from database
and return outputs to be presented on the webpage.

This is the business logic API

***The standardised file header will be here***

At present some of the functions return dummy data - please see below
Tiina Talts
"""

# Add the bl sub-directory to the module path (for testing this routine)
# and the directory above to import the config file
import sys
sys.path.insert(0, "../db")
sys.path.insert(0, "../bl")
sys.path.insert(0, "../")

import dbapi   # Import the database api
import config  # Import configuration information (if needed)
import businesslayer as bl

def getAllEntries():
    """
    ...Function comment header goes here...

    This is a very simple function that just calls the database API to do the SQL to 
    obtain the full list of entries. It doesn't need to do anything else.
    """
    return(dbapi.getAllEntries())

def getByGeneID(query: str, resultslen: int):
    """
    Function that will pass name of the gene (in the chromosome file as '/gene=' as list 
    of strings from db. This is marked as 'gene identifiers' in the requirements file. Can have 
    zero to many result returns.Returns a list of strings for FE.
    """
    return dbapi.getByGeneID(query, resultslen)


def getByProtein(query: str, resultslen: int):
    """
    Function that will pass prot product name (in the chromosome file as '/product=') 
    as list of strings from db. This is marked as 'protein product name' in the requirements 
    file. Can have zero to many result returns. Returns list of strings for FE
    """
    return dbapi.getByProduct(query, resultslen)

def getAccession(query: str):
    """
    Function that will pass accession number (in the chromosome file as 'ACCESSION') as string
    from db. This is marked as 'Genbank accession' in the requirements file. Can have zero to 
    one result returned. Returns a list of strings for search. If no result then returns message??
    """
    return dbapi.getAccession(query)

def getByAccession(query: str, resultslen: int):
    """
    Function that will pass accession number (in the chromosome file as 'ACCESSION') as 
    string from db. This is     marked as 'Genbank accession' in the requirements file. 
    Can have zero to many result returns for a partial search   term. Returns a list of 
    strings for search. If no result then returns message??
    """
    return dbapi.getByAccession(query, resultslen) 

def getByLocus(query: str, resultslen: int):
    """
    Function that will pass chromosomal location as a list of strings from db. In the 
    chromosome file as '/map=' as given by 'source'. This is marked as 'chromosomal location' 
    in the requirements file. Can have zero to many result returns. Returns list of strings for FE
    """
    return dbapi.getByLocus(query, resultslen) 

def ntCoding_region(accession):
    """
    Function that will interact with a Blayer coding_region function that takes accession_id, 
    nt_seq[string], codon_start[int], exon_boundaries[list of int tuples] from the DBlayer and 
    returns string of nt_seq with brackets indicating coding regions e.g. ATC{TGTGTCC}ATGTT, 
    extracted coding region, corresponding accession_id & a list of coding boundaries.
    """
    return bl.coding_region(accession)


def aaNt_seqsAligned(accession):
    """
    Function that will interact with a Blayer function aa_nt that takes accession_id, 
    aa_seq[string] and function coding_region (see above) with corresponding input from 
    the DBlayer, and returns a tuple of nt triplet and corresponding aa letter & corresponding accession_id
    """		
    return bl.aa_nt(accession)

def entryCodon_freq():
    """
    Function that will interact with a Blayer function codonFreq_entry that takes accession_id, 
    extract data needed from a function aa_nt and saved file with adta derived previously from function
    codonFreq_chromosome10 and returns a list of codons for the entry, frequencies per codon per entry
    as float (%), frequencies per codon per chromosome as float (%), corresponding amino acid 
    letter code; & corresponding accession_id for the entry
    """
    return bl.codonFreq_entry(accession)

def chrom10Codon_freq():
    """
    Function that will interact with a Blayer function codonFreq_chromosome10 that takes all 
    available chromosome10 accession_id's in the DB using getAllCodingRegions, extract data needed from a 
    function aa_nt (see above) and returns a list of tuples: codon, freq per codon per all entries as float (%)
     - can be completed once and saved as static values in a file: overallcodonfreqs.txt
    """
    return bl.codonFreq_chromosome10()

def restr_enz(accession):
    """
    Function that will interact with Blayer functions that return a dictionary of list of restriction
    enzyme cutting information that includes enzyme name; cutting site; cutting site length; cutting
    'offset' or positition within the cutting site where the enzyme cuts; cut positions across the
    enrty nucleotide sequence - non-coding region and coding region; cutting frequency; and a flag
    'This is a good enzyme!' if the cutting position is located outside of the coding region: either
    before the start of the first coding region and/or after the end of the last coding region.
    The enzyme list consists of New England Biolabs (NEB) high fidelity (HF) sticky-end restriction 
    enzymes that includes EcoRI, BamHI and BsuMI as XhoI its prototype.   
    """
    return bl.enz_table(accession)

