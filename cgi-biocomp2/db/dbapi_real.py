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
    cursor = connection.cursor()
    sql_selectall = 'SELECT * '
    sql_selectsummary = 'SELECT Accession, GeneID, Product, Locus '
    sql_location = 'FROM genes g '
    sql_join = 'JOIN coding_regions c ON(g.Accession = c.Accession) '
    sql_where = '''WHERE g.{} LIKE '%{}%' '''.format(querytype, query)
    sql_limit = 'LIMIT {};'.format(resultlen)
    
    #List all entry summaries in database
    if querytype == 'getAll' and query == 'getAll':
        sql = sql_selectsummary + sql_location + ';'
        results = list()
        
        cursor.execute(sql)
        for row in cursor.fetchall():
            results_row = dict()
            results_row['Accession'] = row[0]
            results_row['GeneID'] = row[1]
            results_row['Product'] = row[2]
            results_row['Locus'] = row[3]
            results.append(results_row)
    
    #Return list of entry summaries for search results
    if querytype in ['Accession', 'GeneID', 'Product', 'Locus'] and resultlen > 1:
        sql = sql_selectsummary + sql_location + sql_where + sql_limit
        results = list()
        
        cursor.execute(sql)
        for row in cursor.fetchall():
            results_row = dict()
            results_row['Accession'] = row[0]
            results_row['GeneID'] = row[1]
            results_row['Product'] = row[2]
            results_row['Locus'] = row[3]
            results.append(results_row)
    
    #Return all information on specific entry for gene page
    if querytype in ['Accession', 'GeneID', 'Product', 'Locus'] and resultlen == 1:
        sql = sql_selectall + sql_location + sql_join + sql_where + ';'
        results = dict()
        results['Coding Regions'] = dict()
        
        cursor.execute(sql)
        for row in cursor.fetchall():
            results['Accession'] = row[0]
            results['Locus'] = row[2]
            results['GeneID'] = row[3]
            results['Product'] = row[4]
            results['Description'] = row[5]
            results['Source'] = row[6]
            results['Sequence'] = row[7]
            results['Frame'] = row[8]
            results['Translation'] = row[9]
            results['Coding Regions'][row[11]] = row[12]
    
    cursor.close()
    
    return results

def getAllEntries():
    '''
    Returns a list of dictionaries to display on the search page
    keys(): 'Accession', 'GeneID', 'Product', 'Locus'
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
            return getAccession(results[0]['Accession'])
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
            return getAccession(results[0]['Accession'])
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
            return getAccession(results[0]['Accession'])
        else:
            return results
    except pymysql.err.Error as e:
        return 'Database error {}'.format(e)

def getByProduct(query: str, resultslen: int):
    '''
    Function that will return list of summary information on entries whose proteins descriptions are similar to the query.
    If query returns unique entry, calls getAccession(result's accession) to return details for gene page.
    '''
    try:
        results = search('Product', query, resultslen)
        if len(results) == 0:
            return 'No results found'
        if len(results) == 1:
            return getAccession(results[0]['Accession'])
        else:
            return results
    except pymysql.err.Error as e:
        return 'Database error {}'.format(e)
