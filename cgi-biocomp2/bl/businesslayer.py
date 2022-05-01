#!/usr/bin/python3
"""
Program:    businesslayer
File:       businesslayer.py

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
import config
import os
import operator
import re
import ast
from collections import defaultdict

#*************************************************************************




def coding_region(accession):
    """
    For highlighting and extracting the coding region per entry.

    Input:  result       --- The result returned by dbapi getAccession function
    Return: (coding_highlighted, extractedCoding_region, accession, complement, d_coding)
                         --- A list containing the 'highlighted' coding region (boundaries marked
                         by {} wirthing the original DNA sequence), extracted coding region,
                         its respective accession identifier, complement 'Y/N', and dictionary of coding boundaries

    01.05.22  Original   By: TT
    """

    db_output = {}
    d_coding = {}
    source = db.getAccession(accession) 
    db_output.update(source)
    for k, v in db_output.items():
            if k == 'Coding Regions':
                    d_coding.update(v)
    #For highlighting the coding region by marking the start
    #and end with entering '{' and/or '}' respectively
    #into the original DNA sequence:
    coding_highlighted = ''
    the_sequence = ''
    shift = 1
    beginning = []
    end = []
    for k, v in db_output.items():
        if k == 'Sequence':
            seq = str(v).split('\'')
            the_sequence = str(seq[1])
        if k == 'Complement':
            complement = str(v).strip()
    for k, v in d_coding.items():
        beginning.append(int((str(v).split(':'))[0]))
        end.append(int((str(v).split(':'))[1]))
    for nt_index, nts in enumerate(the_sequence):
        for b in beginning:
            if nt_index == b - shift:
                coding_highlighted += '{'
        for e in end:
            if nt_index == e:
                coding_highlighted += '}'
        else:
            coding_highlighted += nts
    shift += 2
    #For extracting the coding region by directing
    #the nucleotides into separate strings based on the
    #numbering of the coding region dictionary:
    coding_seq = ''
    noncoding_seq = ''
    base_correction = 2
    complement_nts = ''
    for k, v in d_coding.items():
        start = int((str(v).split(':'))[0])
        stop = int((str(v).split(':'))[1])
        for nt_index, nts in enumerate(the_sequence):
            if nt_index > start - base_correction:
                if nt_index < stop:
                    coding_seq += nts
            else:
                noncoding_seq += nts
    if complement == 'Y':
        for nt in coding_seq:
            if nt == 'G':
                complement_nts += 'C'
            elif nt == 'C':
                complement_nts += 'G'
            elif nt == 'A':
                complement_nts += 'T'
            elif nt == 'T':
                complement_nts += 'A'
        complement_seq = complement_nts[::-1]
    if complement == 'Y':
        extractedCoding_region = complement_seq
    elif complement == 'N':
        extractedCoding_region = coding_seq
    return coding_highlighted, extractedCoding_region, accession, complement, d_coding

def aa_nt(accession):
    """
    For returning the amino acid sequence with the coding nucleotide or codon sequence.

    Input:  result       --- The result returned by dbapi getAccession function
    Return: (zipped, nt_triplets, accession)
                         --- A list containing the nucleotide codon and amino acid letter as a tuple,
                         nucleotide codon and its respective accession identifier

    01.05.22  Original   By: TT
    """
    
    from businesslayer import coding_region
    #Extracts the amino acid sequence string via dbapi getAccession function
    #and dictionary key 'Translation' value; adds a stop codon '*' at the end:
    db_output = {}
    d_coding = {}
    source = db.getAccession(accession)
    db_output.update(source)
    aminoacids = []
    u_triplets = []
    for k, v in db_output.items():
        if k == 'Translation':
            aa_seq = str(v).replace('b\'','').replace(' ', '').replace('\'', '')
            aaseq_stop = aa_seq + '*'
    #Generates triplets for the return of the coding region function per entry,
    #and zippes the triplets into tuples with its respective amino acid letters:
    coding_Seq = bl.coding_region(accession)
    coding_ntSeq = coding_Seq[1]
    nt_triplets = [coding_ntSeq[i:i + 3] for i in range(0, len(coding_ntSeq), 3)]
    for l in nt_triplets:
        codon_u = l.replace('T', 'U')
        u_triplets.append(codon_u)
    for s in aaseq_stop:
        aminoacids.append(s)
    zipped1 = list(zip(nt_triplets, aminoacids))
    zipped2 = list(zip(u_triplets, aminoacids))
    return zipped1, nt_triplets, accession, zipped2, u_triplets

def enz_table(accession):
    """
    For returning the return sticky-end restriction enzyme sites in the genomic DNA - i.e. in
    both coding and non-coding regions.

    Input:  result       --- The result returned by businesslayer coding_region that in turn takes result from
                         dbapi getAccession function
    Return: (table_dic, 'List of noncutters: ', freq0, accession)
                         --- A list containing the restricion enzyme cutting information as a dictionary,
                         a list of non-cutting enzymes and its respective accession identifier

    01.05.22  Original   By: TT
    """
    enzyme_file = '../NEB_HF_restr_enz.txt'
    
    from businesslayer import coding_region
    
    table_dic = {}
    enzyme = []
    restr_site = []
    site_length = []
    cutting_offset = []

    #Takes the enzyme file and creates a dictionary for the list of enzymes
    #used in this search of restirction sites for the entry:
    with open(enzyme_file, 'r') as f:
        file = f.read().splitlines() 
    for i in file:
        enzyme.append(i.split('=')[0])
        site = i.split('=')[1]
        restr_site.append(site)
        site_len = len(site)
        site_length.append(site_len)
        cutting_offset = int(i.split('=')[2])
        table_dic[i.split('=')[0]] = ['Site:', site, 'Site_len:', site_len, 'Cutting_offset:', cutting_offset, 'Cut position(s):']
        site_len = 0
    
    boundaries0 = []
    coding_Seq = bl.coding_region(accession)
    coding_ntSeq = coding_Seq[1]

    #Determines the boundaries of the coding regions for the entry
    #to help determine if enzyme is 'good' via min and max boundary number:
    d_coding = {}
    source = bl.coding_region(accession) 
    d_coding.update(source[3])
    for x, y in d_coding.items():
        boundaries0.append(int((str(y).split(':'))[0]))
        boundaries0.append(int((str(y).split(':'))[1]))
        coding_beginning = min(boundaries0)
        coding_end = max(boundaries0)
        boundaries = [coding_beginning, coding_end]
  
    freq0 = []
    degen = 'RYSWKMBDHVN'
    pattern = ''
    freq = 0
    badcutterlist = 0
    #Creates a pattern for each enzyme using its cutting sequence and performes a regular
    #expression search for each pattern in the given entry sequence;
    #takes into account degenerate bases in the enzyme cutting sequence
    #NOTE: not all degenerate patterns are entered into the code but only the ones
    #that feature in the enzyme list given in the enzyme file - if enzymes added into the file, the code here
    #needs revisiting and any additional degeneracies added!:
    for k, v in table_dic.items():
        for nucleotide in v[1]:
            if nucleotide in degen:
                if nucleotide == 'R':
                    pattern += '[AG]'
                elif nucleotide == 'Y':
                    pattern += '[CT]'
                elif nucleotide == 'W':
                    pattern += '[AT]'
                elif nucleotide == 'N':
                    pattern += '[ATCG]'
            else:
                pattern += nucleotide
        for match in re.finditer(pattern, coding_ntSeq):
            ss = match.start() + v[5]
            freq += 1
            #Counts the bad cutters that cut within the coding boundaries:
            if boundaries[0] <= ss <= boundaries[1]:
                badcutterlist += 1
            table_dic[k].append(ss)
        table_dic[k].append('Frequency:')
        table_dic[k].append(freq)
        #If frequency is zero for that enzyme adds the
        #dictionary keys or enzyme name to the non-cutter list:
        if freq == 0:
            freq0.append(k)
        #If bad cutter list is zero and frequency is not
        #equal to zero means this is a good enzyme that cuts outside of the coding region:
        if badcutterlist == 0:
            if freq != 0:
                table_dic[k].append('This is a good enzyme!')
        badcutterlist = 0
        pattern = ''
        freq = 0
    return table_dic, 'List of noncutters: ', freq0, accession


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

def codonFreq_entry(accession):
    """
    """
    
    from businesslayer import aa_nt

    codonfreq_file = "../bl/overallcodonfreqs.txt"
    
    d = defaultdict(int)
    d_entryFreq = {}
    d_chromFreq = {}
    source = bl.aa_nt(accession)
    return_aaNt = source[3]
    u_triplets = source[4]

    with open(codonfreq_file, 'r') as f:
        file = f.read()
        data = ast.literal_eval(file)
        d_chromFreq.update(data)
    
    for item in return_aaNt:
        d_entryFreq[item[0]] = [item[1]]
    for i in u_triplets:
        d[i] += 1
    length_entryCodons = len(return_aaNt)
    for codon, v in d.items():
        entryFreq_value = round((v/length_entryCodons)*100, 3)
        d_entryFreq[codon].append(entryFreq_value)
    for k, v in d_chromFreq.items():
        for codon, value in d_entryFreq.items():
            if k == codon:
                d_entryFreq[codon].append(v)    
                   
    return d_entryFreq, accession

    
        
