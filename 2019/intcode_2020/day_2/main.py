import argparse
import logging
import sys

from dataclasses import dataclass

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
class IntcodeComputer:
    program: list

    def __post_init__(self):
        self.reset_registers()

        self.opcode_map = {
            1: self.add,
            2: self.mul
        }

    def copy(self):
        return IntcodeComputer(self.program.copy())

    def reset_registers(self):
        self.inst = 0

    def read(self, program_index):
        return self.program[program_index]

    def write(self, program_index, value):
        self.program[program_index] = value

    def run(self):
        self.reset_registers()

        while self.program[self.inst] != 99:
            logging.debug(self.program)
            self.step()
        logging.debug(self.program)

    def step(self):
        # Look up function name via opcode_map
        func = self.opcode_map[self.program[self.inst]]
        func()

    def add(self):
        # Resolve parameters
        var1_index = self.program[self.inst + 1]
        var1 = self.program[var1_index]

        var2_index = self.program[self.inst + 2]
        var2 = self.program[var2_index]

        dest_index = self.program[self.inst + 3]

        # Execute function
        self.program[dest_index] = var1 + var2

        self.inst += 4

    def mul(self):
        # Resolve parameters
        var1_index = self.program[self.inst + 1]
        var1 = self.program[var1_index]

        var2_index = self.program[self.inst + 2]
        var2 = self.program[var2_index]

        dest_index = self.program[self.inst + 3]

        # Execute function
        self.program[dest_index] = var1 * var2

        self.inst += 4


# Load Inputs

input_lines = []
input_file = args.input_file
with open(input_file) as f:
    program = list(map(int, f.read().split(',')))

# Main Logic

computer = IntcodeComputer(program)

new_computer = computer.copy()
new_computer.run()
logging.info(f'Unmodified result: {new_computer.read(0)}')

if verbosity == 'DEBUG':
    sys.exit()

target_value = 19690720
logging.info(f'Trying to produce {target_value}')

for i in range(100):
    for j in range(100):
        new_computer = computer.copy()

        new_computer.write(1, i)
        new_computer.write(2, j)
        new_computer.run()

        if new_computer.read(0) == target_value:
            logging.info(f'Found. Final result: {100 * i + j}')
            break
    if new_computer.read(0) == target_value:
        break
else:
    logging.info('Not found.')
