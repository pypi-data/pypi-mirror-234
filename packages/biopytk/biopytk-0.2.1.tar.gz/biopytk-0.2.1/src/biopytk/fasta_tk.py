# FASTA Toolkit
#
# This module contains FASTA file analysis tools. 
#
# Classes included in this file:
#
#
# https://www.stephendoescomp.bio
# Stephen Cheney © 2023

import pandas as pd
from collections import defaultdict
from structs import *
from sequenceBuilder import *
from bio_seq import *
from aa_seq import *
from datetime import datetime

def dictFromFASTA(fasta_File):
    """
    Given a FASTA file, return a dict of sequence names and their respective sequence
    \n Notes: Does not discriminate between DNA, RNA, or Nucleotide sequences
    \n\tReturns empty {} if no properly formatted FASTA sequences
    \n<- fasta_File: FASTA formatted file 
    \n-> dict
    """
    lines = readFile(fasta_File)
    fastaDict = {}
    seqLabel = ''

    for line in lines:
        if line[0] == '>':
            seqLabel = line[1:].rstrip()
            fastaDict[seqLabel] = ''
        else:
            fastaDict[seqLabel] += line.rstrip()
    # Remove empty values
    fastaDict = {k:v for k,v in fastaDict.items() if v != ''}
    return fastaDict



def percentGC_fasta(seq):
    """
    Return GC percentage of a DNA sequence in % form
    \n<- bio_seq obj
    \n-> float
    """
    temp_seq = bio_seq(seq)
    bases = len(seq)
    return float(temp_seq.nucFrequencyDict()['G']/bases * 100) + float(temp_seq.nucFrequencyDict()['C']/bases * 100)


def gcContentFromFASTA(fasta_File):
    """
    Given a FASTA file, return a dict of sequence names and their respective GC content
    \n<- fasta_File: FASTA formatted file 
    \n-> dict
    """
    seqDict = dictFromFASTA(fasta_File)
    gcDict = {k:percentGC_fasta(v) for k,v in seqDict.items()}
    return gcDict


def getMaxGCFromFASTA(fasta_File):
    """
    Given a FASTA file, return the sequence with the largest GC content
    \n<- fasta_File: FASTA formatted file 
    \n-> dict
    """    
    gcDict = gcContentFromFASTA(fasta_File)
    maxKey = max(gcDict, key=gcDict.get)
    return {maxKey:gcDict[maxKey]}


def parseFASTA(fasta_File, labels = [], seq_type = 'AA'):
    """
    Parse a FASTA file into bio_seq or aa_seq objects
    \nNotes: labels empty by default returns all sequences, otherwise returns list of bio_seq objects that match label in labels
    \n\tseq_type specifies what sequence type the function should interpret the FASTA file as. Default to amino acid/protein sequence.
    \n<- fasta_File: FASTA formatted file, labels: str[],  
    \n-> bio_seq[] || aa_seq[]
    """
    seqDict = dictFromFASTA(fasta_File)
    if not bool(seqDict):
        return [] # Empty dict, no seqs
    
    if not bool(labels):
        if seq_type == 'AA':
            seqs = [aa_seq(v,k) for k,v in seqDict.items()]
        else:
            seqs = [bio_seq(v,seq_type,k) for k,v in seqDict.items()]
    else:
        if seq_type == 'AA':
            seqs = [aa_seq(v,k) for k,v in seqDict.items() if k in labels]
        else:
            seqs = [bio_seq(v,seq_type,k) for k,v in seqDict.items() if k in labels]
    
    return seqs
    

def dfFromFASTA(fasta_File, seq_type = 'AA',  cols = []):
    """
    Parse a FASTA file into a dataframe
    \nNotes: cols empty by default returns dataframe with all bio_seq/aa_seq attributes, otherwise only returns df with spec'd cols
    \n\tseq_type specifies what sequence type the function should interpret the FASTA file as. Default to amino acid/protein sequence.
    \n<- fasta_File: FASTA formatted file, cols: str[],  
    \n-> bio_seq[]
    """
    seqList = parseFASTA(fasta_File, [], seq_type)
    df = pd.DataFrame([d.__dict__ for d in seqList])
    if not cols: out = df
    else: out = df[cols]
    return out
    
def ancestryToFASTA(ancestry_file, outfile_name = 'output_'+ datetime.now().strftime("%Y%m%d_%H%M%S")+'.fasta', al = 0):
    """
    Parse a standard Ancestry DNA .txt file into FASTA format
    \nNotes: Will parse through file and disregard until the "rsid	chromosome	position	allele1	allele2" line of text is found.
    \n\tBy default, al = 0 will return a fasta file with allele 1 appended by allele 2 in singular file, 1 for allele 1, 2 for allele 2
    \n<- (AncestryDNA.txt): default Ancestry DNA .txt file from download , outfile_name: str, al: int
    \n-> outfile_name.fasta
    """    
    assert al == 0 or al == 1 or al == 2 
    lines = readFile(ancestry_file)
    for line in lines[:]:
        if line[0] == '#':
            lines.remove(line) # remove beginning comments
        if line[0] != '#':
            print(line)
            lines.remove(line) # remove the header line and break
            break
    allele1 = defaultdict(list)
    allele2 = defaultdict(list)
    
    count = 0
    for line in lines:
        count += 1
        stripped = line.strip()
        line_arr = stripped.split('\t')
        chromosome = line_arr[1]
        if chromosome not in allele1.keys():
            count = 0 # reset wrapping for new chr/label 
        allele1[chromosome].append(line_arr[3].replace('0', '-')) # Ancestry deletions are represented by 0
        allele2[chromosome].append(line_arr[4].replace('0', '-'))
        if count >= 60:
            allele1[chromosome].append('\n')
            allele2[chromosome].append('\n')
            count = 0

        

    allele1_out = ""
    for chr, seq in allele1.items():
        allele1_out += ">allele_1_chr_" + chr + '\n'
        allele1_out += ''.join(seq) + '\n'

    allele2_out = ""
    for chr, seq in allele2.items():
        allele2_out += ">allele_2_chr_" + chr + '\n'
        allele2_out += ''.join(seq) + '\n'
      
    
    if al == 0:
        writeFile([allele1_out, allele2_out], outfile_name)
    elif al == 1:
        writeFile(allele1_out, outfile_name)
    elif al == 2:    
        writeFile(allele2_out, outfile_name)
    
    

