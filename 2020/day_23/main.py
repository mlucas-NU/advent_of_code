from __future__ import annotations

import argparse
import logging
import tqdm

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
class Cup:
    label: int
    prev: Cup = None
    next: Cup = None


class CupGame:
    def __init__(self, cup_labels: List[int]):
        self.current_cup = Cup(cup_labels[0])
        self.cup_index = {cup_labels[0]: self.current_cup}

        previous_cup = self.current_cup
        for label in cup_labels[1:]:
            cup = Cup(label, previous_cup, None)
            cup.prev.next = cup
            self.cup_index[label] = cup

            previous_cup = cup

        cup.next = self.current_cup
        self.current_cup.prev = cup

    def play(self, num_rounds: int) -> int:
        largest_cup = max(self.cup_index.keys())
        for i in tqdm.trange(num_rounds):
            start_cup = self.current_cup.next
            end_cup = start_cup.next.next

            invalid_cups = {self.current_cup.label, start_cup.label, start_cup.next.label, end_cup.label}
            target_cup = self.current_cup.label - 1

            if target_cup == 0:
                target_cup = largest_cup
            while target_cup in invalid_cups:
                target_cup -= 1
                if target_cup == 0:
                    target_cup = largest_cup

            target_cup = self.cup_index[target_cup]

            # Close gap between current_cup and end_cup.next
            self.current_cup.next = end_cup.next
            end_cup.next.prev = self.current_cup

            # Insert moved cups after target_cup
            target_cup.next.prev = end_cup
            end_cup.next = target_cup.next

            target_cup.next = start_cup
            start_cup.prev = target_cup

            self.current_cup = self.current_cup.next

    def concat_after_1(self) -> str:
        result = ''
        cup = self.cup_index[1].next
        while cup.label != 1:
            result += str(cup.label)
            cup = cup.next

        return result

    def multiply_2_cups_after_1(self) -> str:
        cup1 = self.cup_index[1].next
        cup2 = cup1.next

        return cup1.label * cup2.label


# Load Inputs

input_file = args.input_file
with open(input_file) as f:
    raw_state = f.read()
cup_labels = list(map(int, raw_state[:-1]))

# Main Logic

game = CupGame(cup_labels.copy())
game.play(100)
final_state = game.concat_after_1()
logging.info(f'State after 100 rounds: {final_state}')

game = CupGame(cup_labels.copy() + list(range(10, 10**6+1)))
game.play(10**7)
final_state = game.multiply_2_cups_after_1()
logging.info(f'State after 100 rounds: {final_state}')
