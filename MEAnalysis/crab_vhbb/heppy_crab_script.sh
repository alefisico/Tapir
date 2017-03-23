source env.sh
python heppy_crab_script.py $@ &> log
echo Finished_vhbbb
python mem_crab_script.py $@ >> log 2>&1
EXITCODE=$?
echo ExitCode $EXITCODE
./post.sh $EXITCODE
