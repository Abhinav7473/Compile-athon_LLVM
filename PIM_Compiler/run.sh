#!/bin/bash
# Set LLVM path
export PATH=$(pwd)/llvm:$PATH

# Run the compiler
./dist/PIM_Compiler
