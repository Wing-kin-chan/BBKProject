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
	'''
		Function that will pass name of the gene (in the chromosome file as '/gene=' as list of strings from db. This is marked as 'gene identifiers' in the requirements file. Can have zero to many result returns.
		Returns a list of strings for FE
	'''
	return dbapi.getByGeneID(query, resultslen)


def getByProtein(query: str, resultslen: int):
	'''
		Function that will pass prot product name (in the chromosome file as '/product=') as list of strings from db. This is marked as 'protein product name' in the requirements file. Can have zero to many result returns.
		Returns list of strings for FE
	'''
	return dbapi.getByProduct(query, resultslen)

def getAccession(query: str):
	'''
		Function that will pass accession number (in the chromosome file as 'ACCESSION') as string from db. This is marked as 'Genbank accession' in the requirements file. Can have zero to one result returned.
		Returns a list of strings for search. If no result then returns message??
	'''
	return dbapi.getAccession(query)

def getByAccession(query: str, resultslen: int):
	'''
		Function that will pass accession number (in the chromosome file as 'ACCESSION') as string from db. This is marked as 'Genbank accession' in the requirements file. Can have zero to many result returns for a partial search term.
		Returns a list of strings for search. If no result then returns message??
	'''
	return dbapi.getByAccession(query, resultslen) 

def getByLocus(query: str, resultslen: int):
	'''
		Function that will pass chromosomal location as a list of strings from db. In the chromosome file as '/map=' as given by 'source'. This is marked as 'chromosomal location' in the requirements file. Can have zero to many result returns.
		Returns list of strings for FE
	'''
	return dbapi.getByLocus(query, resultslen) 

def ntCoding_region(accession):
	'''
		Function that will interact with a Blayer coding_region function that takes accession_id, nt_seq[string], codon_start[int], exon_boundaries[list of int tuples] from the DBlayer and returns string of nt_seq with brackets indicating coding regions e.g. ATC{TGTGTCC}ATGTT, extracted coding region & corresponding accession_id
	'''
	return bl.coding_region(accession)


def aaNt_seqsAligned(accession):
	'''
		Function that will interact with a Blayer function aa_nt that takes accession_id, aa_seq[string] and function coding_region (see above) with corresponding input from the DBlayer, and returns a tuple of nt triplet and corresponding aa letter & corresponding accession_id
	'''		
	return bl.aa_nt(accession)

def entryCodon_freq():
	'''
		RETURNS DUMMY DATA
		Function that will interact with a Blayer function3 that takes accession_id, extract data needed from a function1 (see above) which is similar to def nt_coding and returns a list of freq per codon per entry as float (%), ratio  as abundance of that codon relative to all of the codons for that particular amino acid, amino acid letter code; & corresponding accession_id
	'''
	return('AB032150', "[('aug', 'M', '4.321','0.1'), ('gau', 'D', '4.321','0.1'), ('ucg', 'S', '4.012','0.1'), ('aaa', 'K', '3.704','0.1'), ('uau', 'Y', '3.704','0.1'), ('cag', 'Q', '3.704','0.1'), ('ugu', 'C', '3.704','0.1'), ('gug', 'V', '3.395','0.1'), ('aag', 'K', '3.086','0.1'), ('cug', 'L', '3.086','0.1'), ('aau', 'N', '2.778','0.1'), ('gau', 'D', '2.778','0.1'), ('ggu', 'G', '2.469','0.1'), ('cac', 'H', '2.16','0.1'), ('uuc', 'F', '2.16','0.1'), ('aug', 'M', '2.16','0.1'), ('ccu', 'P', '2.16','0.1'), ('guc', 'V', '1.852','0.1'), ('cug', 'L', '1.852','0.1'), ('gga', 'G', '1.852','0.1'), ('uuu', 'F', '1.852','0.1'), ('ggc', 'G', '1.852','0.1'), ('acc', 'T', '1.543','0.1'), ('uau', 'Y', '1.543','0.1'), ('gcg', 'A', '1.543','0.1'), ('ccu', 'P', '1.543','0.1'), ('gca', 'A', '1.543','0.1'), ('gag', 'E', '1.543','0.1'), ('guu', 'V', '1.543','0.1'), ('ccu', 'P', '1.543','0.1'), ('aaa', 'K', '1.543','0.1'), ('agu', 'S', '1.543','0.1'), ('aaa', 'K', '1.543','0.1'), ('gcu', 'A', '1.235','0.1'), ('uua', 'L', '1.235','0.1'), ('gag', 'E', '1.235','0.1'), ('gcc', 'A', '1.235','0.1'), ('acc', 'T', '1.235','0.1'), ('aaa', 'K', '0.926','0.1'), ('uug', 'L', '0.926','0.1'), ('gca', 'A', '0.926','0.1'), ('auu', 'I', '0.926','0.1'), ('gaa', 'E', '0.926','0.1'), ('gcu', 'A', '0.926','0.1'), ('ggc', 'G', '0.926','0.1'), ('uuc', 'F', '0.926','0.1'), ('cgc', 'R', '0.617','0.1'), ('cau', 'H', '0.617','0.1'), ('auu', 'I', '0.617','0.1'), ('gau', 'D', '0.617','0.1'), ('ucu', 'S', '0.617','0.1'), ('gcu', 'A', '0.617','0.1'), ('cau', 'H', '0.309','0.1'), ('uua', 'L', '0.309','0.1'), ('uac', 'Y', '0.309','0.1'), ('aau', 'N', '0.309','0.1'), ('aau', 'N', '0.309','0.1'), ('gag', 'E', '0.309','0.1'), ('gag', 'E', '0.309','0.1'), ('cag', 'Q', '0.309','0.1'), ('guu', 'V', '0.309','0.1')]")

