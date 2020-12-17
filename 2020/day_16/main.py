import argparse
import logging
import pandas as pd
import re

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

class TicketScanner:

    def __init__(self, raw_input: str):
        regex_pattern = re.compile('(.*)\n\nyour ticket:\n(.*)\n\nnearby tickets:\n(.*)', re.MULTILINE | re.DOTALL)
        regex_matches = re.match(regex_pattern, raw_input)

        self.rules = {}
        for rule in regex_matches.group(1).splitlines():
            rule_matches = re.match(r'([^:]+): ([0-9]+)-([0-9]+) or ([0-9]+)-([0-9]+)', rule)

            rule_name = rule_matches.group(1)
            range1_start = int(rule_matches.group(2))
            range1_end = int(rule_matches.group(3))
            range2_start = int(rule_matches.group(4))
            range2_end = int(rule_matches.group(5))

            self.rules[rule_name] = [(range1_start, range1_end), (range2_start, range2_end)]

        self.my_ticket = [int(x) for x in regex_matches.group(2).split(',')]

        self.tickets = []
        for ticket in regex_matches.group(3).splitlines():
            self.tickets.append([int(x) for x in ticket.split(',')])

        logging.debug(f'Rules: {self.rules}')
        logging.debug(f'My ticket: {self.my_ticket}')
        logging.debug(f'Nearby: {self.tickets}')

    def calc_error_rate(self):
        error_rate = 0
        for ticket in self.tickets:
            for value in ticket:
                if not self._is_valid_value(value):
                    error_rate += value

        return error_rate

    def discard_invalid_tickets(self):
        valid_tickets = []
        for ticket in self.tickets:
            for value in ticket:
                if not self._is_valid_value(value):
                    break
            else:
                valid_tickets.append(ticket)

        self.tickets = valid_tickets

    def _is_valid_value(self, value):
        # Return true if valid for at least one column
        for rule in self.rules.values():
            if (value >= rule[0][0] and value <= rule[0][1]) or (value >= rule[1][0] and value <= rule[1][1]):
                return True

        return False

    def align_fields(self):
        valid_values_df = {}
        for rule_name, rule in self.rules.items():
            # Find columns where rule is always followed
            valid_columns = []
            for column_index in range(len(self.my_ticket)):
                for ticket in self.tickets:
                    value = ticket[column_index]
                    if (value < rule[0][0] or value > rule[0][1]) and (value < rule[1][0] or value > rule[1][1]):
                        valid_columns.append(0)  # invalid, end early
                        break
                else:
                    valid_columns.append(1)      # valid (no invalid columns found)

            valid_values_df[rule_name] = valid_columns

        valid_values_df = pd.DataFrame(valid_values_df)
        rule_assignments = {}
        while valid_values_df.shape[0] > 0:
            # Select any rule that only has 1 matching column
            column_counts = valid_values_df.sum()
            next_rule = column_counts[column_counts == column_counts.min()].sample(1).index[0]
            column_index = valid_values_df.index[valid_values_df[next_rule].argmax()]

            # Remove it from dataframe and assign it to correct column
            valid_values_df = valid_values_df.drop(column_index, axis=0).drop(next_rule, axis=1)
            rule_assignments[next_rule] = column_index

        final_result = 1
        for rule, column_index in rule_assignments.items():
            if rule.startswith('departure'):
                final_result *= self.my_ticket[column_index]

        return final_result


# Load Inputs

input_file = args.input_file
with open(input_file) as f:
    raw_input = f.read()

# Main Logic

scanner = TicketScanner(raw_input)
error_rate = scanner.calc_error_rate()
logging.info(f'Error Rate: {error_rate}')

scanner.discard_invalid_tickets()
logging.debug(f'Valid tickets: {scanner.tickets}')

alignment_result = scanner.align_fields()
logging.info(f'Alignment result: {alignment_result}')
