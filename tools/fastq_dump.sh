#!/bin/bash

FASTQ_DUMP="/class/stamps-software/sratoolkit.2.8.2-1-centos_linux64/bin/fastq-dump"

SRR_ID=$1

$FASTQ_DUMP --clip \
            --dumpbase \
            --fasta 0 \
            --origfmt \
            --read-filter pass \
            --readids \
            --skip-technical \
            --split-files \
            $SRR_ID
