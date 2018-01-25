#!/bin/bash

while read dataset; do
    dasgoclient -query="file dataset=$dataset instance=prod/phys03"
done

