#!/bin/bash
source env.sh
env
cd $SGE_O_WORKDIR
~jpata/anaconda/bin/python ~jpata/anaconda/bin/rq worker --url $1
