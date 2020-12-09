from __future__ import annotations  # Enable self-referential type hinting of a class within its own functions  # noqa E501

import argparse
import logging
import sys

from dataclasses import dataclass
from typing import Dict, List, Tuple


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

class WireSpan:
    __dir_map = {
        'L': (-1, 0),
        'R': (1, 0),
        'D': (0, -1),
        'U': (0, 1)
    }

    def __init__(self, input_string: str):
        self.direction = self.__dir_map[input_string[0]]
        self.length = int(input_string[1:])


@dataclass
class BoundaryCoords:
    x_min: int
    x_max: int
    y_min: int
    y_max: int


@dataclass
class Circuit:
    boundary: BoundaryCoords

    circuit: List[List[str]] = None
    wire_length_cache: Dict[str, List[List[int]]] = None

    def __post_init__(self):
        self.circuit = self._generate_empty_circuit()
        self.wire_length_cache = dict()

    def _generate_empty_circuit(self) -> List[List[str]]:  # noqa E501
        circuit = []
        for j in range(self.boundary.y_max - self.boundary.y_min + 1):
            circuit.append([' ' for i in range(self.boundary.x_max - self.boundary.x_min + 1)])  # noqa E501b

        return circuit

    def draw_wire(
        self,
        wire: List[WireSpan],
        icon: str,
        x_min: int,
        y_min: int
    ) -> List[Tuple[int]]:
        # Draws wire and returns coordinates of collisions with other wires

        # Shift origin by x_min and y_min
        x = -boundary.x_min
        y = -boundary.y_min

        # Store a circuit containing number of steps taken to each position
        length_cache = self._generate_empty_circuit()

        # Remember collision locations for returning
        collisions = []

        position = 0
        for span in wire:
            for _ in range(span.length):
                x += span.direction[0]
                y += span.direction[1]
                position += 1

                if self.circuit[y][x] != ' ' and self.circuit[y][x] != icon:
                    collisions.append((x + x_min, y + y_min))
                self.circuit[y][x] = icon

                if length_cache[y][x] == ' ':
                    length_cache[y][x] = position
            # print_circuit(self.circuit)

        self.wire_length_cache[icon] = length_cache
        return collisions


# Helper Functions

def parse_wire(line: str) -> List[WireSpan]:
    spans = line.split(',')
    spans = list(map(WireSpan, spans))
    return spans


def get_boundaries(wires: Tuple[List[WireSpan]]) -> BoundaryCoords:
    x_min = x_max = y_min = y_max = 0

    for wire in wires:
        x = y = 0
        for span in wire:
            x += span.direction[0] * span.length
            y += span.direction[1] * span.length
            logging.debug(f'Boundary: {(x, y)}')

            x_min = min(x_min, x)
            x_max = max(x_max, x)
            y_min = min(y_min, y)
            y_max = max(y_max, y)

    return BoundaryCoords(x_min, x_max, y_min, y_max)


def print_circuit(circuit: List[List[int]]) -> None:
    for row in circuit:
        for value in row:
            print(value, end='')
        print('')  # Endline between rows
    print('')      # Extra endline after circuits


def find_nearest_distance(collisions: List[tuple]) -> int:
    nearest_distance = float('inf')

    for coords in collisions:
        manhattan_distance = sum(map(abs, coords))
        nearest_distance = min(nearest_distance, manhattan_distance)

    return nearest_distance


def find_shortest_walk(collisions: List[tuple], circuit: Circuit) -> int:
    shortest_walk = float('inf')

    for coords in collisions:
        total_walk = 0
        for icon, length_cache in circuit.wire_length_cache.items():
            walk_length = length_cache[coords[1] - circuit.boundary.y_min][coords[0] - circuit.boundary.x_min]  # noqa E501
            total_walk += walk_length
            logging.debug(icon, walk_length)

        shortest_walk = min(total_walk, shortest_walk)

    return shortest_walk


# Load Inputs

input_file = args.input_file
with open(input_file) as f:
    wire_pairs = []

    for line in f:
        wire_1 = parse_wire(line)
        wire_2 = parse_wire(next(f))

        wire_pairs.append((wire_1, wire_2))


# Main Logic

for wire_1, wire_2 in wire_pairs:
    boundary = get_boundaries((wire_1, wire_2))
    logging.debug(boundary)

    circuit = Circuit(boundary)

    try:
        collisions = circuit.draw_wire(
            wire_1,
            'A',
            boundary.x_min,
            boundary.y_min
        )
        assert collisions == []
        collisions = circuit.draw_wire(
            wire_2,
            'B',
            boundary.x_min,
            boundary.y_min
        )
        logging.debug(f'Collisions: {collisions}')
    except IndexError:
        logging.exception('Failed to write wires.')
        sys.exit(1)

    # print_circuit(circuit.wire_length_cache['A'])
    # print_circuit(circuit.wire_length_cache['B'])

    nearest_distance = find_nearest_distance(collisions)
    shortest_walk = find_shortest_walk(collisions, circuit)
    logging.info(f'Nearest point (manhattan distance): {nearest_distance}')
    logging.info(f'Shortest walk: {shortest_walk}')
