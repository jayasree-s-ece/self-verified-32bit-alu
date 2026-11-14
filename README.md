# 32-bit ALU with Fault Detection

A 32-bit ALU in Verilog with a built-in fault checker based on mod-3 residue and parity. A Python model generates test vectors and measures single-bit fault detection.

## Features
- 8 operations selected by a 3-bit `op`: ADD, SUB, AND, OR, XOR, SLT (signed), SLL, SRL
- Checker compares the ALU result with an expected mod-3 residue and expected parity; `fault_flag` goes high if either check fails
- Python golden model generates 864 functional and 1,024 fault-injection test vectors

## Repository structure
| Folder | Contents |
|---|---|
| `rtl/` | `alu_core.v` (ALU), `checker.v` (residue + parity checker), `alu_top.v` (top level) |
| `tb/` | Verilog testbenches |
| `model/` | Python golden model and generated vector files (CSV) |
| `synth/` | Yosys scripts and synthesis logs |
| `docs/` | Project report and simulation outputs |

## Results (Python model)
| Operation | Faults injected | Detected | Rate |
|---|---|---|---|
| Each of 8 operations | 128 | 128 | 100% |
| **All** | **1,024** | **1,024** | **100%** |

Why single-bit faults are always caught: a flipped bit always changes the parity, and it changes the value by ±2^k, which is never a multiple of 3, so the mod-3 residue changes too.

## How to run
Python model (generates the CSV vectors and prints the detection table):
```
cd model
python alu_golden_model.py
```
Verilog simulation with Icarus Verilog:
```
iverilog -o sim rtl/alu_core.v tb/tb_alu_core.v
vvp sim
```

## Status
- Fault-injection results above come from the Python model.
- The Verilog testbenches are basic smoke tests. A self-checking testbench that reads the CSV vectors is planned.
- Full details are in the report in `docs/`.
