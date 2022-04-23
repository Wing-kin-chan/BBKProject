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
		Function that will interact with a Blayer coding_region function that takes accession_id, nt_seq[string], codon_start[int], exon_boundaries[list of int tuples] from the DBlayer and returns string of nt_seq with brackets indicating coding regions e.g. ATC{TGTGTCC}ATGTT & corresponding accession_id
	'''
	return bl.coding_region(accession)


def aaNt_seqsAligned():
	'''
		RETURNS DUMMY DATA
		Function that will interact with a Blayer function2 that takes accession_id, aa_seq[string] and function1 (see above) with corresponding input from the DBlayer, and returns a tuple of nt triplet and corresponding aa letter [or string of nt_seq (coding region only) 1st row & aa_seq 2nd row aligned?]; & corresponding accession_id
	'''		
	return('AB032150', "[('ATG', 'M'), ('GAT', 'D'), ('TCG', 'S'), ('AAA', 'K'), ('TAT', 'Y'), ('CAG', 'Q'), ('TGT', 'C'), ('GTG', 'V'), ('AAG', 'K'), ('CTG', 'L'), ('AAT', 'N'), ('GAT', 'D'), ('GGT', 'G'), ('CAC', 'H'), ('TTC', 'F'), ('ATG', 'M'), ('CCT', 'P'), ('GTC', 'V'), ('CTG', 'L'), ('GGA', 'G'), ('TTT', 'F'), ('GGC', 'G'), ('ACC', 'T'), ('TAT', 'Y'), ('GCG', 'A'), ('CCT', 'P'), ('GCA', 'A'), ('GAG', 'E'), ('GTT', 'V'), ('CCT', 'P'), ('AAA', 'K'), ('AGT', 'S'), ('AAA', 'K'), ('GCT', 'A'), ('TTA', 'L'), ('GAG', 'E'), ('GCC', 'A'), ('ACC', 'T'), ('AAA', 'K'), ('TTG', 'L'), ('GCA', 'A'), ('ATT', 'I'), ('GAA', 'E'), ('GCT', 'A'), ('GGC', 'G'), ('TTC', 'F'), ('CGC', 'R'), ('CAT', 'H'), ('ATT', 'I'), ('GAT', 'D'), ('TCT', 'S'), ('GCT', 'A'), ('CAT', 'H'), ('TTA', 'L'), ('TAC', 'Y'), ('AAT', 'N'), ('AAT', 'N'), ('GAG', 'E'), ('GAG', 'E'), ('CAG', 'Q'), ('GTT', 'V'), ('GGA', 'G'), ('CTG', 'L'), ('GCC', 'A'), ('ATC', 'I'), ('CGA', 'R'), ('AGC', 'S'), ('AAG', 'K'), ('ATT', 'I'), ('GCA', 'A'), ('GAT', 'D'), ('GGC', 'G'), ('AGT', 'S'), ('GTG', 'V'), ('AAG', 'K'), ('AGA', 'R'), ('GAA', 'E'), ('GAC', 'D'), ('ATA', 'I'), ('TTC', 'F'), ('TAC', 'Y'), ('ACT', 'T'), ('TCA', 'S'), ('AAG', 'K'), ('CTT', 'L'), ('TGG', 'W'), ('TGC', 'C'), ('AAT', 'N'), ('TCC', 'S'), ('CAT', 'H'), ('CGA', 'R'), ('CCA', 'P'), ('GAG', 'E'), ('TTG', 'L'), ('GTC', 'V'), ('CGA', 'R'), ('CCA', 'P'), ('GCC', 'A'), ('TTG', 'L'), ('GAA', 'E'), ('AGG', 'R'), ('TCA', 'S'), ('CTG', 'L'), ('AAA', 'K'), ('AAT', 'N'), ('CTT', 'L'), ('CAA', 'Q'), ('TTG', 'L'), ('GAT', 'D'), ('TAT', 'Y'), ('GTT', 'V'), ('GAC', 'D'), ('CTC', 'L'), ('TAC', 'Y'), ('CTT', 'L'), ('ATT', 'I'), ('CAT', 'H'), ('TTT', 'F'), ('CCA', 'P'), ('GTG', 'V'), ('TCT', 'S'), ('GTA', 'V'), ('AAG', 'K'), ('CCA', 'P'), ('GGT', 'G'), ('GAG', 'E'), ('GAA', 'E'), ('GTG', 'V'), ('ATC', 'I'), ('CCA', 'P'), ('AAA', 'K'), ('GAT', 'D'), ('GAA', 'E'), ('AAT', 'N'), ('GGA', 'G'), ('AAA', 'K'), ('ATA', 'I'), ('CTA', 'L'), ('TTT', 'F'), ('GAC', 'D'), ('ACA', 'T'), ('GTG', 'V'), ('GAT', 'D'), ('CTC', 'L'), ('TGT', 'C'), ('GCC', 'A'), ('ACG', 'T'), ('TGG', 'W'), ('GAG', 'E'), ('GCC', 'A'), ('GTG', 'V'), ('GAG', 'E'), ('AAG', 'K'), ('TGT', 'C'), ('AAA', 'K'), ('GAT', 'D'), ('GCA', 'A'), ('GGA', 'G'), ('TTG', 'L'), ('GCC', 'A'), ('AAG', 'K'), ('TCC', 'S'), ('ATC', 'I'), ('GGG', 'G'), ('GTG', 'V'), ('TCC', 'S'), ('AAC', 'N'), ('TTC', 'F'), ('AAC', 'N'), ('CGC', 'R'), ('AGG', 'R'), ('CAG', 'Q'), ('CTG', 'L'), ('GAG', 'E'), ('ATG', 'M'), ('ATC', 'I'), ('CTC', 'L'), ('AAC', 'N'), ('AAG', 'K'), ('CCA', 'P'), ('GGG', 'G'), ('CTC', 'L'), ('AAG', 'K'), ('TAC', 'Y'), ('AAG', 'K'), ('CCT', 'P'), ('GTC', 'V'), ('TGC', 'C'), ('AAC', 'N'), ('CAG', 'Q'), ('GTG', 'V'), ('GAA', 'E'), ('TGT', 'C'), ('CAT', 'H'), ('CCT', 'P'), ('TAC', 'Y'), ('TTC', 'F'), ('AAC', 'N'), ('CAG', 'Q'), ('AGA', 'R'), ('AAA', 'K'), ('CTG', 'L'), ('CTG', 'L'), ('GAT', 'D'), ('TTC', 'F'), ('TGC', 'C'), ('AAG', 'K'), ('TCA', 'S'), ('AAA', 'K'), ('GAC', 'D'), ('ATT', 'I'), ('GTT', 'V'), ('CTG', 'L'), ('GTT', 'V'), ('GCC', 'A'), ('TAT', 'Y'), ('AGT', 'S'), ('GCT', 'A'), ('CTG', 'L'), ('GGA', 'G'), ('TCC', 'S'), ('CAC', 'H'), ('CGA', 'R'), ('GAA', 'E'), ('GAA', 'E'), ('CCA', 'P'), ('TGG', 'W'), ('GTG', 'V'), ('GAC', 'D'), ('CCG', 'P'), ('AAC', 'N'), ('TCC', 'S'), ('CCG', 'P'), ('GTG', 'V'), ('CTC', 'L'), ('TTG', 'L'), ('GAG', 'E'), ('GAC', 'D'), ('CCA', 'P'), ('GTC', 'V'), ('CTT', 'L'), ('TGT', 'C'), ('GCC', 'A'), ('TTG', 'L'), ('GCA', 'A'), ('AAA', 'K'), ('AAG', 'K'), ('CAC', 'H'), ('AAG', 'K'), ('CGA', 'R'), ('ACC', 'T'), ('CCA', 'P'), ('GCC', 'A'), ('CTG', 'L'), ('ATT', 'I'), ('GCC', 'A'), ('CTG', 'L'), ('CGC', 'R'), ('TAC', 'Y'), ('CAG', 'Q'), ('CTA', 'L'), ('CAG', 'Q'), ('CGT', 'R'), ('GGG', 'G'), ('GTT', 'V'), ('GTG', 'V'), ('GTC', 'V'), ('CTG', 'L'), ('GCC', 'A'), ('AAG', 'K'), ('AGC', 'S'), ('TAC', 'Y'), ('AAT', 'N'), ('GAG', 'E'), ('CAG', 'Q'), ('CGC', 'R'), ('ATC', 'I'), ('AGA', 'R'), ('CAG', 'Q'), ('AAC', 'N'), ('GTG', 'V'), ('CAG', 'Q'), ('GTG', 'V'), ('TTT', 'F'), ('GAA', 'E'), ('TTC', 'F'), ('CAG', 'Q'), ('TTG', 'L'), ('ACT', 'T'), ('TCA', 'S'), ('GAG', 'E'), ('GAG', 'E'), ('ATG', 'M'), ('AAA', 'K'), ('GCC', 'A'), ('ATA', 'I'), ('GAT', 'D'), ('GGC', 'G'), ('CTA', 'L'), ('AAC', 'N'), ('AGA', 'R'), ('AAT', 'N'), ('GTG', 'V'), ('CGA', 'R'), ('TAT', 'Y'), ('TTG', 'L'), ('ACC', 'T'), ('CTT', 'L'), ('GAT', 'D'), ('ATT', 'I'), ('TTT', 'F'), ('GCT', 'A'), ('GGC', 'G'), ('CCC', 'P'), ('CCT', 'P'), ('AAT', 'N'), ('TAT', 'Y'), ('CCA', 'P'), ('TTT', 'F'), ('TCT', 'S'), ('GAT', 'D'), ('GAA', 'E'), ('TAT', 'Y'), ('TAA', '*')]")

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

