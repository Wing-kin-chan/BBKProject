'''
Code for parsing GenBank files.


'''
import re

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
        {source: [(value = '1:268', type = 'location'),
                 (value = 'Homo sapiens', type = 'qualifier', key = 'organism'),
                 (value = '10', type = 'qualifier', key = 'chromosome'),
                 (value = '10q23', type = 'qualifier', key = 'map']), etc...
         CDS:    [(value = '1:30', '50:94', '121:174', '203:259', type = 'location'),
                 (value = 'bifunctional enzyme', type = 'qualifier', key = 'function'),
                 (value = 'fructose-6-phosphate kinase', type = 'qualifier', key = 'product'),
                 (value = 'MATRGNPILLLEYAAPLREVLCCYAL', type = 'qualifier', key = 'translation') etc...]
        }
    - sequence - A string to store the sequence provided under the ORIGIN header of GenBank files.
    '''
    
    GB_MAX_LINE_LEN = 79
    GB_ANNOT_INDENT = 12
    GB_FEATR_INDENT = 21
    GB_SEQ_LINE_LEN = 75
    GB_SEQ_START = 10
    GB_SEQ_END = 74
    
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

class Feature:
    '''
    Class to hold information on GenBank features
    
    Attributes:
    - type - Location or Qualifier
    - key - A key that references the qualifier title as is in the GenBank record e.g 'translation'.
            If type is location, key is None
    - value - The value of the feature e.g 'MAHGLLIEPA...'
    '''
    GB_LOCATION = re.compile(r'(>|<)*[0-9]+\.{2}[0-9]+')
    GB_QUALIFIER = re.compile(r'\B/[a-zA-Z]+\_*[a-zA-Z]+')
    
    def __init__(self, type = str, key = str, value = str, ):
        '''Initialise the features class'''
        self.type = str()
        self.key = str()
        self.value = str()
        