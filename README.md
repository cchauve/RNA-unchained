-----------------------------------------------------------------------------------
                       RNA-unchained v1.0 Overview
-----------------------------------------------------------------------------------


RNA-unchained (Chaining sequence/structure seeds for computing RNA similarity)
find seeds of pattern matching between an RNA query and other RNA) to boost the
alignment of these RNA.  RNAunchained explicitly chains and aligns based
on both RNA sequence and structure. It compute pairwise analyse between a query
and the computed RNA index database.


RNA-unchained consists of three steps:

(1) The constitution of an index of RNA which contains for each RNA
	all computed seeds. These index can deal with multiple seeds size
	and can be modified by adding new RNA.
(2) Given a file containing one or multiple query it finds all common
	seeds between query and RNAs of the index and compute the corresponding
	anchor. Multiple chaining options are available. A file of constraints for 
	each pairwise analyse is computed. 
(3) Given the constraints file of the pairwise chaining a pairwise
	alignment is done with Locarna. The alignment is computed only if
	there is an anchor between 

The chaining filter algorithm restricts the search space of alignments by computing
a file of constraints between both RNAs to align.


Version: 1.0
Contact: Laetitia Bourgeade, laetitia.bourgeade@labri.fr


-----------------------------------------------------------------------------------
                            INSTALL
-----------------------------------------------------------------------------------

Run RNA-unchained with python v2.7 or higher but not python v3.0 or higher.  No other
compilation is necessary, except installing and configuring other packages.

The following software packages are required

-- LocARNA v1.7.5 or higher     
   http://www.bioinf.uni-freiburg.de/Software/LocARNA/ 

   
-- ViennaRNA v2.1.1 or higher
   https://www.tbi.univie.ac.at/~ronny/RNA/  

If they are not installed to '/usr/local',which is typically the default directory
when installed as root, you have to add the path in the shell path.

You can use directly RNA-unchained by adding the path of RNA-unchained folder in
the shell path.

-------------------------------------------------------------------------
                            USAGE
-------------------------------------------------------------------------

Chaining in sequence and structure RNAs before aligning them:

(1) Input file must be at fasta format. It can contains struture but if not
	RNAfold will be used to compute Minimum Free Enerdy (MFE) struture. 
(2) Given a fasta file, an index contening all seeds of given sizes is
	constituted.
(3) Given a fasta file, all pairwise analysis between each RNA of the file
	and each RNA of the index database is done. It generates a file per
	analysis containing the constraints. 
(4) Two files one with alignments and one with alignments score is generated
	with Locarna using the constraints file computed before.


Run RNA-unchained with the command

Command: RNA-unchaind.py [options] file.fa

Calculate pairwise alignment using chaining and seeds method

positional arguments:
  file.fa                    Fasta file containing RNAs

optional arguments:
  -h  --help            show this help message and exit
  -c, --chaining        use the chaining algorithm to find best chain with one
                        type of seeds
  -a, --alignment       align with constraints
  -m, --makeIndex       Construct Index with name DBNAME
  --add                 add new RNA to DB
  -db DBNAME, --dbName DBNAME
                        give the name DBNAME to the index database
  -r, --r2              chaining only r2 seeds
  			Not compatible with rfb option
  -rfb, --r2fb          seeds optimization. 
  			Not compatible with r option
  -epc, --epcLCS4l      anchor optimisation
  -f                    forced alignment with Locarna even if there is no
                        constraints
  -ld l d, --ldSeeds l d
                        seq length and str length for seed
  --version             show program's version number and exit




-------------------------------------------------------------------------
                               Output
-------------------------------------------------------------------------

RNA-unchained will generate the following files in the folder with the name
of the index db (if no name given a random one is used)

(1) An 'RNAunchainedProjects' folder is created in your home. It will contains all
    RNA-unchained analysis.
(2) A folder with the specified or random name of the index is created in
    'RNAunchainedProjects'. It will contains all analysis computed with
    this database.
(3) The 'indexDB' folder contains the index database.
(4) The 'results' folder contains all analysis with one folder with the name 
    of the RNA per query RNA. 
(5) For each RNA query there is 3 files:
		- RNAname_constraints: contains computed constraints
		- chaining_alignments: contains alignments
		- chaining_score: contains scores of alignments

