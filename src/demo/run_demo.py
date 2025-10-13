#!/usr/bin/env python3
"""
QuantumViz Agent - Easy Demo Runner for Judges
Run all demo scenarios with one command.
"""

import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from braket.circuits import Circuit
from braket.devices import LocalSimulator

def print_header(title):
    """Print formatted header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60 + "\n")

def run_circuit_demo(name, circuit_data):
    """Run a single circuit demo."""
    print(f"Running: {name}")
    print(f"Description: {circuit_data['description']}\n")
    
    # Create circuit
    circuit = Circuit()
    for gate in circuit_data['circuit']['gates']:
        gate_type = gate['type']
        qubit = gate['qubit']
        target = gate.get('target')
        
        if gate_type == 'H':
            circuit.h(qubit)
        elif gate_type == 'X':
            circuit.x(qubit)
        elif gate_type == 'CNOT':
            circuit.cnot(qubit, target)
    
    print("Circuit:")
    print(circuit)
    print()
    
    # Run simulation
    simulator = LocalSimulator()
    result = simulator.run(circuit, shots=1024)
    counts = result.result().measurement_counts
    
    print("Results:")
    for state, count in sorted(counts.items()):
        probability = count / 1024
        bar = "█" * int(probability * 50)
        print(f"  |{state}⟩: {count:4d} times ({probability:5.1%}) {bar}")
    
    print("\nExpected Results:")
    for state, prob in circuit_data.get('expected_results', {}).items():
        if isinstance(prob, float):
            print(f"  |{state}⟩: {prob:.1%}")
        else:
            print(f"  {state}: {prob}")
    
    print("\n" + "-" * 60)

def main():
    """Run all demo scenarios."""
    print_header("QuantumViz Agent - Demo Scenarios")
    print("This demo shows quantum circuit simulations without AWS credentials.")
    print("All simulations run locally using Amazon Braket Local Simulator.")
    
    # Load sample circuits
    demo_dir = os.path.dirname(os.path.abspath(__file__))
    circuits_file = os.path.join(demo_dir, 'sample_circuits.json')
    
    with open(circuits_file, 'r') as f:
        circuits = json.load(f)
    
    # Run each demo
    for circuit_name, circuit_data in circuits.items():
        print_header(f"Demo: {circuit_data['name']}")
        run_circuit_demo(circuit_data['name'], circuit_data)
        
        input("\nPress Enter to continue to next demo...")
    
    print_header("Demo Complete!")
    print("Key Takeaways:")
    print("  1. Bell State shows perfect quantum entanglement (50/50 split)")
    print("  2. Superposition demonstrates quantum probability")
    print("  3. GHZ State extends entanglement to 3 qubits")
    print("  4. Quantum Teleportation transfers quantum states")
    print("\nFor more demos, see DEMO_GUIDE.md")
    print("To run with real quantum hardware, configure AWS credentials.")

if __name__ == "__main__":
    main()