def chrom10Codon_freq():
	'''
		RETURNS DUMMY DATA
		Function that will interact with a Blayer function4 that takes all available chromosome10 accession_id's in the DB, extract data needed from a function1 (see above) which is similar to def nt_coding and returns a list of freq per codon per all entries as float (%) - can be completed once and saved as static values in a file
	'''
	return("['gug', 4.321]['aag', 4.321]['gag', 4.012]['gau', 3.704]['aaa', 3.704]['cug', 3.704]['gcc', 3.704]['cag', 3.395]['gaa', 3.086]['cca', 3.086]['aau', 2.778]['uug', 2.778]['aac', 2.469]['uau', 2.16]['uuc', 2.16]['auu', 2.16]['uac', 2.16]['ccu', 1.852]['uuu', 1.852]['guu', 1.852]['cga', 1.852]['gac', 1.852]['ugu', 1.543]['guc', 1.543]['gga', 1.543]['ggc', 1.543]['gca', 1.543]['gcu', 1.543]['cau', 1.543]['auc', 1.543]['cuu', 1.543]['ucc', 1.543]['cuc', 1.543]['aug', 1.235]['acc', 1.235]['cgc', 1.235]['aga', 1.235]['uca', 1.235]['cac', 0.926]['agu', 0.926]['ucu', 0.926]['aua', 0.926]['ugg', 0.926]['ugc', 0.926]['cua', 0.926]['ggg', 0.926]['ggu', 0.617]['uua', 0.617]['agc', 0.617]['acu', 0.617]['agg', 0.617]['ccg', 0.617]['ucg', 0.309]['gcg', 0.309]['caa', 0.309]['gua', 0.309]['aca', 0.309]['acg', 0.309]['cgu', 0.309]['ccc', 0.309]['uaa', 0.309], ['uag', 0.009]['uga', 0.009]['cgg', 0.009]")

