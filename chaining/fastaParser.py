#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import shlex
import subprocess
import re

def executeProg(command_line):
    """
    Execute a command line 
    """
    p = subprocess.call(command_line,shell=True)
    #p.wait()
    if p!=0:
       print "error : command ligne ",command_line, " failled"
       sys.exit(0)

def numberSequences(fastaFile, STRUCTURE):
    """
    Compute the number of sequences in a given fasta file
    @STRUCTURE:=boolean of presence of secondary structure
    @return:=the number of sequences in the fastaFile
    """
    with open(fastaFile,'r') as FASTA:
        fastaLines=FASTA.readlines()
    FASTA.closed
    if STRUCTURE:
        return len(fastaLines)/3
    else:
        return len(fastaLines)/2
    

def isFasta(lines, outputFile):
    """
    Check if a given file is a fasta file or not.
    Check also if sequences and structures formats are valid formats
    and if they contains specific caracters like IUPAC ones.
    If it is a fasta file it is duplicated in the analysis folder.
    """
    fasta=""
    seqPattern=re.compile("[^ACGUacgu]")#None si que ces caracteres
    iupacPattern=re.compile("[^ACGUWSMKRYBDHVNacguwsmkrybdhvn]")
    strPattern=re.compile("[^.()]")

    names=[]

    IUPAC=False
    STRUCTURE=False
    FIRST=True
    l=0
    w=0
    while l < len(lines) :
        if FIRST:
            FIRST=False
            if lines[l][0]!='>':
                print "error : It is not a fasta file, first line must begin with >"
                sys.exit(0)
            else:
                seqLength=0
            """else:
                fasta+=lines[l].strip()
                names.append(lines[l].strip())
                FIRSTSEQ=True
                FIRSTSTR=True
                seqLength=0"""
        SAME=False
        if lines[l][0]=='>':
            w+=1
            if STRUCTURE and seqLength!=0:
                print "error: sequence length and structure length are differents"
                sys.exit(0)
            if lines[l].strip() not in names:
                names.append(lines[l].strip())
            else:
                print "WARNING: 2 sequences have the same name"
                SAME=True
            if not SAME:
                fasta+="\n"+lines[l].strip()
            FIRSTSEQ=True
            FIRSTSTR=True
            j=l+1
            while j<len(lines) and lines[j][0]!=">":
                if seqPattern.search(lines[j].strip()) == None:
                    if SAME:
                        pass
                    elif FIRSTSEQ:
                        FIRSTSEQ=False
                        fasta+="\n"+lines[j].strip().lower()
                    else:
                        fasta+=lines[j].strip().lower()
                    if not SAME:
                        seqLength+=len(lines[j].strip())
                elif iupacPattern.search(lines[j].strip()) == None:
                    if not IUPAC: 
                        IUPAC=True
                    if SAME:
                        pass
                    elif FIRSTSEQ:
                        FIRSTSEQ=False
                        fasta+="\n"+lines[j].strip().lower()
                    else:
                        fasta+=lines[j].strip().lower()
                    if not SAME:
                        seqLength+=len(lines[j].strip())
                elif strPattern.search(lines[j].strip()) == None:
                    if not STRUCTURE:
                        STRUCTURE=True
                    if SAME:
                        pass
                    elif FIRSTSTR:
                        FIRSTSTR=False
                        fasta+="\n"+lines[j].strip()
                    else:
                        fasta+=lines[j].strip()
                    if not SAME:
                        seqLength-=len(lines[j].strip())
                else:
                    print lines[j].strip()
                    print "error: unsupported characters"
                    sys.exit(0)
                j+=1
            l=j
    
    fasta = fasta[1:]

    if STRUCTURE and seqLength!=0:
        print "error: sequence length and structure length are differents"
        sys.exit(0)
    if not STRUCTURE and len(fasta.split('\n'))%2!=0:
        print "error: sequence missing"
        sys.exit(0)

    if STRUCTURE:
        nbSeq = len(fasta.split('\n'))/3
    else:
        nbSeq = len(fasta.split('\n'))/2
    
    with open(outputFile,'w') as OUTPUT:
        print >>OUTPUT, fasta
    OUTPUT.closed
        
    return outputFile, STRUCTURE, IUPAC, nbSeq


def compute(fastaName, outputDirectory):
    """
    Main fonction. Given a file and an output directory check if
    the file is in the rigth format and copy it in the analysis 
    folder.
    """
    outputFile=os.path.join(outputDirectory, fastaName.split('/').pop())
    tmp=os.path.join(outputDirectory, "tmp")
    #sed '/^$/d' chaining_alignment.txt>chaining_alignment2.txt && mv chaining_alignment2.txt test
    executeProg("sed '/^$/d' "+str(fastaName)+" > "+tmp)
    with open(tmp, 'r') as FASTA:
        lines=FASTA.readlines()
    FASTA.closed
    os.remove(tmp)

    if len(lines)<2:
        print "error: fasta file must avant at least 2 lines:name & sequence"
        sys.exit(0)

    return isFasta(lines, outputFile)

if __name__ == "__main__":
    fastaFile=sys.argv[1]

    executeProg("sed '/^$/d' "+str(fastaFile)+" > tmp")
    with open("tmp", 'r') as FASTA:
        lines=FASTA.readlines()
    FASTA.closed

    if len(lines)<2:
        print "error: fasta file must avant at least 2 lines"
        sys.exit(0)

    STRUCTURE,IUPAC = isFasta(lines, "tmp")
    if STRUCTURE:
        print "WARNING: you already have the secondary structure in your fasta file"
    if IUPAC:
        print "WARNING: you use IUPAC character in your fasta file not compatible with RNAShapes"
    
