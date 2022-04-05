#!/usr/bin/python3
'''
TT
'''


import sys
sys.path.insert(0, "../db")
sys.path.insert(0, "../")


import dbapi as db
import config

new_file = "../bl/getallcodingregions.txt"

with open(new_file, 'w') as f:
    tt = db.getAllCodingRegions()
    f.write(str(tt))
#print(tt)
