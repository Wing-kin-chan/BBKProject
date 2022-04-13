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
        self.keywords = str()
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
    GB_ANNOT_SPACE = '            '
    GB_FEATR_INDENT = 5
    GB_REFERENCE_HEADERS = ['  AUTHORS   ', '  TITLE     ', '  JOURNAL   ', '   PUBMED   ', '  REMARK    ']
    GB_REFERENCE_NO = re.compile(r'REFERENCE(.*?)[0-9]')
    GB_AUTHORS = re.compile(r'AUTHORS((.|\n)*?)TITLE')
    GB_TITLE = re.compile(r'TITLE((.|\n)*?)JOURNAL')
    GB_JOURNAL = re.compile(r'JOURNAL((.|\n)*?)(PUBMED|REMARK|$)')
    GB_PUBMED = re.compile(r'PUBMED((.|\n)*?)(REMARK|$)')
    GB_REMARK = re.compile(r'REMARK((.|\n)*?)$')
    GB_SEQ_START = 10
    GB_SEQ_END = 74
    GB_LOCATION = re.compile(r'(>|<)*[0-9]+\.{2}[0-9]+')
    GB_QUALIFIER = re.compile(r'\B/(.*?)\w\"')
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
        
        >>> for record in GenBank().strip_records(input)
        ...     print(record)
        ['LOCUS XXXXX XXXXXXX 19-MAR-2008', 'ACCESSION AB0238483', 'DEFINITION', '//']
        ['LOCUS XXXXX XXXXXXX 19-MAR-2011', 'ACCESSION Y47293233', 'DEFINITION', '//']
        '''
        record = list()
        found_start = False
        i = 0
        while i <= len(file) - 1:
            if not found_start:
                for line in file[i:]:
                    if line[:self.GB_ANNOT_INDENT] == self.GB_RECORD_START:
                        found_start = True
                        record.append(line)
                        i += 1
                        break
                    else:
                        i += 1
                        continue
            if found_start:
                for line in file[i:]:
                    if line != self.GB_RECORD_END:
                        assert line[:self.GB_ANNOT_INDENT] != self.GB_RECORD_START, 'Incomplete record: line {}, missing //'.format(i-1)
                        record.append(line)
                        i += 1
                    else:
                        record.append(line)
                        yield record
                        record = list()
                        found_start = False
                        i += 1
                        break
                    
    def condense(self, record):
        '''
        Sub routine function
        Many GenBank features and annotations span multiple lines. This function iterates through a record returned by strip_records,
        checks if the header of such has changed and if not, condenses the lines into a single string for parsing to the appropriate class.
        
        >>> input = ['LOCUS       XXXXX XXXXXXX 19-MAR-2011', 
        ...     'ACCESSION   Y47293233', 
        ...     'DEFINITION  partial CDS', '            FGF-2 Receptor', '//',]
        
        >>> for line in GenBank().condense(input):
        ...     print(line)
        LOCUS       XXXXX XXXXXXX 19-MAR-2011
        ACCESSION   Y47293233
        DEFINITION  partial CDS FGF-2 Receptor
        '''
        annotation = ''
        for line in record:
            header = line[:self.GB_ANNOT_INDENT]
            if header != self.GB_ANNOT_SPACE and header not in self.GB_REFERENCE_HEADERS and not any(char.isdigit() for char in header):
                new_annotation = True
            else:
                new_annotation = False
            if new_annotation:
                yield annotation
                annotation = line
            if not new_annotation:
                if header == self.GB_ANNOT_SPACE:
                    annotation += ' ' + line[self.GB_ANNOT_INDENT:]
                if header in self.GB_REFERENCE_HEADERS:
                    annotation += line
                elif any(char.isdigit() for char in header):
                    annotation += line[self.GB_SEQ_START:].replace(" ", "").upper()
        
    def feature_extractor(self, line):
        header = line[:self.GB_ANNOT_INDENT]
        if header == 'LOCUS       ':
            values = line[self.GB_ANNOT_INDENT:].split()
            size = values[1] + values[2]
            residue_type = values[3]
            date = values[6]
            return size, residue_type, date
                
        if header == 'DEFINITION  ':
            definition = line[self.GB_ANNOT_INDENT:]
            return definition
        
        if header == 'VERSION     ':
            geneID = line[self.GB_ANNOT_INDENT:].split()[1][3:]
            return geneID
        
        if header == 'ACCESSION   ':
            accessions = list()
            for value in line[self.GB_ANNOT_INDENT:].split():
                accessions.append(value)
            return accessions
        
        if header == 'KEYWORDS    ':
            keywords = line[self.GB_ANNOT_INDENT:]
            return keywords
        
        if header == 'SOURCE      ':
            source = line[self.GB_ANNOT_INDENT:]
            return source
        
        if header == '  ORGANISM  ':
            organism = line[self.GB_ANNOT_INDENT:]
            return organism
        
        if header == 'REFERENCE   ':
            if self.GB_PUBMED.search(line):
                pubmed = self.GB_PUBMED.search(line).group(1).strip()
            else:
                pubmed = None
                
            if self.GB_REMARK.search(line):
                remarks = self.GB_REMARK.search(line).group(1).strip()
            else:
                remarks = None
            reference = {
                'authors': self.GB_AUTHORS.search(line).group(1).strip(),
                'title': self.GB_TITLE.search(line).group(1).strip(),
                'journal': self.GB_JOURNAL.search(line).group(1).strip(),
                'pubmed': pubmed,
                'remarks': remarks
            }
            return reference
        
        if header == 'ORIGIN      ':
            sequence = line[self.GB_ANNOT_INDENT:]
            return sequence

    def parse(self, handle):
        with open(handle, 'r') as f:
            self.file = f.read().splitlines()
            
        for record in self.strip_records(self.file):
            output = Record()
            for line in self.condense(record):
                output.update(line)
            return output

a = ['ACCESSION AB0238483', 'DEFINITION', '//',
    'LOCUS XXXXX XXXXXXX 19-MAR-2008', 'ACCESSION AB0238483', 'DEFINITION', '//',
     'LOCUS XXXXX XXXXXXX 19-MAR-2011', 'ACCESSION Y47293233', 'DEFINITION    partial CDS', 'FGF-2 Receptor', '//',
     'ACCESSION AB0238483', 'DEFINITION', '//',
     'LOCUS XXXXX XXXXXXX 21-JUL-2008', 'ACCESSION E98342334', 'DEFINITION', '//',
     'LOCUS XXXXX XXXXXXX 22-OCT-1997', 'ACCESSION AL2352545', 'DEFINITION', '//']

with open('test.gb', 'r') as f:
    testgb = f.read().splitlines()

b = list()
for record in GenBank().strip_records(testgb):
    for line in GenBank().condense(record):
        GenBank().feature_extractor(line)


line = 'LOCUS       AB009903                 268 bp    DNA     linear   PRI 14-APR-2000'

