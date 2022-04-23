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
    
    coding_highlighted = ''
    s2 = ''
    i = 0
    beginning = []
    end = []
    for k, v in db_output.items():
        if k == 'Sequence':
            s1 = str(v).split('\'')
            s2 = str(s1[1])
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
    return coding_highlighted, accession
