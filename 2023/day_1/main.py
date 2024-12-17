import argparse
import logging
import re

from dataclasses import dataclass

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
class SimpleExtractor:
    line: str

    def __init__(self, raw_line: str):
        self.line = raw_line

    def get_calibration_value(self):
        numeric_characters = ''.join(c for c in self.line if c.isnumeric())
        return int(numeric_characters[0] + numeric_characters[-1])


@dataclass
class ComplexExtractor:
    line: str

    def __init__(self, raw_line: str):
        line_map = {
            'one': '1',
            'two': '2',
            'three': '3',
            'four': '4',
            'five': '5',
            'six': '6',
            'seven': '7',
            'eight': '8',
            'nine': '9'
        }
        re_pattern = re.compile(r'(one|two|three|four|five|six|seven|eight|nine)')

        line = raw_line
        match = re_pattern.search(line)
        while match is not None:
            span = match.span()
            line = line[:span[0]] + line_map[match.group()] + line[span[1]:]
            match = re_pattern.search(line)
        logging.debug(f'{raw_line} => {line}')
        self.line = line

    def get_calibration_value(self):
        numeric_characters = ''.join(c for c in self.line if c.isnumeric())
        return int(numeric_characters[0] + numeric_characters[-1])


# Load Inputs

input_lines = []
input_file = args.input_file
with open(input_file) as f:
    for line in f.readlines():
        assert re.match(r'^[0-9a-z]+$', line) is not None
        input_lines.append(line[:-1])

# Main Logic

logging.debug('SimpleExtractor')
simple_total = 0
for line in input_lines:
    simple_extractor = SimpleExtractor(line)
    try:
        simple_total += simple_extractor.get_calibration_value()
    except IndexError:
        logging.debug(f'ERROR: Could not parse integers from {simple_extractor.line}')

logging.debug('ComplexExtractor')
complex_total = 0
for line in input_lines:
    complex_extractor = ComplexExtractor(line)
    try:
        complex_total += complex_extractor.get_calibration_value()
    except IndexError:
        logging.debug(f'ERROR: Could not parse integers from {complex_extractor.line}')
    complex_total += complex_extractor.get_calibration_value()

logging.info(f'Simple sum: {simple_total}')
logging.info(f'Complex sum: {complex_total}')
