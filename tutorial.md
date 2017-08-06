SEPP/TIPP Tutorial
==================
In this tutorial, we will analyze biological datasets aquired through (16S) amplicon and whole shotgun sequencing using TIPP and SEPP. The 16S (454 GS FLX Titanium) sample ([SRR1219742](https://www.ncbi.nlm.nih.gov/biosample/SAMN02725485) -- Lemur Vaginal Sample) comes from Yildirim et al., 2014 ([doi:10.1038/ismej.2014.90](https://www.ncbi.nlm.nih.gov/pubmed/25036926)). The shotgun (Illumina Genome Analyzer II) sample ([SRR059421](https://www.ncbi.nlm.nih.gov/sra/SRX022983[accn]) -- Human Stool Sample) comes from the [Human Microbiome Project](http://www.hmpdacc.org). All runs were downloaded from the NCBI database using this [fastq-dump command](tools/fastq_dump.sh). Additional pre-processing of reads could be done before using SEPP or TIPP.

Part I: Taxonomic Identification using TIPP
-------------------------------------------
Recall that SEPP and TIPP require the following inputs:
+ A reference alignment and tree, and
+ A set of query sequences, i.e., fragments/reads of unknown origin

The [RDP 2016 Bacteria reference package](refpkgs/RDP_2016_Bacteria.refpkg) is used for phylogenetic placement (SEPP) and taxonomic identification (TIPP) of 16S samples. This reference package contains an alignment and tree that were built on the 11,988 sequences from the [RDP database](https://rdp.cme.msu.edu/) -- selecting >1200 site-length, type isolates with quality "Good", and the NCBI taxonomy. 

The size of the reference package and the number of query sequences affect the running time of SEPP and TIPP. For example, the number of sequences in the reference dataset and the alignment subset size determine how many profile HMMs must be built over the reference alignment. Then each query sequence in the sample must be aligned (and scored) to each of these profile HMMs. 

Running TIPP on the first 2,500 sequences from the 16S sample (SRR1219742) showed that the majority of classified reads (929 reads) were identified as Clostridia. For this tutorial, the RDP Bacteria reference package was constrained to 707 sequences in the Clostridia class. You will be classifying these reads at the family, genus, and species levels using TIPP!

If you haven't done so already, ssh onto the MBL servers, clone this respository, and load the python 2.7.12 module.
```
git clone https://github.com/ekmolloy/stamps-tutorial.git
module purge
module load python/2.7.12-201701011205
```
Change into the tipp directory,
```
cd stamps-tutorial/tipp
```
and run TIPP using the following command
```
python /class/stamps-software/sepp/run_tipp.py \
    -a ../refpkgs/RDP_2016_Clostridia.refpkg/pasta.fasta \
    -t ../refpkgs/RDP_2016_Clostridia.refpkg/pasta.taxonomy \
    -r ../refpkgs/RDP_2016_Clostridia.refpkg/RAxML_info.taxonomy \
    -tx ../refpkgs/RDP_2016_Clostridia.refpkg/taxonomy.table \
    -txm ../refpkgs/RDP_2016_Clostridia.refpkg/species.mapping \
    -A 100 \
    -P 1000 \
    -at 0.95 \
    -pt 0.95 \
    -f ../samples/16S/SRR1219742_RDP_2016_Clostridia.fasta \
    -o TIPP-RDP-CLOSTRIDIA-95-SRR1219742 \
    --tempdir tmp \
    --cpu 2
```
This will take 5-6 minutes to finish. In the meantime, let's breakdown the command. The first five options specify files included in the reference package
+ `-a [`[`reference multiple sequence alignment -- fasta format`](refpkgs/RDP_2016_Clostridia.refpkg/pasta.fasta)`]`
+ `-t [`[`reference taxonomy -- newick format`](refpkgs/RDP_2016_Clostridia.refpkg/pasta.taxonomy)`]`
+ `-r [`[`reference tree model parameters -- RAxML info file`](refpkgs/RDP_2016_Clostridia.refpkg/RAxML_info.taxonomy)`]`
+ `-tx [`[`mapping taxonomic id to taxonomy information -- csv`](refpkgs/RDP_2016_Clostridia.refpkg/taxonomy.table)`]`
+ `-txm [`[`mapping sequence names to taxonomic IDs -- csv`](refpkgs/RDP_2016_Clostridia.refpkg/species.mapping)`]`

The next two options specify the decomposition of the reference alignment and tree into subsets.
+ `-A [alignment subset size]`
+ `-P [placement subset size]`

TIPP was run with an alignment subset size of 100 (slightly less than 10% of the Clostridia reference package) and a placement subset size of 1000 (greater than the entire Clostridia reference package). Recall that running SEPP/TIPP with larger placement subset sizes can increase accuracy but is more computationally intensive. The default alignment/placement subset sizes follow the 10% rule.

The next two options specify the support thresholds used by TIPP.
+ `-at [alignment support threshold]`
+ `-pt [placement support threshold]`

TIPP was run with support thresholds of 0.95, which is the default. 

The next two options specify the input and output
+ `-f [`[`fragment file -- fasta`](samples/16S/SRR1219742_RDP_2016_Clostridia.fasta)`]`
+ `-o [prefix of output files]`

The final options are set specifically for STAMPS tutorial to prevent temporary files from being written all over the MBL servers and limit the number of CPUs per user.

To see all of the [TIPP options](tipp-help.md), run
```
python /class/stamps-software/sepp/run_tipp.py -h
```
By now TIPP may have finished and written the following files
+ [classification information -- csv](tipp/out/TIPP-RDP-CLOSTRIDIA-95-SRR1219742_classification.txt)
+ [phylogenetic placement information -- json](tipp/out/TIPP-RDP-CLOSTRIDIA-95-SRR1219742_placement.json)
+ [alignment on both the reference and query sequences -- fasta](tipp/out/TIPP-RDP-CLOSTRIDIA-95-SRR1219742_alignment.fasta.gz)

The classification file shows the support of classifying sequences at each taxonomic rank. Check out the support for each read classified at the species level
```
grep ",species," TIPP-RDP-CLOSTRIDIA-95-SRR1219742_classification.txt
```
Computing the number of reads classified at each taxonomic rank
```
python ../tools/restructure_tipp_classification.py \
    -i TIPP-RDP-CLOSTRIDIA-95-SRR1219742_classification.txt \
    -o FINAL-TIPP-RDP-CLOSTRIDIA-95-SRR1219742
```
and examing the read count for species-level classification
```
cat FINAL-TIPP-RDP-CLOSTRIDIA-95-SRR1219742_species.csv
```
shows the vast majority of reads are unclassified (545 reads). Classified reads are largely Fastidiosipila sanguinis (213 reads) and Anaerovorax odorimutans (144 reads). What do read counts look like at the genus and family level? 

*Before moving on, repeat this portion of the tutorial running TIPP with a lower alignment/placement support threshold (e.g., 0.50). What do the support values look like for reads classified at the species level? How does the number of reads unclassified at the species level compare to TIPP run with an alignment/placement support threshold of 0.95?*

**NOTE: In general, SEPP/TIPP should be run on reads and their reverse complement. This has already been taken care of in setting up the 16S reads for this tutorial.**


Part II: Phylogenetic Placement using SEPP
------------------------------------------
Now let's take a closer look at some select reads using phylogenetic placement. Based on the TIPP classification (using an alignment/placement support threshold of 0.50), many sequences were identified as the Ruminococcaceae family including
+ GEQJ1S112HF5CU
+ GEQJ1S110GHR11
+ GEQJ1S110GEAZV 
+ GEQJ1S112HNELY  
+ GBEHU2E07D5RLY

You can examine the support at which these reads are classfied at the family level by using grep, e.g.,
```
grep "GEQJ1S112HF5CU" TIPP-RDP-CLOSTRIDIA-95-SRR1219742_classification.txt 
```

SEPP can be used to place these five query sequences into the RDP Bacteria reference package; however, we will use SEPP with a RDP Bacteria reference package constrained to the Ruminococcaceae family (55 sequences) for visualization purposes. Change into the sepp directory
```
cd ../sepp
```
and run SEPP using the following command
```
python /class/stamps-software/sepp/run_sepp.py \
    -a ../refpkgs/RDP_2016_Ruminococcaceae.refpkg/pasta_labeled.fasta \
    -t ../refpkgs/RDP_2016_Ruminococcaceae.refpkg/pasta_labeled.taxonomy \
    -r ../refpkgs/RDP_2016_Ruminococcaceae.refpkg/RAxML_info.taxonomy \
    -A 25 \
    -P 100 \
    -f ../samples/16S/READS-Ruminococcaceae.fasta \
    -o SEPP-RDP-RUMINO-READS \
    --tempdir tmp \
    --cpu 2
```
Both the command and the output are nearly identical to TIPP; however, alignment and placement support thresholds are not specified, and the classification file is not written. Use the [placement file from SEPP](sepp/out/SEPP-RDP-RUMINO-READS_placement.json) to rank the five reads by the branch length connecting the read to the Ruminococcaceae tree. You may need read more about the json file format [here](https://matsen.github.io/pplacer/generated_rst/pplacer.html) (search for JSON format specification) or [here](http://journals.plos.org/plosone/article?id=10.1371/journal.pone.0031009). 

Now we will visualize these placements by converting the placement file into a tree format (e.g., newick or xml) with [guppy](https://matsen.github.io/pplacer/generated_rst/guppy.html)
```
/class/stamps-software/sepp/.sepp/bundled-v4.3.2/guppy tog \
    --xml \
    SEPP-RDP-RUMINO-READS_placement.json
```
Download the xml file onto your personal computer, e.g., by opening a new terminal and typing
```
scp [user-name]@class.mbl.edu:~/stamps-tutorial/sepp/SEPP-RDP-RUMINO-READS_placement.tog.xml ~/Desktop
```
and open the file with your favorite tree viewer. [EvolView](http://www.evolgenius.info/evolview) can be used to visualize the placement of query sequences in the reference tree with [colored branches](http://evolview.codeplex.com/wikipage?title=DatasetBranchColor) and [colored leaves](https://evolview.codeplex.com/wikipage?title=DatasetLeafColor). After the uploading the file, hover over "Annatotation upload", click on the buttons that are second (branch color) and third (leaf color) from the left, and add the text
```
GEQJ1S112HF5CU red ad   
GEQJ1S110GHR11 red ad   
GEQJ1S110GEAZV red ad   
GEQJ1S112HNELY red ad   
GBEHU2E07D5RLY red ad   
```
**NOTE: that the above spaces need to be tabs!**

Examining the [cladogram](images/rumino-cladogram.pdf), we can notice that GEQJ1S112HNELY was placed closer to the root than the GEQJ1S112HF5CU, which was placed sister to Saccharofermentans acetigenes -- however based on the [branch length](images/rumino-phylogeny.pdf) GEQJ1S112HF5CU may not necessarily have very high sequence identity to Saccharofermentans accetigenes. Branch lengths can also be very short, see placement of the query sequence GEQJ1S112HN8VO on the Heliobacterium reference package [here](https://github.com/ekmolloy/stamps-tutorial/blob/master/images/helio-phylogeny.pdf).

Use the [alignment file from SEPP](sepp/out/SEPP-RDP-RUMINO-READS_alignment.fasta) to compare the read GEQJ1S112HF5CU to the reference sequence Saccharofermentans_acetigenes_1. Extract the two sequences into a new fasta file
```
grep -A1 "GEQJ1S112HF5CU" SEPP-RDP-RUMINO-READS_alignment.fasta > SEPP-RDP-RUMINO-READS_subset.fasta
grep -A1 "Saccharofermentans_acetigenes_1" SEPP-RDP-RUMINO-READS_alignment.fasta >> SEPP-RDP-RUMINO-READS_subset.fasta
```
and download it onto your personal computer, e.g., by opening a new terminal and typing
```
scp [user-name]@class.mbl.edu:~/stamps-tutorial/sepp/SEPP-RDP-RUMINO-READS_subset.fasta ~/Desktop
```
[MSAViewer](http://msa.biojs.net) can be used to visualize the multiple sequence alignment. Scroll down and click he little arrow icon under "Use It". Then click "Import" followed by "From file".

*Before moving on, let's consider the relationship between alignment, placement, and classification. Go back to the TIPP directory*
```
cd ../TIPP
```
*Use the [cladogram](images/helio-cladogram.pdf) to identify reference sequences near GEQJ1S112HN8VO (e.g., Heliobacterium_modesticaldum_11). Extract these sequences from the alignment file from TIPP and visualize. Now examine the placement file from TIPP. What are branch lengths and maximum likelihood scores for placements of GEQJ1S112HN8VO onto the Clostridia reference tree? Now discuss TIPP (with 0.50 support thresholds) classifying GEQJ1S112HN8VO as Heliobacterium modesticaldum Ice1 (below species level) versus TIPP (with 0.95 support thresholds) classifying GEQJ1S112HN8VO as Clostridiales order and Unclassified at the family, genus, and species levels.*

**JUST A REMINDER: Small reference alignments and trees are used in this tutorial to save time and make visualization easier; however, the benefits of using SEPP/TIPP are greatest when trees have a large evolutionary diameters -- which is more likely for trees are large. New tools for visualizing phylogenetic placements for large trees are on the way courtesy of [Mike Nute](https://publish.illinois.edu/michaelnute/)!**

Part III: Phylogenetic (Abundance) Profiling with TIPP
------------------------------------------------------
All prior analyses are on 16S, which is not a single copy. TIPP can be used for phylogenetic (abundance) profiling by using a collection of marker genes as reference alignments and trees. First, BLAST is used to identify whether a read is a match for a specific marker gene. If so, TIPP is used to classify the read. To run this analysis (in the future), create an output directory
```
mkdir TIPP-COGS-95-SRR059420
mkdir TIPP-COGS-95-SRR059420/markers
```
and run TIPP using the following command
```
python /class/stamps-software/sepp/run_abundance.py \
    -G cogs \
    -c /class/stamps-software/sepp/.sepp/tipp.config \
    -at 0.95 \
    -pt 0.95 \
    -f ../samples/shotgun/SRR059420_pass_1_1-25000.fasta \
    -d TIPP-COGS-95-SRR059420 \
    --tempdir tmp \
    --cpu 2
```
The above command includes the following new options
+ `-G [whether marker genes or COGs should be used]`
+ `-c [configuration file for TIPP]`
+ `-d [name of output directory]`

And the [output](tipp/out/TIPP-95-COGS-SRR059420) includes the abundance profile for each taxonomic rank, for example, the [genus-level abundance profile](tipp/out/TIPP-95-COGS-SRR059420/abundance.genus.csv) shows that the 95% of reads (that match to a COG) are classified as Bacteroides. Finally, the [markers folder](https://github.com/ekmolloy/stamps-tutorial/tree/master/tipp/out/TIPP-95-COGS-SRR059420/markers) contains the output from running TIPP on each of the markers.

Thank you!
----------
Thank you for taking the time to do this tutorial, and please let us know if you have any more questions or comments!
