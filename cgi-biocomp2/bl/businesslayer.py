#!/usr/bin/python3
'''
TT
'''


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
from collections import defaultdict

def coding_region(accession):
    '''
    
    '''

    db_output = {}
    d_coding = {}
    source = db.getAccession(accession) 
    db_output.update(source)
    for k, v in db_output.items():
            if k == 'Coding Regions':
                    d_coding.update(v)
    #For highlighting the coding region:
    coding_highlighted = ''
    s2 = ''
    i = 1
    beginning = []
    end = []
    for k, v in db_output.items():
        if k == 'Sequence':
            s1 = str(v).split('\'')
            s2 = str(s1[1])
        if k == 'Complement':
            complement = str(v).strip()
    for k, v in d_coding.items():
        beginning.append(int((str(v).split(':'))[0]))
        end.append(int((str(v).split(':'))[1]))
    for u, n in enumerate(s2):
        for l in beginning:
            if u == l - i:
                coding_highlighted += '{'
        for e in end:
            if u == e:
                coding_highlighted += '}'
        else:
            coding_highlighted += n
    i += 2
    #For extracting the coding region:
    t = ''
    j = ''
    p = 2
    complement_nts = ''
    for k, v in d_coding.items():
        start = int((str(v).split(':'))[0])
        stop = int((str(v).split(':'))[1])
        for u, n in enumerate(s2):
            if u > start - p:
                if u < stop:
                    t += n
            else:
                j += n
    if complement == 'Y':
        for s in t:
            if s == 'G':
                complement_nts += 'C'
            elif s == 'C':
                complement_nts += 'G'
            elif s == 'A':
                complement_nts += 'T'
            elif s == 'T':
                complement_nts += 'A'
        complement_seq = complement_nts[::-1]
    if complement == 'Y':
        extractedCoding_region = complement_seq
    elif complement == 'N':
        extractedCoding_region = t
    return coding_highlighted, extractedCoding_region, accession, complement, d_coding

def aa_nt(accession):
    """
    
    """
    
    from businesslayer import coding_region
    db_output = {}
    d_coding = {}
    source = db.getAccession(accession)
    db_output.update(source)
    aminoacids = []
    for k, v in db_output.items():
        if k == 'Translation':
            aa_seq = str(v).replace('b\'','').replace(' ', '').replace('\'', '')
            aaseq_stop = aa_seq + '*'
    coding_Seq = bl.coding_region(accession)
    coding_ntSeq = coding_Seq[1]
    nt_triplets = [coding_ntSeq[i:i + 3] for i in range(0, len(coding_ntSeq), 3)]
    for s in aaseq_stop:
        aminoacids.append(s)
    zipped = list(zip(nt_triplets, aminoacids))
    return zipped, nt_triplets, accession

def enz_table(accession):
    """
    
    """
    enzyme_file = '../NEB_HF_restr_enz.txt'
    
    from businesslayer import coding_region
    
    table_dic = {}
    enzyme = []
    restr_site = []
    site_length = []
    cutting_offset = []

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
            if boundaries[0] <= ss <= boundaries[1]:
                badcutterlist += 1
            table_dic[k].append(ss)
        table_dic[k].append('Frequency:')
        table_dic[k].append(freq)
        if freq == 0:
            freq0.append(k)
        if badcutterlist == 0:
            if freq != 0:
                table_dic[k].append('This is a good enzyme!')
        badcutterlist = 0
        pattern = ''
        freq = 0
    return table_dic, 'List of noncutters: ', freq0, accession


def getAllCodingRegions():
    """

    """
    from businesslayer import coding_region, aa_nt

    db_out = {}
    d = defaultdict(int)
    final_list = []
    all_triplets = []
    allFreq_values = []
    unique_triplets = []
    source = db.getAllCodingRegions()
    for entry in source:
        db_out.update(entry)

        for k, v in db_out.items():
            #if k == 'Translation':
             #   if v == b'No Protein Product':
              #      break
            if k == 'Accession':
                accession_id = str(v).strip('\'')
                return_result = bl.coding_region(accession_id)
                final_list.append(return_result[1:3])
                coding_triplets = bl.aa_nt(accession_id)
                all_triplets.append(coding_triplets[1])
    for i in all_triplets:
        d[i] += 1
    length_alltriplets = len(all_triplets)
    for k, v in sorted(d.items(), key=operator.itemgetter(0)):
        unique_triplets.append(k)
        allfreq_value = str(round((v/length_alltriplets)*100, 3))
        allFreq_values.append(allfreq_value)
    zipped3 = list(zip(unique_triplets, allFreq_values)
                   
    return final_list, zipped3
    
        