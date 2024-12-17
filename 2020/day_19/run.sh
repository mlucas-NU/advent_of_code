set -e
SCRIPT_DIR=$(dirname "$0")

GRAMMAR_FILE=$SCRIPT_DIR/monster_grammar.ebnf
PARSER_SCRIPT=$SCRIPT_DIR/monster_parser.py

TEST_ANSWER=2
TEST1_INPUT_FILE=$SCRIPT_DIR/input_test1.txt
TEST2_INPUT_FILE=$SCRIPT_DIR/input_test2.txt
TEST3_INPUT_FILE=$SCRIPT_DIR/input_test3.txt
PART1_INPUT_FILE=$SCRIPT_DIR/input_1.txt
PART2_INPUT_FILE=$SCRIPT_DIR/input_2.txt

function build_parser () {
    # Expects two arguments:
    #  $1: Advent of Code input file (formal grammar followed by two newline followed by candidate words)
    #  $2: Log level (generally DEBUG | INFO)

    echo "Building parser from $1"

    # Generate Grammar
    python3 $SCRIPT_DIR/build_grammar.py $1 $GRAMMAR_FILE --verbosity $2

    # Build Parser with tatsu (https://tatsu.readthedocs.io/en/stable/)
    tatsu --generate-parser $GRAMMAR_FILE --outfile $PARSER_SCRIPT 2> /dev/null
}

echo "TEST 1 (basic): Running on $TEST1_INPUT_FILE. Expected result: $TEST_ANSWER"
build_parser $TEST1_INPUT_FILE DEBUG
python3 $SCRIPT_DIR/main.py --verbosity DEBUG $TEST1_INPUT_FILE

echo "TEST 2 (long): Running on $TEST2_INPUT_FILE. Expected result: $TEST_ANSWER"
build_parser $TEST2_INPUT_FILE DEBUG
python3 $SCRIPT_DIR/main.py --verbosity DEBUG $TEST2_INPUT_FILE

echo "TEST 3 (long + replaced): Running on $TEST3_INPUT_FILE. Expected result: $TEST_ANSWER"
build_parser $TEST3_INPUT_FILE DEBUG
python3 $SCRIPT_DIR/main.py --verbosity DEBUG $TEST3_INPUT_FILE

explode

echo "PART 1: Running on $PART1_INPUT_FILE"
build_parser $PART1_INPUT_FILE INFO
python3 $SCRIPT_DIR/main.py $PART1_INPUT_FILE

echo "PART 2: Running on $PART2_INPUT_FILE"
build_parser $PART2_INPUT_FILE INFO
python3 $SCRIPT_DIR/main.py $PART2_INPUT_FILE
