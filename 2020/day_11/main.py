import argparse
import logging

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
class Seating:

    def __init__(self, raw_layout: str):
        self.layout = [list(row) for row in raw_layout.strip().split('\n')]
        self.num_rows = len(self.layout)
        self.num_cols = len(self.layout[0])

    def count_assigned_seats(self):
        num_assigned = 0
        for row in self.layout:
            for seat in row:
                if seat == '#':
                    num_assigned += 1
        return num_assigned

    def assign_seats_adjacency(self):
        while self._step_adjacency():
            pass

    def _step_adjacency(self):
        new_layout = []
        any_updates = False
        for i in range(self.num_rows):
            new_row = []
            for j in range(self.num_cols):
                seat_contents = self.layout[i][j]
                if seat_contents == '.':                          # Don't seat people on the floor
                    new_row.append('.')
                    continue
                num_neighbors = self._count_neighbors(i, j)

                if seat_contents == 'L' and num_neighbors == 0:   # Assign seat if it is empty and has no neighbors
                    new_row.append('#')
                    any_updates = True
                elif seat_contents == '#' and num_neighbors > 3:  # Remove assignment if passenger has > 3 neighbors
                    new_row.append('L')
                    any_updates = True
                else:
                    new_row.append(seat_contents)                 # Base case: leave seat unchanged
            new_layout.append(new_row)

        self.layout = new_layout

        return any_updates

    def _count_neighbors(self, row_id, column_id):
        num_neighbors = 0

        for i in range(max(0, row_id - 1), min(self.num_rows, row_id + 2)):
            for j in range(max(0, column_id - 1), min(self.num_cols, column_id + 2)):
                # logging.info((row_id, column_id, i, j, self.num_rows, self.num_cols))
                if i == row_id and j == column_id:
                    continue

                if self.layout[i][j] == '#':
                    num_neighbors += 1

        return num_neighbors

    def assign_seats_eyesight(self):
        while self._step_eyesight():
            pass

    def _step_eyesight(self):
        new_layout = []
        any_updates = False
        for i in range(self.num_rows):
            new_row = []
            for j in range(self.num_cols):
                seat_contents = self.layout[i][j]
                if seat_contents == '.':                          # Don't seat people on the floor
                    new_row.append('.')
                    continue
                num_neighbors = self._count_visible(i, j)

                if seat_contents == 'L' and num_neighbors == 0:   # Assign seat if it is empty and has no neighbors
                    new_row.append('#')
                    any_updates = True
                elif seat_contents == '#' and num_neighbors > 4:  # Remove assignment if passenger has > 4 visible neighbors
                    new_row.append('L')
                    any_updates = True
                else:
                    new_row.append(seat_contents)                 # Base case: leave seat unchanged
            new_layout.append(new_row)

        self.layout = new_layout

        return any_updates

    def _count_visible(self, row_id, column_id):
        num_neighbors = 0

        for direction in [[-1,-1], [-1,0], [-1,1], [0,-1], [0,1], [1,-1], [1,0], [1,1]]:  # noqa E231
            position = [row_id + direction[0], column_id + direction[1]]

            while position[0] >= 0 and position[0] < self.num_rows and position[1] >= 0 and position[1] < self.num_cols:
                # logging.debug(f'{direction} {position} {self.layout[position[0]][position[1]]}')

                if self.layout[position[0]][position[1]] == '#':
                    num_neighbors += 1
                    break
                elif self.layout[position[0]][position[1]] == 'L':
                    break

                position[0] += direction[0]
                position[1] += direction[1]

        return num_neighbors


# Load Inputs

input_file = args.input_file
with open(input_file) as f:
    raw_layout = f.read()

# Main Logic

seating = Seating(raw_layout)
seating.assign_seats_adjacency()
num_assigned_seats = seating.count_assigned_seats()
logging.info(f'Num seats assigned (adjacency): {num_assigned_seats}')

seating = Seating(raw_layout)
seating.assign_seats_eyesight()
num_assigned_seats = seating.count_assigned_seats()
logging.info(f'Num seats assigned (vision): {num_assigned_seats}')
