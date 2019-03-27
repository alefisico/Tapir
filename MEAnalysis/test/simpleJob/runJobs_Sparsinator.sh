#!/usr/bin/env sh

### Usage: .

FILESFOLDER="/work/algomez/work/ttH/CMSSW_10_2_11/src/TTH/MEAnalysis/test/simpleJob/datasets/nanoPostMEAnalysis/"
sample=${1}
VERSION="v01_20190316"


WORKDIR=sparJobs/
if test x"$WORKDIR" != x; then
   mkdir -p $WORKDIR
fi

if [[ ${sample} == *"all"* ]]; then
    samplesArray=$(ls ${FILESFOLDER})
else
    samArray=$(ls ${FILESFOLDER})
    if [[ " ${samArray[@]} " =~ "${sample}"  ]]; then
        samplesArray=( ${sample} )
    else
        echo "No "${sample}".txt file in "${FILESFOLDER}
        return
    fi
fi

for isam in ${samplesArray}; do

    isam=${isam%.txt*}
    echo "Runnning "${isam}

    BATCHFILE=${WORKDIR}/submitJob_${isam}.sh
    echo '''#!/bin/bash
#################################
# PSI Tier-3 example batch Job  #
#################################

##### CONFIGURATION ##############################################
# Output files to be copied back to the User Interface
# (the file path must be given relative to the working directory)
#OUTFILES="TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8_nanoAOD_90_postprocessed.root"

# Output files to be copied to the SE
# (as above the file path must be given relative to the working directory)
SEOUTFILES="'${isam}'_sparsinator_'${VERSION}'.root"

# By default, the files will be copied to $USER_SRM_HOME/$username/$JOBDIR,
# but here you can define the subdirectory under your SE storage path
# to which files will be copied (uncomment line)
SEUSERSUBDIR="ttH/Sparsinator/'${VERSION}'/"
#
# Users CMS hypernews name (needed for users SE storage home path
# USER_SRM_HOME below)
HN_NAME='${USER}'

# set DBG=1 for additional debug output in the job report files
# DBG=2 will also give detailed output on SRM operations
DBG=2

#### The following configurations you should not need to change
# The SEs user home area (SRMv2 URL)
USER_SRM_HOME="srm://t3se01.psi.ch/pnfs/psi.ch/cms/trivcat/store/user/"

# Top working directory on worker nodes local disk. The batch
# job working directory will be created below this
TOPWORKDIR=/scratch/`whoami`

# Basename of job sandbox (job workdir will be $TOPWORKDIR/$JOBDIR)
JOBDIR=sgejob-$JOB_ID
##################################################################


############ BATCH QUEUE DIRECTIVES ##############################
# Lines beginning with #$ are used to set options for the SGE
# queueing system (same as specifying these options to the qsub
# command

# Job name (defines name seen in monitoring by qstat and the
#     job scripts stderr/stdout names)
#$ -N job_'${isam}'

### Specify the queue on which to run
#$ -q all.q

# Change to the current working directory from which the job got
# submitted (will also result in the job report stdout/stderr being
# written to this directory)
#$ -cwd

# here you could change location of the job report stdout/stderr files
#  if you did not want them in the submission directory
#$ -o '${PWD}'/sparJobs/
#$ -e '${PWD}'/sparJobs/

##################################################################



##### MONITORING/DEBUG INFORMATION ###############################
DATE_START=`date +%s`
echo "Job started at " `date`
cat <<EOF
################################################################
## QUEUEING SYSTEM SETTINGS:
HOME=$HOME
USER=$USER
JOB_ID=$JOB_ID
JOB_NAME=$JOB_NAME
HOSTNAME=$HOSTNAME
TASK_ID=$TASK_ID
QUEUE=$QUEUE

EOF

echo "################################################################"

if test 0"$DBG" -gt 0; then
   echo "######## Environment Variables ##########"
   env
   echo "################################################################"
fi


##### SET UP WORKDIR AND ENVIRONMENT ######################################
STARTDIR=`pwd`
WORKDIR=$TOPWORKDIR/$JOBDIR
RESULTDIR=$STARTDIR/$JOBDIR
if test x"$SEUSERSUBDIR" = x; then
   SERESULTDIR=$USER_SRM_HOME/$HN_NAME/$JOBDIR
else
   SERESULTDIR=$USER_SRM_HOME/$HN_NAME/$SEUSERSUBDIR
fi
if test -e "$WORKDIR"; then
   echo "ERROR: WORKDIR ($WORKDIR) already exists! Aborting..." >&2
   exit 1
fi
mkdir -p $WORKDIR
if test ! -d "$WORKDIR"; then
   echo "ERROR: Failed to create workdir ($WORKDIR)! Aborting..." >&2
   exit 1
fi

cd $WORKDIR
cat <<EOF
################################################################
## JOB SETTINGS:
STARTDIR=$STARTDIR
WORKDIR=$WORKDIR
RESULTDIR=$RESULTDIR
SERESULTDIR=$SERESULTDIR
EOF

###########################################################################
## YOUR FUNCTIONALITY CODE GOES HERE
# set up CMS environment

source /swshare/psit3/etc/profile.d/cms_ui_env.sh
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd /work/algomez/work/ttH/CMSSW_10_2_11/src/TTH/MEAnalysis/test/simpleJob/
eval `scramv1 runtime -sh`

PYTHON_CFG="/work/algomez/work/ttH/CMSSW_10_2_11/src/TTH/MEAnalysis/test/simpleJob/simpleJob_sparsinator.py"
CONFIG_FILE="/work/algomez/work/ttH/CMSSW_10_2_11/src/TTH/MEAnalysis/test/simpleJob/simpleJob_config.cfg"

cd $WORKDIR
python ${PYTHON_CFG} --sample '${isam}' --inputDir '${FILESFOLDER}' --analysis_cfg ${CONFIG_FILE}
mv '${isam}'_sparsinator.root '${isam}'_sparsinator_'${VERSION}'.root

#### RETRIEVAL OF OUTPUT FILES AND CLEANING UP ############################
cd $WORKDIR
if test 0"$DBG" -gt 0; then
    echo "########################################################"
    echo "############# Working directory contents ###############"
    echo "pwd: " `pwd`
    ls -Rl
    echo "########################################################"
    echo "YOUR OUTPUT WILL BE MOVED TO $RESULTDIR"
    echo "########################################################"
fi

if test x"$OUTFILES" != x; then
   mkdir -p $RESULTDIR
   if test ! -e "$RESULTDIR"; then
          echo "ERROR: Failed to create $RESULTDIR ...Aborting..." >&2
          exit 1
   fi
   for n in $OUTFILES; do
       if test ! -e $WORKDIR/$n; then
          echo "WARNING: Cannot find output file $WORKDIR/$n. Ignoring it" >&2
       else
          cp -a $WORKDIR/$n $RESULTDIR/$n
          if test $? -ne 0; then
             echo "ERROR: Failed to copy $WORKDIR/$n to $RESULTDIR/$n" >&2
          fi
   fi
   done
fi

if test x"$SEOUTFILES" != x; then
   if test 0"$DBG" -ge 2; then
      srmdebug="-v"
   fi
   for n in $SEOUTFILES; do
       if test ! -e $WORKDIR/$n; then
          echo "WARNING: Cannot find output file $WORKDIR/$n. Ignoring it" >&2
       else
          env -i X509_USER_PROXY=~/.x509up_u`id -u` gfal-copy $srmdebug                  $WORKDIR/$n $SERESULTDIR/$n  --force
          if test $? -ne 0; then
             echo "ERROR: Failed to copy $WORKDIR/$n to $SERESULTDIR/$n" >&2
          fi
   fi
   done
fi

echo "Cleaning up $WORKDIR"
#rm -rf $WORKDIR

###########################################################################
DATE_END=`date +%s`
RUNTIME=$((DATE_END-DATE_START))
echo "################################################################"
echo "Job finished at " `date`
echo "Wallclock running time: $RUNTIME s"
exit 0
    ''' > $BATCHFILE
    qsub $BATCHFILE

done
