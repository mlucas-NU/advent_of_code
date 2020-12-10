import argparse
import logging


# Parse Arguments

parser = argparse.ArgumentParser()
parser.add_argument('map_file', help='input file containing slope map')
parser.add_argument('directions_file', help='input file containing x_step, y_step pairs for navigating')
parser.add_argument('--verbosity', help='specify verbosity level (DEBUG|INFO)')
args = parser.parse_args()

verbosity = 'INFO'
if args.verbosity:
    verbosity = args.verbosity
logging.getLogger().setLevel(logging.getLevelName(verbosity))


# Helper functions

def traverse_map(travel_map, x_step, y_step):
    x_position = 0
    num_trees = 0

    for row in travel_map[y_step::y_step]:
        x_position = (x_position + x_step) % len(row)

        if row[x_position] == '#':
            num_trees += 1

    return num_trees


# Load Inputs

travel_map = []
map_file = args.map_file
with open(map_file) as f:
    for line in f.readlines():
        travel_map.append(list(line[:-1]))

assert len(set(map(len, travel_map))) == 1, 'All lines in the input file should have the same length.'

directions = []
directions_file = args.directions_file
with open(directions_file) as f:
    for line in f.readlines():
        directions.append(map(int, line.split(' ')))

# Main Logic - Part 1

tree_product = 1
for x_step, y_step in directions:

    num_trees = traverse_map(travel_map, x_step, y_step)
    logging.info(f'Num Trees: {num_trees}')

    tree_product *= num_trees

logging.info(f'Product of all counts: {tree_product}')
