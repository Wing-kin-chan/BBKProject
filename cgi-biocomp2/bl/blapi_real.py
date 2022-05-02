#!/usr/bin/python3
"""
Program:    blapi_real
File:       blapi_real.py

Version:    V1.0
Date:       01.05.22
Function:   This is the business logic API to obtain modified and
            calculated data from the businesslayer (BL) by calling the BL
            functions and return for various tasks and searches for the FE

Copyright:  (c) Tiina Talts, Bioinformatics MSc Student, Birkbeck UoL, 2022
Author:     Tiina Talts
Address:    Institute of Structural and Molecular Biology
            Birkbeck University of London

---------------------------------------------------------------------------
Description:
============
This is the business logic API to obtain modified and calculated data from
the businesslayer (BL) by calling the BL functions and return for various
tasks and searches for the FE
The various tasks that are called include:
-- return the complete DNA sequence with the coding regions specified
-- return the amino acid sequence with the coding DNA sequence
-- return codon usage frequencies within the coding region
-- return the overall codon usage within the chromoseme 10
-- return sticky-end restriction enzyme sites in the genomic DNA - i.e. in
   both coding and non-coding regions

---------------------------------------------------------------------------
Revision History:
=================
V1.0   01.05.22   Original   By: TT
"""

#*************************************************************************
# Import libraries
import sys
sys.path.insert(0, "../db")
sys.path.insert(0, "../bl")
sys.path.insert(0, "../")

import dbapi
import config
import businesslayer as bl

def getAllEntries():
    """
    This is a function that calls the database API to do the SQL to 
    obtain the full list of entries.

    Input:  search   --- Search term as string entered from the webpage
    Return: (accession)
                     --- A list of strings of Accession identifiers
    
    """
    return(dbapi.getAllEntries())

def getByGeneID(query: str, resultslen: int):
    """
    Function that will pass name of the gene (in the chromosome file as
    '/gene=') as list of strings from db. This is marked as 'gene identifiers'
    in the requirements file. Can have zero to many result returns.
    Returns a list of strings for FE.

    Input:  search   --- Search term as string entered from the webpage
    Return: (gene_id)
                     --- A list of strings of gene name identifiers
    """
    return dbapi.getByGeneID(query, resultslen)

def getByProtein(query: str, resultslen: int):
    """
    Function that will pass prot product name (in the chromosome file as
    '/product=') as list of strings from db. This is marked as
    'protein product name' in the requirements file. Can have zero to
    many result returns. Returns list of strings for FE

    Input:  search   --- Search term as string entered from the webpage
    Return: (product)
                     --- A list of strings of protein name identifiers
    """
    return dbapi.getByProduct(query, resultslen)

def getAccession(query: str):
    """
    Function that will pass accession number (in the chromosome file
    as 'ACCESSION') as string from db. This is marked as
    'Genbank accession' in the requirements file. Can have zero to one
    result returned. Returns a list of strings for search.
    If no result then returns message: 'Database error {}'

    Input:  search   --- Search term as string entered from the webpage
    Return: (accession)
                     --- A list of strings of accession identifiers
    """
    return dbapi.getAccession(query)

def getByAccession(query: str, resultslen: int):
    """
    Function that will pass accession number (in the chromosome file as
    'ACCESSION') as string from db. This is marked as 'Genbank accession'
    in the requirements file. Can have zero to many result returns for
    a partial search term. Returns a list of strings for search.
    If no result then returns message: 'Database error {}'
    
    Input:  search   --- Partial search term as string entered from the webpage
    Return: (accession)
                     --- A list of strings of accession identifiers
    """
    return dbapi.getByAccession(query, resultslen) 

def getByLocus(query: str, resultslen: int):
    """
    Function that will pass chromosomal location as a list of strings
    from db. In the chromosome file as '/map=' as given by 'source'.
    This is marked as 'chromosomal location' in the requirements file.
    Can have zero to many result returns. Returns list of strings for FE

    Input:  search   --- Search term as string entered from the webpage
    Return: (locus)
                     --- A list of strings of locus identifiers
    """
    return dbapi.getByLocus(query, resultslen) 

def ntCoding_region(accession):
    """
    Function that will interact with a Blayer 'coding_region' function that
    takes accession_id, nt_seq[string], codon_start[int],
    exon_boundaries[list of int tuples] from the DBlayer and returns
    string of nt_seq with brackets indicating coding regions
    e.g. ATC{TGTGTCC}ATGTT, extracted coding region,
    corresponding accession_id & a list of coding boundaries.
    
    Input:  accession   --- Search term as string entered from the webpage
    
    Return: (coding_highlighted, extractedCoding_region, accession,
                        complement, d_coding)
                        --- A list of strings of 'coding region highlighted',
                        coding region extrcated, corresponding accession
                        identifier, complement 'Y/N'; and a dictionary of
                        coding regions
    """
    return bl.coding_region(accession)

def aaNt_seqsAligned(accession):
    """
    Function that will interact with a Blayer function aa_nt that
    takes accession_id, aa_seq[string] and function coding_region
    with corresponding input from the DBlayer, and returns a list of
    tuples of nt triplet and corresponding aa letter; & corresponding
    accession_id
    
    Input:  accession   --- Search term as string entered from the webpage
    
    Return: (zipped1, nt_triplets, accession, zipped2, u_triplets)
                        --- A list of tuples of codons with their respective
                        amino acid one letter code, a list of codons,
                        corresponding accession identifier, a list of tuples
                        of codons where 'T' is replaced with 'U' and its
                        corresponding amino acid one letter code, a list of
                        codons where 'T' is replaced with 'U'
    """		
    return bl.aa_nt(accession)

def entryCodon_freq(accession):
    """
    Function that will interact with a Blayer function codonFreq_entry
    that takes accession_id, extract data needed from a function aa_nt
    and saved .txt file with data derived previously from function
    codonFreq_chromosome10 and returns a list of codons for the entry,
    frequencies per codon per entry as float (%), frequencies per codon
    per chromosome as float (%), corresponding amino acid letter code;
    & corresponding accession_id for the entry

    Input:  accession   --- Search term as string entered from the webpage
    
    Return: (d_entryFreq, accession)
                        --- A dictionary containing the unique
                            codons for the entry coding region, its
                            respective amino acid one letter code,
                            codon usage frequency value per entry,
                            codon usage frequency value per chromosome;
                            and respective accession identifier for the entry
    """
    return bl.codonFreq_entry(accession)

def restr_enz(accession):
    """
    Function that will interact with Blayer functions that return a
    dictionary of list of restriction enzyme cutting information
    that includes enzyme name; cutting site; cutting site length; cutting
    'offset' or positition within the cutting site where the enzyme cuts;
    cut positions across the enrty nucleotide sequence - non-coding region
    and coding region; cutting frequency; and a flag 'This is a good enzyme!'
    if the cutting position is located outside of the coding region: either
    before the start of the first coding region and/or after the end of the
    last coding region. The enzyme list consists of New England Biolabs (NEB)
    high fidelity (HF) sticky-end restriction enzymes that includes
    EcoRI, BamHI and BsuMI as XhoI its prototype.

    Input:  accession    --- Search term as string entered from the webpage

    Return: (table_dic, 'List of noncutters: ', freq0, accession)
                         --- A list containing the restricion enzyme
                         cutting information as a dictionary, a list of
                         non-cutting enzymes and its respective accession
                         identifier
    """
    return bl.enz_table(accession)
