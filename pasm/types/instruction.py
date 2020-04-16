# This file handles Instructions

from dataclasses import dataclass
from typing import List
from .argument import Argument

@dataclass
class Instruction: 
    
    mnemonic:str
    binary:int
    expected_args:int
    args:List[Argument]