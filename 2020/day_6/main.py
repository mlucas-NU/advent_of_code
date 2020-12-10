import argparse
import logging
import re

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

input_file = args.input_file
with open(input_file) as f:
    raw_groups = f.read()

raw_groups = re.compile('\n{2,}').split(raw_groups.strip())

# Main Logic

total_union_counts = 0
total_intersection_counts = 0
for group in raw_groups:
    customers = group.split('\n')

    union_answers = set(customers.pop())
    intersection_answers = union_answers.copy()
    for customer in customers:
        union_answers.update(customer)
        intersection_answers.intersection_update(customer)

    total_union_counts += len(union_answers)
    total_intersection_counts += len(intersection_answers)

logging.info(f'Sum of group union counts: {total_union_counts}')
logging.info(f'Sum of group intersection counts: {total_intersection_counts}')
