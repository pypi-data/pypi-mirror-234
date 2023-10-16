# BioPy Genetic Structures
# Last updated: 8/15/23
#
# This file contains relevant genetic constants and values
#
#  included in this file:
#   - nucleotides
#   - codons
#
# https://www.stephendoescomp.bio
# Stephen Cheney © 2023

nucleotides = ['A', 'C', 'T', 'G', '-']
rnaNucleotides = ['A', 'C', 'U', 'G', '-']

codons = {'UUU':'F','UUC':'F','UUA':'L','UUG':'L','CUU':'L','CUC':'L','CUA':'L','CUG':'L','AUU':'I',
          'AUC':'I','AUA':'I','AUG':'M','GUU':'V','GUC':'V','GUA':'V','GUG':'V','UCU':'S','UCC':'S',
          'UCA':'S','UCG':'S','CCU':'P','CCC':'P','CCA':'P','CCG':'P','ACU':'T','ACC':'T','ACA':'T',
          'ACG':'T','GCU':'A','GCC':'A','GCA':'A','GCG':'A','UAU':'Y','UAC':'Y','UAA':'*','UAG':'*',
          'CAU':'H','CAC':'H','CAA':'Q','CAG':'Q','AAU':'N','AAC':'N','AAA':'K','AAG':'K','GAU':'D',
          'GAC':'D','GAA':'E','GAG':'E','UGU':'C','UGC':'C','UGA':'*','UGG':'W','CGU':'R','CGC':'R',
          'CGA':'R','CGG':'R','AGU':'S','AGC':'S','AGA':'R','AGG':'R','GGU':'G','GGC':'G','GGA':'G','GGG':'G'}

startCodon = {'AUG':'M'}
stopCodons = {'UAA':'*','UAG':'*','UGA':'*'}
innerCodons = {'UUU':'F','UUC':'F','UUA':'L','UUG':'L','CUU':'L','CUC':'L','CUA':'L','CUG':'L','AUU':'I',
          'AUC':'I','AUA':'I','GUU':'V','GUC':'V','GUA':'V','GUG':'V','UCU':'S','UCC':'S',
          'UCA':'S','UCG':'S','CCU':'P','CCC':'P','CCA':'P','CCG':'P','ACU':'T','ACC':'T','ACA':'T',
          'ACG':'T','GCU':'A','GCC':'A','GCA':'A','GCG':'A','UAU':'Y','UAC':'Y',
          'CAU':'H','CAC':'H','CAA':'Q','CAG':'Q','AAU':'N','AAC':'N','AAA':'K','AAG':'K','GAU':'D',
          'GAC':'D','GAA':'E','GAG':'E','UGU':'C','UGC':'C','UGG':'W','CGU':'R','CGC':'R',
          'CGA':'R','CGG':'R','AGU':'S','AGC':'S','AGA':'R','AGG':'R','GGU':'G','GGC':'G','GGA':'G','GGG':'G'}