import argparse
import logging

# Parse Arguments

parser = argparse.ArgumentParser()
parser.add_argument('input_file', help='input file to read')
parser.add_argument('preamble_length', help='Number of integers in preamble and sliding window for validation')
parser.add_argument('--verbosity', help='specify verbosity level (DEBUG|INFO)')
args = parser.parse_args()

verbosity = 'INFO'
if args.verbosity:
    verbosity = args.verbosity
logging.getLogger().setLevel(logging.getLevelName(verbosity))

# Load Inputs

xmas_sequence = []
input_file = args.input_file
with open(input_file) as f:
    for line in f.readlines():
        xmas_sequence.append(int(line))

# Main Logic

preamble_length = int(args.preamble_length)
for i in range(preamble_length, len(xmas_sequence)):

    window = set(xmas_sequence[i-preamble_length:i])
    for candidate in window:
        if xmas_sequence[i] - candidate in window:
            break
    else:
        invalid_entry = xmas_sequence[i]
        break

logging.info(f'Found invalid entry: {invalid_entry}')


start_index = 0
end_index = 0
total = 0
while total != invalid_entry:
    if total < invalid_entry:
        if end_index >= len(xmas_sequence):
            raise ValueError(f'Sequence doesn\'t have a valid span totaling {invalid_entry}')
        total += xmas_sequence[end_index]
        end_index += 1
    else:
        total -= xmas_sequence[start_index]
        start_index += 1

span = xmas_sequence[start_index:end_index]
result = min(span) + max(span)
logging.info(f'Found matching spam. Min + max = {result}')
