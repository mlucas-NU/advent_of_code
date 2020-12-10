import argparse
import logging
import re

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

# Load Inputs

rules = {}
input_file = args.input_file
with open(input_file) as f:
    for line in f.readlines():
        match = re.match(r'(.*) bags contain (.*)', line)
        container, contents = match.groups()

        if contents == 'no other bags.':
            rules[container] = set()
        else:
            internal_bags = set()
            while len(contents) > 0:
                match = re.match(r'\s*([0-9]+) ([^,\.]*) bags?[,\.](.*)', contents)
                count, color, contents = match.groups()

                internal_bags.add((color, int(count)))

            rules[container] = internal_bags

# Main Logic

count = 0
for start_color in rules.keys():
    open_set = {start_color}
    closed_set = set()

    while len(open_set) > 0:
        key = open_set.pop()

        for new_key, _ in rules[key]:
            if new_key != key and new_key not in closed_set:
                open_set.add(new_key)

        closed_set.add(key)

        if 'shiny gold' in open_set:
            count += 1
            break

logging.info(f'Bags containing shiny gold: {count}')

open_set = defaultdict(int)
open_set['shiny gold'] = 1
total = 0
while len(open_set) > 0:
    key, count = open_set.popitem()
    total += count

    logging.debug((key, count))
    logging.debug(f'Rule: {rules[key]}')
    for new_key, new_count in rules[key]:
        open_set[new_key] += count * new_count


logging.info(f'1 Shiny Gold contains {total - 1} bags')
