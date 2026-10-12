from collections import Counter

# Try Aer first (fast sampling); otherwise use Statevector probabilities + sampling.
USE_AER=True
try:
    from qiskit_aer import Aer
except Exception:
    USE_AER=False

from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Statevector

def run_counts(qc, shots=4096):
    """Return measurement counts for a measured circuit."""
    if USE_AER:
        backend = Aer.get_backend('qasm_simulator')
        job = backend.run(transpile(qc, backend), shots=shots)
        return job.result().get_counts()

    # Fallback: evolve statevector, then sample bitstrings according to probabilities
    qc_no_meas, _ = qc.remove_final_measurements(inplace=False)
    sv = Statevector.from_instruction(qc_no_meas)
    probs = sv.probabilities_dict()
    # If the circuit has classical bits, use their order; otherwise, default to standard order.
    # For our circuits, measure([0,1,...],[0,1,...]) keeps natural left-to-right bitstring order.
    import numpy as np
    bitstrings = list(probs.keys())
    p = [probs[b] for b in bitstrings]
    samples = np.random.choice(bitstrings, size=shots, p=p)
    return dict(Counter(samples))

def print_header(title):
    bar = "="*len(title)
    print(f"\n{bar}\n{title}\n{bar}")

# -------------------- Part A.1: Single-qubit --------------------
print_header("Part A.1 — Single-Qubit States & Gates")

# |0>
qc0 = QuantumCircuit(1,1)
qc0.measure(0,0)
print("|0> :", run_counts(qc0))

# |1> = X|0>
qc1 = QuantumCircuit(1,1); qc1.x(0); qc1.measure(0,0)
print("|1> :", run_counts(qc1))

# |+> = H|0>
qc_plus = QuantumCircuit(1,1); qc_plus.h(0); qc_plus.measure(0,0)
print("|+> :", run_counts(qc_plus))

# |-> = H|1>
qc_minus = QuantumCircuit(1,1); qc_minus.x(0); qc_minus.h(0); qc_minus.measure(0,0)
print("|-> :", run_counts(qc_minus))

print("\nGate showcase on |+> (apply gate then measure):")
showcase = [
    ("X", lambda q: q.x(0)),
    ("Y", lambda q: q.y(0)),
    ("Z", lambda q: q.z(0)),
    ("H", lambda q: q.h(0)),
]
for name, apply_gate in showcase:
    qc = QuantumCircuit(1,1)
    qc.h(0)              # prepare |+>
    apply_gate(qc)       # apply gate
    qc.measure(0,0)
    print(f"{name}|+> :", run_counts(qc))

print("\nBloch-sphere note:")
print(" |0>,|1> are ±Z poles; |+>,|-> are ±X equator states.")
print(" X swaps |0>↔|1> (π about X); Z adds a π phase (π about Z);")
print(" Y is π about Y; H maps Z-eigenstates ↔ X-eigenstates.")

# -------------------- Part A.2: Bell states --------------------
print_header("Part A.2 — Bell States")

def measure_bell(ops_builder):
    qc = QuantumCircuit(2,2)
    ops_builder(qc)
    qc.measure([0,1],[0,1])
    return run_counts(qc)

# |Φ+> : H(0); CX(0,1)
phi_plus = measure_bell(lambda qc: (qc.h(0), qc.cx(0,1)))
print("|Φ+> :", phi_plus)

# |Φ-> : Z on control after |Φ+>
phi_minus = measure_bell(lambda qc: (qc.h(0), qc.cx(0,1), qc.z(0)))
print("|Φ-> :", phi_minus)

# |Ψ+> : X on target after |Φ+>
psi_plus = measure_bell(lambda qc: (qc.h(0), qc.cx(0,1), qc.x(1)))
print("|Ψ+> :", psi_plus)

# |Ψ-> : Z on control and X on target after |Φ+>
psi_minus = measure_bell(lambda qc: (qc.h(0), qc.cx(0,1), qc.z(0), qc.x(1)))
print("|Ψ-> :", psi_minus)

print("\nBell-state note:")
print(" |Φ±> give outcomes 00/11 only; |Ψ±> give 01/10 only (≈50/50).")
print(" Z toggles the relative phase (±), X flips the target bit.")

# -------------------- Part B (Option 2): GHZ --------------------
print_header("Part B — GHZ State (Advanced)")

def ghz_circuit(measure=True):
    qc = QuantumCircuit(3, 3 if measure else 0)
    qc.h(0)
    qc.cx(0,1)
    qc.cx(0,2)
    if measure:
        qc.measure([0,1,2],[0,1,2])
    return qc

# Z-basis counts: only 000 and 111 (perfect all-equal correlation)
ghz_counts = run_counts(ghz_circuit(measure=True), shots=4096)
print("Z-basis counts:", ghz_counts)

total = sum(ghz_counts.values())
all_equal = ghz_counts.get('000',0) + ghz_counts.get('111',0)
print(f"All-equal fraction in Z (expect ~1.000): {all_equal/total:.3f}")

# Single-qubit marginals ~ 0.5/0.5 (each qubit individually random)
def marginal(bitpos, bitval):
    # bitpos 0,1,2 correspond to left->right chars of the 3-bit string
    return sum(v for k,v in ghz_counts.items() if k[bitpos]==str(bitval)) / total

for q in range(3):
    p0 = marginal(q,0); p1 = marginal(q,1)
    print(f"Q{q} marginals: P(0)≈{p0:.3f}, P(1)≈{p1:.3f} (each ~0.5)")

# X-basis correlation: apply H⊗H⊗H (i.e., measure in X); GHZ+ gives even parity ~1.0
qc_x = QuantumCircuit(3,3)
qc_x.h(0); qc_x.cx(0,1); qc_x.cx(0,2)     # prepare GHZ+
qc_x.h([0,1,2])                            # rotate to X basis before Z-measure
qc_x.measure([0,1,2],[0,1,2])
x_counts = run_counts(qc_x, shots=4096)
x_total = sum(x_counts.values())

def parity3(s):  # XOR of three bits
    return (int(s[0]) ^ int(s[1]) ^ int(s[2]))

even_x = sum(v for k,v in x_counts.items() if parity3(k)==0) / x_total
print("X-basis counts:", x_counts)
print(f"Even parity in X (expect ~1.000): {even_x:.3f}")

print("\nGHZ commentary:")
print(" GHZ = (|000>+|111>)/√2 generalises Bell’s |Φ+> to three qubits.")
print(" In Z: outcomes are 000/111 only (all-equal correlation ~1.0).")
print(" Each qubit alone is random (½,½) — genuine tripartite entanglement.")
print(" In X: the parity of three outcomes is even with prob ~1.0 (non-classical 3-party correlation).")
print(" Tracing out one qubit destroys 2-qubit entanglement (leaves a classical mixture).")