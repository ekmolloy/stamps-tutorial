#!/bin/bash

#FRAGMENTS="SRR1219742_pass_2_1-2500.fasta"
#OUTPUT="TIPP-RDP-BACTERIA-95-SRR1219742"

FRAGMENTS="SRR1219742_pass_2_1-2500_REVCOM.fasta"
OUTPUT="TIPP-RDP-BACTERIA-95-SRR1219742-REVCOM"

# Set path to TIPP program
TIPP="/class/stamps-software/sepp/run_tipp.py"

# Set path to RDP 2016 Bacteria Reference Package
REFPKG="../../refpkg/rdp_bact_2016.refpkg/"
ALIGNMENT_FILE="$REFPKG/pasta.fasta"
TREE_FILE="$REFPKG/pasta.taxonomy"
RAXML_INFO_FILE="$REFPKG/RAxML_info.taxonomy"
NAMEMAP="$REFPKG/species.mapping"
TAXONOMY="$REFPKG/taxonomy.table"

# Define threholds
ALIGNMENT_THRESHOLD=0.95
PLACEMENT_THRESHOLD=0.95

# Define subsets sizes
ALIGNMENT_SUBSET_SIZE=1000
PLACEMENT_SUBSET_SIZE=1000

# Run TIPP
python $TIPP -a $ALIGNMENT_FILE \
             -t $TREE_FILE \
             -r $RAXML_INFO_FILE \
             -tx $TAXONOMY \
             -txm $NAMEMAP \
             -A $ALIGNMENT_SUBSET_SIZE \
             -P $PLACEMENT_SUBSET_SIZE \
             -at $ALIGNMENT_THRESHOLD \
             -pt $PLACEMENT_THRESHOLD \
             -f $FRAGMENTS \
             -o $OUTPUT \
             -d $OUTPUT \
             --tempdir tmp
