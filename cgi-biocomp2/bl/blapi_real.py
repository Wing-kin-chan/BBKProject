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
    extracted coding region & corresponding accession_id
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
    RETURNS DUMMY DATA
    Function that will interact with a Blayer function3 that takes accession_id, 
    extract data needed from a function1 (see above) which is similar to def nt_coding 
    and returns a list of freq per codon per entry as float (%), ratio  as abundance of 
    that codon relative to all of the codons for that particular amino acid, amino acid 
    letter code; & corresponding accession_id
    """
    return('AB032150', "[('aug', 'M', '4.321','0.1'), ('gau', 'D', '4.321','0.1'), ('ucg', 'S', '4.012','0.1'), ('aaa', 'K', '3.704','0.1'), ('uau', 'Y', '3.704','0.1'), ('cag', 'Q', '3.704','0.1'), ('ugu', 'C', '3.704','0.1'), ('gug', 'V', '3.395','0.1'), ('aag', 'K', '3.086','0.1'), ('cug', 'L', '3.086','0.1'), ('aau', 'N', '2.778','0.1'), ('gau', 'D', '2.778','0.1'), ('ggu', 'G', '2.469','0.1'), ('cac', 'H', '2.16','0.1'), ('uuc', 'F', '2.16','0.1'), ('aug', 'M', '2.16','0.1'), ('ccu', 'P', '2.16','0.1'), ('guc', 'V', '1.852','0.1'), ('cug', 'L', '1.852','0.1'), ('gga', 'G', '1.852','0.1'), ('uuu', 'F', '1.852','0.1'), ('ggc', 'G', '1.852','0.1'), ('acc', 'T', '1.543','0.1'), ('uau', 'Y', '1.543','0.1'), ('gcg', 'A', '1.543','0.1'), ('ccu', 'P', '1.543','0.1'), ('gca', 'A', '1.543','0.1'), ('gag', 'E', '1.543','0.1'), ('guu', 'V', '1.543','0.1'), ('ccu', 'P', '1.543','0.1'), ('aaa', 'K', '1.543','0.1'), ('agu', 'S', '1.543','0.1'), ('aaa', 'K', '1.543','0.1'), ('gcu', 'A', '1.235','0.1'), ('uua', 'L', '1.235','0.1'), ('gag', 'E', '1.235','0.1'), ('gcc', 'A', '1.235','0.1'), ('acc', 'T', '1.235','0.1'), ('aaa', 'K', '0.926','0.1'), ('uug', 'L', '0.926','0.1'), ('gca', 'A', '0.926','0.1'), ('auu', 'I', '0.926','0.1'), ('gaa', 'E', '0.926','0.1'), ('gcu', 'A', '0.926','0.1'), ('ggc', 'G', '0.926','0.1'), ('uuc', 'F', '0.926','0.1'), ('cgc', 'R', '0.617','0.1'), ('cau', 'H', '0.617','0.1'), ('auu', 'I', '0.617','0.1'), ('gau', 'D', '0.617','0.1'), ('ucu', 'S', '0.617','0.1'), ('gcu', 'A', '0.617','0.1'), ('cau', 'H', '0.309','0.1'), ('uua', 'L', '0.309','0.1'), ('uac', 'Y', '0.309','0.1'), ('aau', 'N', '0.309','0.1'), ('aau', 'N', '0.309','0.1'), ('gag', 'E', '0.309','0.1'), ('gag', 'E', '0.309','0.1'), ('cag', 'Q', '0.309','0.1'), ('guu', 'V', '0.309','0.1')]")

def chrom10Codon_freq():
    """
    RETURNS DUMMY DATA
    Function that will interact with a Blayer function4 that takes all 
    available chromosome10 accession_id's in the DB, extract data needed from a 
    function1 (see above) which is similar to def nt_coding and returns a list of 
    freq per codon per all entries as float (%) - can be completed once and saved as static values in a file
    """
    return("['gug', 4.321]['aag', 4.321]['gag', 4.012]['gau', 3.704]['aaa', 3.704]['cug', 3.704]['gcc', 3.704]['cag', 3.395]['gaa', 3.086]['cca', 3.086]['aau', 2.778]['uug', 2.778]['aac', 2.469]['uau', 2.16]['uuc', 2.16]['auu', 2.16]['uac', 2.16]['ccu', 1.852]['uuu', 1.852]['guu', 1.852]['cga', 1.852]['gac', 1.852]['ugu', 1.543]['guc', 1.543]['gga', 1.543]['ggc', 1.543]['gca', 1.543]['gcu', 1.543]['cau', 1.543]['auc', 1.543]['cuu', 1.543]['ucc', 1.543]['cuc', 1.543]['aug', 1.235]['acc', 1.235]['cgc', 1.235]['aga', 1.235]['uca', 1.235]['cac', 0.926]['agu', 0.926]['ucu', 0.926]['aua', 0.926]['ugg', 0.926]['ugc', 0.926]['cua', 0.926]['ggg', 0.926]['ggu', 0.617]['uua', 0.617]['agc', 0.617]['acu', 0.617]['agg', 0.617]['ccg', 0.617]['ucg', 0.309]['gcg', 0.309]['caa', 0.309]['gua', 0.309]['aca', 0.309]['acg', 0.309]['cgu', 0.309]['ccc', 0.309]['uaa', 0.309], ['uag', 0.009]['uga', 0.009]['cgg', 0.009]")

def restr_enz():
    """
    Function that will interact with Blayer functions that result and return nt_coding_region 
    (see def above) with added enzyme sites into the string where the enzyme cuts in the sequence. 
    Takes Enzyme restriction site information from the DB? or from a file? Returns also string list 
    of noncutters and accession_id. Sites outside of the coding region or the good sites are 
    indicated with double asterisk '**Enz**'; Unique sites are indicated: '*&Enz&* and good unique sites: '*&*Enz*&*'.
    """
    return 

