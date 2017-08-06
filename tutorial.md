SEPP/TIPP Tutorial
==================
In this tutorial, we will analyze biological datasets aquired through (16S) amplicon and whole shotgun sequencing using TIPP and SEPP. The 16S (454 GS FLX Titanium) sample ([SRR1219742](https://www.ncbi.nlm.nih.gov/biosample/SAMN02725485) -- Lemur Vaginal Sample) comes from Yildirim et al. (2014). Primate vaginal microbiomes exhibit species specificity without universal Lactobacillus dominance. *International Society for Microbial Ecology Journal*. 8(12):2431-44. [doi:10.1038/ismej.2014.90](https://www.ncbi.nlm.nih.gov/pubmed/25036926). The shotgun (Illumina Genome Analyzer II) sample ([SRR059421](https://www.ncbi.nlm.nih.gov/sra/SRX022983[accn]) -- Human Stool Sample) comes from the [Human Microbiome Project](http://www.hmpdacc.org). All runs were downloaded from the NCBI database using this [fastq-dump command](tools/fastq_dump.sh). You could also do further pre-processing before using SEPP or TIPP.

Part I: Taxonomic Identification using TIPP
-------------------------------------------
The [RDP 2016 Bacteria reference package](refpkgs/RDP_2016_Bacteria.refpkg) can be used for phylogenetic placement (SEPP) or taxonomic identification (TIPP) of 16S samples. This reference package contains an alignment and tree that were built on the 11,988 sequences from the [RDP database](https://rdp.cme.msu.edu/) -- selecting >1200 site-length, type isolates with quality "Good" and taxonomy from NCBI. However, recall that SEPP and TIPP require the following inputs:
+ A reference alignment and tree, and
+ A set of query sequences, i.e., fragments/reads of unknown origin
Both inputs affect the running time of SEPP and TIPP. For example, the number of sequences in the reference dataset and the alignment subset size determines how many profile HMMs must be built over the reference alignment. Each query sequence in the sample must be aligned (and scored) to each of these profile HMMs. 

To save time for this tutorial, TIPP was run on the first 2,500 sequences from the 16S sample (SRR1219742) and the majority of reads (929 out of the first 2,500 reads) were identified as Clostridia. The RDP Bacteria reference package was constrained to 707 sequences in the Clostridia class. **Now you will be classifying these reads at the family, genus, and species levels using TIPP!**

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

The first five options specify files included in the reference package
+ -a [Reference multiple sequence alignment -- fasta format](refpkgs/RDP_2016_Clostridia.refpkg/pasta.fasta)
+ -t [Reference taxonomy -- newick format](refpkgs/RDP_2016_Clostridia.refpkg/pasta.taxonomy)
+ -r [Reference tree model parameters -- RAxML info file](refpkgs/RDP_2016_Clostridia.refpkg/RAxML_info.taxonomy)
+ -tx [CSV file mapping taxonomic id to taxonomy information](refpkgs/RDP_2016_Clostridia.refpkg/taxonomy.table)
+ -txm [CSV mapping sequence names to taxonomic IDs](refpkgs/RDP_2016_Clostridia.refpkg/species.mapping)

The next two options specify the decomposition of the reference alignment and tree into subsets.
+ -A [alignment subset size]
+ -P [placement subset size]

TIPP was run with an alignment subset size of 100 (slightly less than 10% of the Clostridia reference package) and a placement subset size of 1000 (greater than the entire Clostridia reference package). Recall that running SEPP/TIPP with larger placement subset sizes can increase accuracy but is more computationally intensive. The default alignment/placement subset sizes follow the 10% rule.

The next two options specify the support thresholds used by TIPP.
+ -at [alignment support threshold]
+ -pt [placement support threshold]

TIPP was run with support thresholds of 0.95, which is the default. 

The next two options specify the input and output
+ -f [fragment file -- fasta](samples/16S/SRR1219742_RDP_2016_Clostridia.fasta)
+ -o [prefix of output files]

The final options set specifically for STAMPS tutorial to prevent temporary files from being written all over the MBL servers and limit the number of CPUs per user.

To see all of the [TIPP options](tipp-help.md), run
```
python /class/stamps-software/sepp/run_tipp.py -h
```
By now TIPP may have finished and written the following five files
+ [classification information -- csv](tipp/out/TIPP-RDP-CLOSTRIDIA-95-SRR1219742_classification.txt)
+ [phylogenetic placement information -- json](tipp/out/TIPP-RDP-CLOSTRIDIA-95-SRR1219742_placement.json)
+ [alignment on both the reference and query sequences -- fasta](tipp/out/TIPP-RDP-CLOSTRIDIA-95-SRR1219742_alignment.fasta.gz)
The classification file shows the support of classifying sequences at each taxonomic rank. Check out the support for species-level classification via
```
grep ",species," TIPP-RDP-CLOSTRIDIA-95-SRR1219742_classification.txt
```
The number of reads classified at each taxonomic rank can be computed using
```
python ../tools/restructure_tipp_classification.py \
    -i TIPP-RDP-CLOSTRIDIA-95-SRR1219742_classification.txt \
    -o FINAL-TIPP-RDP-CLOSTRIDIA-95-SRR1219742
```
and examining this files
```
cat FINAL-TIPP-RDP-CLOSTRIDIA-95-SRR1219742_species.csv
```
shows the vast majority of reads are identified as Fastidiosipila sanguinis (213 reads) followed by Anaerovorax odorimutans (144 reads).

**Before moving on, it is important to note that TIPP should be run on reads and their reverse complement.**


Part II: Phylogenetic Placement using SEPP
------------------------------------------
Now let's take a closer look at our data using phylogenetic placement.

It is also important to note that the reference package has changed from Clostridia (class) to Ruminococcaceae (family). A smaller reference package was made on Ruminococcaceae (

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
    -o SEPP-RDP-RUMINO-READS \
    --tempdir tmp \
    --cpu 2
```

which will take a few seconds to finish. This command is nearly identical to that of TIPP except that the alignment and placement support thresholds are not specified. 

In order to visualize the placements, the placement file (json) into a tree format (e.g., newick or xml) using guppy
```
/class/stamps-software/sepp/.sepp/bundled-v4.3.2/guppy tog \
    --xml \
    SEPP-RDP-RUMINO-READS_placement.json
```
The tree file can then be downloaded onto your personal computer, for example, by opening a new terminal and typing
```
scp [user-name]@[mbl-server-name]:~/stamps-tutorial/sepp/SEPP-RDP-RUMINO-READS_placement.tog.xml ~/Desktop
```
You may use your favorite tree viewer to examine this data. If you don't have one, consider using
[EvolView](http://www.evolgenius.info/evolview) to visualize the placement of query sequences in the reference tree with [colored branches](http://evolview.codeplex.com/wikipage?title=DatasetBranchColor) and [colored leaves](https://evolview.codeplex.com/wikipage?title=DatasetLeafColor). After the file is uploaded, check the 

```
GEQJ1S112HF5CU red ad   
GEQJ1S110GHR11 red ad   
GEQJ1S110GEAZV red ad   
GEQJ1S112HNELY red ad   
GBEHU2E07D5RLY red ad   
```
**Note: that the above spaces need to be tabs!**

Examining these files...

**Before moving on, it is important to note that small reference alignments and trees were used in this tutorial to save time and make visualization easier to interpret; however, the benefits of using SEPP/TIPP are greatest when trees have a large evolutionary diameters -- which is more likely when trees are large. New tools for visualizing phylogenetic placement data from SEPP are on the way courtesy of [Mike Nute](https://publish.illinois.edu/michaelnute/)!**


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
