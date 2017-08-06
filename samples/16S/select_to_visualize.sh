#!/bin/bash

FASTA="SRR1219742_RDP_2016_Clostridia.fasta"

READS=( "GBEHU2E07D5RLY" \
        "GEQJ1S112HF5CU" \
        "GEQJ1S110GEAZV" \
        "GEQJ1S110GHR11" \
        "GEQJ1S112HNELY" )

echo -n "" > reads-Ruminococcaceae.fasta
for READ in ${READS[@]}; do
    grep -A1 "$READ" $FASTA >> reads-Ruminococcaceae.fasta
done

grep -A1 "GEQJ1S112HN8VO" $FASTA > reads-Heliobacteriaceae.fasta
