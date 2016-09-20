#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

import fastaParser
import generateSecondaryStructure

def computeProcess(cmdLine, RESULTS=False):
    """
    Compute a process with or without results
    @cmdLine:= string of commande line to execute
    @RESULTS:=boolean to specify if it keep results

    @output:=liste of results
    """
    if RESULTS:
        tmp_fd, tmp_name=tempfile.mkstemp()
        r=subprocess.call(cmdLine,shell=True, stdout=tmp_fd)
        if r!=0:
            print "error : ", cmdLine
            sys.exit(1)
        os.close(tmp_fd)
        with open(tmp_name,"r") as f:
            results = f.read()
        os.unlink(tmp_name)
        return results
    else :
        r=subprocess.call(cmdLine,shell=True)
        if r!=0:
            print "error : ", cmdLine
            sys.exit(1)

def isChained(fastaFile, db, ldTable, r, rfb, epc):
    """
    Check if a chaining has been computed
    @return:=boolean
    """
    if not os.path.exists(os.path.join(db,'results')):
        return False
    with open(fastaFile,'r') as FILE:
        lines = FILE.readlines()
    FILE.closed

    extensionName = '_'+ldTable[0]+'_'+ldTable[1]
    if r == 1:
        extensionName += '_r'
    elif rfb == 1:
        extensionName += '_rfb'
    if epc == 1:
        extensionName += '_epc'
    extensionName += '_constraints'

    for i in range(0, len(lines),3):
        if not os.path.exists(os.path.join(os.path.join( os.path.join(db,'results'), lines[i].strip().replace('>','') ), lines[i].strip().replace('>','')+extensionName) ):
            return False
    return True

def str2bool(val):
    """ 
    Convert string value to integer that play the part of boolean values
    """
    if val == 'True':
        return 1
    elif val == 'False':
        return 0
    else:
        print "error: conversion str to bool"
        sys.exit(1)

def analyseFile(name,db, struct):
    """
    Check if the given file contains structures. If not it uses RNAfold
    to compute RNA secondary structure.
    @name:=given file
    @db:=analysis folder
    @struct:=use or not of RNAfold
    @return:=fasta file with secondary structure path in the results folder 
    in the RNAunchained workspace
    """
    #Analyse du fichier en entree
    fastaFile, STRUCTURE, IUPAC, nbSeq = fastaParser.compute(name,db)
    if not STRUCTURE and struct=='False':
        print "ERROR: Need structures do not use -s option"
        sys.exit(1)
    elif not STRUCTURE and struct=='True':
        print "Generates secondary structures"
        fastaFile = generateSecondaryStructure.run(fastaFile, db)
    return fastaFile
