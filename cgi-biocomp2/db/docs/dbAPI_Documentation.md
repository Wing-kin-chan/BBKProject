============================================ DATABASE API DOCUMENTATION =================================================
- Author: Wing-kin Chan

The database API provides functions to interact with, and query the database such that these actions are abstracted from 
other code layers. The database API functions are the following:

    - search(querytype, query, resultlen):  This is a parameterized search function that reads in the query-type (Accession,
                                            GeneID, Protein, Locus), the query submitted on the webpage by the user, and also
                                            the number of results the user would like to see. This function is called by other
                                            database query functions.
  
    - getAllEntries():                      This function returns all entries stored in the database and is used to return data
                                            for the listall.cgi webpage.

    - getAccession(query):                  This function returns all information on a single record.
    
    - getByAccession(query, resultlen):     This function returns a list of summaries of all entries whose accession number is
                                            like the query. If the search returns one result, calls getAccession.
                                        
    - getByGeneID(query, resultlen):        This function returns a list of summaries of all entries whose GeneID is like the   
                                            query. If the search returns one result, calls getAccession.

    - getByProduct(query, resultlen):       This function returns a list of summaries of all entries whose protein name is like 
                                            the query. If the search returns one result, calls getAccession.

    - getByLocus(query, resultlen):         This function returns a list of summaries of all entries whose locus is like the 
                                            query. If the search returns one result, calls getAccession. 

    - updateCodingSeq(Accession, CodingSeq):This function updates the genomic coding sequence string with introns removed of the  
                                            entry, with a value calculated by the business layer API.     
    
    - updateComplement(Accession, Complement):This function updates the complementary/antisense string of the sequence of the 
                                            entry, with a value calculated by the business layer API.
                          
    - getAllCodingRegions():                This function returns all codings regions stored in the database accompanied by record
                                            identifying summaries such as Accession, GeneID, Protein, and Locus.

To connect to the database, the PyMySQL library is used with a connection object that references information in cgi-biocomp2/config.py.
