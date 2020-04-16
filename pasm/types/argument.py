from typing import List
from ..errors import addWarning, addError
from dataclasses import dataclass

@dataclass
class Argument:

    type: int
    value: int

    def assemble(self) -> List[int]:
        output: list = [self.type]
        
        # Handle errors
        if self.value < 0:
            addError(f"Type: {self.type}, Value: {self.value} ! pCPU does not allow negative numbers")
        
        if self.value > 511:
            addWarning(f"Type: {self.type}, Value: {self.value} # Value greater than 512. Truncating.")

        if self.value > 255:
            output.append((self.value >> 8) & 0xff)

        output.append(self.value & 0xff)

        return output
