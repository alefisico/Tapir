source env.sh
python heppy_crab_script.py $@ &> log
EXITCODE=$?
echo ExitCode $EXITCODE
./post.sh $EXITCODE
