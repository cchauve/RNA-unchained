#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, getopt, glob, shutil, shlex, shutil, subprocess , tempfile

BASE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
JAR_FILE_PATH = os.path.join(BASE_DIRECTORY, "RNA-unchained.jar")
JAR_CALL = "java -cp " + JAR_FILE_PATH+" "

##compute comparison
def computeIndexDB(indexdir, struct):
   """
   Compute the index database and add all sequences in it.
   @indexdir:=folder that will contains the index 
   @struct:=RNAs to put inside the index
   """
   executeProg(JAR_CALL + "org.research.rna.database.OnDiskDB " + str(indexdir) + " create")
   ##add RNA to database
   executeProg(JAR_CALL + "org.research.rna.database.OnDiskDB "+ str(indexdir) + " add " + struct)
   executeProg(JAR_CALL + "org.research.rna.index.CsmDB " + str(indexdir) + " create")

def executeProg(command_line):
   """
   fonction to execute commande line
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
   main fonction.
   @fastaFile:= the path of a fasta file of sequences and structures
   @path:=the analysis folder to record results 
   """
   indexpath =  os.path.join(path, "indexDB")
      
   #create index DB
   computeIndexDB(indexpath, fastaFile)
      

   
   
