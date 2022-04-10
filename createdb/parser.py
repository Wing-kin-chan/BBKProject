'''
Code for parsing GenBank files.


'''
import re
import doctest

class Record:
    '''
    Holds all information of a GenBank record
    
    Attributes:
    - accessions - Accession numbers of an entry e.g AB012229
    - residue_type - DNA, RNA, Protein or others...
    - date - The date the record was submitted
    - size - Length of the sequence in Origin header
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
         CDS:    [(value = ['1:30', '50:94', '121:174', '203:259'], type = 'location'),
                 (value = 'bifunctional enzyme', type = 'qualifier', key = 'function'),
                 (value = 'fructose-6-phosphate kinase', type = 'qualifier', key = 'product'),
                 (value = 'MATRGNPILLLEYAAPLREVLCCYAL', type = 'qualifier', key = 'translation') etc...]
        }
    - sequence - A string to store the sequence provided under the ORIGIN header of GenBank files.
    '''
    
    def __init__(self):
        '''Initialise the Record class'''
        self.accessions = list()
        self.residue_type = str()
        self.date = str()
        self.size = str()
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
    
    def __init__(self, type = None, key = None, value = None, ):
        '''Initialise the features class'''
        self.type = type
        self.key = key
        self.value = value

class GenBank:
    '''Functions used to import and parse GenBank files'''
    GB_RECORD_START = 'LOCUS       '
    GB_DATE = re.compile(r'[0-9]{2}-[a-zA-Z]{3}-[0-9]{4}') 
    GB_MAX_LINE_LEN = 79
    GB_ANNOT_INDENT = 12
    GB_FEATR_INDENT = 21
    GB_SEQ_LINE_LEN = 75
    GB_SEQ_START = 10
    GB_SEQ_END = 74
    GB_LOCATION = re.compile(r'(>|<)*[0-9]+\.{2}[0-9]+')
    GB_QUALIFIER = re.compile(r'\B/[a-zA-Z]+\_*[a-zA-Z]+')
    GB_RECORD_END = '//'
    
    def __init__(self):
        pass
    
    def strip_records(self, file: list):
        '''
        Sub-routine generator function
        Splits multi GenBank file into individual records given records always begins with LOCUS and ends with //
        Not to be used on its own
        
        >>> input = ['ACCESSION AB0238483', 'DEFINITION', '//',
        ...     'LOCUS XXXXX XXXXXXX 19-MAR-2008', 'ACCESSION AB0238483', 'DEFINITION', '//',
        ...     'LOCUS XXXXX XXXXXXX 19-MAR-2011', 'ACCESSION Y47293233', 'DEFINITION', '//']
        
        >>> for record in strip_records(input)
        ...     print(record)
        ['LOCUS XXXXX XXXXXXX 19-MAR-2008', 'ACCESSION AB0238483', 'DEFINITION']
        ['LOCUS XXXXX XXXXXXX 19-MAR-2011', 'ACCESSION Y47293233', 'DEFINITION']
        '''
        record = list()
        found_start = False
        i = 0
        while not found_start:
            for line in file:
                if line[:self.GB_ANNOT_INDENT] == self.GB_RECORD_START:
                    found_start = True
                    record.append(line)
                    i += 1
                    break
                else:
                    i += 1
                    continue
        while found_start:
            for line in file[i:]:
                if line != self.GB_RECORD_END:
                    record.append(line)
                    i += 1
                else:
                    yield record
                    record = list()
                    found_start = False
                    i += 1
                    
    def format_record(self, record: list):
        '''
        Sub routine function
        Takes single record list returned by strip_records and formats it into Record class type object
        Not to be used on its own
        '''