import argparse
import logging

from collections import defaultdict


# Parse Arguments

parser = argparse.ArgumentParser()
parser.add_argument('input_file', help='input file to read')
parser.add_argument('--verbosity', help='specify verbosity level (DEBUG|INFO)')
args = parser.parse_args()

verbosity = 'INFO'
if args.verbosity:
    verbosity = args.verbosity
logging.getLogger().setLevel(logging.getLevelName(verbosity))


# Helper Functions

def count_paths(elements):
    return _count_helper(elements[0], elements[1:len(elements)-1], elements[-1])


def _count_helper(start_val, elements, end_val):
    if len(elements) == 0:
        assert end_val - start_val < 4
        return 1

    total_subpaths = 0
    for i in range(min(3, len(elements))):
        if elements[i] - start_val < 4:
            total_subpaths += _count_helper(elements[i], elements[i+1:], end_val)

    if end_val - start_val < 4:
        total_subpaths += 1

    return total_subpaths


# Load Inputs

input_file = args.input_file
with open(input_file) as f:
    adapters = list(map(int, f.readlines()))

adapters.append(0)
adapters.append(max(adapters) + 3)
adapters.sort()

# Main Logic

counter = defaultdict(int)
for i in range(len(adapters)-1):
    diff = adapters[i+1] - adapters[i]
    counter[diff] += 1

logging.info(f'3-diff * 1-diff: {counter[1] * counter[3]}')

seq_start = 0
num_paths = 1
for i in range(len(adapters)-1):
    diff = adapters[i+1] - adapters[i]

    if diff == 3:
        seq_length = i - seq_start + 1
        if seq_length > 2:
            num_paths *= count_paths(adapters[seq_start:i+1])

        logging.debug(f'{i - seq_start + 1}: {adapters[seq_start:i+1]} => {count_paths(adapters[seq_start:i+1])}')
        seq_start = i+1

logging.info(f'Num Paths: {num_paths}')
