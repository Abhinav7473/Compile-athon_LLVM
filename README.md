# Compiler for pPIM Architecture

## Overview

This project implements a compiler tailored for a custom **Processing-in-Memory (PIM)** architecture called **pPIM**, designed for AI/ML applications. The compiler translates high-level C++ programs into a stream of custom ISA-compatible instructions that drive the pPIM architecture. By leveraging the LLVM framework, the compiler ensures efficient translation, optimization, and integration with the pPIM hardware.

### DRAM Bank and Cluster Design
![DRAM Bank and Cluster Design](https://pplx-res.cloudinary.com/image/upload/v1743272862/user_uploads/SBCVNrPrPQXGIVs/image.jpg)

The pPIM architecture integrates **Processing Elements (Clusters)** directly within DRAM banks, enabling near-subarray computing. Key components include:
- **Local Row Buffer**: Holds one DRAM page of data at a time.
- **Clusters**: Groups of programmable LUTs that perform micro-computations.
- **Router Microarchitecture**: Facilitates interconnections among LUTs for efficient data routing.

### Instruction Set Architecture (ISA)
![Instruction Set Architecture](https://pplx-res.cloudinary.com/image/upload/v1743272871/user_uploads/LbhaPNgiudAjHyz/image.jpg)

The pPIM ISA is designed for fixed-length instructions with the following fields:
- **Opcode**: Specifies the operation type (e.g., PROG, EXE, END).
- **Core Pointer/ID**: Used for programming LUTs.
- **Rd/Wr Bits**: Enable memory operations.
- **Row Address**: Specifies the DRAM row address.

---

## Problem Statement

The project addresses the following objectives:
1. Develop a compiler for a custom **Processor-in-Memory (PIM)** architecture optimized for AI/ML workloads.
2. **Input**: A C++ program performing matrix multiplication with parameterized integer operands.
3. **Output**: A stream of **custom ISA-compatible instructions** for the pPIM architecture.
   - Includes physical memory mapping.
   - ISA format adheres to Section IV-D of the research paper *"Flexible Instruction Set Architecture for Programmable Look-up Table based Processing-in-Memory"*.
4. Preferred adoption of the **LLVM framework** for IR generation and optimization.

---

## pPIM Architecture

### Key Features:
- **LUT-Based Computing**:
  - Each cluster contains nine 8-bit LUT cores.
  - LUTs are runtime programmable and interconnected via an all-to-all router.
  - Supports 4-bit multiplications and additions decomposed from higher-precision operations.

- **Memory Integration**:
  - DRAM banks with local row buffers interface directly with clusters.
  - Clusters perform computations on data fetched from row buffers.

- **Instruction Set Architecture (ISA)**:
  - Fixed-length 24-bit instructions with fields for opcodes, core pointers, read/write bits, and row addresses.
  - Three instruction types:
    - Memory Access
    - LUT Programming
    - Compute (Logic/Arithmetic)

- **SIMD Layout**:
  - Enables parallel execution across clusters interfaced with memory subarrays.

---

## Repository Structure

Here is the structure of the repository:

![Repository Structure Diagram](https://pplx-res.cloudinary.com/image/upload/v1743303699/user_uploads/atpAFaSUGCyNxOU/image.jpg)

---

## Installation & Usage

### Prerequisites:
- Python 3.x
- streamlit==1.44.0
- llvmlite==0.40.0
- libclang==14.0.0
- numpy>=1.0

### Installation:
1. Clone the repository:
    git clone https://github.com/Abhinav7473/Compile-athon_LLVM.git
    cd Compile-athon_LLVM
2. Install Dependencies using `requirements.txt`

### Running the Compiler:
1. Start the server:
    npm start
2. Access the web interface at `http://localhost:3000`.
3. Upload your C++ code for compilation or use `example.cpp`.

### Outputs:
Compiled files will be available in the `/output` directory.

---

## Code Overview

### `example.cpp`
Implements matrix multiplication using nested loops. Accepts two matrices as input, verifies their compatibility for multiplication, and computes the resultant matrix.

### `LUT.py`
Analyzes operation frequency in C++ code and maps operations to short-form ISA mnemonics using a lookup table.

### `tac_extractor.py`
Parses LLVM IR to extract instructions in Three-Address Code (TAC) format using regular expressions. Identifies binary operations, comparisons, loads/stores, and branching instructions.

### `app.py`
A Node.js backend that handles compilation requests via REST API endpoints. Generates `.ll`, `.tac`, `.asm`, and lookup files based on user-provided C++ code.

![Enhanced PIM Architecture Compiler Interface](https://pplx-res.cloudinary.com/image/upload/v1743303664/user_uploads/fCqiIIeFzaFzBfk/WhatsApp-Image-2025-03-30-at-07.24.10_f901eec7.jpg)

![Uploaded C++ Code Content](https://pplx-res.cloudinary.com/image/upload/v1743303684/user_uploads/ZbwyClznIsieZpB/WhatsApp-Image-2025-03-30-at-07.24.11_5334f421.jpg)

![Compilation Results](https://pplx-res.cloudinary.com/image/upload/v1743303689/user_uploads/VCHLWuFjWqjpJPA/WhatsApp-Image-2025-03-30-at-07.24.11_78afd6fa.jpg)

---

## pPIM ISA Design

### Instruction Format:

| Bits        | Field          | Description                              |
|-------------|----------------|------------------------------------------|
| 18–17       | Opcode         | Operation type (e.g., PROG, EXE, END)    |
| 16–11       | Core Pointer   | Identifies LUT cores within clusters     |
| 10          | Read Bit       | Enables memory read                     |
| 9           | Write Bit      | Enables memory write                    |
| 8–0         | Row Address    | Specifies DRAM row address              |

### Supported Operations:

| Operation              | Steps | Core Configurations |
|------------------------|-------|---------------------|
| Unsigned MAC (8-bit)   | 9     | 2                   |
| Unsigned MAC (4-bit)   | 5     | 2                   |
| Signed MAC (8-bit)     | 13    | 5                   |
| ReLU (16-bit)          | 4     | 1                   |
| Max Index (16-bit)     | 13    | 4                   |

---

## Future Work

- Finalize ISA code generation for edge cases.
- Extend support for additional AI/ML workloads beyond matrix multiplication.
- Optimize memory mapping strategies for larger datasets.

---

## References

This project is based on concepts discussed in *"Flexible Instruction Set Architecture for Programmable Look-up Table based Processing-in-Memory"* presented at ICCD 2021 by Connolly et al., which outlines the pPIM architecture and its custom ISA design principles.

For further details, refer to Section IV-D of the research paper included in this repository.

---
