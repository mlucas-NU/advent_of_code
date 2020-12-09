import logging

from dataclasses import dataclass, field
from typing import List


@dataclass
class Parser:
    program: List[int]
    simulated_inputs: List[int]
    simulated_outputs: List[int] = field(default_factory=list)

    # Registers
    inst = 0  # Current Instruction pointer

    # Shortcut pointers to functions
    def __post_init__(self):
        self._function_map = {
            1: self._add,
            2: self._multiply,
            3: self._input,
            4: self._output,
            5: self._jump_if_true,
            6: self._jump_if_false,
            7: self._less_than,
            8: self._equals
        }

    # Main logic
    def run(self):
        while True:
            instruction = self.program[self.inst]
            opcode = instruction % 100
            mode = int(str(int(instruction / 100)), 2)

            if opcode == 99:
                logging.info('Exiting')
                return

            function = self._function_map[opcode]
            logging.debug(f'Function: {function.__name__} Mode: {mode}')

            output_val = function(mode)
            if output_val is not None:
                yield output_val
            # logging.debug(f'Program: {self.program}')

    # Arithmetic Operators
    def _add(self, mode):
        ''' Addition (Opcode 1)
        Write the sum of two numbers to a specific location of the program

        Mode: See documentation for resolving mode here: https://adventofcode.com/2019/day/5
          Here's the gist: It's a binary string, one value for each input and
          each bit determines whether the input value should be read as an
          immediate value (1) or as a reference to a location within the
          program (0)

        Inputs (following 3 positions in program):
            a: First number to add
            b: Second number to add
            dest: Index in the program to write sum to
        ''' # noqa E501

        # Get values to add
        if mode & 0b01:  # Immediate
            val_a = self.program[self.inst + 1]
        else:             # Relative (position)
            ptr_a = self.program[self.inst + 1]
            val_a = self.program[ptr_a]

        if mode & 0b10:  # Immediate
            val_b = self.program[self.inst + 2]
        else:             # Relative (position)
            ptr_b = self.program[self.inst + 2]
            val_b = self.program[ptr_b]

        # Get info of output
        ptr_dest = self.program[self.inst + 3]

        # Operation: Addition
        self.program[ptr_dest] = val_a + val_b

        # Update instruction pointer
        self.inst += 4

    def _multiply(self, mode):
        ''' Multipllication (Opcode 2)
        Write the sum of two numbers to a specific location of the program

        Mode: See documentation for resolving mode here: https://adventofcode.com/2019/day/5
          Here's the gist: It's a binary string, one value for each input and
          each bit determines whether the input value should be read as an
          immediate value (1) or as a reference to a location within the
          program (0)

        Inputs (following 3 positions in program):
            a: First number to multiply
            b: Second number to multiply
            dest: Index in the program to write product to
        ''' # noqa E501

        # Get values to add
        if mode & 0b01:  # Immediate
            val_a = self.program[self.inst + 1]
        else:             # Relative (position)
            ptr_a = self.program[self.inst + 1]
            val_a = self.program[ptr_a]

        if mode & 0b10:  # Immediate
            val_b = self.program[self.inst + 2]
        else:             # Relative (position)
            ptr_b = self.program[self.inst + 2]
            val_b = self.program[ptr_b]

        # Get index of output
        ptr_dest = self.program[self.inst + 3]

        # Operation: Multiplication
        self.program[ptr_dest] = val_a * val_b

        # Update instruction pointer
        self.inst += 4

    # Storage Operators
    def _input(self, mode):
        ''' Read user input (Opcode 3)
        Read user input and write to a specified program location 

        Mode: Ignored in this operator.

        Inputs (following 1 position):
            ptr_dest: index in memory to write the value read from input
        ''' # noqa E501

        if len(self.simulated_inputs) == 0:
            raise BufferError('No input available for reading.')

        # Get index of location to write value
        ptr_dest = self.program[self.inst + 1]

        # Operation: Read simulated user znput
        self.program[ptr_dest] = self.simulated_inputs.pop()

        # Update instruction pointer
        self.inst += 2

    def _output(self, mode):
        ''' Print value to console (Opcode 4)
        Read user input and write to a specified program location 

        Mode: Ignored in this operator.

        Inputs (following 1 position):
            ptr_dest: index in memory to retrieve and output to console
        ''' # noqa E501

        # Get index of value to output
        ptr_dest = self.program[self.inst + 1]

        # Update instruction pointer
        self.inst += 2

        # Operation: Output value to simulated console
        return self.program[ptr_dest]

    # Jump Operators
    def _jump_if_true(self, mode):
        ''' Jump if first parameter is not zero (Opcode 5)

        Mode: See documentation for resolving mode here: https://adventofcode.com/2019/day/5
          Here's the gist: It's a binary string, one value for each input and
          each bit determines whether the input value should be read as an
          immediate value (1) or as a reference to a location within the
          program (0)

        Inputs (following 3 positions in program):
            a: Value tested
            dest: Value to set Instruction Pointer to if a != 0
        ''' # noqa E501

        # Get values to test
        if mode & 0b01:  # Immediate
            val_a = self.program[self.inst + 1]
        else:             # Relative (position)
            ptr_a = self.program[self.inst + 1]
            val_a = self.program[ptr_a]

        # Get jump index
        if mode & 0b10:  # Immediate
            ptr_dest = self.program[self.inst + 2]
        else:             # Relative (position)
            ptr_dest = self.program[self.inst + 2]
            ptr_dest = self.program[ptr_dest]

        # Operation: Jump If True
        if val_a != 0:
            self.inst = ptr_dest
        else:
            self.inst += 3

    def _jump_if_false(self, mode):
        ''' Jump if first parameter is equal to zero (Opcode 6)

        Mode: See documentation for resolving mode here: https://adventofcode.com/2019/day/5
          Here's the gist: It's a binary string, one value for each input and
          each bit determines whether the input value should be read as an
          immediate value (1) or as a reference to a location within the
          program (0)

        Inputs (following 3 positions in program):
            a: Value tested
            dest: Value to set Instruction Pointer to if a == 0
        ''' # noqa E501

        # Get value to test
        if mode & 0b01:  # Immediate
            val_a = self.program[self.inst + 1]
        else:             # Relative (position)
            ptr_a = self.program[self.inst + 1]
            val_a = self.program[ptr_a]

        # Get jump index
        if mode & 0b10:  # Immediate
            ptr_dest = self.program[self.inst + 2]
        else:             # Relative (position)
            ptr_dest = self.program[self.inst + 2]
            ptr_dest = self.program[ptr_dest]

        # Operation: Jump If True
        if val_a == 0:
            self.inst = ptr_dest
        else:
            self.inst += 3

    # Comparison Operators
    def _less_than(self, mode):
        ''' Store whether first parameter is less than second (Opcode 7)

        Mode: See documentation for resolving mode here: https://adventofcode.com/2019/day/5
          Here's the gist: It's a binary string, one value for each input and
          each bit determines whether the input value should be read as an
          immediate value (1) or as a reference to a location within the
          program (0)

        Inputs (following 3 positions in program):
            a: Value tested
            b: Value tested
            dest: Value to set Instruction Pointer to if a < b
        ''' # noqa E501

        # Get values to compare
        if mode & 0b01:  # Immediate
            val_a = self.program[self.inst + 1]
        else:             # Relative (position)
            ptr_a = self.program[self.inst + 1]
            val_a = self.program[ptr_a]

        if mode & 0b10:  # Immediate
            val_b = self.program[self.inst + 2]
        else:             # Relative (position)
            ptr_b = self.program[self.inst + 2]
            val_b = self.program[ptr_b]

        # Get index of output
        ptr_dest = self.program[self.inst + 3]

        # Operation: Write result of a < b to dest
        self.program[ptr_dest] = int(val_a < val_b)
        self.inst += 4

    def _equals(self, mode):
        ''' Store whether first parameter is equal to second (Opcode 8)
        
        Mode: See documentation for resolving mode here: https://adventofcode.com/2019/day/5
          Here's the gist: It's a binary string, one value for each input and
          each bit determines whether the input value should be read as an
          immediate value (1) or as a reference to a location within the
          program (0)

        Inputs (following 3 positions in program):
            a: Value tested
            b: Value tested
            dest: Value to set Instruction Pointer to if a == b
        ''' # noqa E501

        # Get values to compare
        if mode & 0b01:  # Immediate
            val_a = self.program[self.inst + 1]
        else:             # Relative (position)
            ptr_a = self.program[self.inst + 1]
            val_a = self.program[ptr_a]

        if mode & 0b10:  # Immediate
            val_b = self.program[self.inst + 2]
        else:             # Relative (position)
            ptr_b = self.program[self.inst + 2]
            val_b = self.program[ptr_b]

        # Get index of output
        ptr_dest = self.program[self.inst + 3]

        # Operation: Write result of a == b to dest
        self.program[ptr_dest] = int(val_a == val_b)
        self.inst += 4
