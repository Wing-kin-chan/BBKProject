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
            
    
    return db_output
