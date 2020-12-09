import argparse
import logging

from parser import Parser

# Parse Arguments

parser = argparse.ArgumentParser()
parser.add_argument('input_file', help='input file to read')
parser.add_argument('--verbosity', help='specify verbosity level (DEBUG|INFO)')
args = parser.parse_args()

verbosity = 'INFO'
if args.verbosity:
    verbosity = args.verbosity
logging.getLogger().setLevel(logging.getLevelName(verbosity))


# Load Inputs

input_file = args.input_file
with open(input_file) as f:
    all_programs = []
    for line in f:
        values = line.split(',')
        values = list(map(int, values))
        all_programs.append(values)


# Main Logic

for i, program in enumerate(all_programs):
    parser = Parser(program)
    logging.info(f'Program {i}')
    parser.run()
