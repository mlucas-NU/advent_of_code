import argparse
import logging

from dataclasses import dataclass
from typing import List

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

@dataclass
class BusSchedule:
    start_time: int
    routes: List[int]

    def find_earliest(self):
        earliest = None
        earliest_route = None

        for route in self.routes:
            try:
                route = int(route)
            except ValueError:
                continue

            arrival = route - (self.start_time % route)
            logging.debug(f'Route {route} arrives in {arrival} minutes')
            if earliest is None or arrival < earliest:
                earliest = arrival
                earliest_route = route

        return earliest * earliest_route

    def solve_contest(self):
        routes = [int(x) for x in self.routes if x != 'x']
        offsets = [i for i, x in enumerate(self.routes) if x != 'x']

        candidate = routes[0]
        for i in range(1, len(routes)):
            while (candidate + offsets[i]) % routes[i] != 0:
                increment = 1
                for route in routes[:i]:
                    increment *= route
                candidate += increment

        return candidate


# Load Inputs

input_file = args.input_file
with open(input_file) as f:
    start_time = int(f.readline())
    routes = f.read().strip().split(',')

# Main Logic

schedule = BusSchedule(start_time, routes)
result = schedule.find_earliest()
logging.info(f'Part 1 answer: {result}')

result = schedule.solve_contest()
logging.info(f'Part w answer: {result}')
