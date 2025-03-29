const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const fs = require('fs');
const path = require('path');

const app = express();
const port = 3000;

// Middleware
app.use(cors());
app.use(bodyParser.json());
app.use(express.static('public'));

// Lookup table for instruction mapping
const lookup_table = {
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
};

// Helper function to generate 24-bit ISA instruction
function generateISAInstruction(type, memoryAccess) {
    // Upper 8 bits for execution operations (PROG, EXE, END)
    let upperBits = 0;
    switch(type) {
        case 'PROG': upperBits = 0x01; break;
        case 'EXE': upperBits = 0x02; break;
        case 'END': upperBits = 0x03; break;
    }
    
    // Middle 6 bits reserved for expansion (set to 0)
    const middleBits = 0;
    
    // Lower 10 bits for memory access
    const lowerBits = memoryAccess & 0x3FF;
    
    // Combine all bits into a 24-bit instruction
    return (upperBits << 16) | (middleBits << 10) | lowerBits;
}

// Endpoint to handle code compilation
app.post('/compile', (req, res) => {
    const { code } = req.body;
    if (!code) {
        return res.status(400).json({ error: 'No code provided' });
    }

    try {
        // Create output directory if it doesn't exist
        const outputDir = path.join(__dirname, 'output');
        if (!fs.existsSync(outputDir)) {
            fs.mkdirSync(outputDir);
        }

        // Generate .ll file (LLVM IR)
        const llCode = generateLLVMIR(code);
        fs.writeFileSync(path.join(outputDir, 'output.ll'), llCode);

        // Generate binary file
        const binaryCode = generateBinary(llCode);
        fs.writeFileSync(path.join(outputDir, 'output.bin'), binaryCode);

        // Generate ISA file
        const isaCode = generateISA(llCode);
        fs.writeFileSync(path.join(outputDir, 'output.isa'), isaCode);

        // Generate lookup file
        const lookupCode = generateLookup(code);
        fs.writeFileSync(path.join(outputDir, 'lookup.txt'), lookupCode);

        res.json({
            message: 'Compilation successful',
            files: {
                ll: '/download/output.ll',
                binary: '/download/output.bin',
                isa: '/download/output.isa',
                lookup: '/download/lookup.txt'
            }
        });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Download endpoint
app.get('/download/:file', (req, res) => {
    const file = path.join(__dirname, 'output', req.params.file);
    res.download(file);
});

// Helper functions for code generation
function generateLLVMIR(code) {
    // Basic LLVM IR generation for matrix multiplication
    return `; Matrix Multiplication LLVM IR\n${code}`;
}

function generateBinary(llCode) {
    // Simple binary generation
    return Buffer.from(llCode).toString('binary');
}

function generateISA(llCode) {
    let isaInstructions = [];
    
    // Add PROG instruction for configuration
    isaInstructions.push(generateISAInstruction('PROG', 0));
    
    // Add EXE instructions for matrix operations
    isaInstructions.push(generateISAInstruction('EXE', 1));
    
    // Add END instruction
    isaInstructions.push(generateISAInstruction('END', 0));
    
    return isaInstructions.join('\n');
}

function generateLookup(code) {
    let result = 'Operation Frequency:\n';
    
    // Count operations
    for (const [op, shortForm] of Object.entries(lookup_table)) {
        const count = (code.match(new RegExp(op, 'g')) || []).length;
        if (count > 0) {
            result += `${op}: ${count}\n`;
        }
    }
    
    result += '\nLookup Table:\n';
    for (const [op, shortForm] of Object.entries(lookup_table)) {
        result += `${op.padEnd(15)} -> ${shortForm}\n`;
    }
    
    return result;
}

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});