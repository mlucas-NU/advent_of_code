SCRIPT_DIR=$(dirname "$0")

TEST1_ANSWER=35
TEST1_INPUT_FILE=$SCRIPT_DIR/input_test1.txt
TEST2_ANSWER=220
TEST2_INPUT_FILE=$SCRIPT_DIR/input_test2.txt
MAIN_INPUT_FILE=$SCRIPT_DIR/input_1.txt

echo "TEST 1: Running on $TEST1_INPUT_FILE. Expected result: $TEST1_ANSWER"
python3 $SCRIPT_DIR/main.py --verbosity DEBUG $TEST1_INPUT_FILE
echo "TEST 2: Running on $TEST2_INPUT_FILE. Expected result: $TEST2_ANSWER"
python3 $SCRIPT_DIR/main.py --verbosity DEBUG $TEST2_INPUT_FILE
echo "MAIN: Running on $MAIN_INPUT_FILE"
python3 $SCRIPT_DIR/main.py $MAIN_INPUT_FILE
