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
class PAParser:
    commands: List[str]

    def __post_init__(self):
        self.orientation = 0    # Point East (value is Degrees counter-clockwise from Due East)
        self.position = [0, 0]  # Begin at origin
        self.waypoint = [10, 1]

    def follow_commands(self):
        for command in self.commands:
            action = command[0]
            value = int(command[1:])

            if action == 'N':    # Move north by the given value.
                self.position[1] += value
            elif action == 'S':  # Move south by the given value.
                self.position[1] -= value
            elif action == 'E':  # Move east by the given value.
                self.position[0] += value
            elif action == 'W':  # Move west by the given value.
                self.position[0] -= value
            elif action == 'L':  # Turn left the given number of degrees.
                self.orientation = (self.orientation + value) % 360
            elif action == 'R':  # Turn right the given number of degrees.
                self.orientation = (self.orientation - value) % 360
            elif action == 'F':  # Move forward by the given value in the direction the ship is currently facing.
                if self.orientation == 0:  # East
                    self.position[0] += value
                elif self.orientation == 90:  # North
                    self.position[1] += value
                elif self.orientation == 180:  # West
                    self.position[0] -= value
                elif self.orientation == 270:  # South
                    self.position[1] -= value
                else:
                    raise ValueError(f'Haven\'t accounted for non-cardinal directions yet: {self.orientation}')

            else:
                raise ValueError(f'Unknown action: {action}')

    def follow_waypoint(self):
        for command in self.commands:
            action = command[0]
            value = int(command[1:])
            logging.debug((self.position, self.waypoint))

            if action == 'N':    # Move waypoint north by the given value.
                self.waypoint[1] += value
            elif action == 'S':  # Move waypoint south by the given value.
                self.waypoint[1] -= value
            elif action == 'E':  # Move waypoint east by the given value.
                self.waypoint[0] += value
            elif action == 'W':  # Move waypoint west by the given value.
                self.waypoint[0] -= value
            elif action == 'L':  # Rotate waypoint left the given number of degrees.
                if value == 0:
                    pass
                elif value == 90:
                    self.waypoint = [-self.waypoint[1], self.waypoint[0]]
                elif value == 180:
                    self.waypoint = [-self.waypoint[0], -self.waypoint[1]]
                elif value == 270:
                    self.waypoint = [self.waypoint[1], -self.waypoint[0]]
                else:
                    raise ValueError(f'Haven\'t accounted for non-cardinal directions yet: {self.orientation}')
            elif action == 'R':  # Rotate waypoint right the given number of degrees.
                if value == 0:
                    pass
                elif value == 90:
                    self.waypoint = [self.waypoint[1], -self.waypoint[0]]
                elif value == 180:
                    self.waypoint = [-self.waypoint[0], -self.waypoint[1]]
                elif value == 270:
                    self.waypoint = [-self.waypoint[1], self.waypoint[0]]
                else:
                    raise ValueError(f'Haven\'t accounted for non-cardinal directions yet: {self.orientation}')
            elif action == 'F':  # Move to waypoint, repeat as many times as {value}
                self.position[0] += value * self.waypoint[0]
                self.position[1] += value * self.waypoint[1]
            else:
                raise ValueError(f'Unknown action: {action}')
        logging.debug((self.position, self.waypoint))


# Load Inputs

input_commands = []
input_file = args.input_file
with open(input_file) as f:
    for line in f.readlines():
        input_commands.append(line.strip())

# Main Logic

parser = PAParser(input_commands)
parser.follow_commands()
logging.info(f'Hamming Distance from origin: {sum(map(abs, parser.position))}')

parser = PAParser(input_commands)
parser.follow_waypoint()
logging.info(f'Hamming Distance from origin: {sum(map(abs, parser.position))}')
