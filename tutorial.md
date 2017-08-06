SEPP/TIPP Tutorial
==================
In this tutorial, we will analyze biological datasets aquired through (16S) amplicon and whole shotgun using TIPP and SEPP.

The 16S (454 GS FLX Titanium) sample come from Yildirim et al. (2014). Primate vaginal microbiomes exhibit species specificity without universal Lactobacillus dominance. *International Society for Microbial Ecology Journal*. 8(12):2431-44. [doi:10.1038/ismej.2014.90](https://www.ncbi.nlm.nih.gov/pubmed/25036926):
+ [SRR1219742](https://www.ncbi.nlm.nih.gov/biosample/SAMN02725485) -- Lemur Vaginal Sample

The shotgun (Illumina Genome Analyzer II) sample comes from the [Human Microbiome Project](http://www.hmpdacc.org):
+  [SRR059421](https://www.ncbi.nlm.nih.gov/sra/SRX022983[accn]) -- Human Stool Sample

All runs were downloaded from the NCBI database using this [fastq-dump command](samples/fastq_dump.sh). However, you could also use your laboratory's pre-processing protocol before using SEPP or TIPP.

Part I: Taxonomic Identification using TIPP
-------------------------------------------
Recall that both SEPP and TIPP require the following inputs:
+ Query sequences, i.e., fragments/reads of unknown origin
+ Reference tree and alignment

Both of these inputs affects SEPP/TIPP's running time. For example, the number of sequences in the reference dataset and the alignment subset size determines how many profile HMMs must be built over the reverse alignment. Each query sequence in the sample must be aligned (and scored) to each of these profile HMMs. The [RDP 2016 Bacteria reference package](refpkgs/RDP_2016_Bacteria.refpkg) contains an alignment and phylogenetic tree on 11,988 sequences from the RDP database from selecting >1200 site-length, type isolates with quality "Good" and taxonomy from NCBI. To reduce the analysis time, this reference package was constrained to 707 sequences in the Clostridia class -- as the majority of reads (929 out of the first 2,500 reads) from the 16S sample (SRR1219742) were indentified as Clostridia using TIPP. **You will be classifying these 929 reads at the family, genus, and species levels using TIPP**

If you haven't done so already, ssh onto the MBL servers, clone this respository, and load the python 2.7.12 module.
```
git clone https://github.com/ekmolloy/stamps-tutorial.git
module purge
module load python/2.7.12-201701011205
```
Then change into the tipp directory.
```
cd stamps-tutorial/tipp
```
and run TIPP using the following command:
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
This will take 5-6 minutes to finish. In the meantime, let's breakdown this command.

To see all of the [TIPP options](tipp-help.md), run
```
python /class/stamps-software/sepp/run_tipp.py -h
```

Part II: Phylogenetic Placement using SEPP
------------------------------------------
Let's examine some of the reads that have been classified...

Change into the sepp directory
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
    -o SEPP-RDP-RUMINO-95-SRR1219742 \
    --tempdir tmp \
    --cpu 2
```

which will take a few seconds to finish. This command is nearly identical to that of TIPP, but we do not need to specify alignment or placement support thresholds. Unlike TIPP, SEPP...

Let's visualize these placements. First, we will need to convert the json placement file into a tree format (e.g., newick or xml) using guppy.
```
/class/stamps-software/sepp/.sepp/bundled-v4.3.2/guppy tog \
    --xml \
    SEPP-RDP-RUMINO-READS_placement.json
```
Download the tree files onto your personal computer, e.g., by opening a new terminal and typing
```
scp *.tog.xml ~/Desktop
```
[EvolView](http://www.evolgenius.info/evolview) can then be used to visualize the placement of query sequences in the reference tree with [colored branches](http://evolview.codeplex.com/wikipage?title=DatasetBranchColor) and [colored leaves](https://evolview.codeplex.com/wikipage?title=DatasetLeafColor). Simply 

```
GEQJ1S112HF5CU red ad   
GEQJ1S110GHR11  red ad   
GEQJ1S110GEAZV  red ad   
GEQJ1S112HNELY  red ad   
GBEHU2E07D5RLY  red ad   
```
Note: that the above spaces are actually tabs!

Looking at these placements...

To see all of the [SEPP options](sepp-help.md), run
```
python /class/stamps-software/sepp/run_sepp.py -h
```

Part III: Phylogenetic (Abundance) Profiling with TIPP
------------------------------------------------------
Analyzing metagenomic datasets requires...

Change back into the tipp directory,
```
cd ../tipp
```
create an output directory,
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
break down command and view the output...
