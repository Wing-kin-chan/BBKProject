#!/usr/bin/python3
"""
Dummy business layer APIs
List of function definitions to parse, and perform operations on Genbank entries from database
and return outputs to be presented on the webpage.

This is the business logic API

FIRST SEARCH RESULT PAGE:
	-def geneIdentifier(gene_name) 0...*
		gene_name as string (list of strings) from db
		Returns string (list of strings) for FE
	
	-def proteinProduct(prot_product) 0...*
		prot_product as string (list of strings) from bd
		Returns string (list of strings) for FE

	-def accession(accession_id) 0...1
		takes string form db
		Returns string for search

	-def chromosome(chrom_location) 0...*
		takes string (list of strings) from db
		Returns string (list of strings) for FE

SECOND SEARCH RESULT PAGE from links in first search result page:
	-def nt_coding(accession_id, nt_seq[string], codon_start[int], exon_boundaries[list of int tuples])
		Returns string of nt_seq with brackets indicating coding regions e.g. ATC{TGTGTCC}ATGTT & corresponding accession_id

	-def aant_seq(accession_id, aa_seq[string])
		Return nt_seq coding region only 1st row & aa_seq 2nd row aligned

	-def entry_codon_freq(accession_id)
		extract from a function similar to def nt_coding
		Returns freq per codon per entry as float

	-def overallcodon_usage(list_of_accession_id) accession*
		extract nt_coding regions from def nt_coding
		len(general list of codons), count per codon
		Return freq per codon per chromosome as float

	-def restr_enz(accession_id, enzyme[entered from webpage ??])
		Returns [nt_coding] with added [enz] into string where cuts

"""

# Add the bl sub-directory to the module path (for testing this routine)
# and the directory above to import the config file
import sys
sys.path.insert(0, "../db/")
sys.path.insert(0, "../")

import dbapi   # Import the database api
import config  # Import configuration information (if needed)

def getAllEntries():
    """
    ...Function comment header goes here...

    This is a very simple function that just calls the database API to do the SQL to 
    obtain the full list of entries. It doesn't need to do anything else.
    """
    return(dbapi.getAllEntries())

def gene_identifier():
	'''
		Dummy function that will pass name of the gene (in the chromosome file as '/gene=' as list of strings from db. This is marked as 'gene identifiers' in the requirements file. Can have zero to many result returns.
		Returns a list of strings for FE
	'''
	return(dbapi.getByGeneID())


def protein_product():
	'''
		Dummy function that will pass prot product name (in the chromosome file as '/product=') as list of strings from db. This is marked as 'protein product name' in the requirements file. Can have zero to many result returns.
		Returns list of strings for FE
	'''
	return(dbapi.getByProtein())

def accession_number():
	'''
		Dummy function that will pass accession number (in the chromosome file as 'ACCESSION') as string from db. This is marked as 'Genbank accession' in the requirements file. Can have zero to one result returned.
		Returns a list of strings for search. If no result then returns message??
	'''
	return(dbapi.getAccession)

def partial_accession_query():
	'''
		Dummy function that will pass accession number (in the chromosome file as 'ACCESSION') as string from db. This is marked as 'Genbank accession' in the requirements file. Can have zero to many result returns for a partial search term.
		Returns a list of strings for search. If no result then returns message??
	'''
	return(dbapi.getByAccessions())

def chromosomal_location():
	'''
		Dummy code that will pass chromosomal location as a list of strings from db. In the chromosome file as '/map=' as given by 'source'. This is marked as 'chromosomal location' in the requirements file. Can have zero to many result returns.
		Returns list of strings for FE
	'''
	return(dbapi.getByLocus())













