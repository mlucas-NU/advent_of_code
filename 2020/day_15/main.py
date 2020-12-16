import argparse
import logging

from typing import List

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

class MemoryGame:

    def __init__(self, starting_sequence: List[int]):
        self.previous_value = starting_sequence[-1]
        self.previous_index = len(starting_sequence) - 1

        self.memory = {}
        for i, value in enumerate(starting_sequence[:-1]):
            self.memory[value] = i

    def find_nth_number(self, n):
        for i in range(self.previous_index, n - 1):
            age = self.memory.get(self.previous_value)
            if age is None:
                next_value = 0
            else:
                next_value = i - age
            self.memory[self.previous_value] = i
            self.previous_value = next_value

        return self.previous_value


# Load Inputs

input_file = args.input_file
with open(input_file) as f:
    starting_sequence = list(map(int, f.read().strip().split(',')))

# Main Logic

game = MemoryGame(starting_sequence)
final_value = game.find_nth_number(2020)
logging.info(f'2020th value: {final_value}')

game = MemoryGame(starting_sequence)
final_value = game.find_nth_number(30000000)
logging.info(f'2020th value: {final_value}')
