import argparse
import copy
import logging
import math

from collections import defaultdict
from dataclasses import dataclass
from typing import List, Tuple


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
class AsteroidMap:
    asteroid_indices: List[List[int]]

    def optimize_location(self) -> Tuple[List[int], int]:
        asteroids = copy.deepcopy(self.asteroid_indices)

        most_angles = 0
        for i, candidate in enumerate(asteroids):
            unique_angles = set()
            for j, other in enumerate(asteroids):
                if i == j:
                    continue
                x_dist = candidate[0] - other[0]
                y_dist = candidate[1] - other[1]
                unique_angles.add(math.atan2(y_dist, x_dist))

            if len(unique_angles) > most_angles:
                best_location = candidate
                most_angles = len(unique_angles)

        return best_location, most_angles

    def destroy_n(self, station_coords: List[int], n: int) -> List[int]:
        angle_map = defaultdict(list)

        # Aggregate asteroids by angle
        for other in self.asteroid_indices:
            if other == station_coords:
                continue
            x_dist = - station_coords[0] + other[0]
            y_dist = - station_coords[1] + other[1]
            angle = math.atan2(x_dist, y_dist) + math.pi

            angle_map[angle].append(other)

        # Shortcut: we can identify how many full 360's need to be completed by
        #   counting (n) how many angles have at least k planets. By iterating
        #   over values of k = 1, 2, 3... and summing n until the next
        #   iteration would surpass 200, we can limit any rotation logic to the
        #   final iteration.
        total_destroyed = 0
        for depth in range(0, 200):
            matching_angles = []

            # TODO: Don't double-check so much, consider sorting
            for angle, planets in angle_map.items():
                if len(planets) > depth:
                    matching_angles.append(angle)

            if total_destroyed + len(matching_angles) >= 200:
                break

            total_destroyed += len(matching_angles)

        matching_angles = sorted(list(matching_angles), reverse=True)

        final_angle = matching_angles[n - 1 - total_destroyed]
        print(angle_map[final_angle])
        logging.debug(f'Final Angle: {final_angle}')

        logging.debug(total_destroyed)
        logging.debug(len(matching_angles))


# Load Inputs

input_file = args.input_file
with open(input_file) as f:

    asteroids = []
    for y, line in enumerate(f.readlines()):
        for x, char in enumerate(line):
            if char == '#':
                asteroids.append([x, y])

# Main Logic

asteroid_map = AsteroidMap(asteroids)
best_location, most_angles = asteroid_map.optimize_location()
logging.info(f'Best Location: {best_location}')
logging.info(f'Asteroids Detected: {most_angles}')

coords = asteroid_map.destroy_n(best_location, 200)
logging.info(f'200th destroyed asteroid: {coords}')
