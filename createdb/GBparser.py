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
        self.accessions = None
        self.residue_type = None
        self.date = None
        self.size = None
        self.definition = None
        self.keywords = None
        self.geneID = None
        self.source = None
        self.organism = None
        self.references = dict()
        self.features = dict()
        self.sequence = None
        self.reference_no = 0
        
    def update(self, input):
        '''Reads in outputs from the annotation_feeder and stores values in appropriate fields'''
        if input == None:
            return
        
        if input[0] == 'LOCUS':
            self.size = input[1]
            self.residue_type = input[2]
            self.date = input[3]
        
        if input[0] == 'DEFENITION':
            self.definition = input[1]
            
        if input[0] == 'GENEID':
            self.geneID = input[1]
            
        if input[0] == 'ACCESSION':
            self.accessions = input[1]
            
        if input[0] == 'KEYWORDS':
            self.keywords = input[1]
            
        if input[0] == 'SOURCE':
            self.source = input[1]
            
        if input[0] == 'ORGANISM':
            self.organism = input[1]
            
        if input[0] == 'REFERENCE':
            self.reference_no += 1
            self.references['{}'.format(self.reference_no)] = input[1]
            
        if input[0] == 'FEATURE':
            self.features['{}'.format(input[1])] = {'location': input[2],
                                                    'qualifiers': input[3:]}
            
        if input[0] == 'SEQUENCE':
            self.sequence = input[1]
        
    
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
        
    def __str__(self):
        feature_str = ''
        if self.type == 'location':
            feature_str += self.type + ': ' + self.value
        elif self.type == 'qualifier':
            feature_str += self.type + ', ' + self.key + ': ' + self.value
        return feature_str
    
    '''def __repr__(self):
        feature_repr = ''
        if self.type == 'location':
            feature_str += self.type + ': ' + self.value
        elif self.type == 'qualifier':
            feature_str += self.type + ', ' + self.key + ': ' + self.value
        return feature_repr'''
        

