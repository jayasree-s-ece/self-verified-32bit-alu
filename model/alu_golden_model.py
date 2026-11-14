import csv
import random
MASK32  = 0xFFFFFFFF
MODULUS = 3

OPS = {
    "ADD" : 0b000,
    "SUB" : 0b001,
    "AND" : 0b010,
    "OR"  : 0b011,
    "XOR" : 0b100,
    "SLT" : 0b101,
    "SLL" : 0b110,
    "SRL" : 0b111,
}

def alu(op, a, b):
    a &= MASK32
    b &= MASK32
    if op == "ADD": return (a + b) & MASK32
    elif op == "SUB": return (a - b) & MASK32
    elif op == "AND": return (a & b) & MASK32
    elif op == "OR":  return (a | b) & MASK32
    elif op == "XOR": return (a ^ b) & MASK32
    elif op == "SLT":
        a_s = a if a < 0x80000000 else a - 0x100000000
        b_s = b if b < 0x80000000 else b - 0x100000000
        return 1 if a_s < b_s else 0
    elif op == "SLL": return (a << (b & 0x1F)) & MASK32
    elif op == "SRL": return (a >> (b & 0x1F)) & MASK32

def residue3(x):
    return x % MODULUS

def parity(x):
    x &= MASK32
    x ^= x >> 16
    x ^= x >> 8
    x ^= x >> 4
    x ^= x >> 2
    x ^= x >> 1
    return x & 1

def checker_flags_fault(op, a, b, faulty_result):
    correct = alu(op, a, b)
    residue_fail = int(residue3(correct) != residue3(faulty_result))
    parity_fail  = int(parity(correct)   != parity(faulty_result))
    return int(residue_fail or parity_fail)

def generate_functional_vectors():
    vectors = []
    edge_pairs = [
        (0x00000000, 0x00000000),
        (0xFFFFFFFF, 0x00000001),
        (0x7FFFFFFF, 0x00000001),
        (0x80000000, 0x80000000),
        (0xFFFFFFFF, 0xFFFFFFFF),
        (0x00000001, 0x00000001),
        (0xAAAAAAAA, 0x55555555),
        (0x12345678, 0x9ABCDEF0),
    ]
    random.seed(42)
    for op_name, opcode in OPS.items():
        for a, b in edge_pairs:
            result = alu(op_name, a, b)
            vectors.append({"op_name": op_name, "opcode": opcode,
                "a": a, "b": b, "expected_result": result,
                "exp_residue": residue3(result), "exp_parity": parity(result)})
        for _ in range(100):
            a = random.randint(0, MASK32)
            b = random.randint(0, MASK32)
            result = alu(op_name, a, b)
            vectors.append({"op_name": op_name, "opcode": opcode,
                "a": a, "b": b, "expected_result": result,
                "exp_residue": residue3(result), "exp_parity": parity(result)})
    return vectors

def generate_fault_vectors():
    vectors = []
    test_inputs = [
        (0x12345678, 0x9ABCDEF0),
        (0xFFFFFFFF, 0x00000001),
        (0xAAAAAAAA, 0x55555555),
        (0x00000001, 0x7FFFFFFF),
    ]
    for op_name, opcode in OPS.items():
        for a, b in test_inputs:
            correct = alu(op_name, a, b)
            for bit in range(32):
                faulty   = correct ^ (1 << bit)
                detected = checker_flags_fault(op_name, a, b, faulty)
                vectors.append({"op_name": op_name, "opcode": opcode,
                    "a": hex(a), "b": hex(b), "correct_result": hex(correct),
                    "flipped_bit": bit, "faulty_result": hex(faulty),
                    "fault_detected": detected})
    return vectors

def print_summary(fault_vecs):
    from collections import defaultdict
    stats = defaultdict(lambda: {"total": 0, "detected": 0})
    for v in fault_vecs:
        stats[v["op_name"]]["total"]    += 1
        stats[v["op_name"]]["detected"] += v["fault_detected"]
    print("\n========================================")
    print(f"{'Op':<6} {'Detected':>10} {'Total':>8} {'Rate':>8}")
    print("----------------------------------------")
    gt = gd = 0
    for op, s in stats.items():
        print(f"{op:<6} {s['detected']:>10} {s['total']:>8} {100*s['detected']//s['total']:>7}%")
        gt += s["total"]; gd += s["detected"]
    print("----------------------------------------")
    print(f"{'ALL':<6} {gd:>10} {gt:>8} {100*gd//gt:>7}%")
    print("PASS" if gd == gt else "FAIL")
    print("========================================\n")

def main():
    fv = generate_functional_vectors()
    with open("functional_vectors.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fv[0].keys())
        w.writeheader(); w.writerows(fv)
    print(f"Generated {len(fv)} functional vectors -> functional_vectors.csv")
    fault_vecs = generate_fault_vectors()
    with open("fault_inject_vectors.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fault_vecs[0].keys())
        w.writeheader(); w.writerows(fault_vecs)
    print(f"Generated {len(fault_vecs)} fault vectors -> fault_inject_vectors.csv")
    print_summary(fault_vecs)

if __name__ == "__main__":
    main()
