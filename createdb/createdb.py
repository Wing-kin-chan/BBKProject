#!/usr/bin/env python3
'''
Code to first parse the genbank file into Python, then load onto MySQL Database.
Written by Wing
'''
#Import dependencies to read data data and parser
import Bio
from Bio import SeqIO
import re

#Define regex for parsing Exons
s = re.compile(r'(>|<)?[0-9]+:(>|<)?[0-9]+') 

#Import data
chrom_10 = SeqIO.parse('chrom_CDS_10.gb', 'genbank')
first = next(chrom_10)

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

#Parse data into variable as lists
for record in SeqIO.parse('chrom_CDS_10.gb', 'genbank'):
    #Accessions
    accessions.append(record.annotations['accessions'][0])
    
    #Dates
    dates.append(record.annotations['date'])
    
    #Loci
    if 'map' in  [feature for feature in record.features if feature.type == 'source'][0].qualifiers.keys():
        location = [feature for feature in record.features if feature.type == 'source'][0].qualifiers['map'][0]
    else:
        location = [feature for feature in record.features if feature.type == 'source'][0].qualifiers['chromosome'][0]
    loci.append(location)
    
    #GeneIDs
    geneIDs.append(record.annotations['gi'])
    
    #Protein Products
    if 'product' in [feature for feature in record.features if feature.type == 'CDS'][0].qualifiers.keys():
        proteinproduct = [feature for feature in record.features if feature.type == 'CDS'][0].qualifiers['product'][0]
    else:
        proteinproduct = ''
    protein_products.append(proteinproduct)
    
    #Description
    descriptions.append(record.description)
    
    #Sources
    sources.append(record.annotations['source'])
    
    #Genomic Sequence
    sequences.append(str(record.seq))
    
    #Codon Start
    reading_frames.append([feature for feature in record.features if feature.type == 'CDS'][0].qualifiers['codon_start'][0])
    
    #Protein sequence
    if 'translation' in [feature for feature in record.features if feature.type == 'CDS'][0].qualifiers.keys():
        translation = [feature for feature in record.features if feature.type == 'CDS'][0].qualifiers['translation'][0]
    else:
        translation = 'No Protein Product'
    translations.append(translation)
    
    #CDS Boundaries
    cds_no = 0
    coding_seqs = dict()
    coding_seq_str = str([feature for feature in record.features if feature.type == 'CDS'][0].location)
    if record.annotations['accessions'][0][:2] in coding_seq_str: #If CDS feature has splice variants, returns first match entry which is longest CDS
        cds_no += 1
        coding_seqs['CDS {}'.format(cds_no)] = s.search(coding_seq_str).group()
    else:
        for match in s.finditer(coding_seq_str):
            cds_no += 1
            coding_seqs['CDS {}'.format(cds_no)] = match.group()
    coding_regions.append(coding_seqs)

#Import dependencies
import pymysql
from pymysql import cursors

#Database connection details:
dbname = 'biodb'
dbhost = 'pandora'
port = 3306
dbuser = 'biodb_user'
dbpass = 'biodb_p'

#Connection object
connection = pymysql.connect(
    host = dbhost,
    port = port,
    user = dbuser,
    password = dbpass,
    db = dbname,
)

#Cursor Object
cursor = connection.cursor()

#Create tables
create_tbls = '''
DROP TABLE IF EXISTS coding_regions;
DROP TABLE IF EXISTS genes;

CREATE TABLE genes(
    Accession VARCHAR(12) PRIMARY KEY,
    Date DATE NOT NULL,
    Locus VARCHAR(40) NOT NULL,
    GeneID VARCHAR(8) NOT NULL,
    Protein VARCHAR(255) NOT NULL,
    Description VARCHAR(255) NOT NULL,
    Source VARCHAR(60) NOT NULL,
    Sequence LONGBLOB NOT NULL,
    Coding_Seq LONGBLOB NOT NULL,
    Frame INT(1) NOT NULL,
    Translation LONGBLOB NOT NULL 
)ENGINE = InnoDB;

CREATE TABLE coding_regions(
    Accession VARCHAR(12) PRIMARY KEY,
    Region_No INT(100) NOT NULL,
    Base_No VARCHAR(24) NOT NULL,
    FOREIGN KEY(Accession)
        REFERENCES genes(Accession)
        ON DELETE CASCADE
)Engine = InnoDB;
'''

try:
    cursor.execute(create_tbls)
    print('Successfully created tables')
    cursor.commit()
except pymysql.err.Error as e:
    print(f'Failed creating tables: {e}')
    exit(1)
    
#Load data into SQL Server
load_genetbl = '''
INSERT INTO genes(Accession, Date, Locus, GeneID, Protein, Description, Source, Sequence, Frame, Translation)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
'''

load_codingtbl = '''
INSERT INTO coding_regions VALUES(%s, %s, %s);
'''

cursor.execute(load_genetbl, (accessions, dates, loci, geneIDs, protein_products, descriptions, sources, sequences, reading_frames, translations))
cursor.commit()

i = -1 #Counter to reference accession numbers for DB Table PK
for entry in coding_regions:
    i += 1
    for k, v in entry.items():
        cursor.execute(load_codingtbl, (accessions[i], k, v)) #Loads coding regions (keys) and base ranges (values) into table with accession number for PK
        cursor.commit()

cursor.close()
connection.close()