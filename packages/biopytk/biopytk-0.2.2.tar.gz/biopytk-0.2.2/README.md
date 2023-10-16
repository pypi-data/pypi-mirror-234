
# BioPyTK

Personal Toolkit for Bioinformatics and Computational Biology pipelines.
Latest release: **v0.1.2**

## In this README:

- [Features](#features)
- [Usage](#usage)
  - [Initial setup](#initial-setup)
  - [Examples](#examples)
- [FAQ](#faq)

## Features

This package contains the following modules:

⚙️ [bio_seq](https://github.com/Steve-Cheney/biopytk/blob/main/src/biopytk/bio_seq.py)
- DNA/RNA sequencing tools.

||||
|--|--|--|
| `__init__()` | `printSeq()` | `nucFrequencyDict()`|
| `validateSeq()` | `percentGC()` | `transcribe()`|
| `dnaCompliment()` | `rnaCompliment()` | `dna_reverseCompliment()`|
| `rna_reverseCompliment()` | `getBasePairs()` | `hammingDist()`|
| `seqCompare()` | `translate()` | `seqSummary()`|
| `get_reading_frames()` | `getAllORFProteins()` | `globalAlign()` |

⚙️ [aa_seq](https://github.com/Steve-Cheney/biopytk/blob/main/src/biopytk/aa_seq.py)
- Amino Acid & Polypeptide analysis tools.

	`getProteinsFromRF()`
	
⚙️ [fasta_tk](https://github.com/Steve-Cheney/biopytk/blob/main/src/biopytk/fasta_tk.py)
- FASTA file analysis tools.
	- Supports: `.fasta`, `.fa` file types.
	- More support to come in later releases

||||
|--|--|--|
| `percentGC_fasta()` | `gcContentFromFASTA()` | `getMaxGCFromFASTA()`|
| `dictFromFASTA()` | `parseFASTA()` | `dfFromFASTA()`|

## Usage

### Initial setup

1. cd to your desired install directory and use [pip](https://pypi.org/project/pip/) to install the package.

   
    ```
    pip install biopytk
    ```
    ***OR***
2. Navigate to the [PyPi BioPyTK download page](https://pypi.org/project/biopytk/#files) and install manually.
		*Need help installing packages? [Click here](https://packaging.python.org/en/latest/tutorials/installing-packages/).* 
### Examples
*Coming soon!*

## FAQ

#### Can I use this package for my own work?
Absolutely! Please see the [License](#License) information below.
#### Will this package work with older versions of Python?
It is recommended to use ``>Python 3.11.1`` as this was the version the package was built on. If future Python releases cause dependency issues, patches will be released.
#### Why are you making this if [BioPython](https://biopython.org/) exists?
This is a personal project to practice bioinformatics tooling creation, package management, and overall explore bioinformatics. This is in no way intended to take over large open-source projects, but rather act as a sandbox for personal research and development!

## License
Steve-Cheney/biopytk is licensed under  the [MIT License](https://github.com/Steve-Cheney/biopytk/blob/main/LICENSE).

Copyright (c) 2023 Stephen Cheney
