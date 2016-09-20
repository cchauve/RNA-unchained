#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, getopt, glob, shutil, shlex, shutil, subprocess , tempfile
from ProgressBar import *

def computeLocarna(indexPath, queriesConstraints, l, d, extensionName) :
    """
    for each pair of query and indexed RNA compute constrained
    alignment with locaRNA
    """
    results = {}
    scoreresults = {}
    alignresults = {}

    nbQuery = 0
     
    nbTot=0
    for q,c in queriesConstraints.items():
        nbTot+=len(c)
    progress = ProgressBar(nbTot, 40, 'Alignments')

    for query, constraints in queriesConstraints.items():
        scoreres = {}
        alignres = {}

        seqresultspath = os.path.join(os.path.join(os.path.join(indexPath,'results'), query[:-2]),"chaining_alignment_"+str(l)+"_"+str(d)+extensionName+".txt")
        scoreresultspath = os.path.join(os.path.join(os.path.join(indexPath,'results'), query[:-2]),"chaining_score_"+str(l)+"_"+str(d)+extensionName+".txt")

        for constraint in constraints:

            name1 = constraint.split('\n')[0].replace('>','')
            if name1 == query:
                name2 = constraint.split('\n')[5].replace('>','')
            else:
                name2 = name1
                name1 = query
            filename = os.path.join(indexPath,"locarna_input_constraints_"+name1.strip()+"_"+name2.strip()+".txt")
            
            with open(filename,'w') as RNAFILE:
                RNAFILE.write(constraint)
            RNAFILE.closed
            
            ##compute locarna
            tmp_fd, tmp_name=tempfile.mkstemp()
            r=subprocess.call("mlocarna -v "+filename,stdout=tmp_fd, stderr=subprocess.STDOUT, shell=True)
            if r!=0:
                print "error : mlocarna failed"
                sys.exit(1)
            os.close(tmp_fd)
            os.unlink(tmp_name)
            with open(filename+".out/results/result_prog.aln","r") as f:
                lines = f.read()
            f.closed
            #erase temporary folder and files
            os.remove(filename)
            shutil.rmtree(filename+".out")

            align = lines.split()
            #get alignment
            a = ["",""]
            for ll in range(align.index('Score:')+3, len(align), 4):
                a[0] += align[ll]
                a[1] += align[ll+2]
            
            if align[align.index('Score:')+2] != query:
                a[0],a[1] = a[1],a[0]

            alignres[name2] = a
            scoreres[name2] = align[align.index('Score:')+1]

        writeSeqFile(seqresultspath, query[:-2], alignres)
        writeScoreFile(scoreresultspath, query[:-2], scoreres)

        alignresults[name1] = alignres
        scoreresults[name1] = scoreres

        nbQuery += len(constraints)
        
        progress.update(nbQuery)
    
    results["score"] = scoreresults
    results["alignment"] = alignresults
    return results

def executeProg(command_line):
    args = shlex.split(command_line)
    p = subprocess.call(args)
    if p!=0:
       print "command ligne : ",args
       sys.exit(0)

def writeSeqFile(filename, query, values):
    """
    For each query write all alignments with each RNA 
    of the index database in a file in the resuts folder
    """
    with open(filename, 'w') as FILE:
        for k,v in values.items():
            FILE.write('>'+query+'\n'+v[0]+"\n"+'>'+k+'\n'+v[1]+"\n")
    FILE.closed

def writeScoreFile(filename, query, values):
    """
    For each query write all scores of alignments with each
    RNA of the index database in a file in the resuts folder
    """
    with open(filename, 'w') as FILE:
        for k,v in values.items():
            FILE.write(query+","+k+":"+v+"\n")
    FILE.closed

def getConstraints(queries, forced, extension):
    """
    For each RNA query store the constraints computed by the previous step
    of chaining.
    @forced:=boolean to specify if pairwise analysis without constriants
    have to be aligned with LocaRNA
    """
    queriesConstraints = {}
    if forced:
        for query in queries:
            queryName = query.split('/').pop()
            queryConstraints = []
            with open(os.path.join(query, queryName+extension+'_constraints')) as CONSTRAINTS:
                lines = CONSTRAINTS.readlines()
            CONSTRAINTS.closed

            for i in range(0, len(lines),12):
                constraint = ""
                FIRST = True
                for k in range(2):
                    if FIRST:
                        constraint += lines[i+6*k].strip()+"_q\n"+ lines[i+1+6*k]
                        FIRST = False
                    else:
                        constraint += lines[i+6*k] + lines[i+1+6*k]
                    for j in range (3,6):
                        constraint += lines[i+6*k+j]
                queryConstraints.append(constraint)
        
            queriesConstraints[queryName+"_q"] = queryConstraints
    else:
        for query in queries:
            queryName = query.split('/').pop()
            queryConstraints = []
            with open(os.path.join(query, queryName+extension+'_constraints')) as CONSTRAINTS:
                lines = CONSTRAINTS.readlines()
            CONSTRAINTS.closed
            for i in range(0, len(lines),12):
                constraint = ""
                FIRST = True
                if '1' in lines[i+3].split('#')[0]:
                    for k in range(2):
                        if FIRST:
                            constraint += lines[i+6*k].strip()+"_q\n"+ lines[i+1+6*k]
                            FIRST = False
                        else:
                            constraint += lines[i+6*k] + lines[i+1+6*k]
                        for j in range (3,6):
                            constraint += lines[i+6*k+j]
                    if constraint != "":
                        queryConstraints.append(constraint)
                if queryConstraints != []:
                    queriesConstraints[queryName+"_q"] = queryConstraints
    
    return queriesConstraints           

def run(indexPath,ldTable, forced, r, rfb, epc):
    """
    main fonction to align chained RNAs
    """
    l = ldTable[0]
    d = ldTable[1]

    extensionName = ''
    if r == 1:
        extensionName += '_r'
    elif rfb == 1:
        extensionName += '_rfb'
    if epc == 1:
        extensionName += '_epc'

    extension = '_'+ldTable[0]+'_'+ldTable[1]+extensionName
 
    resultsPath = os.path.join(indexPath,"results")
    queriesConstraints = getConstraints(glob.glob(resultsPath+'/*'), forced, extension)
                                        
    locarnaResults=computeLocarna(indexPath,queriesConstraints,l,d, extensionName)
    
   

   
   
