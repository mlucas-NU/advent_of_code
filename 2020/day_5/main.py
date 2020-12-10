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


# Load Inputs

boarding_passes = []
input_file = args.input_file
with open(input_file) as f:
    for line in f.readlines():
        boarding_passes.append(line[:-1])

# Main Logic

seat_ids = []
for boarding_pass in boarding_passes:
    boarding_pass = boarding_pass.translate(str.maketrans('BFLR', '1001'))
    seat_ids.append(int(boarding_pass, 2))

logging.info(f'Highest Seat ID: {max(seat_ids)}')

seat_ids.sort()
for i in range(len(seat_ids)):
    if seat_ids[i] != seat_ids[i+1] - 1:
        logging.info(f'My Seat ID is between: {seat_ids[i]} and {seat_ids[i+1]}')
        break
