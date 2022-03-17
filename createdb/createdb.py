#!/usr/bin/env python3
#Import dependencies
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
    "Exons BLOB NOT NULL,"
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
Exons = list()

#Parse data into variable as lists
for record in SeqIO.parse('chrom_CDS_10.gb', 'genbank'):
    #Accessions
    Accessions.append(record.annotations['accessions'])
    
    #Dates
    Dates.append(record.annotations['date'])
    
    #Loci
    if 'map' in  [feature for feature in record.features if feature.type == 'source'][0].qualifiers.keys():
        location = [feature for feature in record.features if feature.type == 'source'][0].qualifiers['map'][0]
    else:
        location = [feature for feature in record.features if feature.type == 'source'][0].qualifiers['chromosome'][0]
    Loci.append(location)
    
    #GeneIDs
    GeneIDs.append(record.annotations['gi'])
    
    #Protein Products
    if 'product' in [feature for feature in record.features if feature.type == 'CDS'][0].qualifiers.keys():
        proteinproduct = [feature for feature in record.features if feature.type == 'CDS'][0].qualifiers['product'][0]
    else:
        proteinproduct = ''
    ProteinProducts.append(proteinproduct)
    
    #Description
    Description.append(record.description)
    
    #Sources
    Sources.append(record.annotations['source'])
    
    #Genomic Sequence
    Origins.append(str(record.seq))
    
    #Protein sequence
    if 'translation' in [feature for feature in record.features if feature.type == 'CDS'][0].qualifiers.keys():
        translation = [feature for feature in record.features if feature.type == 'CDS'][0].qualifiers['translation'][0]
    else:
        translation = 'No Protein Product'
    Translations.append(translation)
    
    #Intron/Exon Boundaries
    Exons.append(str([feature for feature in record.features if feature.type == 'CDS'][0].location))
    
#Load data into SQL Server

