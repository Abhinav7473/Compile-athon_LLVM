import re

def parse_llvm_to_tac(input_ll_file, output_tac_file):
    """
    Parses an LLVM IR (.ll) file and extracts instructions in TAC format.
    Writes the extracted TAC instructions to a .tac file.
    """
    tac_instructions = []

    # Regular expressions to match LLVM IR instructions
    binary_op_pattern = re.compile(r"^\s*%(\w+)\s*=\s*(add|sub|mul|div|sdiv|and|or|xor)\s+\w+\s+%(\w+),\s*%(\w+)")
    compare_pattern = re.compile(r"^\s*%(\w+)\s*=\s*(icmp\s+\w+)\s+\w+\s+%(\w+),\s*%(\w+)")
    load_pattern = re.compile(r"^\s*%(\w+)\s*=\s*load\s+\w+,.*")
    store_pattern = re.compile(r"^\s*store\s+\w+\s+%(\w+),.*")
    branch_pattern = re.compile(r"^\s*br\s+(label|i1).*")

    try:
        with open(input_ll_file, 'r') as ll_file:
            lines = ll_file.readlines()

        for line in lines:
            # Match binary operations
            binary_match = binary_op_pattern.match(line)
            if binary_match:
                dest, op, op1, op2 = binary_match.groups()
                tac_instructions.append(f"{dest} = {op} {op1}, {op2}")
                continue

            # Match comparison operations
            compare_match = compare_pattern.match(line)
            if compare_match:
                dest, cmp_op, op1, op2 = compare_match.groups()
                tac_instructions.append(f"{dest} = {cmp_op} {op1}, {op2}")
                continue

            # Match load instructions
            load_match = load_pattern.match(line)
            if load_match:
                dest = load_match.group(1)
                tac_instructions.append(f"{dest} = LOAD")
                continue

            # Match store instructions
            store_match = store_pattern.match(line)
            if store_match:
                src = store_match.group(1)
                tac_instructions.append(f"STORE {src}")
                continue

            # Match branching instructions
            branch_match = branch_pattern.match(line)
            if branch_match:
                tac_instructions.append(f"BRANCH {line.strip()}")
                continue

        # Write TAC instructions to output file
        with open(output_tac_file, 'w') as tac_file:
            for instruction in tac_instructions:
                tac_file.write(instruction + '\n')

        print(f"TAC successfully written to {output_tac_file}")

    except FileNotFoundError:
        print(f"Error: File '{input_ll_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Input and output files
input_ll_file = "optimized_example.ll"
output_tac_file = "optimized_example.tac"

# Run the conversion
parse_llvm_to_tac(input_ll_file, output_tac_file)