def restr_enz():
	'''
		RETURNS DUMMY DATA
		Function that will interact with Blayer functions that result and return nt_coding_region (see def above) with added enzyme sites into the string where the enzyme cuts in the sequence. Takes Enzyme restriction site information from the DB? or from a file? Returns also string list of noncutters and accession_id. Sites outside of the coding region or the good sites are indicated with double asterisk '**Enz**'; Unique sites are indicated: '*&Enz&* and good unique sites: '*&*Enz*&*'.
	'''
	return('AB032150', 'Noncutters: BsiWI, BstEII, EagI, KpnI, MluI, NotI, PvuI, SalI, SbfI, SphI, XhoI', "'{'AgeI': ['Site:', 'ACCGGT', 'Site_len:', 6, 'Cutting_offset:', 1, 'Cut position(s):', 11866, 'Frequency:', 1], 'ApoI': ['Site:', 'RAATTY', 'Site_len:', 6, 'Cutting_offset:', 1, 'Cut position(s):', 531, 1649, 1876, 2422, 2455, 2774, 3401, 3517, 3614, 3620, 3648, 3676, 3815, 4155, 4182, 7083, 7199, 8176, 9412, 9529, 9800, 9854, 10615, 11392, 11572, 11622, 11883, 11944, 12630, 12654, 13105, 13191, 13900, 14087, 14165, 14177, 14562, 14873, 15044, 15254, 15385, 16356, 16915, 18368, 'Frequency:', 44], 'BamHI': ['Site:', 'GGATCC', 'Site_len:', 6, 'Cutting_offset:', 1, 'Cut position(s):', 5679, 11811, 14138, 15937, 'Frequency:', 4], 'BclI': ['Site:', 'TGATCA', 'Site_len:', 6, 'Cutting_offset:', 1, 'Cut position(s):', 2373, 3995, 5962, 6583, 9255, 11069, 14550, 'Frequency:', 7], 'BmtI': ['Site:', 'GCTAGC', 'Site_len:', 6, 'Cutting_offset:', 5, 'Cut position(s):', 8252, 'Frequency:', 1], 'BsiWI': ['Site:', 'CGTACG', 'Site_len:', 6, 'Cutting_offset:', 1, 'Cut position(s):', 'Frequency:', 0], 'BsrGI': ['Site:', 'TGTACA', 'Site_len:', 6, 'Cutting_offset:', 1, 'Cut position(s):', 7701, 15769, 16623, 'Frequency:', 3], 'BstEII': ['Site:', 'GGTNACC', 'Site_len:', 7, 'Cutting_offset:', 1, 'Cut position(s):', 'Frequency:', 0], 'DraIII': ['Site:', 'CACNNNGTG', 'Site_len:', 9, 'Cutting_offset:', 6, 'Cut position(s):', 10453, 15778, 16993, 'Frequency:', 3], 'EagI': ['Site:', 'CGGCCG', 'Site_len:', 6, 'Cutting_offset:', 1, 'Cut position(s):', 'Frequency:', 0], 'EcoRI': ['Site:', 'GAATTC', 'Site_len:', 6, 'Cutting_offset:', 1, 'Cut position(s):', 7083, 9854, 15385, 'Frequency:', 3], 'HindIII': ['Site:', 'AAGCTT', 'Site_len:', 6, 'Cutting_offset:', 1, 'Cut position(s):', 5452, 'Frequency:', 1], 'KpnI': ['Site:', 'GGTACC', 'Site_len:', 6, 'Cutting_offset:', 5, 'Cut position(s):', 'Frequency:', 0], 'MfeI': ['Site:', 'CAATTG', 'Site_len:', 6, 'Cutting_offset:', 1, 'Cut position(s):', 5476, 6518, 9670, 9859, 13616, 15325, 'Frequency:', 6], 'MluI': ['Site:', 'ACGCGT', 'Site_len:', 6, 'Cutting_offset:', 1, 'Cut position(s):', 'Frequency:', 0], 'NcoI': ['Site:', 'CCATGG', 'Site_len:', 6, 'Cutting_offset:', 1, 'Cut position(s):', 606, 9005, 10135, 11829, 12828, 'Frequency:', 5], 'NheI': ['Site:', 'GCTAGC', 'Site_len:', 6, 'Cutting_offset:', 1, 'Cut position(s):', 8248, 'Frequency:', 1], 'NotI': ['Site:', 'GCGGCCGC', 'Site_len:', 8, 'Cutting_offset:', 2, 'Cut position(s):', 'Frequency:', 0], 'NsiI': ['Site:', 'ATGCAT', 'Site_len:', 6, 'Cutting_offset:', 5, 'Cut position(s):', 2449, 11326, 12390, 13398, 14152, 14549, 18252, 'Frequency:', 7], 'PstI': ['Site:', 'CTGCAG', 'Site_len:', 6, 'Cutting_offset:', 5, 'Cut position(s):', 3049, 5245, 6450, 8989, 11722, 15155, 17622, 'Frequency:', 7], 'PvuI': ['Site:', 'CGATCG', 'Site_len:', 6, 'Cutting_offset:', 4, 'Cut position(s):', 'Frequency:', 0], 'SacI': ['Site:', 'GAGCTC', 'Site_len:', 6, 'Cutting_offset:', 5, 'Cut position(s):', 5834, 7349, 12820, 15620, 'Frequency:', 4], 'SalI': ['Site:', 'GTCGAC', 'Site_len:', 6, 'Cutting_offset:', 1, 'Cut position(s):', 'Frequency:', 0], 'SbfI': ['Site:', 'CCTGCAGG', 'Site_len:', 8, 'Cutting_offset:', 6, 'Cut position(s):', 'Frequency:', 0], 'SpeI': ['Site:', 'ACTAGT', 'Site_len:', 6, 'Cutting_offset:', 1, 'Cut position(s):', 42, 3803, 5211, 6395, 7126, 9481, 10054, 10561, 11347, 16502, 17538, 'Frequency:', 11], 'SphI': ['Site:', 'GCATGC', 'Site_len:', 6, 'Cutting_offset:', 5, 'Cut position(s):', 'Frequency:', 0], 'StyI': ['Site:', 'CCWWGG', 'Site_len:', 6, 'Cutting_offset:', 1, 'Cut position(s):', 606, 6492, 8161, 8717, 8957, 9005, 10135, 10708, 11422, 11829, 12155, 12354, 12828, 13033, 15688, 16069, 17801, 'Frequency:', 17], 'XhoI': ['Site:', 'CTCGAG', 'Site_len:', 6, 'Cutting_offset:', 1, 'Cut position(s):', 'Frequency:', 0]}'")

