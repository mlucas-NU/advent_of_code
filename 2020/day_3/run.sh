SCRIPT_DIR=$(dirname "$0")

TEST_ANSWER=7
TEST_INPUT_FILES="$SCRIPT_DIR/input_test.txt $SCRIPT_DIR/directions.txt"
MAIN_INPUT_FILES="$SCRIPT_DIR/input_1.txt $SCRIPT_DIR/directions.txt"

echo "TEST: Running on $TEST_INPUT_FILES. Expected result: $TEST_ANSWER"
python3 $SCRIPT_DIR/main.py --verbosity DEBUG $TEST_INPUT_FILES
echo "MAIN: Running on $MAIN_INPUT_FILES"
python3 $SCRIPT_DIR/main.py $MAIN_INPUT_FILES
