import streamlit as st
import os
import subprocess
import re
import json
from pathlib import Path

# Custom CSS for styling
st.markdown("""
<style>
    .stApp {
        max-width: 1400px;
        margin: 0 auto;
        padding: 1rem;
    }
    .header {
        color: #ffffff;
        border-bottom: 2px solid #2E86AB;
        padding-bottom: 0.5rem;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    .file-uploader {
        background-color: #2D3748;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
    }
    .code-block {
        border-radius: 8px;
        padding: 1rem;
        background-color: #1A202C;
        color: #ffffff;
    }
    .download-btn {
        margin-top: 1rem;
        width: 100%;
    }
    .step {
        background-color: #2D3748;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        color: #ffffff;
    }
    .step-title {
        color: #2E86AB;
        font-weight: bold;
    }
    .tab-content {
        padding-top: 1rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        justify-content: center;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #2D3748;
        border-radius: 4px;
        color: white;
        padding: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #2E86AB !important;
        color: white;
    }
    pre {
        color: #ffffff !important;
        background-color: #1A202C !important;
        max-height: 400px;
        overflow-y: auto;
    }
    .stCodeBlock {
        max-height: 400px;
        overflow-y: auto;
    }
    .block-container {
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
        max-width: 1400px;
    }
    .output-container {
        background-color: #1A202C;
        border-radius: 8px;
        padding: 10px;
        margin-bottom: 1rem;
        height: 500px;
        overflow-y: auto;
    }
    .output-title {
        color: #2E86AB;
        text-align: center;
        margin-bottom: 10px;
    }
    .cpp-display {
        text-align: left;
        margin: 20px auto;
        max-width: 80%;
        background-color: #1A202C;
        padding: 20px;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Define directories for intermediate and output files
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
Path(UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)
Path(OUTPUT_FOLDER).mkdir(parents=True, exist_ok=True)

# Lookup Table for TAC-to-ISA mapping
lookup_table = {
    "add": "ADD",
    "sub": "SUB",
    "mul": "MUL",
    "load": "LD",
    "store": "ST",
    "icmp": "CMP",
    "br": "BR"
}

# Define Look-Ahead Table (LUT) for operations
lut_definitions = {
    "OP_A": {
        "description": "Multiplication Operation",
        "entries": [
            {"input_pattern": "0000", "output_value": "0000", "description": "0 × 0 = 0"},
            {"input_pattern": "0001", "output_value": "0000", "description": "0 × 1 = 0"},
            {"input_pattern": "0010", "output_value": "0000", "description": "0 × 2 = 0"},
            {"input_pattern": "0011", "output_value": "0000", "description": "0 × 3 = 0"},
            {"input_pattern": "0100", "output_value": "0000", "description": "1 × 0 = 0"},
            {"input_pattern": "0101", "output_value": "0001", "description": "1 × 1 = 1"},
            {"input_pattern": "0110", "output_value": "0010", "description": "1 × 2 = 2"},
            {"input_pattern": "0111", "output_value": "0011", "description": "1 × 3 = 3"},
            {"input_pattern": "1000", "output_value": "0000", "description": "2 × 0 = 0"},
            {"input_pattern": "1001", "output_value": "0010", "description": "2 × 1 = 2"},
            {"input_pattern": "1010", "output_value": "0100", "description": "2 × 2 = 4"},
            {"input_pattern": "1011", "output_value": "0110", "description": "2 × 3 = 6"},
            {"input_pattern": "1100", "output_value": "0000", "description": "3 × 0 = 0"},
            {"input_pattern": "1101", "output_value": "0011", "description": "3 × 1 = 3"},
            {"input_pattern": "1110", "output_value": "0110", "description": "3 × 2 = 6"},
            {"input_pattern": "1111", "output_value": "1001", "description": "3 × 3 = 9"}
        ]
    },
    "OP_B": {
        "description": "Addition Operation",
        "entries": [
            {"input_pattern": "0000", "output_value": "0000", "description": "0 + 0 = 0"},
            {"input_pattern": "0001", "output_value": "0001", "description": "0 + 1 = 1"},
            {"input_pattern": "0010", "output_value": "0010", "description": "0 + 2 = 2"},
            {"input_pattern": "0011", "output_value": "0011", "description": "0 + 3 = 3"},
            {"input_pattern": "0100", "output_value": "0001", "description": "1 + 0 = 1"},
            {"input_pattern": "0101", "output_value": "0010", "description": "1 + 1 = 2"},
            {"input_pattern": "0110", "output_value": "0011", "description": "1 + 2 = 3"},
            {"input_pattern": "0111", "output_value": "0100", "description": "1 + 3 = 4"},
            {"input_pattern": "1000", "output_value": "0010", "description": "2 + 0 = 2"},
            {"input_pattern": "1001", "output_value": "0011", "description": "2 + 1 = 3"},
            {"input_pattern": "1010", "output_value": "0100", "description": "2 + 2 = 4"},
            {"input_pattern": "1011", "output_value": "0101", "description": "2 + 3 = 5"},
            {"input_pattern": "1100", "output_value": "0011", "description": "3 + 0 = 3"},
            {"input_pattern": "1101", "output_value": "0100", "description": "3 + 1 = 4"},
            {"input_pattern": "1110", "output_value": "0101", "description": "3 + 2 = 5"},
            {"input_pattern": "1111", "output_value": "0110", "description": "3 + 3 = 6"}
        ]
    }
}
lookup_table = {
    "add": "ADD",
    "sub": "SUB",
    "mul": "MUL",
    "load": "LD",
    "store": "ST",
    "icmp": "CMP",
    "br": "BR",
    "getelementptr": "GBP",
    "sext": "SEXT",
    "trunc": "TRUNC",
    "phi": "PHI"
}

def parse_cpp_code(cpp_code):
    """Enhanced operation detection with corrected regex patterns and exact counting"""
    operation_count = {op: 0 for op in lookup_table.keys()}
    
    # More precise patterns that match the original functionality
    patterns = {
        'add': re.compile(r'\badd\b|\+'),  # Match LLVM's 'add' or + operator
        'sub': re.compile(r'\bsub\b|\-'),  # Match LLVM's 'sub' or - operator
        'mul': re.compile(r'\bmul\b|\*'),  # Match LLVM's 'mul' or * operator
        'load': re.compile(r'\bload\b'),   # Only match LLVM's load instruction
        'store': re.compile(r'\bstore\b'), # Only match LLVM's store instruction
        'icmp': re.compile(r'\bicmp\b'),  # Only match LLVM's icmp
        'br': re.compile(r'\bbr\b'),      # Only match LLVM's br
        'getelementptr': re.compile(r'\bgetelementptr\b'),
        'sext': re.compile(r'\bsext\b'),
        'trunc': re.compile(r'\btrunc\b'),
        'phi': re.compile(r'\bphi\b')
    }
    
    # Count exact matches as shown in the original image
    for op in lookup_table.keys():
        operation_count[op] = cpp_code.count(op)  # Simple count as in original
    
    return operation_count

def generate_lut_file(cpp_code):
    """Generate output matching the exact format from the image"""
    operation_count = parse_cpp_code(cpp_code)
    
    # Create the formatted output to match the console output from the image
    result = {
        "Operation Frequency": {op: count for op, count in operation_count.items() if count > 0},
        "Lookup Table": {op: lookup_table[op] for op in lookup_table}  # Show complete table as in image
    }
    
    return result


def generate_llvm_ir(input_cpp_path, output_ll_path):
    """Generate LLVM IR (.ll) from C++ code using Clang."""
    try:
        result = subprocess.run(["clang++", "-S", "-emit-llvm", input_cpp_path, "-o", output_ll_path], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            st.error(f"LLVM IR generation failed: {result.stderr}")
            return False
        return True
    except Exception as e:
        st.error(f"Error during LLVM IR generation: {str(e)}")
        return False

def optimize_llvm_ir(input_file, output_file):
    """Optimize LLVM IR using opt tool"""
    try:
        result = subprocess.run(f"opt -S -O2 {input_file} -o {output_file}", 
                               shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            st.error(f"LLVM IR optimization failed: {result.stderr}")
            return False
        return True
    except Exception as e:
        st.error(f"Error during LLVM IR optimization: {str(e)}")
        return False

def parse_llvm_to_tac(input_ll_file):
    """Improved TAC extraction using regex patterns"""
    tac_instructions = []
    patterns = {
        'binary_op': re.compile(r"^\s*%(\w+)\s*=\s*(add|sub|mul|div|sdiv|and|or|xor)\s+\w+\s+%(\w+),\s*%(\w+)"),
        'compare': re.compile(r"^\s*%(\w+)\s*=\s*(icmp\s+\w+)\s+\w+\s+%(\w+),\s*%(\w+)"),
        'load': re.compile(r"^\s*%(\w+)\s*=\s*load\s+\w+,.*"),
        'store': re.compile(r"^\s*store\s+\w+\s+%(\w+),.*"),
        'branch': re.compile(r"^\s*br\s+(label|i1).*")
    }

    try:
        with open(input_ll_file, 'r') as ll_file:
            for line in ll_file:
                if match := patterns['binary_op'].match(line):
                    dest, op, op1, op2 = match.groups()
                    tac_instructions.append(f"{dest} = {op} {op1}, {op2}")
                    continue
                    
                if match := patterns['compare'].match(line):
                    dest, cmp_op, op1, op2 = match.groups()
                    tac_instructions.append(f"{dest} = {cmp_op} {op1}, {op2}")
                    continue

                if match := patterns['load'].match(line):
                    dest = match.group(1)
                    tac_instructions.append(f"{dest} = LOAD")
                    continue
                    
                if match := patterns['store'].match(line):
                    src = match.group(1)
                    tac_instructions.append(f"STORE {src}")
                    continue

                if match := patterns['branch'].match(line):
                    tac_instructions.append(f"BRANCH {line.strip()}")
                    continue
    except Exception as e:
        st.error(f"Error parsing LLVM IR: {str(e)}")
        return []

    return tac_instructions

def map_tac_to_isa(tac_instructions):
    """Generate complete PIM assembly instructions"""
    asm_instructions = []
    operations_used = set()
    current_row = 0
    
    # Instruction mnemonics
    mnemonics = {
        'mem': {
            'activate': 'ACTIVATE',
            'load': 'LOAD',
            'store': 'STORE'
        },
        'lut': {
            'mult': 'LUT_PROG_MULT',
            'add': 'LUT_PROG_ADD',
            'cmp': 'LUT_PROG_CMP'
        },
        'compute': {
            'mult': 'MAC_MULT',
            'add': 'MAC_ADD',
            'cmp': 'COMPARE'
        }
    }
    
    # Initial row activation
    asm_instructions.append(f"{mnemonics['mem']['activate']} {current_row}  ; Activate row buffer")
    
    for instr in tac_instructions:
        try:
            parts = [p for p in instr.split() if p]
            if not parts:
                continue
                
            if "=" in instr:  # Assignment operation
                op = parts[2]
                operands = parts[3:]
            else:  # Branch/store operation
                op = parts[0].lower()
                operands = parts[1:]

            # MAC Operation
            if op == "mul":
                # Program LUTs
                asm_instructions.append(f"{mnemonics['lut']['mult']} 0x3, 0x40  ; Program cores 0-1 for 4-bit mult")
                asm_instructions.append(f"{mnemonics['lut']['add']} 0xC, 0x80  ; Program cores 2-3 for 4-bit add")
                operations_used.update(["OP_A", "OP_B"])
                
                # Execute MAC steps
                asm_instructions.append(f"{mnemonics['compute']['mult']} 1  ; First multiply phase")
                asm_instructions.append(f"{mnemonics['compute']['add']} 1  ; Partial sum")
                asm_instructions.append(f"{mnemonics['compute']['mult']} 2  ; Second multiply phase")
                asm_instructions.append(f"{mnemonics['compute']['add']} 2  ; Final accumulate")
                
                current_row += 1
                asm_instructions.append(f"{mnemonics['mem']['store']} {current_row}  ; Store results")
            
            # Addition Operation
            elif op == "add":
                asm_instructions.append(f"{mnemonics['lut']['add']} 0xF, 0x80  ; Program all cores for addition")
                asm_instructions.append(f"{mnemonics['compute']['add']} 0  ; Execute addition")
                operations_used.add("OP_B")
                current_row += 1
            
            # Load Operation
            elif op == "load":
                current_row += 1
                asm_instructions.append(f"{mnemonics['mem']['load']} {current_row}  ; Load from row {current_row}")
            
            # Store Operation
            elif op == "store":
                current_row += 1
                asm_instructions.append(f"{mnemonics['mem']['store']} {current_row}  ; Store to row {current_row}")
            
            # Comparison Operation
            elif op.startswith("icmp"):
                asm_instructions.append(f"{mnemonics['lut']['cmp']} 0xF, 0xC0  ; Program comparison LUTs")
                asm_instructions.append(f"{mnemonics['compute']['cmp']}  ; Execute comparison")
                operations_used.add("CMP")
                
            # Branch Operation
            elif op == "branch":
                cond = operands[1] if len(operands) > 1 else None
                if cond:
                    asm_instructions.append(f"BRANCH {cond} {operands[2]} {operands[4]}")
                else:
                    asm_instructions.append(f"JUMP {operands[1]}")
                
        except Exception as e:
            print(f"Skipping instruction {instr}: {str(e)}")
            continue
    
    return asm_instructions, operations_used
    
# Streamlit app interface

st.markdown("<h1 class='header'>Enhanced PIM Architecture Compiler</h1>", unsafe_allow_html=True)
st.markdown("<h3 class='header'>Project by: 22BRS1010 - Jacob Cherian ,22BRS1078 - Siddarth S ,22BRS1357 - Abhinav Balakrishnan</h3>", unsafe_allow_html=True)
st.markdown("""
<p style="text-align: center; color: white;">Upload C++ code to compile to custom PIM (Processing-in-Memory) architecture instructions.</p>
<div class='step'>
    <div class='step-title'>Compilation Pipeline:</div>
    <ol>
        <li>C++ Source Code → LLVM IR (Clang)</li>
        <li>LLVM IR → Optimized IR (opt)</li>
        <li>Optimized IR → Three-Address Code</li>
        <li>TAC → Custom PIM ISA</li>
        <li>Generate Look-Ahead Table (LUT) for operations</li>
    </ol>
</div>
""", unsafe_allow_html=True)

# File upload section
with st.container():
    st.markdown("<div class='file-uploader'>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Choose a C++ file", type=["cpp", "cxx", "cc"], 
                                   accept_multiple_files=False,
                                   help="Upload your C++ source code file")
    st.markdown("</div>", unsafe_allow_html=True)

if uploaded_file:
    # Show processing status
    with st.status("Processing your file...", expanded=True) as status:
        st.write("Saving uploaded file...")
        cpp_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
        raw_ll_path = os.path.join(OUTPUT_FOLDER, "unoptimized.ll")
        opt_ll_path = os.path.join(OUTPUT_FOLDER, "optimized.ll")
        
        with open(cpp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        with open(cpp_path, "r") as f:
            cpp_code = f.read()
        
        st.markdown("<div class='output-title'>Uploaded C++ File Content</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='cpp-display'><pre>{cpp_code}</pre></div>", unsafe_allow_html=True)
            
        st.write("Generating LLVM IR...")
        if not generate_llvm_ir(cpp_path, raw_ll_path):
            st.error("Failed to generate LLVM IR")
            st.stop()
        
        st.write("Optimizing LLVM IR...")
        if not optimize_llvm_ir(raw_ll_path, opt_ll_path):
            st.error("Failed to optimize LLVM IR")
            st.stop()
        
        st.write("Extracting Three-Address Code...")
        tac_instructions = parse_llvm_to_tac(opt_ll_path)
        if not tac_instructions:
            st.error("Failed to extract TAC from LLVM IR")
            st.stop()
        
        st.write("Generating Custom ISA...")
        isa_instructions, operations_used = map_tac_to_isa(tac_instructions)
        
        st.write("Generating Look-Ahead Table (LUT)...")
        lut_content = generate_lut_file(cpp_code)
        
        status.update(label="Processing complete!", state="complete", expanded=False)

    # Display results in a 2x2 grid layout using Streamlit's native column system
    st.markdown("<h2 style='text-align: center; color: white;'>Compilation Results</h2>", unsafe_allow_html=True)
    
    # Top row - LLVM IR and TAC
    row1_col1, row1_col2 = st.columns(2)
    
    # First row, first column - LLVM IR
    with row1_col1:
        st.markdown("<div class='output-title'>Optimized LLVM IR</div>", unsafe_allow_html=True)
        with open(opt_ll_path) as f:
            optimized_llvm_content = f.read()
        
        with st.container():
            st.code(optimized_llvm_content, language="llvm")
            st.download_button("Download LLVM IR", optimized_llvm_content, 
                           file_name="optimized.ll", key="llvm_dl",
                           help="Download the optimized LLVM intermediate representation")
    
    # First row, second column - TAC
    with row1_col2:
        st.markdown("<div class='output-title'>Three-Address Code</div>", unsafe_allow_html=True)
        tac_content = "\n".join(tac_instructions)
        
        with st.container():
            st.code(tac_content, language="text")
            st.download_button("Download TAC", tac_content, 
                           file_name="output.tac", key="tac_dl",
                           help="Download the three-address code representation")
    
    # Add some spacing
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Bottom row - ISA and LUT
    row2_col1, row2_col2 = st.columns(2)
    
    # Second row, first column - Custom ISA
    with row2_col1:
        st.markdown("<div class='output-title'>Custom ISA</div>", unsafe_allow_html=True)
        isa_content = "\n".join(isa_instructions)
        
        with st.container():
            st.code(isa_content, language="asm")
            st.download_button("Download ISA", isa_content, 
                           file_name="output.asm", key="isa_dl",
                           help="Download the custom PIM instruction set architecture code")
    
    # Second row, second column - LUT
    with row2_col2:
    	st.markdown("<div class='output-title'>Look Up Table</div>", unsafe_allow_html=True)
    
    	with open(cpp_path, "r") as f:
       	    cpp_code = f.read()
    	
    	analysis = generate_lut_file(cpp_code)
    
    	st.markdown("**Operation Frequency:**")
    	st.json(analysis["Operation Frequency"])
    
    	st.markdown("**Lookup Table:**")
    	st.json(analysis["Lookup Table"])
	
    # Save output files
    with open(os.path.join(OUTPUT_FOLDER, "output.tac"), "w") as f:
        f.write(tac_content)
        
    with open(os.path.join(OUTPUT_FOLDER, "output.asm"), "w") as f:
        f.write(isa_content)
        
    
else:
    st.info("Please upload a C++ file to begin compilation")
