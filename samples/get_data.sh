#!/bin/bash

# 16S Samples
# -----------
# Yildirim S et al., "Primate vaginal microbiomes exhibit species
#    specificity without universal Lactobacillus dominance.", ISME J,
#    2014 Jul 18;8(12):2431-44
#
# Library Information:
# Name: VE0506
# Instrument: 454 GS FLX Titanium
# Strategy: AMPLICON
# Source: GENOMIC
# Selection: PCR
# Layout: SINGLE

if [ ! -d 16S ]; then
    mkdir 16S
fi
cd 16S

# BioSample: SAMN02725485; Sample name: Lemurs; SRA: SRS591181
../../tools/fastq_dump.sh SRR1219742
head -n5000 SRR1219742_pass_2.fasta SRR1219742_pass_2_1-2500.fasta
python ../../tools/reverse_complement_fasta.py \
       SRR1219742_pass_2_1-2500.fasta \
       SRR1219742_pass_2_1-2500_REVCOM.fasta

# BioSample: SAMN02725483; Sample name: Humans; SRA: SRS591179
#./fastq_dump.sh SRR1233025
#head -n5000 SRR1233025_pass_2.fasta SRR1233025_pass_2_1-2500.fasta
#python ../tools/reverse_complement_fasta.py \
#       SRR1233025_pass_2_1-2500.fasta \
#       SRR1233025_pass_2_1-2500_REVCOM.fasta

# Shotgun Samples
# ---------------
# Human Microbiome Project (Stool Sample)
#
# Library Information:
# Name: Solexa-26720
# Instrument: Illumina Genome Analyzer II
# Strategy: WGS
# Source: GENOMIC
# Selection: RANDOM
# Layout: PAIRED

cd ../
if [ ! -d shotgun ]; then
    mkdir shotgun
fi
cd shotgun

# BioSample: SAMN00034120; SRA: SRS012902
./fastq_dump.sh SRR059420
head -n50000 SRR059420_pass_1.fasta SRR059420_pass_1_1-25000.fasta
head -n50000 SRR059420_pass_2.fasta SRR059420_pass_2_1-25000.fasta
