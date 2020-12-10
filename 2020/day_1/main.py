import argparse
import logging


# Helper functions

def part2(expenses):

    for exp1 in expenses:
        for exp2 in expenses:
            for exp3 in expenses:
                if len(set([exp1, exp2, exp3])) < 3:
                    continue
                if exp1 + exp2 + exp3 == 2020:
                    return exp1 * exp2 * exp3

    raise ValueError('Cannot find answer to Part 2.')


# Parse Arguments

parser = argparse.ArgumentParser()
parser.add_argument('input_file', help='input file to read')
parser.add_argument('--verbosity', help='specify verbosity level (DEBUG|INFO)')
args = parser.parse_args()

verbosity = 'INFO'
if args.verbosity:
    verbosity = args.verbosity
logging.getLogger().setLevel(logging.getLevelName(verbosity))


# Load inputs

expenses = set()

input_file = args.input_file
with open(input_file) as f:
    for line in f.readlines():
        expenses.add(int(line))

# Main Logic

for expense in expenses:
    if 2020 - expense in expenses:
        logging.info(f'Part 1 Answer: {expense * (2020 - expense)}')
        break
else:
    raise ValueError('Cannot find answer to Part 1.')

answer2 = part2(expenses)
logging.info(f'Part 2 Answer: {answer2}')
