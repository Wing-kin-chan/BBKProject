#!/usr/bin/env python3
#Import dependencies
from numpy import where
import pymysql
from pymysql import cursors

#Database connection details:
dbhost = 'pandora'
dbname = 'biodb'
port = 3306
dbuser = 'cw001'
dbpass = 'trp38ile'

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
createGeneTable = (
    "DROP TABLE IF EXISTS genes;"
    "CREATE TABLE genes ("
    "Accession VARCHAR(12) PRIMARY KEY,"
    "Date DATE NOT NULL"
    "Locus VARCHAR(6) NOT NULL,"
    "GeneID VARCHAR(6) NOT NULL,"
    "ProteinProduct VARCHAR(6) NOT NULL"
    "Definition VARCHAR(255) NOT NULL,"
    "Source VARCHAR(60) NOT NULL,"
    "Origin LONGBLOB NOT NULL,"
    "Translation LONGBLOB NOT NULL,"
    "CDS BLOB NOT NULL,"
    ")ENGINE = INNODB;"
)

try:
    cursor.execute(createGeneTable)
    print(f'Created Empty Gene Table')
    cursor.close()
except pymysql.err.Error as e:
    print(f'Failed creating Gene Table: {e}')
    cursor.close()
    exit(1)
 
#Import dependencies to read data data and parser
import Bio
from Bio import SeqIO

chrom_10 = SeqIO.parse('chrom_CDS_10.gb', 'genbank')
first = next(chrom_10)

Accessions = list()
Dates = list()
Loci = list()
GeneIDs = list()
ProteinProducts = list()
Description = list()
Sources = list()
Origins = list()
Translations = list()
CDSs = list()

#Parse data into variable as lists
for record in SeqIO.parse('chrom_CDS_10.gb', 'genbank'):
    Accessions.append(record.annotations['accessions'])
    Dates.append(record.annotations['date'])
    Loci.append([feature for feature in record.features if feature.type == 'source'][0].qualifiers['map'])
    GeneIDs.append(record.annotations['gi'])
    ProteinProducts.append([feature for feature in record.features if feature.type == 'CDS'][0].qualifiers['product'])
    Description.append(record.description)
    Sources.append(record.annotations['source'])
    Origins.append(record.seq)
    Translations.append(record.seq.translate())
    CDSs.append([feature for feature in record.features if feature.type == 'exon'])
    
[f for f in first.features if f.type == 'CDS']