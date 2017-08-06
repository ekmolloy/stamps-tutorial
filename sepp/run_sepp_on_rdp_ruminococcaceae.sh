#!/bin/bash

# Set path to SEPP program
SEPP="/class/stamps-software/sepp/run_sepp.py"
GUPPY="/class/stamps-software/sepp/.sepp/bundled-v4.3.2/guppy"

# Set path to RDP 2016 Reference Package
REFPKG="../refpkgs/RDP_2016_Ruminococcaceae.refpkg"

# Define subsets sizes
ALIGNMENT_SUBSET_SIZE=25
PLACEMENT_SUBSET_SIZE=10

# Decide on 
OUTPUT="SEPP-RDP-RUMINO-READS"

# Run SEPP
python $SEPP -a "$REFPKG/pasta_labeled.fasta" \
             -t "$REFPKG/pasta_labeled.taxonomy" \
             -r "$REFPKG/RAxML_info.taxonomy" \
             -A $ALIGNMENT_SUBSET_SIZE \
             -P $PLACEMENT_SUBSET_SIZE \
             -f "../samples/16S/reads-Ruminococcaceae.fasta" \
             -o $OUTPUT \
             --tempdir tmp

# Create a tree to visualize from the placement file
$GUPPY tog --xml ${OUTPUT}_placement.json
