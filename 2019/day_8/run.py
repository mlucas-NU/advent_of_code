import argparse
import logging

from collections import Counter
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
class Image:
    width: int
    height: int
    raw_image: List[int]

    display_charmap = {
        0: ' ',
        1: '█',
        2: '▓',
    }

    def __post_init__(self):
        logging.debug(f'Parsing raw image of length {len(raw_image)}')

        self.layers = []
        for i in range(0, len(self.raw_image), self.width * self.height):
            raw_layer = self.raw_image[i:i + self.width * self.height]

            layer = []
            for j in range(0, len(raw_layer), self.width):
                layer.append(raw_layer[j:j + self.width])

            self.layers.append(layer)

    def validate_image(self):
        least_zeroes = float('inf')
        best_product = -1

        for index, layer in enumerate(self.layers):
            logging.debug(f'Layer {index}')
            counter = Counter()
            for row in layer:
                counter.update(row)
                logging.debug((''.join(map(str, row)), counter))

            if counter[0] < least_zeroes:
                least_zeroes = counter[0]
                best_product = counter[1] * counter[2]
                logging.debug(f'New best product: {best_product}')

        return best_product

    def display(self):
        output = [[2 for i in range(self.width)] for j in range(self.height)]

        for layer in self.layers:
            for y, row in enumerate(layer):
                for x, pane in enumerate(row):
                    if output[y][x] == 2 and pane < 2:
                        output[y][x] = pane

        for row in output:
            print(''.join(map(self._color_map, row)))

    # Helper function to map colors from dict (cannot call map on a dict)
    def _color_map(self, color_key):
        return self.display_charmap[color_key]


# Load Inputs

input_file = args.input_file
with open(input_file) as f:
    file_contents = f.read()[:-1]
    width, height, raw_image = file_contents.split(' ')
    width, height = int(width), int(height)
    raw_image = list(map(int, raw_image))


# Main Logic

image = Image(width, height, raw_image)
best_product = image.validate_image()
logging.info(f'Validation: {best_product}')
image.display()
