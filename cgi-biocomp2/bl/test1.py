#!/usr/bin/python3
'''
TT
'''


import sys
sys.path.insert(0, "../db")
sys.path.insert(0, "../")


import dbapi as db
import config

new_file = "../bl/AB032150_getAccession.txt"

with open(new_file, 'w') as f:
	tt = db.getAccession('AB032150')
	f.write(str(tt))
