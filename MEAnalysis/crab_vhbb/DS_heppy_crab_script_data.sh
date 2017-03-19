source env.sh
#manually copy the data configuration
cp heppy_config_data.py heppy_config.py
python DS_heppy_crab_script.py $@ &> log
echo Finished_vhbbb
python DS_mem_crab_script.py $@ >> log 2>&1
EXITCODE=$?
echo ExitCode $EXITCODE
./post.sh $EXITCODE
