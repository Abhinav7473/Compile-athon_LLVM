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
![Screenshot 2025-03-30 093110](https://github.com/user-attachments/assets/efefe4f0-4ae6-4e9e-a3d2-851ca99ff8ba)



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
(Currently this project is intented to work on Linux only)
1. Run the compiler
```
chmod +x run.sh
# Execute the compiler
./run.sh
```
2. Access the web interface at `http://localhost:3000`.
3. Upload your C++ code for compilation or use `example.cpp`.

### Outputs:
Compiled files will be available in the `/PIM_Compiler/outputs` directory.

---

## Code Overview

### `streamlit_app.py`
A comprehensive compiler interface that translates C++ code to custom PIM architecture instructions through a multi-stage pipeline.

#### **File Processing**
- Handles C++ file uploads and displays content in formatted view.  
- Manages uploads and outputs directories.  
- Provides download functionality for all generated files.  

#### **Compilation Pipeline**
- **LLVM IR Generation**: Uses `clang++` to convert C++ to LLVM IR.  
- **IR Optimization**: Applies `-O2` optimizations via `opt` tool.  
- **TAC Extraction**: Parses LLVM IR to Three-Address Code (TAC) using regex patterns.  
- **ISA Generation**: Converts TAC to custom PIM assembly instructions.  
- **LUT Generation**: Creates operation frequency analysis and lookup tables.  

#### **Core Components**
- **Operation Detection**: Regex-based pattern matching for LLVM operations.  
- **PIM ISA Mapping**: Implements LUT programming and execution phases.  
- **Memory Operations**: Handles `ACTIVATE`, `LOAD`, and `STORE` commands.  
- **Compute Operations**: Manages `MAC` operations (multiply-accumulate).  

#### **UI Features**
- Modern dark-themed interface with custom CSS.  
- Real-time compilation status tracking.  
- Two-column results display (LLVM IR + TAC, ISA + LUT).  
- Responsive design with download buttons for all outputs.  

#### **Key Functions**
- `generate_llvm_ir()`: Converts C++ to LLVM IR.  
- `optimize_llvm_ir()`: Applies compiler optimizations.  
- `parse_llvm_to_tac()`: Extracts Three-Address Code.  
- `map_tac_to_isa()`: Generates PIM-specific assembly.  
- `generate_lut_file()`: Creates operation analysis reports.  

This application provides a complete workflow from C++ source to PIM-executable code with visual feedback at each compilation stage.


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

## Team Members
- Jacob Cherian (22BRS1010)
- Siddarth S (22BRS1078)
- Abhinav Balakrishnan (22BRS1357)
