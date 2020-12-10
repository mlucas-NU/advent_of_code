SCRIPT_DIR=$(dirname "$0")

TEST_ANSWER=2
TEST_INPUT_FILE=$SCRIPT_DIR/input_test.txt
MAIN_INPUT_FILE=$SCRIPT_DIR/input_1.txt

echo "TEST: Running on $TEST_INPUT_FILE. Expected result: $TEST_ANSWER"
python3 $SCRIPT_DIR/main.py --verbosity DEBUG $TEST_INPUT_FILE
echo "MAIN: Running on $MAIN_INPUT_FILE"
python3 $SCRIPT_DIR/main.py $MAIN_INPUT_FILE
