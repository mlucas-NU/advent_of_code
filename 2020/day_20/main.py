import argparse
import logging
import re

from collections import defaultdict
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

class Puzzle:

    def __init__(self, raw_puzzle: str):

        self.tiles = {}
        self.edge_map = defaultdict(set)

        tiles = raw_puzzle.split('\n\n')
        for raw_tile in tiles:
            regex_pattern = re.compile(r'Tile ([0-9]+):\n(.*)', re.MULTILINE | re.DOTALL)
            match = re.match(regex_pattern, raw_tile)
            tile_id = int(match.group(1))
            tile = match.group(2).splitlines()

            boundaries = self._parse_boundaries(tile)
            for boundary in boundaries:
                self.tiles[tile_id] = set(boundaries)
                self.edge_map[boundary].add(tile_id)

        self.num_edge_bits = len(tile[0])

    def get_corners(self) -> int:
        result = 1
        for tile, edges in self.tiles.items():
            outside_edges = 0
            for i, edge in enumerate(edges):
                if len(self.edge_map[edge]) + len(self.edge_map[self._reverse_edge(edge)]) == 1:
                    outside_edges += 1
            if outside_edges == 2:
                result *= tile

        return result

    def _parse_boundaries(self, tile: List[str]) -> List[int]:
        # Get boundaries, going clockwise
        boundary_strings = [
            tile[0],                                   # Top (left to right)
            ''.join([row[-1] for row in tile]),        # Right (top to bottom)
            tile[-1][::-1],                            # Bottom (right to left
            ''.join([row[0] for row in tile])[::-1]    # Left (bottom to top)
        ]

        return [int(s.replace('#', '1').replace('.', '0'), 2) for s in boundary_strings]

    def _reverse_edge(self, edge: int) -> int:
        binary_string = f'{edge:0{self.num_edge_bits}b}'
        return int(binary_string[::-1], 2)


# Load Inputs

input_file = args.input_file
with open(input_file) as f:
    raw_puzzle = f.read()

# Main Logic

puzzle = Puzzle(raw_puzzle)
corner_product = puzzle.get_corners()
logging.info(f'Part 1: {corner_product}')