class GenBank:
    '''Functions used to import and parse GenBank files'''
    GB_RECORD_START = 'LOCUS       '
    GB_DATE = re.compile(r'[0-9]{2}-[a-zA-Z]{3}-[0-9]{4}') 
    GB_MAX_LINE_LEN = 79
    GB_ANNOT_INDENT = 12
    GB_ANNOT_SPACE = '            '
    GB_FEATR_INDENT = 5
    GB_FEATR_SPACE = '     '
    GB_QUALIFR_SPACE = '          '
    GB_REFERENCE_HEADERS = ['  AUTHORS   ', '  TITLE     ', '  JOURNAL   ', '   PUBMED   ', '  REMARK    ']
    GB_REFERENCE_NO = re.compile(r'REFERENCE(.*?)[0-9]')
    GB_AUTHORS = re.compile(r'AUTHORS((.|\n)*?)(TITLE|JOURNAL|$)')
    GB_TITLE = re.compile(r'TITLE((.|\n)*?)(JOURNAL|PUBMED|REMARK|$)')
    GB_JOURNAL = re.compile(r'JOURNAL((.|\n)*?)(PUBMED|REMARK|$)')
    GB_PUBMED = re.compile(r'PUBMED((.|\n)*?)(REMARK|$)')
    GB_REMARK = re.compile(r'REMARK((.|\n)*?)$')
    GB_SEQ_START = 10
    GB_SEQ_END = 74
    GB_LOCATION = re.compile(r'([a-zA-Z][a-zA-Z0-9_\.\|]*[a-zA-Z0-9]?\:)?(>|<)*[0-9]+\.{2}(>|<)*[0-9]+')
    GB_QUALIFIER = re.compile(r'\B/(\w|=)*(\"|[0-9]).+?(?=(\"|/[a-z]))')
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
            if header != self.GB_ANNOT_SPACE and header not in self.GB_REFERENCE_HEADERS and not header[:self.GB_SEQ_START].strip().isdigit():
                new_annotation = True
            else:
                new_annotation = False               
            if new_annotation and annotation != '':
                yield annotation
                annotation = line
            elif new_annotation and annotation == '':
                annotation = line
            elif not new_annotation:
                if header == self.GB_ANNOT_SPACE:
                    annotation += ' ' + line[self.GB_ANNOT_INDENT:]
                if header in self.GB_REFERENCE_HEADERS:
                    annotation += line
                elif header[:self.GB_SEQ_START].strip().isdigit():
                    annotation += line[self.GB_SEQ_START:].replace(" ", "").upper()
        
    def annotation_feeder(self, line):
        '''
        Sub routine function
        Reads condensed lines from condense function, and extracts data to be passed onto the record updater.
        '''
        header = line[:self.GB_ANNOT_INDENT]
        if header == 'LOCUS       ':
            values = line[self.GB_ANNOT_INDENT:].split()
            size = values[1] + values[2]
            residue_type = values[3]
            date = values[6]
            return 'LOCUS', size, residue_type, date
                
        if header == 'DEFINITION  ':
            definition = line[self.GB_ANNOT_INDENT:]
            return 'DEFENITION', definition
        
        if header == 'VERSION     ':
            geneID = line[self.GB_ANNOT_INDENT:].split()[1][3:]
            return 'GENEID', geneID
        
        if header == 'ACCESSION   ':
            accessions = list()
            for value in line[self.GB_ANNOT_INDENT:].split():
                accessions.append(value)
            return 'ACCESSION', accessions
        
        if header == 'KEYWORDS    ':
            keywords = line[self.GB_ANNOT_INDENT:]
            return 'KEYWORDS', keywords
        
        if header == 'SOURCE      ':
            source = line[self.GB_ANNOT_INDENT:]
            return 'SOURCE', source
        
        if header == '  ORGANISM  ':
            organism = line[self.GB_ANNOT_INDENT:]
            return 'ORGANISM', organism
        
        if header == 'REFERENCE   ':
            if self.GB_AUTHORS.search(line):
                authors = self.GB_AUTHORS.search(line).group(1).strip()
            else:
                authors = None                
            
            if self.GB_TITLE.search(line):
                title = self.GB_TITLE.search(line).group(1).strip()
            else:
                title = None
            
            if self.GB_JOURNAL.search(line):
                journal = self.GB_JOURNAL.search(line).group(1).strip()
            else:
                journal = None
            
            if self.GB_PUBMED.search(line):
                pubmed = self.GB_PUBMED.search(line).group(1).strip()
            else:
                pubmed = None
                
            if self.GB_REMARK.search(line):
                remarks = self.GB_REMARK.search(line).group(1).strip()
            else:
                remarks = None
            reference = {
                'authors': authors,
                'title': title,
                'journal': journal,
                'pubmed': pubmed,
                'remarks': remarks
            }
            return 'REFERENCE', reference
        
        if header[:self.GB_ANNOT_INDENT] == 'COMMENT     ':
            pass
        
        if header[:self.GB_ANNOT_INDENT] == 'FEATURES    ':
            pass
        
        if header[:self.GB_FEATR_INDENT] == self.GB_FEATR_SPACE and not header[:self.GB_SEQ_START].strip().isdigit():
            feature_name = line.split()[0]
            
            location_str = ''
            if 'complement' in line.split()[1]:
                direction = '(-)'
            else:
                direction = ''
            for match in self.GB_LOCATION.finditer(line):
                location_str += match.group().replace('..', ':') + direction + ', '
            location = Feature('location', None, location_str)
            
            qualifiers = list()
            for match in self.GB_QUALIFIER.finditer(line):
                key = match.group().split('=')[0][1:]
                value = match.group().split('=')[1].strip('"').replace(self.GB_QUALIFR_SPACE, ' ')
                qualifier = Feature('qualifier', key, value)
                qualifiers.append(qualifier)
                
            return 'FEATURE', feature_name, location, qualifiers    
          
        if header == 'ORIGIN      ':
            sequence = line[self.GB_ANNOT_INDENT:]
            return 'SEQUENCE', sequence

def parse(handle):
    '''
    GenBank parser method
    
    Generator object for parsing multi GenBank files yield record objects for each record within the file.
    '''
    with open(handle, 'r') as f:
        file = f.read().splitlines()
        
    for record in GenBank().strip_records(file):
        output = Record()
        for line in GenBank().condense(record):
            output.update(GenBank().annotation_feeder(line))
        yield output
