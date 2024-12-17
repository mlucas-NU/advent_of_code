import argparse
import logging
import re

# Parse Arguments

parser = argparse.ArgumentParser()
parser.add_argument('input_file', help='input file to read')
parser.add_argument('output_file', help='output file to write grammar (.ebnf file)')
parser.add_argument('--verbosity', help='specify verbosity level (DEBUG|INFO)')
args = parser.parse_args()

verbosity = 'INFO'
if args.verbosity:
    verbosity = args.verbosity
logging.getLogger().setLevel(logging.getLevelName(verbosity))


# Load Inputs

regex_pattern = re.compile(r'(.*)\n\n.*', re.MULTILINE | re.DOTALL)
input_file = args.input_file
with open(input_file) as f:
    match = re.match(regex_pattern, f.read())
raw_rules = match.group(1).splitlines()


# Main Logic

grammar_rules = []
for rule in raw_rules:
    rule = re.sub(r'(\d+)', r'rule_\1', rule)
    key, expression = rule.split(': ')
    grammar_rules.append([key, expression])
grammar_rules.sort()

output_file = args.output_file
with open(output_file, 'w') as f:
    f.write('@@grammar::Monster\n\n')
    f.write('start = rule_0 $;\n')

    for key, expression in grammar_rules:
        f.write(f'{key} = {expression};\n')
