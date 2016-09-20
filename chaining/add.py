#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, getopt, glob, shutil, shlex, shutil, subprocess , tempfile

BASE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
JAR_FILE_PATH = os.path.join(BASE_DIRECTORY, "RNA-unchained.jar")
JAR_CALL = "java -cp " + JAR_FILE_PATH+" "

##compute comparison
def computeAdd(indexdir, struct):
   """
   Add in the given index database all new RNAs and update the index, i.e. compute
   for each new RNA all seeds of all l-d tables of the index.
   """
   ##add RNA to database
   executeProg(JAR_CALL+"org.research.rna.database.OnDiskDB "+ str(indexdir) + " add " + struct)

   ##compute table
   #tableIndex = getTable(indexdir, ldTable)
   executeProg(JAR_CALL+"org.research.rna.index.CsmDB " + indexdir + " update ")

def executeProg(command_line):
   """
   execute a commande line
   """
   args = shlex.split(command_line)
   p = subprocess.call(args)
   #p.wait()
   if p!=0:
      print "command ligne : ",args
      print "command ligne : ",command_line
      sys.exit(0)

def run(fastaFile, path):
   """
   Add all RNAs to the given index
   """
   indexpath =  os.path.join(path, "indexDB")
      
   #create index DB
   computeAdd(indexpath, fastaFile)
      

   
   

