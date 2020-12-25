import argparse
import logging
import re

from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple

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
class HexGrid:
    black_tiles: Set = field(default_factory=set)
    offset_map: Dict = field(default_factory=lambda: {
        'e': (2, 0),
        'se': (1, -1),
        'sw': (-1, -1),
        'w': (-2, 0),
        'nw': (-1, 1),
        'ne': (1, 1)
    })

    def flip_paths(self, paths: List[str]) -> None:

        for raw_path in paths:
            path = re.findall(r'(e|se|sw|w|nw|ne)', raw_path)

            cur_tile = (0, 0)
            for direction in path:
                offset = self.offset_map[direction]
                cur_tile = (cur_tile[0] + offset[0], cur_tile[1] + offset[1])

            if cur_tile in self.black_tiles:
                self.black_tiles.remove(cur_tile)
            else:
                self.black_tiles.add(cur_tile)

    def run(self, num_days: int) -> None:
        for i in range(num_days):
            new_grid = set()
            for tile in self.black_tiles:
                if self.num_black_neighbors(tile) in {1, 2}:
                    new_grid.add(tile)

                for offset in self.offset_map.values():
                    adjacent_tile = (tile[0] + offset[0], tile[1] + offset[1])
                    if adjacent_tile in self.black_tiles:
                        continue

                    if self.num_black_neighbors(adjacent_tile) == 2:
                        new_grid.add(adjacent_tile)

            self.black_tiles = new_grid
            if (i < 10) or (i % 10 == 9):
                logging.debug(f'Day {i+1}: {len(self.black_tiles)}')

    def num_black_neighbors(self, tile: Tuple[int]) -> int:
        num_neighbors = 0
        for offset in self.offset_map.values():
            adjacent_tile = (tile[0] + offset[0], tile[1] + offset[1])
            if adjacent_tile in self.black_tiles:
                num_neighbors += 1

        return num_neighbors


# Load Inputs

input_file = args.input_file
with open(input_file) as f:
    paths = f.read().splitlines()

# Main Logic

grid = HexGrid()
grid.flip_paths(paths)
logging.info(f'Initial # Black Tiles: {len(grid.black_tiles)}')

grid.run(100)
logging.info(f'Final # Black Tiles: {len(grid.black_tiles)}')
