class GenePage:
    '''
    Class for all the information on a genepage
    '''

def __init__(self):
    self.gene = str()
    self.genelongname = str()
    self.accession = str()
    self.source = str()
    self.locus = str()
    self.dna = str()
    self.protein = str()
    
import dbapi.py

def gene(self):
    self.gene = dbapi.output['gene']
    
def genelongname(self):
    self.genelongname = dbapi.output['genelongname']    