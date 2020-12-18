import argparse
import itertools
import logging

from collections import defaultdict

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

class Life:

    def __init__(self, raw_grid: str, num_extra_dimensions: int):
        self.active_cubes = set()
        for y, line in enumerate(raw_grid.splitlines()):
            for x, state in enumerate(line.strip()):
                if state == '#':
                    self.active_cubes.add((x, y) + (0,) * num_extra_dimensions)

        self.num_dimensions = 2 + num_extra_dimensions
        logging.debug(self.num_dimensions)

    def run(self, num_steps):
        for i in range(num_steps):
            self.step()

        return len(self.active_cubes)

    def step(self):
        num_active_neighbors = defaultdict(int)
        for cube in self.active_cubes:
            neighbor_offsets = []
            for value in cube:
                neighbor_offsets.append((value - 1, value, value + 1))

            for neighbor in itertools.product(*neighbor_offsets):
                if neighbor == cube:
                    continue
                num_active_neighbors[neighbor] += 1

        updated_active_cubes = set()
        for cube, count in num_active_neighbors.items():
            if count == 3:
                updated_active_cubes.add(cube)
            elif cube in self.active_cubes and count == 2:
                updated_active_cubes.add(cube)

        self.active_cubes = updated_active_cubes

    def debug_print(self):
        ranges = []
        for i in range(self.num_dimensions):
            dimension_values = [x[i] for x in self.active_cubes]
            min_val = min(dimension_values)
            max_val = max(dimension_values)

            ranges.append((min_val, max_val + 1))

        for z in range(*ranges[2]):
            logging.debug(f'z={z}')
            for y in range(*ranges[1]):
                row = ''
                for x in range(*ranges[0]):
                    if (x, y, z) in self.active_cubes:
                        row += '#'
                    else:
                        row += '.'
                logging.debug(row)
            logging.debug('')


# Load Inputs

input_file = args.input_file
with open(input_file) as f:
    raw_grid = f.read()

# Main Logic

life = Life(raw_grid, 1)
num_active = life.run(6)
logging.info(f'# Active after 6 steps: {num_active}')

life = Life(raw_grid, 2)
num_active = life.run(6)
logging.info(f'# Active after 6 steps: {num_active}')
