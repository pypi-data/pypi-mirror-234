# Bio Seq Toolkit
#
# This module contains DNA/RNA sequencing tools. 
#
# Classes included in this file:
#   - bio_seq
#   - AlignScore
#
# https://www.stephendoescomp.bio
# Stephen Cheney © 2023

import collections
from structs import *
from sequenceBuilder import *
from aa_seq import aa_seq
from aa_seq import *

class bio_seq():
    def __init__(self, seq = "ACTG", seq_type = 'DNA', label = 'No Label'):
        self.seq = seq.upper()
        self.seq_type = seq_type
        self.label = label
        self.is_valid = self.validateSeq()
        self.length = len(seq)
        assert self.is_valid, f"Input {seq_type} sequence is invalid: {self.seq}"


    def __str__(self):
        return f'{self.label}:\n{self.seq}'
    

    def validateSeq(self):
        """
        Return True if input sequence is a valid DNA sequence, return False otherwise
        \n<- bio_seq obj
        \n-> bool
        """
        if self.seq_type == 'DNA':
            return set(nucleotides).issuperset(self.seq)
        if self.seq_type == 'RNA':
            return set(rnaNucleotides).issuperset(self.seq)
        else:
            return False


    def printSeq(self, direc):
        """
        Return an annotated DNA sequence in given direction
        \nNotes: direc - 'f' for (5' -> 3'), 'r' for (3' -> 5')
        \n<- bio_seq obj, direc: chr
        \n-> str
        """
        if direc == 'f':
            return '5\' ' + self.seq + ' 3\''
        if direc == 'r':
            return '3\' ' + self.seq + ' 5\''
        

    def nucFrequencyDict(self):
        """
        Return a frequency dict of nucleotide bases in a given sequence
        \n<- bio_seq obj
        \n-> dict
        """
        dna_dict = dict(collections.Counter(self.seq))
        dna_dict.setdefault('A', 0)
        dna_dict.setdefault('T', 0)
        dna_dict.setdefault('G', 0)
        dna_dict.setdefault('C', 0)
        return dna_dict

    def percentGC(self):
        """
        Return GC percentage of a DNA sequence in % form
        \n<- bio_seq obj
        \n-> float
        """
        bases = len(self.seq)
        return float(self.nucFrequencyDict()['G']/bases * 100) + float(self.nucFrequencyDict()['C']/bases * 100)


    def transcribe(self):
        """
        Return the RNA transcription of a given DNA sequence
        \n<- bio_seq obj
        \n-> bio_seq obj RNA
        """
        assert self.seq_type == 'DNA', f"Input seq type is {self.seq_type}, not DNA"
        temp_seq = self.seq
        out_seq = temp_seq.replace('T', 'U')
        return bio_seq(out_seq, 'RNA')


    def dnaCompliment(self):
        """
        Return the matched sequence of a given DNA sequence
        \n<- bio_seq obj
        \n-> bio_seq obj DNA
        """
        assert self.seq_type == 'DNA', f"Input seq type is {self.seq_type}, not DNA"
        translationTable = str.maketrans('ATCG', 'TAGC')
        temp_seq = self.seq
        out_seq = temp_seq.translate(translationTable)
        return bio_seq(out_seq, 'DNA')


    def rnaCompliment(self):
        """
        Return the matched sequence of a given RNA sequence
        \n<- bio_seq obj
        \n-> bio_seq obj RNA
        """
        assert self.seq_type == 'RNA', f"Input seq type is {self.seq_type}, not RNA"
        translationTable = str.maketrans('AUCG', 'UAGC')
        temp_seq = self.seq
        out_seq = temp_seq.translate(translationTable)
        return bio_seq(out_seq, 'RNA')


    def dna_reverseCompliment(self):
        """
        Return the reverse compliment of a given DNA sequence
        \nNotes: Returns 5' -> 3'
        \n<- bio_seq obj
        \n-> bio_seq obj DNA
        """
        assert self.seq_type == 'DNA', f"Input seq type is {self.seq_type}, not DNA"
        temp_seq = bio_seq(self.seq[::-1], 'DNA')
        return temp_seq.dnaCompliment()


    def rna_reverseCompliment(self):
        """
        Return the reverse compliment of a given RNA sequence
        \nNotes: Returns 5' -> 3'
        \n<- bio_seq obj
        \n-> bio_seq obj RNA
        """
        assert self.seq_type == 'RNA', f"Input seq type is {self.seq_type}, not RNA"
        temp_seq = bio_seq(self.seq[::-1], 'RNA')
        return temp_seq.rnaCompliment()


    def getBasePairs(self):
        """
        Return a string of the complimentary base pairs of a given DNA sequence
        \n<- bio_seq obj
        \n-> str
        """
        return self.printSeq('f') + '\n   ' + '|'*len(self.seq) + '\n' + self.dnaCompliment().printSeq('r')


    def hammingDist(self, seq2):
        """
        Returns Hamming Distance of 2 given sequences
        \n<- bio_seq obj,\n\tseq2: bio_seq obj
        \n-> int
        """
        seq1Len = len(self.seq)
        seq2Len = len(seq2.seq)
        
        tempseq1 = self.seq
        tempseq2 = seq2.seq

        if seq1Len < seq2Len:
            tempseq1 = self.seq + ('X' * (seq2Len - seq1Len))
        if seq2Len < seq1Len:
            tempseq2 = seq2.seq + ('X' * (seq1Len - seq2Len))
        
        h_dist = 0
        for i in range(len(tempseq1)):
            if tempseq1[i] != tempseq2[i]:
                h_dist += 1
        return h_dist


    def seqCompare(self, seq2):    
        """
        Returns a visual comparison of 2 input sequences
        \n<- seq1: bio_seq obj,\n\tseq2: bio_seq obj
        \n-> str
        """
        seqLen = min(len(self.seq), len(seq2.seq))
        compStr = ''
        for i in range(seqLen):
            if self.seq[i] == seq2.seq[i]:
                compStr += '|'
            elif self.seq[i] == '-' or seq2.seq[i] == '-':
                compStr += ' '
            else:
                compStr += '.'
                
        return self.seq + '\n' + compStr + '\n' + seq2.seq


    def translate(self, init_pos = 0):
        """
        Return the list of codons of a given RNA sequence and starting position in sequence
        \n<- bio_seq obj, init_pos: int
        \n-> chr[]
        """
        return aa_seq(''.join([codons[self.seq[pos:pos + 3]] for pos in range(init_pos, len(self.seq) - 2, 3)]))


    def seqSummary(self):
        """
        Return summary details of a given DNA sequence.
        \n Notes: seq_name [Optional] is a given name of a sequence for ease of use
        \n Format:
        \n\t Nucleotide Frequency
        \n\t GC Content
        \n\t Forward Strand
        \n\t Compliment
        \n\t Reverse Compliment
        \n\t RNA Transcription
        \n<- bio_seq obj
        \n-> None
        """
        summary = ''
        summary += f'==== Sequence: {self.label} ====\n'
        summary += f'Nucleotide Freq: {self.nucFrequencyDict()}\n'
        summary += f'GC Content: {self.percentGC()}\n'
        summary += f'Base Pairs: \n{self.getBasePairs()}\n'
        summary += f'Reverse Compliment:\n'
        summary += self.dna_reverseCompliment().printSeq('f')
        summary += f'\nTranscribed:\n{self.transcribe().printSeq("f")}'

        return summary
    

    def get_reading_frames(self, start_pos = 0, end_pos = None):
        """
        Given an RNA seq, return a list of translated codon reading frames
        \n<- bio_seq obj RNA
        \n-> [aa_seq obj]
        """
        assert self.seq_type == 'RNA', f"Input seq type is {self.seq_type}, not RNA"
        if end_pos == None:
            end_pos = self.length
        frames = []
        temp_seq = bio_seq(self.seq[start_pos:end_pos], 'RNA', self.label+ f': Pos {start_pos} : {end_pos}')
        for i in range(0,3):
            frames.append(temp_seq.translate(i))
        for i in range(0,3):
            frames.append(temp_seq.rna_reverseCompliment().translate(i))
        return frames


    def getAllORFProteins(self, start_pos = 0, end_pos = None, ordered = False):
        """
        Given an RNA sequence, starting position, and ending position, return all possible polypeptides within the ORFs
        \nNotes: ordered == True: sort AAs by length, descending, else do not sort
        \n<- bio_seq obj start_pos: int, end_pos: int, ordered: bool
        \n-> str[]
        """
        assert self.seq_type == 'RNA', f"Input seq type is {self.seq_type}, not RNA"
        if end_pos == None:
            end_pos = self.length

        if end_pos > start_pos:
            frames = self.get_reading_frames(start_pos, end_pos)
        else:
            frames = self.get_reading_frames(start_pos, end_pos)
        
        output = []
        for frame in frames:
            proteins = frame.getProteinsFromRF()
            for protein in proteins:
                output.append(protein)
        
        if ordered:
            return sorted(output, key = len, reverse = True)
        return output


    def globalAlign(self, compSeq, match=1, mismatch=0, gap=0, extend=0):
        """
        Perform a global alignment on self and given sequence (Needleman–Wunsch)
        \n<- bio_seq obj compSeq: bio_seq obj, gap: int, match: int, mismatch: int
        \n-> (str, str)
        """

        @staticmethod
        def __getScoreMatrix(seq1, seq2, gap):
            '''
            Initialize scoring matrix
            --------------------------
            seq1 & seq2 should be strings representations of the sequences without labels
            '''
            matrix = []
            for i in range(len(seq1)+1):
                subMatrix = []
                for j in range(len(seq2)+1):
                    subMatrix.append(0)
                matrix.append(subMatrix)
            
            for i in range(1, len(seq1)+1):
                matrix[i][0] = i * gap   
            for j in range(1, len(seq2)+1):
                matrix[0][j] = j * gap
            return matrix

        @staticmethod
        def __getTracebackMatrix(seq1, seq2):
            '''
            Initialize traceback matrix
            --------------------------
            seq1 & seq2 should be strings representations of the sequences without labels
            '''
            matrix = []
            for i in range(len(seq1)+1):
                subMatrix = []
                for j in range(len(seq2)+1):
                    subMatrix.append('0')
                matrix.append(subMatrix)
            
            for i in range(1, len(seq1)+1):
                matrix[i][0] = 'up'   
            for j in range(1, len(seq2)+1):
                matrix[0][j] = 'left'
            matrix[0][0] = 'done'
            return matrix
        
        class AlignScore:
            def __init__(self,match, mismatch, gap, extend):
                self.gap = gap
                self.match = match
                self.mismatch = mismatch
                self.extend = extend
            def misMatchChr(self, a, b):
                if a != b:
                    return self.mismatch
                return self.match
        
        @staticmethod
        def getAlignmentMatricies(seq1, seq2, score):
            '''
            Propagate alignment matricies
            --------------------------
            - seq1 & seq2 should be strings representations of the sequences without labels
            - score is an AlignScore object
            '''
            scoreMatrix = __getScoreMatrix(seq1, seq2, score.gap)
            traceBackMatrix = __getTracebackMatrix(seq1, seq2)
            
            for i in range(1, len(seq1)+1):
                for j in range(1, len(seq2)+1):
                    # calculate the surrounding scores for the current point
                    left = scoreMatrix[i][j-1] + score.gap
                    up = scoreMatrix[i-1][j] + score.gap
                    diag = scoreMatrix[i-1][j-1] + score.misMatchChr(seq1[i-1], seq2[j-1])
                    scoreMatrix[i][j] = max(left, up, diag)
                    if scoreMatrix[i][j] == left:
                        traceBackMatrix[i][j] = 'left'
                    elif scoreMatrix[i][j] == up:
                        traceBackMatrix[i][j] = 'up'
                    else:
                        traceBackMatrix[i][j] = 'diag'
                    
            return scoreMatrix, traceBackMatrix
              
        aSeq = self.seq
        bSeq = compSeq.seq
        i = self.length
        j = compSeq.length
        xSeq = []
        ySeq = []
        finalScore = 0
        temp = getAlignmentMatricies(aSeq, bSeq, AlignScore(match, mismatch, gap, extend))
        scoreMatrix = temp[0]
        traceBackMatrix = temp[1]
        gapOpen = False
        while(i > 0 or j > 0):            
            if traceBackMatrix[i][j] == 'diag':
                xSeq.append(aSeq[i-1])
                ySeq.append(bSeq[j-1])
                if aSeq[i-1] == bSeq[j-1]:
                    # Match
                    finalScore += match
                else: 
                    # Mismatch
                    finalScore += mismatch
                i -= 1
                j -= 1
                gapOpen = False
            elif traceBackMatrix[i][j] == 'left':
                # Gap
                xSeq.append('-')
                ySeq.append(bSeq[j-1])
                j -= 1
                if not gapOpen:
                    finalScore += gap
                    gapOpen = True
                else:
                    finalScore += extend
            elif traceBackMatrix[i][j] == 'up':
                # Gap
                xSeq.append(aSeq[i-1])
                ySeq.append('-')
                i -= 1
                if not gapOpen:
                    finalScore += gap
                    gapOpen = True
                else:
                    finalScore += extend
            if traceBackMatrix[i][j] == 'done':
                break
        aSeq = ''.join(xSeq[::-1])
        bSeq = ''.join(ySeq[::-1])

        return bio_seq(aSeq, self.seq_type, self.label), bio_seq(bSeq, compSeq.seq_type, compSeq.label), finalScore
          
    

# ====== Function Comment Template ======

    """
    Purpose of Function
    \nNotes: [notes]
    \n\t[more notes]    
    \n<- input: type
    \n-> type
    """