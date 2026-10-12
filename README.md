# Quantum Computing CA1 — Python & Qiskit

## Project Overview

A university quantum computing project exploring quantum circuits, gate operations, measurement probabilities, and multipartite entanglement using Python and Qiskit.

The project uses quantum circuit simulations to demonstrate fundamental quantum computing concepts and analyze measurement outcomes.

## Key Features

- **Quantum Gate Simulations:** Explore single-qubit states and quantum gate operations.
- **Quantum Measurement:** Simulate measurements and analyze probability distributions.
- **GHZ State Preparation:** Investigate three-qubit GHZ entanglement and its measurement correlations.
- **Z-Basis Analysis:** Demonstrate correlated measurement outcomes for entangled qubits.
- **X-Basis Analysis:** Examine parity correlations in GHZ states.
- **Simulation Results:** Compare observed measurement statistics against theoretical expectations.

## Technologies Used

- Python
- Qiskit
- Qiskit Aer
- Quantum circuit simulation

## Example Results

The GHZ-state simulation produced:

- Z-basis measurements containing only `000` and `111`.
- An all-equal correlation fraction of `1.000`.
- Individual qubit measurement probabilities close to 50%.
- An X-basis even-parity fraction of `1.000`.

These results are consistent with the expected behavior of an ideal three-qubit GHZ state.

## Source Code

The implementation is available in `QuantumAssignment.py`.

## Project Context

Developed as part of university coursework in Quantum Computing.
