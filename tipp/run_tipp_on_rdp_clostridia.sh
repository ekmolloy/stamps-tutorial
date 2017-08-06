#!/bin/bash

# MUST EDIT IF NOT ON MBL SERVERS!
TIPP="/class/stamps-software/sepp/run_tipp.py"

# Set path to RDP 2016 Reference Package
# 707 sequences from the Clostridia class
REFPKG="../refpkgs/RDP_2016_Clostridia.refpkg/"

# Default is 0.95 for both thresholds
ALIGNMENT_THRESHOLD="0.95"
PLACEMENT_THRESHOLD="0.95"

# Default is 10% of the sequences in the reference
ALIGNMENT_SUBSET_SIZE="100"
PLACEMENT_SUBSET_SIZE="1000"

# Set the name of the output file
OUTPUT="TIPP-RDP-CLOSTRIDIA-95-SRR1219742"

python $TIPP -a "$REFPKG/pasta.fasta" \
             -t "$REFPKG/pasta.taxonomy" \
             -r "$REFPKG/RAxML_info.taxonomy" \
             -tx "$REFPKG/taxonomy.table" \
             -txm "$REFPKG/species.mapping" \
             -A $ALIGNMENT_SUBSET_SIZE \
             -P $PLACEMENT_SUBSET_SIZE \
             -at $ALIGNMENT_THRESHOLD \
             -pt $PLACEMENT_THRESHOLD \
             -f "../samples/16S/SRR1219742_RDP_2016_Clostridia.fasta" \
             -o $OUTPUT \
             --tempdir tmp \
             --cpu 2

python ../tools/restructure_tipp_classification.py \
    -i ${OUTPUT}_classification.txt \
    -o FINAL-$OUTPUT
