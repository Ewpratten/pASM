# This file handles Instructions

from dataclasses import dataclass
from typing import List
from .argument import Argument
from ..errors import addWarning, addError


@dataclass
class Instruction:

    mnemonic: str
    binary: int
    expected_args: int
    args: List[Argument]

    def assemble(self) -> List[int]:

        # Handle errors
        if len(self.args != self.expected_args):
            addError(
                f"Instruction: {self.mnemonic} ! Expected {self.expected_args} args, got {len(self.args)}")

        output = []

        output.append(self.binary)
        for arg in self.args:
            output += arg.assemble()

        return output