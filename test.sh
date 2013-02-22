PROG=minidc.py
OUT=./test
EXE=$SRC/$PROG

cd $OUT
echo $(pwd)
exec $EXE < test_logic > logic_actual
echo $EXE < test_syntax > syntax_actual
echo $EXE < test_param > param_actual


