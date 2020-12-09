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
    print(f'verbosity: {verbosity}')
logging.getLogger().setLevel(logging.getLevelName(verbosity))


# Helper Functions
def add(index, script):
    val_a = script[script[index+1]]
    val_b = script[script[index+2]]
    dest = script[index+3]

    script[dest] = val_a + val_b


def mul(index, script):
    val_a = script[script[index+1]]
    val_b = script[script[index+2]]
    dest = script[index+3]

    script[dest] = val_a * val_b


# Load Inputs

input_file = args.input_file
with open(input_file) as f:
    all_scripts = []
    for line in f:
        values = line.split(',')
        values = list(map(int, values))
        all_scripts.append(values)


# Main Logic

for script in all_scripts:
    index = 0
    logging.debug(f'Start: {script}')
    while script[index] != 99:
        if script[index] == 1:
            add(index, script)
        elif script[index] == 2:
            mul(index, script)
        else:
            logging.exception(f'Unknown op code {script[index]}')

        logging.debug(script)
        index += 4

    logging.debug(f'Final: {script}')
    logging.info(f'Answer: {script[0]}')
    logging.debug('')
