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
    args: List[Argument] = []

    def addArgument(self, arg: Argument) -> None:
        self.args.append(arg)

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


# Mapping of mnemonics to actual instructions
isa = {
    "nop": Instruction("nop", 0, 0),
    "mov": Instruction("mov", 1, 2),
    "add": Instruction("add", 2, 2),
    "sub": Instruction("sub", 3, 2),
    "mul": Instruction("mul", 4, 2),
    "div": Instruction("div", 5, 2),
    "call": Instruction("call", 6, 1),
    "jmp": Instruction("jmp", 7, 1),
    "cmp": Instruction("cmp", 8, 2),
    "cmpl": Instruction("cmpl", 9, 2),
    "cmpg": Instruction("cmpg", 10, 2),
    "ncmp": Instruction("ncmp", 11, 2)
}
