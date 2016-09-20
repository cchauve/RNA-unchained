#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, getopt, glob, shutil, shlex, shutil, subprocess , tempfile

BASE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
JAR_FILE_PATH = os.path.join(BASE_DIRECTORY, "RNA-unchained.jar")
JAR_CALL = "java -cp " + JAR_FILE_PATH+" "

def run(fastaFile, path, table, rOption,rfbOption,epcOption):
    """
    Compute the pairwise chaining between all RNAs of the fasta file
    and all RNAs of the index database. All chaining results are stored 
    in the analysis folder under the name of the RNA of the given file.
    @table:=l-d table of seeds to use to chain RNAs
    @rOPtion:=boolean to use only r2Seeds
    @rfbOption:=boolean to use r2fbSeeds-seeds optimization option
    @epcOption:=boolean to use anchor optimization option
    """
    indexdir=os.path.join(path,"indexDB")
    resultsdir=os.path.join(path, "results")

    if not os.path.exists(resultsdir):
        try:
            os.mkdir(resultsdir)
        except OSError, e:
            print e.errno, e.strerror, e.filename

    indexTable = getTable(indexdir,table)

    #chaining
    with open(fastaFile, 'r') as FILE:
        lines = FILE.readlines()
    FILE.closed
    for line in range(0, len(lines),3):
        rnadir=os.path.join(resultsdir, lines[line].strip().replace('>',''))
        
        if not os.path.exists(rnadir):
            try:
                os.mkdir(rnadir)
            except OSError, e:
                print e.errno, e.strerror, e.filename

        rnafile=os.path.join(rnadir, lines[line].strip().replace('>',''))+'_'+table[0]+'_'+table[1]

        executeProg(JAR_CALL + "org.research.rna.index.run.CsmCorrelation2 "+ indexdir+ " \""+lines[line+1].strip()+"\" \""+lines[line+2].strip()+"\" "+rnafile+" "+lines[line].strip().replace('>','')+" "+str(rOption)+" "+str(rfbOption)+" "+str(epcOption)+" "+indexTable)

def getTable(fam, ldTable):
   """
   Get the number of the l-d table in the given index database
   """
   tmp_fd, tmp_name=tempfile.mkstemp()
   r=subprocess.call(JAR_CALL + "org.research.rna.index.CsmDB "+ str(fam) + " infos", shell=True,stdout=tmp_fd)
   if r!=0:
      print "error : ompossible to find this table"
      sys.exit(1)
   os.close(tmp_fd)

   with open(tmp_name,"r") as f:
      lines = f.readlines()
   os.unlink(tmp_name)
   
   l = -1
   d = -1
   line = 0
   while l!=int(ldTable[0]) and d!=int(ldTable[1]):
      if "table " in lines[line]:
         tableIndex = lines[line].split(':')[0].split()[1]
      elif "sequence motif length" in lines[line]:
         d = int(lines[line].split(':')[1])
      elif "structure motif length" in lines[line]:
         l = int(lines[line].split(':')[1])
         d = l-d
      line+=1

   return tableIndex

def executeProg(command_line):
    """
    Execute a command line
    """
    p = subprocess.call(command_line, shell=True)
    #p.wait()
    if p!=0:
       print "command ligne : ",command_line
       sys.exit(0)   
   
