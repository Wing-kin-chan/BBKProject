'''
Code for parsing GenBank files.


'''
import re

GB_FIRST_LINE = 79
GB_ANNOT_INDENT = 12
GB_FEATR_INDENT = 21

class Record:
    '''
    Holds all information of a GenBank record
    
    Attributes:
    - accessions - Accession numbers of an entry e.g AB012229
    - residue_type - DNA, RNA, Protein or others...
    - date - The date the record was submitted
    - definition - Definition of the record
    - geneID - Gene Identifier number e.g 2523419
    - source - Species from which the sample was obtained from
    - organism - Entire taxa of source
    - references - Dictionary of dictionaries holding information on literature of the entry:
        {1: {authors:
            title:
            journal:
            pubmed:}
         2: {authours:
            title:
            journal:
            pubmed} etc...
        }
    - features - Dictionary of list of objects of class feature holding feature information:
      Features have main headers which will serve as primary dictionary keys e.g. Source, CDS etc...
      Within each main header, there will be a location type [0-9]..[0-9] or a qualifier type /XXXXXX="" The type 
      will be stored as a type variable in each feature object.
      For qualifiers, the string will be stored as a key variable within each feature object.
        {source: [(1:268, type = 'location'),
                 ('Homo sapiens, type = 'qualifier', key = 'organism'),
                 ('10', type = 'qualifier', key = 'chromosome'),
                 ('10q23', type = 'qualifier', key = 'map']), etc...
         CDS:    [('1:30', '50:94', '121:174', '203:259', type = 'location'),
                 ('bifunctional enzyme', type = 'qualifier', key = 'function'),
                 ('fructose-6-phosphate kinase', type = 'qualifier', key = 'product'),
                 ('MATRGNPILLLEYAAPLREVLCCYAL', type = 'qualifier', key = 'translation') etc...]
        }
    - sequence - A string to store the sequence provided under the ORIGIN header of GenBank files.
    '''
    
    def __init__(self):
        '''Initialise the Record class'''
        self.accessions = list()
        self.residue_type = str()
        self.date = str()
        self.definition = str()
        self.geneID = str()
        self.source = str()
        self.organism = str()
        self.references = dict()
        self.features = dict()
        self.sequence = str()