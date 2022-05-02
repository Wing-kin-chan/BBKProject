#!/usr/bin/python3
"""
Program:    sub_bl
File:       sub_bl.py

Version:    V1.0
Date:       01.05.22
Function:   Obtain data stored in the database (DB) layer by calling the DB API
            functions and use the data in the functions to modify and calculate
            data to return for various tasks and searches for the FE

Copyright:  (c) Tiina Talts, MSc Student, Birkbeck UL, 2022
Author:     Tiina Talts
Address:    Institute of Structural and Molecular Biology
            Birkbeck University of London

--------------------------------------------------------------------------
Description:
============
Obtain data stored in the database (DB) layer by calling the DB API
functions and use the data in the functions to modify and calculate
data to return for various tasks and searches for the FE.
The various tasks that the code performs include:
-- return the complete DNA sequence with the coding regions specified
-- return the amino acid sequence with the coding DNA sequence
-- return codon usage frequencies within the coding region
-- return the overall codon usage within the chromoseme 10
-- return sticky-end restriction enzyme sites in the genomic DNA - i.e. in
   both coding and non-coding regions

--------------------------------------------------------------------------
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


import dbapi as db
import businesslayer as bl
import sub_bl as sub
import config
import os
from collections import defaultdict

#*************************************************************************

def getAllCodingRegions():
    """
    For returning all the coding regions within the database of eligible entries from the human chromoseme 10.

    Input:  result       --- The result returned by dbapi getAllCodingRegions function and
                         by businesslayer coding_region function
    Return: (final_list) --- A list containing the extracted coding region and its respective accession identifier
                         for all entries in the database

    01.05.22  Original   By: TT
    """
    from businesslayer import coding_region

    db_out = {}
    final_list = []
    source = db.getAllCodingRegions()
    for entry in source:
        db_out.update(entry)

        for k, v in db_out.items():
            if k == 'Accession':
                accession_id = str(v).strip('\'')
                return_result = bl.coding_region(accession_id)
                final_list.append(return_result[1:3])
                   
    return final_list


def codonFreq_chromosome10():
    """
    For returning the codon usage frequencies for all the eligible entries from the human chromoseme 10.

    Input:  result       --- The result returned by dbapi getAllCodingRegions function and
                         by businesslayer aa_nt function
    Return: (zipped3)    --- A list containing the unique codons for all the extracted coding regions
                         and its respective frequency value for all eligible entries in the human chromosome 10 database

    01.05.22  Original   By: TT
    """
    from businesslayer import aa_nt

    db_out = {}
    d = defaultdict(int)
    all_triplets = []
    allFreq_values = []
    unique_triplets = []
    source = db.getAllCodingRegions()
    for entry in source:
        db_out.update(entry)

        for k, v in db_out.items():
            if k == 'Accession':
                accession_id = str(v).strip('\'')
                return_result = bl.aa_nt(accession_id)
                coding_triplets = return_result[1]
                for codon in coding_triplets:
                    codon_u = codon.replace('T', 'U')
                    all_triplets.append(codon_u)
    for i in all_triplets:
        d[i] += 1
    length_alltriplets = len(all_triplets)
    for k, v in d.items():
        unique_triplets.append(k)
        allfreq_value = str(round((v/length_alltriplets)*100, 3))
        allFreq_values.append(allfreq_value)
        
    zipped3 = list(zip(unique_triplets, allFreq_values))
                   
    return zipped3

def writeFile_overallcodonfreqs():
    """
    """
    from sub_bl import codonFreq_chromosome10
    
    new_file = "../bl/overallcodonfreqs.txt"
    
    with open(new_file, 'w') as f:
        data = sub.codonFreq_chromosome10()
        f.write(str(data))
        
    if __name__ == '__main__':
        globals()[sys.argv[1]]()


def writeFile_getallcodingregions():
    """
    """
    from sub_bl import getAllCodingRegions
    
    new_file = "../bl/getallcodingregions.txt"
    
    with open(new_file, 'w') as f:
        data = sub.getAllCodingRegions()
        f.write(str(data))

    if __name__ == '__main__':
        globals()[sys.argv[1]]()
