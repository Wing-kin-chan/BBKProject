#!/usr/bin/python3
"""
Program:    sub_bl
File:       sub_bl.py

Version:    V1.0
Date:       01.05.22
Function:   This is a sub code to obtain data stored in the database (DB)
            layer by calling the DB API functions and use the data in the
            functions to modify and calculate data to return a saved static
            files for various tasks for the BL

Copyright:  (c) Tiina Talts, MSc Student, Birkbeck UL, 2022
Author:     Tiina Talts
Address:    Institute of Structural and Molecular Biology
            Birkbeck University of London

--------------------------------------------------------------------------
Description:
============
This is a sub code to obtain data stored in the database (DB)
layer by calling the DB API functions and use the data in the
functions to modify and calculate data to return a saved static
files for various tasks for the BL
The various tasks that the code performs include:
-- return the coding regions for DNA sequences in the database
   and save as a static file in the /bl directory
-- return the overall codon usage within the chromoseme 10
   and save as a static file in the /bl directory


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
    For returning all the coding regions within the database of eligible
    entries from the human chromoseme 10.

    Input:  result       --- The result returned by dbapi getAllCodingRegions
                         function and by businesslayer coding_region function
    Return: (final_list) --- A list containing the extracted coding region
                         and its respective accession identifier for all
                         entries in the database

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
    For returning the codon usage frequencies for all the eligible entries
    from the human chromoseme 10.

    Input:  result       --- The result returned by dbapi getAllCodingRegions
                         function and by businesslayer aa_nt function
    Return: (zipped3)    --- A list containing the unique codons for all the
                         extracted coding regions and its respective frequency
                         value for all eligible entries in the human
                         chromosome 10 database

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
    For creating file overallcodonfreqs.txt that is saved in the /bl directory.

    Function can be run from the command line with command
    'python sub_bl.py writeFile_overallcodonfreqs'
    
    Input:  result                  --- no input from command line needed -
                                    uses function codonFreq_chromosome10
                                    which in turn uses database function
                                    getAllCodingRegions
    Return: (overallcodonfreqs.txt) --- A text file containing the codon
                                    frequencies for all the extracted coding
                                    regions and its respective frequency value
                                    for all eligible entries in the human
                                    chromosome10 database

    01.05.22  Original   By: TT
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
    For creating file getallcodingregions.txt that is saved in the /bl directory.

    Function can be run from the command line with command
    'python sub_bl.py writeFile_getallcodingregions'
    
    Input:  result                    --- no input from command line needed -
                                      uses function getAllCodingRegions
                                      which in turn uses database function
                                      getAllCodingRegions
    Return: (getallcodingregions.txt) --- A text file containing the coding
                                      regions for all the eligible entries in
                                      the human chromosome10 database

    01.05.22  Original   By: TT
    """
    from sub_bl import getAllCodingRegions
    
    new_file = "../bl/getallcodingregions.txt"
    
    with open(new_file, 'w') as f:
        data = sub.getAllCodingRegions()
        f.write(str(data))

    if __name__ == '__main__':
        globals()[sys.argv[1]]()
