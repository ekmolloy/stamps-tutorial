README: Documentation about the construction of this reference package
Author: Michael Nute (nute2@illinois.edu)
Date:	Feb 23, 2017

Description:
	- This reference package is designed to allow TIPP to work with up-to-date 
		16S data. The sequences in this reference alignment were pulled from RDP
		on December 13, 2016. There are 11,988 sequences and they are based on 
		selecting >1200 site-length, type isolates with quality "Good" and taxonomy
		from NCBI.
	- After pulling the sequences, it was necessary to map the sequence names to
		NCBI taxon IDs, which was done with a script provided by Erin Molloy. That 
		lookup table is 'accn-to-taxid.txt'. The remaining steps to generate the 
		unrefined taxonomy tree were done using scripts and instructions from Nam
		Nguyen.
	
	- Description of each individual file is given below.

Files in this folder, and accompanying comments:

CONTENTS.json:
	- standard JSON file to define a reference package for TIPP. I just
		copied this one right from the 16S_bacteria package and changed
		the relevant values in the "files" section
pasta.fasta
	- This is the result of the 11,988 sequences described earlier after alignment
		with PASTA. All default pasta settings were used. 
pasta.taxonomy
	- This is the refined taxonomy used for placement by TIPP. This tree was fit
		by running RAxML with the unrefined taxonomy as a constraint tree. While 
		running, RAxML repeatedly ran into underflow errors during the final step
		of optimizing branch lengths and model paramters. As a result, RAxML was 
		run using settings that skip branch length estimation as a final step.		
	- The branch lengths for this tree were fit by FastTree using the options
		'-mllen -nome -intree <raxml_output_file>'
	- The RAxML command used to generate this tree was:
		raxmlHPC-PTHREADS-SSE3 -m GTRCATI -F -T 16 -p 1111 -g $work/unrefined.taxonomy.renamed -s $work/pasta.fasta -n refined -w $work/raxml_output
pasta.tree
	- This is the RAxML unconstrained gene tree estimated on the same pasta.fasta
		alignment. This is not used in TIPP but is included for reference.
RAxML_info.taxonomy
	- This is the RAxML model information for the pasta.taxonomy tree. It is
		the output of the commands provided above.
RAxML_info.tree
	- Likewise for pasta.tree. This is provided in case a user wants to do SEPP on	
		the unconstrained Tree.
species.mapping
	- The comma-delimited mapping between sequence names in the tree/alignment and
		NCBI taxon IDs.
taxonomy.table
	- The NCBI taxonomy table, as TIPP expects.

*.rawtree_3k
	- RAxML tree and info file run on a different set of sequences, including all of the ones in the other alignment but also including archeae and a small nubmer of eukaryotes. This is a gene tree, not a refined taxonmy.
