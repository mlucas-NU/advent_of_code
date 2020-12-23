import argparse
import logging
import re

from collections import defaultdict
from copy import deepcopy
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


# Helper class

class IngredientAnalyzer:

    def __init__(self, raw_lists: List[str]):
        self.allergen_candidates = {}
        self.ingredient_counts = defaultdict(int)
        for ingredient_list in raw_lists:
            match = re.match(r'(.*) \(contains (.*)\)', ingredient_list)

            ingredients = match.group(1).split(' ')
            allergens = match.group(2).split(', ')

            for ingredient in ingredients:
                self.ingredient_counts[ingredient] += 1

            for allergen in allergens:
                candidates = self.allergen_candidates.get(allergen)
                if candidates is None:
                    self.allergen_candidates[allergen] = set(ingredients)
                else:
                    candidates.intersection_update(set(ingredients))

    def count_safe_ingredients(self):
        possible_allergens = set().union(*self.allergen_candidates.values())

        safe_ingredient_count = 0
        for ingredient, count in self.ingredient_counts.items():
            if ingredient not in possible_allergens:
                safe_ingredient_count += count

        return safe_ingredient_count

    def get_dangerous_ingredients(self):
        allergen_candidates = deepcopy(self.allergen_candidates)

        decoded_allergens = {}
        while len(allergen_candidates) > 0:
            for allergen, candidates in allergen_candidates.items():
                assert len(candidates) > 0, f'Allergen {allergen} has no remaining candidates'
                if len(candidates) == 1:
                    ingredient = candidates.pop()
                    decoded_allergens[allergen] = ingredient

                    del allergen_candidates[allergen]
                    for c in allergen_candidates.values():
                        c.discard(ingredient)

                    break
            else:
                raise ValueError(f'Cannot resolve any allergens: {allergen_candidates}')

        sorted_allergens = sorted(list(self.allergen_candidates.keys()))
        sorted_ingredients = [decoded_allergens[allergen] for allergen in sorted_allergens]

        return ','.join(sorted_ingredients)


# Load Inputs

input_file = args.input_file
with open(input_file) as f:
    raw_lists = f.readlines()

# Main Logic

analyzer = IngredientAnalyzer(raw_lists)
count = analyzer.count_safe_ingredients()
logging.info(f'Part 1: {count}')

dangerous_ingredients = analyzer.get_dangerous_ingredients()
logging.info(f'Part 1: {dangerous_ingredients}')
