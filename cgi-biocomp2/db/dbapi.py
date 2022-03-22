#!/usr/bin/python3
'''
Database API for querying and returning data
Written by Wing
'''

# Add the directory above to the module path to import the config file
import sys
sys.path.insert(0, "../")

import config  # Import configuration information (e.g. database connection)

#Import dependencies
import pymysql
from pymysql import cursors

connection = pymysql.connect(
    host = config.dbhost,
    port = config.port,
    user = config.dbuser,
    password = config.dbpass,
    db = config.dbname,
)

cursor = connection.cursor()

#To save writing repeated SQL queries of similar structure, definied a single function with arguments to query the database.
#Each search function will parse their unique arguments to this function      
def search(querytype: str, query: str, resultlen: int):
    optional_sql = ', Date, Description, Source, Sequence, Coding_seq, Frame, Translation, Region_No, Range'
    sql = [
        'SELECT Accession, GeneID, Protein, Locus',
        'FROM genes g',
        'JOIN coding_regions c ON(g.Accession = c.Accession)',
        'WHERE {} LIKE %{}%'.format(querytype, query),
        'LIMIT {}'.format(resultlen)
    ]
    #List all entries in database
    if querytype == 'getAll' and query == 'getAll':
        results = list()
        
        cursor.execute(sql[0:1])
        for row in cursor.fetchall():
            results_row = dict()
            results_row['Accession'] = row[0]
            results_row['GeneID'] = row[1]
            results_row['Protein'] = row[2]
            results_row['Locus'] = row[3]
            results.append(results_row)
    
    #Return list of entry summaries for search results
    if querytype in ['Accession', 'GeneID', 'Protein', 'Locus'] and resultlen > 1:
        results = list()
        
        cursor.execute(sql)
        for row in cursor.fetchall():
            results_row = dict()
            results_row['Accession'] = row[0]
            results_row['GeneID'] = row[1]
            results_row['Protein'] = row[2]
            results_row['Locus'] = row[3]
            results.append(results_row)
    
    #Return all information on specific entry for gene page
    if querytype in ['Accession', 'GeneID', 'Protein', 'Locus'] and resultlen == 1:
        results = dict()
        results['Coding Regions'] = dict()
        sql[0] += optional_sql[1]
        
        cursor.execute(sql)
        for row in cursor.fetchall():
            results['Accession'] = str(set(row[0]))
            results['GeneID'] = str(set(row[1]))
            results['Protein'] = str(set(row[2]))
            results['Locus'] = str(set(row[3]))
            results['Date'] = str(set(row[4]))
            results['Description'] = str(set(row[5]))
            results['Source'] = str(set(row[6]))
            results['Sequence'] = str(set(row[7]))
            results['Coding_seq'] = str(set(row[8]))
            results['Frame'] = int(set(row[9]))
            results['Translation'] = str(set(row[10]))
            results['Coding Regions']['{}'.format(str(row[11]))] = str(row[12])
    
    cursor.close()
    connection.close()
    
    return results

def getAllEntries():
    '''
    Returns a list of dictionaries to display on the search page
    keys(): 'Accession', 'GeneID', 'Protein', 'Locus'
    '''
    try:
        return search('getAll', 'getAll', 0)
    except pymysql.err.Error as e:
        return 'Database error {}'.format(e)
    
def getAccession(query: str):
    '''
    Function that will return the single database entry for the GenBank accession that matches the query.
    For example getAccession(AB01234) will return all information on the GenBank accession AB01234. This
    will be the function called when accessing a single entry.
    '''
    
    try:
        return search('Accession', query, 1)
    except pymysql.err.Error as e:
        return 'Database error {}'.format(e)
    
def getByAccession(query: str, resultslen: int):
    '''
    Returns all genes that contain the query as a substring in their accession number.
    For example, getAccessions(AB012) will return all genes whose accession starts with with AB012.
    If query returns unique entry, calls getAccession(result's accession) to return details for gene page.
    '''
    try:
        results = search('Accession', query, resultslen)
        if len(results) == 0:
            return 'No results found'
        if len(results) == 1:
            return getAccession(results['Accession'])
        else:
            return results
    except pymysql.err.Error as e:
        return 'Database error {}'.format(e)

def getByGeneID(query: str, resultslen: int):
    '''
    Function that will return list of summary information on entries whose geneIDs are similar to query.
    For example getGeneID(342345) will return summary information on entries with GeneID 342345 or similar.
    If query returns unique entry, calls getAccession(result's accession) to return details for gene page.
    '''
    try:
        results = search('GeneID', query, resultslen)
        if len(results) == 0:
            return 'No results found'
        if len(results) == 1:
            return getAccession(results['Accession'])
        else:
            return results
    except pymysql.error.Error as e:
        return 'Database error {}'.format(e)

def getByLocus(query: str, resultslen: int):
    '''
    Function that will return list of summary information on entries that are within the specified locus.
    If query returns unique entry, calls getAccession(result's accession) to return details for gene page.
    '''
    try:
        results = search('Locus', query, resultslen)
        if len(results) == 0:
            return 'No results found'
        if len(results) == 1:
            return getAccession(results['Accession'])
        else:
            return results
    except pymysql.err.Error as e:
        return 'Database error {}'.format(e)

def getByProtein(query: str, resultslen: int):
    '''
    Function that will return list of summary information on entries whose proteins descriptions are similar to the query.
    If query returns unique entry, calls getAccession(result's accession) to return details for gene page.
    '''
    try:
        results = search('Protein', query, resultslen)
        if len(results) == 0:
            return 'No results found'
        if len(results) == 1:
            return getAccession(results['Accession'])
        else:
            return results
    except: pymysql.err.Error as e:
        return 'Database error {}'.format(e)