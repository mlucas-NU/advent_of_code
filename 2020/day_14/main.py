import argparse
import logging
import re

from itertools import combinations

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

def run_script_v1(script):
    memory = {}
    for instruction in script:
        if instruction.startswith('mask'):
            matches = re.match(r'^mask = ([01X]{36})$', instruction)
            raw_mask = matches.group(1)

            mask = raw_mask.replace('1', '0').replace('X', '1')
            default_value = raw_mask.replace('X', '0')

            # Convert to integer from binary string
            mask = int(mask, 2)
            default_value = int(default_value, 2)

            logging.debug(f'[v1] Raw Mask: {raw_mask} -> mask {mask}; default_value {default_value}')

        elif instruction.startswith('mem'):
            matches = re.match(r'^mem\[([0-9]+)\] = ([0-9]+)$', instruction)
            memory_index, new_value = matches.groups()

            memory[memory_index] = (int(new_value) & mask) + default_value

            logging.debug(f'[v1] New value: mem[{memory_index}] = {new_value} + mask = {(int(new_value) & mask) + default_value}')

        else:
            raise ValueError(f'Unsure how to process line: {instruction}')

    logging.debug(f'[v1] End state memory {memory}')
    return sum(memory.values())


def run_script_v2(script):
    memory = {}
    for instruction in script:
        if instruction.startswith('mask'):
            matches = re.match(r'^mask = ([01X]{36})$', instruction)
            raw_mask = matches.group(1)

            mask = raw_mask.replace('1', '0').replace('X', '1')
            mask = int(mask, 2)

            default_index = raw_mask.replace('X', '0')
            default_index = int(default_index, 2)

            floating_offsets = sorted(generate_floating_offsets(raw_mask))

            logging.debug(f'[v2] Raw Mask: {raw_mask} -> mask {mask}; floating_offsets {floating_offsets}')

        elif instruction.startswith('mem'):
            matches = re.match(r'^mem\[([0-9]+)\] = ([0-9]+)$', instruction)
            memory_index, new_value = map(int, matches.groups())

            memory_index = (memory_index & ~mask) | default_index
            logging.debug(f'[v2] New value. Base mem: {memory_index}')
            for offset in floating_offsets:
                memory[memory_index + offset] = new_value
                logging.debug(f'    mem[{memory_index + offset}] = {new_value}')

        else:
            raise ValueError(f'Unsure how to process line: {instruction}')

    logging.debug(f'[v2] End state memory {memory}')
    return sum(memory.values())


def generate_floating_offsets(raw_mask):
    floating_indices = [len(raw_mask) - char.start() - 1 for char in re.finditer('X', raw_mask)]
    floating_offsets = [2**x for x in floating_indices]

    # Sum all possible combinations of floating_offsets
    all_offsets = []
    for num_offsets in range(len(floating_offsets) + 1):
        for combo in combinations(floating_offsets, num_offsets):
            all_offsets.append(sum(combo))

    return all_offsets


# Load Inputs

input_file = args.input_file
with open(input_file) as f:
    script = f.read().splitlines()

# Main Logic

v1_result = run_script_v1(script)
logging.info(f'v1 memory sum: {v1_result}')

v2_result = run_script_v2(script)
logging.info(f'v2 memory sum: {v2_result}')
