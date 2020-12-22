import argparse
import logging
import re
import uuid

from dataclasses import dataclass, field
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
class CombatGame:

    player1: List[int] = field(default_factory=list)
    player2: List[int] = field(default_factory=list)

    def __post_init__(self):
        self.identity = str(uuid.uuid4())[:8]

    def load_raw_input(self, raw_input: str) -> None:
        regex_pattern = re.compile(r'Player 1:\n([0-9\n]+)\n\nPlayer 2:\n([0-9\n]+)', re.MULTILINE | re.DOTALL)
        match = re.match(regex_pattern, raw_input)

        self.player1 = list(map(int, match.group(1).splitlines()))
        self.player2 = list(map(int, match.group(2).splitlines()))

    def play_simple(self) -> int:
        while len(self.player1) > 0 and len(self.player2) > 0:
            card1 = self.player1.pop(0)
            card2 = self.player2.pop(0)

            if card1 > card2:
                self.player1.extend([card1, card2])
            else:
                self.player2.extend([card2, card1])

        if len(self.player1) > 0:
            return self._calc_score(self.player1)
        return self._calc_score(self.player2)

    def play_recursive(self, log_prefix='') -> Tuple[int]:
        self.previous_states = set()
        while len(self.player1) > 0 and len(self.player2) > 0:
            # See if this is a previous state (base case -> winner is player 1)
            game_state = self._game_state()
            if game_state in self.previous_states:
                return (1, self._calc_score(self.player1))
            self.previous_states.add(game_state)

            # Continue game normally
            card1 = self.player1.pop(0)
            card2 = self.player2.pop(0)

            if len(self.player1) < card1 or len(self.player2) < card2:
                if card1 > card2:
                    self.player1.extend([card1, card2])
                else:
                    self.player2.extend([card2, card1])
            else:
                # When both hands are shorter than the number on the corresponding player's card, start a subgame
                subgame = CombatGame(self.player1[:card1], self.player2[:card2])
                winning_player, score = subgame.play_recursive(log_prefix + '. ')

                if winning_player == 1:
                    self.player1.extend([card1, card2])
                else:
                    self.player2.extend([card2, card1])

        if len(self.player1) > 0:
            return (1, self._calc_score(self.player1))
        return (2, self._calc_score(self.player2))

    def _game_state(self) -> int:
        hand1 = ' '.join(map(str, self.player1))
        hand2 = ' '.join(map(str, self.player2))

        return f'{hand1}_{hand2}'

    def _calc_score(self, winning_hand) -> int:
        score = 0
        for i, card in enumerate(winning_hand[::-1]):
            score += card * (i+1)

        return score


# Load Inputs

input_file = args.input_file
with open(input_file) as f:
    raw_input = f.read()

# Main Logic

game = CombatGame()
game.load_raw_input(raw_input)
final_score = game.play_simple()
logging.info(f'Part 1: {final_score}')

game.load_raw_input(raw_input)
winning_player, final_score = game.play_recursive()
logging.info(f'Part 2: {final_score}')
