#!/bin/bash

for fasta in `ls *.fasta`; do
    gzip $fasta
done
