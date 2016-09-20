#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, getopt, glob,tempfile,subprocess

def compute(inputFile):
    """
    Given a fasta file without secondary structures.
    Compute thanks to RNAfold the dots&brackets structure
    for each RNA in the file.
    """
    structures={}
    sequencesName,struct,seq=getStructure(inputFile)
    for i in range(len(sequencesName)):
        structures[sequencesName[i]]=[seq[i],struct[i]]
    return structures

def getSequence(sequencePath):
    """
    Given a file path it record names and sequences.
    """
    with open(sequencePath,'r') as SEQPATH:
        lines=SEQPATH.readlines()
    SEQPATH.closed
    rna=[]
    names=[]
    i=0
    while i<len(lines):
        if lines[i][0]=='>':
            names.append(lines[i].strip().replace('.','-'))
            rna.append("")
            line=len(names)-1
        else:
            rna[line]+=lines[i].strip()
        i+=1
        
    if len(rna)!=len(names):
        print"error:fasta file is not good:", len(names)," rna but ", len(rna)," sequences."
        sys.exit(1)
    return names,rna
    
def getStructure(sequencePath):
    """
    For all sequences compute with RNAfold its secondary
    structure.
    @return:=three ordered list of the names, the sequences
    and the structures.
    """
    names,sequences=getSequence(sequencePath)
    structures=[]

    for i in range(len(sequences)):
        tmp_fd, tmp_name=tempfile.mkstemp()
        r=subprocess.call("echo "+str(sequences[i])+" | RNAfold --noLP",shell=True, stdout=tmp_fd)
        if r!=0:
            print "ERROR: RNAfold do not succeed"
            sys.exit(1)
        os.close(tmp_fd)
        os.remove('rna.ps')
        with open(tmp_name,"r") as f:
            structureResults = f.read().split("\n")
        os.unlink(tmp_name)
        structureResults.pop()
        structureResults = structureResults[1].split(' ')[0]
        structures.append(structureResults)
    return names,structures,sequences

def run(inputFile,outputDirectory):
    """
    Given a fasta file without secondary structures and an
    output folder. Compute thanks to RNAfold the dots&brackets 
    structure and save the new fasta file in the analysis folder.
    """
    structures=compute(inputFile)

    family=inputFile.split('/').pop().split('.')[0]+'.fasta'
    outfile = os.path.join(outputDirectory,family)
    with open (outfile,'w') as OUTPUT:
        for name,sequences in structures.items():
            print >>OUTPUT,name
            print >>OUTPUT,sequences[0].strip()
            print >>OUTPUT,sequences[1].strip()
    OUTPUT.closed
    return outfile
