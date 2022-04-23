#!/usr/bin/python3
'''
TT
'''


import sys
sys.path.insert(0, "../db")
sys.path.insert(0, "../")


import dbapi as db
import config
import os


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
    i = 0
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
            if u == e - i:
                coding_highlighted += '}'
        else:
            coding_highlighted += n
    i += 2
    #For ectracting the coding region:
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
    return coding_highlighted, extractedCoding_region, accession

def aa_nt(accession):
    """
    
    """
    import businesslayer as bl
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
    return zipped, accession
