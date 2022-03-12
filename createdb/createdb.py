#!/usr/bin/env python3
#Import dependencies
import pymysql
from pymysql import cursors
import mysql

#Database connection details:
dbhost = 'pandora'
dbname = 'biodb'
port = 3306
user = 'cw001'
password = 'trp38ile'

#Connect function
def connectdb():
    '''
    Connects to the MySQL database
    '''

    conn = pymysql.connect(
        host = dbhost,
        port = port,
        user = user,
        password = password,
        db = dbname,
    )

#Define tables
tables = {}
tables['genes'] = (
    "CREATE TABLE 'genes ("
    "'Locus' VARCHAR(12) NOT NULL,"
    "'Definition' VARCHAR(255) NOT NULL,"
    "'Accession' VARCHAR(12) NOT NULL,"
    "'Keywords' VARCHAR(255) NOT NULL,"
    "'Source' VARCHAR(60) NOT NULL,"
    "'Organism' TEXT NOT NULL,"
    "'Origin' LONGBLOB NOT NULL,"
    "'CDS' LONGBLOB NOT NULL,"
    "PRIMARY KEY ('Accession')"
)

cnx = mysql.connector.connect(user = user)
cursor = cnx.cursor()

#Create database function
def createdb(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(dbname))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

#Initialize database
try:
    cursor.execute("USE {}".format(dbname))
except mysql.connector.Error as err:
    print("Database {} does not exist.".format(dbname))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        createdb(cursor)
        print("Database {} created successfully.".format(dbname))
        cnx.database = dbname
    else:
        print(err)
        exit(1)

#Create table
for table in tables:
    table_description = tables[table]
    try:
        print("Creating table {}:".format(table), end = '')
        cursor.execute(table_description)
    except mysql.connect.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("Table already exists, dropping table.")
            cursor.execute("DROP TABLE IF EXISTS {}".format(table), end = '')
        else:
            print(err.msg)
    else:
        print("Successful")
cursor.close()
cnx.close()

#Parse the GenBank file
from Bio import SeqIO
fname = 'chrom_CDS_10.gb'

