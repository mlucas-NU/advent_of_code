SCRIPT_DIR=$(dirname "$0")

echo "TEST files. Expected answers: 142 and 281"
python3 $SCRIPT_DIR/main.py --verbosity DEBUG $SCRIPT_DIR/input_test_1.txt
python3 $SCRIPT_DIR/main.py --verbosity DEBUG $SCRIPT_DIR/input_test_2.txt
echo "MAIN"
python3 $SCRIPT_DIR/main.py $SCRIPT_DIR/input_1.txt
