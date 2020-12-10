import argparse
import logging
import re

from dataclasses import dataclass
from operator import xor

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


# Helper classes

@dataclass
class SimplePasswordPolicy:
    required_char: str
    min_occurrences: int
    max_occurrences: int

    def __init__(self, raw_policy: str):
        regex_matches = re.match(r'([0-9]+)-([0-9]+) ([a-z])', raw_policy)
        self.min_occurrences = int(regex_matches.group(1))
        self.max_occurrences = int(regex_matches.group(2))
        self.required_char = regex_matches.group(3)

    def validate(self, password):
        char_count = password.count(self.required_char)
        return (char_count >= self.min_occurrences) and (char_count <= self.max_occurrences)


@dataclass
class BetterPasswordPolicy:
    required_char: str
    first_position: int
    second_position: int

    def __init__(self, raw_policy: str):
        regex_matches = re.match(r'([0-9]+)-([0-9]+) ([a-z])', raw_policy)
        self.first_position = int(regex_matches.group(1)) - 1
        self.second_position = int(regex_matches.group(2)) - 1
        self.required_char = regex_matches.group(3)

    def validate(self, password):
        logging.debug((password[self.first_position], password[self.second_position]))
        return xor(password[self.first_position] == self.required_char, password[self.second_position] == self.required_char)


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
        logging.info(f'Found invalid entry: {xmas_sequence[i]}')
        break
