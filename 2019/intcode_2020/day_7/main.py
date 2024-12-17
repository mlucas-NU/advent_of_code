import argparse
import logging

from itertools import permutations

from intcodes import Computer

# Parse Arguments

parser = argparse.ArgumentParser()
parser.add_argument('input_file', help='input file to read')
parser.add_argument('--verbosity', help='specify verbosity level (DEBUG|INFO)')
args = parser.parse_args()

verbosity = 'INFO'
if args.verbosity:
    verbosity = args.verbosity
logging.getLogger().setLevel(logging.getLevelName(verbosity))


# Helper functions

def basic_circuit(program):
    best_output = -1
    best_setting = -1
    for phase_setting in permutations(range(5)):
        prev_output = 0
        for setting in phase_setting:
            inputs = [prev_output, setting]

            parser = Computer(program, inputs)
            prev_output = next(parser.run(), None)

        if prev_output > best_output:
            phase_str = ''.join(map(str, phase_setting))
            logging.debug(f' >> {phase_str, prev_output}')
            best_output = prev_output
            best_setting = phase_str

    logging.info(f'Best Output: {best_output}')
    logging.info(f'Best Phase Setting: {best_setting}')


def looping_circuit(program):
    best_output = -1
    best_setting = -1
    for phase_setting in permutations(range(5, 10)):
        phase_setting = [9, 8, 7, 6, 5]
        # Build Circuit
        circuit = [Computer(program, [setting]) for setting in phase_setting]

        # Loop through circuit until it stops
        prev_output = 0
        while True:
            for index, computer in enumerate(circuit):
                computer.enqueue_input(prev_output)
                logging.debug(f'P[{index}] inputs: {computer.queued_inputs}')

                prev_output = next(computer.run(), None)
                logging.debug(f'output: {prev_output}')
                if prev_output is None:
                    break

            if prev_output is None:
                break

            if prev_output > best_output:
                phase_str = ''.join(map(str, phase_setting))
                logging.debug(f' >> {phase_str, prev_output}')
                best_output = prev_output
                best_setting = phase_str

        break

    logging.info(f'Best Output: {best_output}')
    logging.info(f'Best Phase Setting: {best_setting}')


# Load Inputs

input_file = args.input_file
with open(input_file) as f:
    values = f.read().split(',')
    program = list(map(int, values))

# Main Logic

basic_circuit(program)
looping_circuit(program)
