import argparse
import logging

from itertools import permutations

from parser import Parser

# Parse Arguments

parser = argparse.ArgumentParser()
parser.add_argument('input_file', help='input file to read')
parser.add_argument('circuit', help='circuit type (basic|looping)')
parser.add_argument('--verbosity', help='specify verbosity level (DEBUG|INFO)')
args = parser.parse_args()

verbosity = 'INFO'
if args.verbosity:
    verbosity = args.verbosity
logging.getLogger().setLevel(logging.getLevelName(verbosity))


# Helper Functions

def basic_circuit(program):
    best_output = -1
    best_setting = -1
    for phase_setting in permutations(range(5)):
        prev_output = 0
        for setting in phase_setting:
            inputs = [setting, prev_output]
            logging.debug(f'Running with inputs: {inputs}')

            parser = Parser(program, inputs)
            simulated_outputs = parser.run()
            logging.debug(f'outputs: {simulated_outputs}')

            assert len(simulated_outputs) == 1
            prev_output = simulated_outputs[0]

        if prev_output > best_output:
            phase_str = ''.join(map(str, phase_setting))
            logging.info(f' >> {phase_str, prev_output}')
            best_output = prev_output
            best_setting = phase_str

    logging.info(f'Best Output: {best_output}')
    logging.info(f'Best Phase Setting: {best_setting}')


def looping_circuit(program):
    best_output = -1
    best_setting = -1
    for phase_setting in permutations(range(5, 10)):
        phase_setting = [9, 7, 8, 5, 6]
        # Build Circuit
        circuit = [Parser(program, [setting]) for setting in phase_setting]

        # Loop through circuit until it stops
        prev_output = 0
        while True:
            for index, program in enumerate(circuit):
                program.simulated_inputs.append(prev_output)
                logging.debug(f'P[{index}] inputs: {program.simulated_inputs}')

                prev_output = next(program.run(), None)
                logging.debug(f'output: {prev_output}')
                if prev_output is None:
                    break

            if prev_output is None:
                break

            if prev_output > best_output:
                phase_str = ''.join(map(str, phase_setting))
                logging.info(f' >> {phase_str, prev_output}')
                best_output = prev_output
                best_setting = phase_str

        break

    logging.info(f'Best Output: {best_output}')
    logging.info(f'Best Phase Setting: {best_setting}')


# Load Inputs

input_file = args.input_file
with open(input_file) as f:
    values = f.read()[:-1].split(',')
    program = list(map(int, values))


# Main Logic

if args.circuit == 'basic':
    basic_circuit(program)
elif args.circuit == 'looping':
    looping_circuit(program)
else:
    raise ValueError('circuit parameter must be either "basic" or "looping"')
