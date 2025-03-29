lookup_table = {
    "add": "ADD",
    "sub": "SUB",
    "mul": "MUL",
    "load": "LD",
    "store": "ST",
    "icmp": "CMP",
    "br": "BR",
    "getelementptr": "GEP",
    "sext": "SEXT",
    "trunc": "TRUNC",
    "phi": "PHI"
}

def parse_cpp_code():
    print("Enter your C++ code (type 'END' on a new line to stop):")
    
    cpp_code = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        cpp_code.append(line)
    
    cpp_code = "\n".join(cpp_code)

    operation_count = {op: 0 for op in lookup_table.keys()}

    for op in lookup_table.keys():
        operation_count[op] += cpp_code.count(op)

    print("\nOperation Frequency:")
    for op, count in operation_count.items():
        if count > 0:
            print(f"{op}: {count}")

    print("\nLookup Table:")
    for op, short_form in lookup_table.items():
        print(f"{op.ljust(15)} -> {short_form}")

parse_cpp_code()
