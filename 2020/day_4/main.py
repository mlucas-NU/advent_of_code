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
class Passport:
    byr: str
    iyr: str
    eyr: str
    hgt: str
    hcl: str
    ecl: str
    pid: str

    def __init__(self, raw_passport: str):
        for pair in re.compile('\s+').split(raw_passport):  # noqa W605
            field, value = pair.split(':')
            setattr(self, field, value)

    def is_valid(self) -> bool:
        required_fields = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}

        if not required_fields.issubset(dir(self)):
            return False

        try:
            # byr (Birth Year) - four digits; at least 1920 and at most 2002.
            if int(self.byr) < 1920 or int(self.byr) > 2002:
                return False

            # iyr (Issue Year) - four digits; at least 2010 and at most 2020.
            if int(self.iyr) < 2010 or int(self.iyr) > 2020:
                return False

            # eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
            if int(self.eyr) < 2020 or int(self.eyr) > 2030:
                return False

            # hgt (Height) - a number followed by either cm or in:
            # If cm, the number must be at least 150 and at most 193.
            # If in, the number must be at least 59 and at most 76.
            if self.hgt[-2:] == 'cm':
                if int(self.hgt[:-2]) < 150 or int(self.hgt[:-2]) > 193:
                    return False
            elif self.hgt[-2:] == 'in':
                if int(self.hgt[:-2]) < 59 or int(self.hgt[:-2]) > 76:
                    return False
            else:
                return False

            # hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
            if re.match(r'^\#[0-9a-f]{6}$', self.hcl) is None:
                return False

            # ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
            if self.ecl not in {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}:
                return False

            # pid (Passport ID) - a nine-digit number, including leading zeroes.
            if re.match(r'^[0-9]{9}$', self.pid) is None:
                return False

            # cid (Country ID) - ignored, missing or not.

        except Exception:
            return False

        return True


# Load Inputs

input_file = args.input_file
with open(input_file) as f:
    raw_passports = f.read()

raw_passports = re.compile('\n{2,}').split(raw_passports.strip())
passports = [Passport(p) for p in raw_passports]

# Main Logic

num_valid = 0
for passport in passports:
    if passport.is_valid():
        num_valid += 1

logging.info(f'Num Valid: {num_valid}')
