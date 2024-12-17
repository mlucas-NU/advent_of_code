import argparse
import logging
import re
import tatsu

from monster_parser import MonsterParser

# Parse Arguments

parser = argparse.ArgumentParser()
parser.add_argument('input_file', help='input file to read')
parser.add_argument('--verbosity', help='specify verbosity level (DEBUG|INFO)')
args = parser.parse_args()

verbosity = 'INFO'
if args.verbosity:
    verbosity = args.verbosity
logging.getLogger().setLevel(logging.getLevelName(verbosity))


# Helper classes

def count_valid_statements(statements):
    parser = MonsterParser()
    num_valid = 0
    for s in statements:
        try:
            parser.parse(s, whitespace='')
            num_valid += 1
        except tatsu.exceptions.ParseError:
            # logging.exception(e)
            continue

    return num_valid


# Load Inputs

regex_pattern = re.compile(r'.*\n\n(.*)', re.MULTILINE | re.DOTALL)
input_file = args.input_file
with open(input_file) as f:
    match = re.match(regex_pattern, f.read())
statements = match.group(1).splitlines()


# Main Logic

num_valid = count_valid_statements(statements)
logging.info(f'Num valid statements: {num_valid}')
