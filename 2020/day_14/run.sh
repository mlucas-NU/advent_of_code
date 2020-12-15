SCRIPT_DIR=$(dirname "$0")

TEST_INPUT_FILE1=$SCRIPT_DIR/input_test.txt
TEST_INPUT_FILE2=$SCRIPT_DIR/input_test2.txt
MAIN_INPUT_FILE=$SCRIPT_DIR/input_1.txt

echo "TEST: Running on $TEST_INPUT_FILE. Expected v1 result: 165"
python3 $SCRIPT_DIR/main.py --verbosity DEBUG $TEST_INPUT_FILE1
echo "TEST: Running on $TEST_INPUT_FILE. Expected v2 result: 208"
python3 $SCRIPT_DIR/main.py --verbosity DEBUG $TEST_INPUT_FILE2
echo "MAIN: Running on $MAIN_INPUT_FILE"
python3 $SCRIPT_DIR/main.py $MAIN_INPUT_FILE
