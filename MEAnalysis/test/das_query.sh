#!/bin/bash
#run as ./das_query.sh < dataset.txt | sed 's/root/root = 1/' > dataset_files.txt
while read dataset; do
    dasgoclient -query="file dataset=$dataset instance=prod/phys03"
done

