#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import subprocess
import tempfile
import os
import sys
import shutil
import time

#import utilities
#import makeIndex
#import addTable
#import doChaining
#import doLocarna
#import add
from chaining import *

BASE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

def main():
    parser = argparse.ArgumentParser(prog="RNA-unchained", description="Compute pairwise alignment using chaining and seeds method on an indexed database", epilog='fin de l\'aide')
    #exclusive options
    secondaryStructGroup = parser.add_mutually_exclusive_group()
    secondaryStructGroup.add_argument("-s","--RNAfold", action='store_const', const='True', default='True', help="Compute the MFE structure with RNAfold if the given file do not contain structures. Activated by default", dest='subopt')
    #secondaryStructGroup.add_argument("-S", "--shapes", type=int,choices=range(1,11), nargs='?', const='5', help="compute maximum n secondary structure with RNAshapes from n different shapes",dest='shapes')

    #shared options
    parser.add_argument("f1", type=argparse.FileType('r'), nargs='?', action = 'store', help="Fasta file 1")

    #options
    parser.add_argument('-c','--chaining', action='store_const', const='True', default='False', help='Use the chaining algorithm to find best chain with one type of seeds', dest='chaining')
    parser.add_argument('-a','--alignment', action='store_const', const='True', default='False', help='align with constraints', dest='alignment')
    parser.add_argument('-m', '--makeIndex', action='store_const', const='True', default='False', help='Construct Index with name DBNAME',dest='makeIndex')
    parser.add_argument('--add', action='store_const', const='True', default='False', help='Add new RNA to DB', dest='add')
    parser.add_argument('-db', '--dbName', metavar='DBNAME', help='Give the name DBNAME to the index database', dest='db')

    parser.add_argument('-r', '--r2', action='store_const', const='True', default='False', help='Chains only r2 seeds\nNot compatible with rfb option',dest='r')
    parser.add_argument('-rfb', '--r2fb', action='store_const', const='True', default='False', help='Seeds optimization.\nNot compatible with r option',dest='rfb')
    parser.add_argument('-epc', '--epcLCS4l', action='store_const', const='True', default='False', help='anchor optimisation',dest='epc')

    parser.add_argument('-f', action='store_const', const='True', default='False', help='Forces alignment with Locarna even if there is no constraints',dest='forced')

    parser.add_argument('-ld','--ldSeeds', metavar=('l','d'), type=int, action='store', nargs=2, default=('9', '1'), help='Seq length and str length for seed', dest='ldTable')

    parser.add_argument('--version', action='version', version='%(prog)s 1.0')

    #parsed options
    args = parser.parse_args()

    #get HOME to create workspace
    CWD =  os.path.expanduser("~")
    CWD = os.path.join(CWD, 'RNAunchainedProjects')
    if not os.path.exists(CWD):
        try:
            os.mkdir(CWD)
        except OSError, e:
            print e.errno, e.strerror, e.filename
    
    #options management
    r = utilities.str2bool(args.r)
    rfb = utilities.str2bool(args.rfb)
    epc = utilities.str2bool(args.epc)
    f = utilities.str2bool(args.forced)
    CHAINING = False

    #Computing with options
    if args.f1:
        if args.makeIndex == 'True':
            if args.db:
                db=os.path.join(CWD, args.db)
                if not os.path.exists(db):
                    try:
                        os.mkdir(db)
                    except OSError, e:
                        print e.errno, e.strerror, e.filename
                else:
                    print "error:", db.split('/').pop()," name already exists. Use an another name for index"
                    sys.exit(1)
                fastaFile = utilities.analyseFile(args.f1.name, db, args.subopt)
                if args.ldTable[0]>2*args.ldTable[1]:
                    print "Create index database ", args.db, " with ", args.ldTable[0], "-", args.ldTable[1], " seeds."
                    makeindex.run(fastaFile, db)
                    addtable.run(CWD, db, args.ldTable[0], args.ldTable[1])
                else:
                    print "error l must be superior than 2d. You wanted ", args.ldTable[0], "-", args.ldTable[1], " seeds."
                    shutil.rmtree(db)
                    sys.exit(1)
            else:
                db=os.path.join(CWD,args.f1.name.split('/').pop().split('.')[0]+time.strftime('%d%m%y%H%M%S',time.localtime()))
                if not os.path.exists(db):
                    try:
                        os.mkdir(db)
                    except OSError, e:
                        print e.errno, e.strerror, e.filename
                fastaFile = utilities.analyseFile(args.f1.name, db, args.subopt)
                if args.ldTable[0]>2*args.ldTable[1]:
                    print "Create index database", db, " (default name) with ", args.ldTable[0], "-", args.ldTable[1], " seeds."
                    makeindex.run(fastaFile, db)
                    addtable.run(CWD,db, args.ldTable[0], args.ldTable[1])
                else:
                    print "error l must be superior than 2d. You wanted ", args.ldTable[0], "-", args.ldTable[1], " seeds." 
                    shutil.rmtree(db)
                    sys.exit(1)
            print "\n\n\t***   INDEX created with name: ", db.split('/').pop(), "   ***\n\n"
        elif args.add=='True' and args.db:
            db=os.path.join(CWD, args.db)
            fastaFile = utilities.analyseFile(args.f1.name, db, args.subopt)
            print "Add new RNAs to ", args.db, " index database"
            add.run(fastaFile, db)
        elif args.db:
            db=os.path.join(CWD, args.db)
            fastaFile = utilities.analyseFile(args.f1.name, db, args.subopt)
            if args.chaining=='True':
                print "Chaining of RNAs on ", args.db, " index database with ", args.ldTable[0], "-", args.ldTable[1], " seeds."
                dochaining.run(fastaFile, db, args.ldTable, r, rfb, epc)
                if args.alignment=='True':
                    print "Alignment of RNAs of ", args.db, " index database."
                    dolocarna.run(db, args.ldTable, f, r, rfb, epc)
            else:
                if args.alignment=='True' and utilities.isChained(fastaFile, db, args.ldTable, r, rfb, epc):
                    print "Alignment of RNAs of ", args.db, " index database."
                    dolocarna.run(db, args.ldTable, f, r, rfb, epc)
                else:
                    print "error: you can not align without chaining before"
                    sys.exit(1)
        else:
            print "error: see help to use RNA-unchained. Index database name is probably missing."
            sys.exit(1)
    else:
            print "error: see help to use RNA-unchained. A fasta file is needed for any option."
            sys.exit(1)

if __name__ == "__main__":
    main()
   
