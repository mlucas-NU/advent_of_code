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
class OrbitalResult:
    you_depth: int
    san_depth: int
    total_depth: int


@dataclass
class DAGNode:

    def __post_init__(self):
        self.children = dict()

    def get_total_orbits(self, depth: int) -> int:
        total_orbits = depth

        logging.debug(f'[Depth {depth}] Child Names: {self.children.keys()}')
        for child in self.children.values():
            total_orbits += child.get_total_orbits(depth+1)

        return total_orbits

    def santa_orbital_distance(self) -> OrbitalResult:
        logging.debug(f'Orbital Child Names: {self.children.keys()}')
        if len(self.children) == 0:
            return OrbitalResult(-1, -1, -1)  # Found nothing
        if 'SAN' in self.children.keys():
            return OrbitalResult(-1, 0, -1)   # Found Santa
        if 'YOU' in self.children.keys():
            return OrbitalResult(0, -1, -1)   # Found Myself (whew)

        # No obvious answers, but we can check children for information
        santa_distance = -1
        you_distance = -1
        for child_name, child in self.children.items():
            result = child.santa_orbital_distance()
            logging.debug(f'\t{child_name} -> {result}')

            # If final answer was known by child, just pass along
            if result.total_depth > -1:
                return result

            # We're the next orbit along the Santa path
            if result.san_depth > -1:
                santa_distance = result.san_depth + 1

            # We're the next orbit along the me path
            if result.you_depth > -1:
                you_distance = result.you_depth + 1

        # If we're the first to be on both paths, return sum as result
        if santa_distance > -1 and you_distance > -1:
            return OrbitalResult(-1, -1, santa_distance + you_distance)
        else:
            # Otherwise, just pass as much info as we know
            return OrbitalResult(you_distance, santa_distance, -1)


@dataclass
class DAG:

    def __post_init__(self):
        self.roots = dict()
        self.nodes = dict()

    def add_orbit(self, name_1, name_2):
        # If orbited planet is new, create it
        if name_1 not in self.nodes.keys():
            logging.debug(f'Creating root "{name_1}"')
            planet_1 = DAGNode()
            self.nodes[name_1] = planet_1

            # New orbited planet must become a DAG root
            self.roots[name_1] = planet_1
        else:
            logging.debug(f'Existing planet "{name_1}"')
            planet_1 = self.nodes[name_1]

        # If orbiting planet is new, create it
        if name_2 not in self.nodes.keys():
            logging.debug(f'Creating orbiter "{name_2}"')
            planet_2 = DAGNode()
            self.nodes[name_2] = planet_2
        else:
            logging.debug(f'Existing orbiter "{name_2}"')
            planet_2 = self.nodes[name_2]

            # Orbiting planet can no longer be a root
            self.roots.pop(name_2, None)

        planet_1.children[name_2] = planet_2

    def total_orbits(self) -> int:
        total_orbits = 0

        for root in planet_dag.roots.values():
            total_orbits += root.get_total_orbits(0)

        return total_orbits

    def santa_orbital_distance(self) -> int:
        assert 'SAN' in self.nodes.keys()
        assert 'YOU' in self.nodes.keys()

        orbital_result = list(self.roots.values())[0].santa_orbital_distance()

        return orbital_result.total_depth


# Load Inputs

planet_dag = DAG()
input_file = args.input_file
with open(input_file) as f:
    for line in f.read().splitlines():
        logging.debug(line)
        planet_1, planet_2 = line.split(')')

        planet_dag.add_orbit(planet_1, planet_2)


# Main Logic

logging.debug(f'Root names: {planet_dag.roots.keys()}')
total_orbits = planet_dag.total_orbits()
logging.info(f'Total: {total_orbits}')
santa_distance = planet_dag.santa_orbital_distance()
logging.info(f'Orbital_distance: {santa_distance}')
