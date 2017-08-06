#!/bin/bash

# MUST EDIT IF NOT ON MBL SERVERS!
SEPP="/class/stamps-software/sepp/"
TIPP="$SEPP/run_abundance.py"

# Default is 0.95 for both thresholds
ALIGNMENT_THRESHOLD="0.95"
PLACEMENT_THRESHOLD="0.95"

# Set the name of the output file
OUTPUT="TIPP-COGS-95-SRR059420"

if [ ! -d TIPP-COGS-95-SRR059420 ]; then
    mkdir TIPP-COGS-95-SRR059420
fi
if [ ! -d TIPP-COGS-95-SRR059420/markers ]; then
    mkdir TIPP-COGS-95-SRR059420/markers
fi

# Run TIPP for abundance profiling
python $TIPP -G "cogs" \
			 -c "$SEPP/.sepp/tipp.config" \
			 -at $ALIGNMENT_THRESHOLD \
             -pt $PLACEMENT_THRESHOLD \
             -f "../samples/shotgun/SRR059420_pass_1_1-25000.fasta" \
             -d $OUTPUT \
             --tempdir tmp \
             --cpu 2
