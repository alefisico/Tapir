#!/bin/bash
source env.sh
cd $SGE_O_WORKDIR
/swshare/anaconda/bin/rq worker -c settings -n $JOB_ID
