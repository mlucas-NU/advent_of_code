import argparse
import logging


# Parse Arguments

parser = argparse.ArgumentParser()
parser.add_argument('input_file', help='input file to read')
parser.add_argument('--verbosity', help='specify verbosity level (DEBUG|INFO)')
args = parser.parse_args()

verbosity = 'INFO'
if args.verbosity:
    verbosity = args.verbosity
    print(f'verbosity: {verbosity}')
logging.getLogger().setLevel(logging.getLevelName(verbosity))


# Helper Functions

def calc_fuel(mass):
    return max(0, int(mass / 3) - 2)


# Load Inputs

input_file = args.input_file
with open(input_file) as f:
    masses = map(float, f.readlines())

# Main Logic

basic_total = 0
advanced_total = 0
for mass in masses:
    logging.debug(f'New Load Mass: {mass}')

    basic_fuel_req = calc_fuel(mass)
    logging.debug(f'\tBasic Fuel Req: {basic_fuel_req}')

    unfueled_mass = basic_fuel_req
    adv_fuel_req = basic_fuel_req
    while unfueled_mass > 0:
        unfueled_mass = calc_fuel(unfueled_mass)
        adv_fuel_req += unfueled_mass

    logging.debug(f'\tAdv. Fuel Req: {adv_fuel_req}')

    basic_total += basic_fuel_req
    advanced_total += adv_fuel_req

logging.info(f'Basic Total Fuel: {basic_total}')
logging.info(f'Adv. Total Fuel: {advanced_total}')
