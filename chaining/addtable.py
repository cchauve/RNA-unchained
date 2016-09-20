#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, getopt, glob, shutil, shlex, shutil, subprocess , tempfile

BASE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
JAR_FILE_PATH = os.path.join(BASE_DIRECTORY, "RNA-unchained.jar")
JAR_CALL = "java -cp " + JAR_FILE_PATH+" "

##compute comparison
def computeNewIndexDB(home,fam, ldTable):
   """
   For a given index compute the l-d table of this index
   that will contains for each RNA all l-d seeds of this RNA.
   """
   indexdir = os.path.join(fam,"indexDB")
   
   ##creation of an empty index for the base with d l seed
   d=int(ldTable[0])-2*int(ldTable[1])
   executeProg(JAR_CALL + "org.research.rna.index.CsmDB " + str(indexdir) + " create " + str(d) + " " + str(ldTable[0]))
   tableIndex = getTable(indexdir, ldTable)
   ##update the empty index with RNA in the database
   executeProg(JAR_CALL + "org.research.rna.index.CsmDB " + indexdir + " update " + tableIndex)

def executeProg(command_line):
   """
   Execute commande line
   """
   args = shlex.split(command_line)
   p = subprocess.call(args)
   #p.wait()
   if p!=0:
      print "command ligne : ",args
      print "command ligne : ",command_line
      sys.exit(0)

def getTable(fam, ldTable):
   """
   Get the number of the l-d table in the given index database
   """
   tmp_fd, tmp_name=tempfile.mkstemp()
   r=subprocess.call(JAR_CALL + "org.research.rna.index.CsmDB "+ str(fam) + " infos", shell=True,stdout=tmp_fd)
   if r!=0:
      print "error : impossible to add table"
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

def run(home, indexPath, l, d):
   """
   main fonction
   """
   computeNewIndexDB(home, indexPath, [l, d])
   

   
   
