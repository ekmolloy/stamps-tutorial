#!/bin/bash

ORIGIN="TIPP-RDP-BACTERIA-95-SRR1219742"
REVCOM="TIPP-RDP-BACTERIA-95-SRR1219742-REVCOM"

#python ../../tools/restructure_tipp_classification.py \
#    -i $ORIGIN/${ORIGIN}_classification.txt \
#    -r $REVCOM/${REVCOM}_classification.txt \
#    -o MERGED-TIPP-RDP-BACTERIA-95-SRR1219742

python ../../tools/extract_fragments_by_taxonomy.py \
	-c MERGED-TIPP-RDP-BACTERIA-95-SRR1219742.csv \
	-f SRR1219742_pass_2_1-2500.fasta \
	-r SRR1219742_pass_2_1-2500_REVCOM.fasta \
	-x "class" -n "Clostridia" \
	-o "../SRR1219742_RDP_2016_Clostridia.fasta"

python ../../tools/extract_fragments_by_taxonomy.py \
	-c MERGED-TIPP-RDP-BACTERIA-95-SRR1219742.csv \
	-f SRR1219742_pass_2_1-2500.fasta \
	-r SRR1219742_pass_2_1-2500_REVCOM.fasta \
	-x "class" -n "Epsilonproteobacteria" \
	-o "../SRR1219742_RDP_2016_Epsilonproteobacteria.fasta"