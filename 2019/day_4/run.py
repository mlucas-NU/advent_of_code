import argparse
import logging


# Parse Arguments

parser = argparse.ArgumentParser()
parser.add_argument('start_value', type=int, help='Beginning of range to search')  # noqa E501
parser.add_argument('end_value', type=int, help='End of range to search')
parser.add_argument('--verbosity', type=str, help='specify verbosity level (DEBUG|INFO)')  # noqa E501
args = parser.parse_args()

verbosity = 'INFO'
if args.verbosity:
    verbosity = args.verbosity
logging.getLogger().setLevel(logging.getLevelName(verbosity))


# Helper Functions

def is_valid_simple(value):
    value_str = str(value)
    has_duplicates = False

    # Simultaneously hecks that entire value is monotonically increasing and
    # has at least one sequential pair of matching value
    for i in range(len(value_str) - 1):
        if value_str[i] > value_str[i+1]:
            return False
        if value_str[i] == value_str[i+1]:
            has_duplicates = True

    return has_duplicates


def is_valid_advanced(value):
    value_str = str(value)

    # Split out check for monotonicity
    for i in range(len(value_str) - 1):
        if value_str[i] > value_str[i+1]:
            return False

    # Check for at least one span of length 2
    span_start = 0
    while span_start < len(value_str):
        span_length = next((i for i, x in enumerate(value_str[span_start:]) if x != value_str[span_start]), len(value_str) - span_start)  # noqa E501

        if span_length == 2:
            return True
        span_start += span_length

    return False


def increment(value):
    value += 1
    value_str = str(value)

    # Scan left->right and overwrite all digits following first order issue
    # Example input:    13499 (ascending)
    # Incremented:      13500 (not ascending)
    # Correct (step 3): 13555 (ascending
    for i in range(len(value_str) - 1):
        if value_str[i] > value_str[i+1]:
            value_str = value_str[:i] + value_str[i] * (len(value_str) - i)
            value = int(value_str)
            break

    return value


# Main Logic

# 1. Increment (find next valid number quickly)
# 2. Check whether it matches the simple and advanced criteria (separately)
# 3. Print counts of simple and advanced matches
simple_count = advanced_count = 0
value = args.start_value
while value < args.end_value:
    if is_valid_simple(value):
        simple_count += 1
    if is_valid_advanced(value):
        advanced_count += 1
    value = increment(value)
    logging.debug(f'{value}: {is_valid_simple(value), is_valid_advanced(value)}')  # noqa E501

logging.info(f'Simple criteria: {simple_count}')
logging.info(f'Advanced criteria: {advanced_count}')
