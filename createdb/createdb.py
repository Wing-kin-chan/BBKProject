#!/usr/bin/env python3
'''
Code to first parse the genbank file into Python, then load onto MySQL Database.
Written by Wing
'''
#Import dependencies to read data data and parser
from Bio import SeqIO
import re
from datetime import datetime

#Create lists for each property of gene entry
accessions = list()
dates = list()
loci = list()
geneIDs = list()
protein_products = list()
descriptions = list()
sources = list()
sequences = list()
translations = list()
coding_regions = list()
reading_frames = list()
complement = list()
partial_CDS_records = 0
overlapping_records = 0

#Define regex for parsing coding regions
cds_search = re.compile(r'[0-9]+:[0-9]+') 
partial_search = re.compile(r'(>|<)[0-9]+')
ext_join_search = re.compile(r'[A-Z]{1,}[0-9]+')

#Import and parse data into variable as lists
for record in SeqIO.parse('chrom_CDS_10.gb', 'genbank'):
    accession = record.annotations['accessions'][0]
    #CDS Boundaries and entry validation
    coding_seq_str = str([feature for feature in record.features if feature.type == 'CDS'][0].location)
    
    #Skip entry due to partial CDS
    if partial_search.search(coding_seq_str):
        print(f'Omitting {accession}: Partial CDS')
        partial_CDS_records += 1
        continue
    #Skip entry due to overlapping with other gene
    if ext_join_search.search(coding_seq_str):
        print(f'Omitting {accession}: External CDS join')
        overlapping_records += 1
        continue
    #If CDS feature of entry is valid, append record
    else:
        #Check if CDS is reverse complement:
        if '(-)' in coding_seq_str:
            complement.append('Y')
        else:
            complement.append('N')
        cds_no = 0
        coding_seqs = dict()
        for match in cds_search.finditer(coding_seq_str):
            cds_no += 1
            coding_seqs['CDS {}'.format(cds_no)] = match.group()
        coding_regions.append(coding_seqs)
        accessions.append(accession)
        dates.append(datetime.strptime(record.annotations['date'], '%d-%b-%Y').strftime('%Y-%m-%d'))
        geneIDs.append(record.annotations['gi'])
        descriptions.append(record.description)
        sources.append(record.annotations['source'])
        sequences.append(str(record.seq))
        reading_frames.append([feature for feature in record.features if feature.type == 'CDS'][0].qualifiers['codon_start'][0])
        
        if 'map' in  [feature for feature in record.features if feature.type == 'source'][0].qualifiers.keys():
            location = [feature for feature in record.features if feature.type == 'source'][0].qualifiers['map'][0]
        else:
            location = [feature for feature in record.features if feature.type == 'source'][0].qualifiers['chromosome'][0]
        loci.append(location)
        
        if 'product' in [feature for feature in record.features if feature.type == 'CDS'][0].qualifiers.keys():
            proteinproduct = [feature for feature in record.features if feature.type == 'CDS'][0].qualifiers['product'][0]
        else:
            proteinproduct = ''
        protein_products.append(proteinproduct)
        
        if 'translation' in [feature for feature in record.features if feature.type == 'CDS'][0].qualifiers.keys():
            translation = [feature for feature in record.features if feature.type == 'CDS'][0].qualifiers['translation'][0]
        else:
            translation = 'No Protein Product'
        translations.append(translation)

print(f'Partial CDS Records Omitted: {partial_CDS_records}')
print(f'Overlapping Records Omitted: {overlapping_records}')

#Import dependencies
import pymysql
from pymysql import cursors

import sys
sys.path.insert(0, "../cgi-biocomp2")

import config 

#Connection object
connection = pymysql.connect(
    host = config.dbhost,
    port = config.port,
    user = config.dbuser,
    password = config.dbpass,
    db = config.dbname,
)

#Cursor Object
cursor = connection.cursor()

#Create tables
create_db = dict()
create_db['drop gene table'] = 'DROP TABLE IF EXISTS genes;'
create_db['gene_tbl'] = '''CREATE TABLE genes(Accession VARCHAR(12) PRIMARY KEY, Date DATE NOT NULL, Locus VARCHAR(40) NOT NULL, GeneID VARCHAR(8) NOT NULL, Product VARCHAR(255) NOT NULL, Description VARCHAR(255) NOT NULL, Source VARCHAR(60) NOT NULL, Sequence LONGBLOB NOT NULL, Frame INT(1) NOT NULL, Translation LONGBLOB NOT NULL, Coding_seq LONGBLOB, Coding_regions BLOB NOT NULL, Complement ENUM('Y', 'N') NOT NULL);'''

for k, v in create_db.items():
    try:
        print('Executing {}: '.format(k), end = '')
        cursor.execute(v)
    except pymysql.err.Error as e:
        print(f'{k} Failed: {e}')
        exit(1)
    else:
        print('OK')
        connection.commit()
cursor.close()
        
#Load data into SQL Server
import json

cursor = connection.cursor()
try:
    for i in range(0, len(accessions)):
        cursor.execute('INSERT INTO genes VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                    (accessions[i], 
                     dates[i], 
                     loci[i], 
                     geneIDs[i], 
                     protein_products[i], 
                     descriptions[i], 
                     sources[i], 
                     sequences[i], 
                     reading_frames[i], 
                     translations[i], 
                     None, 
                     json.dumps(coding_regions[i]),
                     complement[i]
                     )
                    )
    print('Populating genes table: ', end = '')
except pymysql.err.Error as e:
    print(f'Failed: {e}')
else:
    print('OK')

connection.commit()   
cursor.close()
