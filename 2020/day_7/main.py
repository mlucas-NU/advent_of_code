import argparse
import logging
import re

from dataclasses import dataclass
from operator import xor

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

input_lines = []
input_file = args.input_file
with open(input_file) as f:
    for line in f.readlines():
        assert re.match(r'^[0-9]+-[0-9]+ [a-z]: [a-z]+$', line) is not None
        input_lines.append(line[:-1])

# Main Logic

num_valid_simple_passwords = 0
num_valid_better_passwords = 0

for line in input_lines:
    raw_policy, password = line.split(': ')

    simple_policy = SimplePasswordPolicy(raw_policy)
    if simple_policy.validate(password):
        num_valid_simple_passwords += 1

    better_policy = BetterPasswordPolicy(raw_policy)
    if better_policy.validate(password):
        num_valid_better_passwords += 1

    if verbosity == 'DEBUG':
        logging.debug(f'{raw_policy}: {password} => Simple={simple_policy.validate(password)}, Better={better_policy.validate(password)}')


logging.info(f'Num Valid Simple Passwords: {num_valid_simple_passwords}')
logging.info(f'Num Valid Better Passwords: {num_valid_better_passwords}')
