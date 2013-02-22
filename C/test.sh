PROG=minidc

make > /dev/null

if [ -e ./$PROG ]
	./$PROG < test_input
fi

if [ -e ./*.o ]
	then make clean > /dev/null
fi
