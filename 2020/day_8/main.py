import argparse
import logging

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

class Computer:

    def __init__(self, raw_program: str):
        self.instructions = raw_program.strip().split('\n')
        self.reset_registers()

    def reset_registers(self):
        self.inst = 0
        self.accumulator = 0

    def find_infinite_loop(self):
        self.reset_registers()

        visited_instructions = set()
        while self.inst not in visited_instructions:
            visited_instructions.add(self.inst)
            self.step()

            if self.inst >= len(self.instructions):
                break

    def step(self):
        # Parse command (e.g. 'nop +1', 'jmp -4')
        command, parameter = self.instructions[self.inst].split(' ')
        logging.debug(f'inst[{self.inst}]: {command} {parameter}')

        # Call self's function named by the given command
        func = getattr(self, command)
        func(parameter)

    def nop(self, _):
        self.inst += 1

    def acc(self, parameter):
        self.accumulator += int(parameter)
        self.inst += 1

    def jmp(self, parameter):
        self.inst += int(parameter)


# Load Inputs

input_file = args.input_file
with open(input_file) as f:
    computer = Computer(f.read())

# Main Logic

computer.find_infinite_loop()
logging.info(f'Loop found. Accumulator: {computer.accumulator}')

# Not sure whether we need to put much more time into this problem than
# hacking at the same Computer object. Would be worth a better solution
# if we need to reuse the Computer in similar ways in future challenges.
logging.info(f'# Instructions: {len(computer.instructions)}')
logging.debug('Program:\n  ' + '\n  '.join(computer.instructions))
for i in range(len(computer.instructions)):
    command, parameter = computer.instructions[i].split(' ')
    if command == 'jmp':
        logging.debug(f'Switching inst[{i}] from jmp -> nop')
        computer.instructions[i] = f'nop {parameter}'
        computer.find_infinite_loop()
        if computer.inst >= len(computer.instructions):
            break
        computer.instructions[i] = f'jmp {parameter}'
    elif command == 'nop':
        logging.debug(f'Switching inst[{i}] from nop -> jmp')
        computer.instructions[i] = f'jmp {parameter}'
        computer.find_infinite_loop()
        if computer.inst >= len(computer.instructions):
            break
        computer.instructions[i] = f'nop {parameter}'

logging.info(f'Loop fixed. Accumulator: {computer.accumulator}')
