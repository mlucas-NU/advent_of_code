from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Computer:
    program: List[int]
    queued_inputs: Optional[List[int]]
    interactive: bool = False

    def __post_init__(self):
        self.reset_registers()

        if self.interactive:
            self.opcode_map = {
                1: self._add,
                2: self._mul,
                3: self._interactive_input,
                4: self._interactive_output,
                5: self._jump_if_true,
                6: self._jump_if_false,
                7: self._less_than,
                8: self._equals
            }
        else:
            self.opcode_map = {
                1: self._add,
                2: self._mul,
                3: self._read_input,
                4: self._output,
                5: self._jump_if_true,
                6: self._jump_if_false,
                7: self._less_than,
                8: self._equals
            }

    def copy(self):
        return Computer(self.program.copy())

    def enqueue_input(self, value):
        self.queued_inputs.insert(0, value)

    def reset_registers(self):
        self.inst = 0

    def read(self, program_index):
        return self.program[program_index]

    def write(self, program_index, value):
        self.program[program_index] = value

    def run(self):
        while self.program[self.inst] % 100 != 99:
            output = self.step()
            if output is not None:
                yield output
        import logging
        logging.debug('all done!')

    def step(self):
        # Look up function name via opcode_map
        opcode = self.program[self.inst] % 100
        mode = int(str(int(self.program[self.inst] / 100)), 2)

        func = self.opcode_map[opcode]
        import logging
        logging.debug(f'{func.__name__} @ {self.inst}')
        return func(mode)

    # Opcode Functions

    def _add(self, mode):
        # Resolve parameters
        if mode & 0b01:  # Immediate
            var1 = self.program[self.inst + 1]
        else:            # Relative (pointer)
            var1_index = self.program[self.inst + 1]
            var1 = self.program[var1_index]

        if mode & 0b10:  # Immediate
            var2 = self.program[self.inst + 2]
        else:            # Relative (pointer)
            var2_index = self.program[self.inst + 2]
            var2 = self.program[var2_index]

        dest_index = self.program[self.inst + 3]

        # Execute function
        self.program[dest_index] = var1 + var2

        self.inst += 4

    def _mul(self, mode):
        # Resolve parameters
        if mode & 0b01:  # Immediate
            var1 = self.program[self.inst + 1]
        else:            # Relative (pointer)
            var1_index = self.program[self.inst + 1]
            var1 = self.program[var1_index]

        if mode & 0b10:  # Immediate
            var2 = self.program[self.inst + 2]
        else:            # Relative (pointer)
            var2_index = self.program[self.inst + 2]
            var2 = self.program[var2_index]

        dest_index = self.program[self.inst + 3]

        # Execute function
        self.program[dest_index] = var1 * var2

        self.inst += 4

    def _read_input(self, mode):
        # Resolve parameters
        dest_index = self.program[self.inst + 1]

        # Execute function
        import logging
        logging.debug(f'Reading input, got: {self.queued_inputs[-1]}')
        self.program[dest_index] = self.queued_inputs.pop()

        self.inst += 2

    def _output(self, mode):
        # Resolve parameters
        if mode & 0b01:  # Immediate
            var1 = self.program[self.inst + 1]
        else:            # Relative (pointer)
            var1_index = self.program[self.inst + 1]
            var1 = self.program[var1_index]

        self.inst += 2

        # Execute function
        return var1

    def _interactive_input(self, mode):
        # Resolve parameters
        dest_index = self.program[self.inst + 1]

        # Execute function
        self.program[dest_index] = int(input('Gimme a number!'))

        self.inst += 2

    def _interactive_output(self, mode):
        # Resolve parameters
        if mode & 0b01:  # Immediate
            var1 = self.program[self.inst + 1]
        else:            # Relative (pointer)
            var1_index = self.program[self.inst + 1]
            var1 = self.program[var1_index]

        # Execute function
        print(var1)

        self.inst += 2

    def _jump_if_true(self, mode):
        # Resolve parameters
        if mode & 0b01:  # Immediate
            var1 = self.program[self.inst + 1]
        else:            # Relative (pointer)
            var1_index = self.program[self.inst + 1]
            var1 = self.program[var1_index]

        if mode & 0b10:  # Immediate
            var2 = self.program[self.inst + 2]
        else:            # Relative (pointer)
            var2_index = self.program[self.inst + 2]
            var2 = self.program[var2_index]

        # Execute function
        if var1 != 0:
            self.inst = var2
        else:
            self.inst += 3

    def _jump_if_false(self, mode):
        # Resolve parameters
        if mode & 0b01:  # Immediate
            var1 = self.program[self.inst + 1]
        else:            # Relative (pointer)
            var1_index = self.program[self.inst + 1]
            var1 = self.program[var1_index]

        if mode & 0b10:  # Immediate
            var2 = self.program[self.inst + 2]
        else:            # Relative (pointer)
            var2_index = self.program[self.inst + 2]
            var2 = self.program[var2_index]

        # Execute function
        if var1 == 0:
            self.inst = var2
        else:
            self.inst += 3

    def _less_than(self, mode):
        # Resolve parameters
        if mode & 0b01:  # Immediate
            var1 = self.program[self.inst + 1]
        else:            # Relative (pointer)
            var1_index = self.program[self.inst + 1]
            var1 = self.program[var1_index]

        if mode & 0b10:  # Immediate
            var2 = self.program[self.inst + 2]
        else:            # Relative (pointer)
            var2_index = self.program[self.inst + 2]
            var2 = self.program[var2_index]

        dest_index = self.program[self.inst + 3]

        # Execute function
        if var1 < var2:
            self.program[dest_index] = 1
        else:
            self.program[dest_index] = 0

        self.inst += 4

    def _equals(self, mode):
        # Resolve parameters
        if mode & 0b01:  # Immediate
            var1 = self.program[self.inst + 1]
        else:            # Relative (pointer)
            var1_index = self.program[self.inst + 1]
            var1 = self.program[var1_index]

        if mode & 0b10:  # Immediate
            var2 = self.program[self.inst + 2]
        else:            # Relative (pointer)
            var2_index = self.program[self.inst + 2]
            var2 = self.program[var2_index]

        dest_index = self.program[self.inst + 3]

        # Execute function
        if var1 == var2:
            self.program[dest_index] = 1
        else:
            self.program[dest_index] = 0

        self.inst += 4
