import argparse
import os
from . import errors

ap = argparse.ArgumentParser(
    prog="pasm", description="The upgraded assembler for pCPU")
ap.add_argument("infile", help="Path to input file")
ap.add_argument(
    "type", help="i for programming instructions, b for binary")
ap.add_argument("outfile", help="Path to output file")
args = ap.parse_args()

# Check args
if not os.path.exists(args.infile):
    print(f"\"{args.infile}\" is not a valid asm file")
    exit(1)
if args.type not in ["i", "b"]:
    print("Invalid type, use one of: i,b")
    exit(1)

# Load asm file
file = open(args.infile, "r").read().split("\n")
l_num = 0

# Bin format
# JMP to main
# I16 - fn caller addr
# Section - data
# Section - fns
# Section - main

# storage for output
out_bin = [7, 160, 0, 0, 0, 0]

# fn_name: addr
function_labels = {}

# variable_name: prefix, addr
variable_labels = {}
data_to_pref_map = {
    "I8":"%",
    "I16":r"%%"
}

def consumeData():
    global l_num

    while ord(file[l_num][0]) == 32:
        line = file[l_num].split(" ")
        l_num += 1
        line = [x for x in line if x]
        
        # Get needed data
        dtype = line[0]
        varname = line[1]
        value = int(line[2])
        
        # Set var
        variable_labels[varname] = [data_to_pref_map[dtype], len(out_bin)]
        
        if value > 255:
            out_bin.append((value >> 8) & 0xff)
        out_bin.append(value & 0xff)
        

def consumeProgram():
    global l_num

    pass


# Read line-by-line
while l_num < len(file):
    line = file[l_num].split(" ")
    print(line)

    # Handle line types
    if line[0].lower() == "section":
        # Handle sections
        if line[1].lower() == ".data":
            l_num += 1
            consumeData()
        elif line[1].lower() == ".main":
            l_num += 1
            consumeProgram()
        else:
            errors.addError(f"{line[1]} is not a valid section")
    elif line[0].lower() == "fn":
        function_labels[line[1]] = len(out_bin) + 20
        l_num += 1
        consumeProgram()
        # Add a jump back to caller instruction
        out_bin.append(7)
        out_bin.append(192)
        out_bin.append(3)
    else:
        l_num += 1

def bfmt(i):
    x = format(i, '08b')
    
    return x[0] + x[1] + x[2] + x[3] + " "+x[4] + x[5] + x[6] + x[7]

# Handle compiler type
if args.type == "i":
    with open(args.outfile, "w") as f:
        for i, byte in enumerate(out_bin):
            f.write(f"{bfmt(i+20)} # {bfmt(byte)}\n")
        f.close()
else:
    with open(args.outfile, "w") as f:
        f.write(bytes(out_bin))
        f.close()