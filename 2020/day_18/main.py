import argparse
import logging
import re

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
class StackCalculator:
    input_expressions: List[str]

    def run(self) -> int:
        total = 0
        for expression in self.input_expressions:
            self.stack = []

            # logging.debug(f' >>> {expression}')
            for token in re.findall('[0-9]+|[+*()]', expression):
                # logging.debug(f'{self.stack} {token}')
                if token in {'+', '*', '('}:
                    self.stack.append(token)
                elif token == ')':
                    # Close parentheses -- resolve internal value and one existing operation, if it exists
                    assert self.stack[-2] == '(', f'Stack should have an open paren at index -2: {self.stack}'
                    self.stack.pop(-2)

                    self._single_calculation()
                    self._single_calculation()
                elif token.isdigit():
                    # Integer -- push to stack and resolve one existing operation, if it exists (if not, assume we're at the front of the stack)
                    self.stack.append(int(token))
                    self._single_calculation()
                else:
                    raise ValueError(f'unknown: {expression} => {token}')

            assert len(self.stack) == 1, f'Stack should only have 1 value: {self.stack}'
            total += self.stack[0]

        return total

    def _single_calculation(self):
        if len(self.stack) < 3 or '(' in self.stack[-3:]:
            return

        param1 = self.stack.pop()
        operation = self.stack.pop()
        param2 = self.stack.pop()

        if operation == '+':
            self.stack.append(param1 + param2)
        elif operation == '*':
            self.stack.append(param1 * param2)
        else:
            raise ValueError(f'Weird stack: {self.stack + [param2, operation, param1]}')


@dataclass
class ReduceCalculator:
    input_expressions: List[str]

    def run(self) -> int:
        total = 0

        for expression in self.input_expressions:
            result = self._reduce(expression)
            logging.debug(f'{expression} => {result}')

            total += result

        return total

    def _reduce(self, expression: str) -> int:
        # Resolve all statements with parentheses (recursion, but only max-depth 1)
        paren_pattern = re.compile(r'(.*)\(([^()]+)\)(.*)')

        match = re.search(paren_pattern, expression)
        while match is not None:
            result = self._reduce(match.group(2))
            expression = f'{match.group(1)}{result}{match.group(3)}'

            match = re.search(paren_pattern, expression)

        # Resolve all additions
        add_pattern = re.compile(r'(.*?)([0-9]+) \+ ([0-9]+)(.*)')

        match = re.search(add_pattern, expression)
        while match is not None:
            result = int(match.group(2)) + int(match.group(3))
            expression = f'{match.group(1)}{result}{match.group(4)}'

            match = re.search(add_pattern, expression)

        # Resolve all multipllications
        mult_pattern = re.compile(r'(.*?)([0-9]+) \* ([0-9]+)(.*)')

        match = re.search(mult_pattern, expression)
        while match is not None:
            result = int(match.group(2)) * int(match.group(3))
            expression = f'{match.group(1)}{result}{match.group(4)}'

            match = re.search(mult_pattern, expression)

        return int(expression)


# Load Inputs

input_file = args.input_file
with open(input_file) as f:
    input_expressions = f.read().splitlines()

# Main Logic

calculator = StackCalculator(input_expressions)
result = calculator.run()
logging.info(f'Part 1: {result}')

calculator = ReduceCalculator(input_expressions)
result = calculator.run()
logging.info(f'Part 2: {result}')
