#!/usr/bin/env python3
"""
QuantumViz Agent - Simple Quantum Circuit (No Aer dependency)
This script creates and tests a basic quantum circuit.
"""

import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

def create_simple_circuit():
    """Create a simple quantum circuit."""
    print("🎯 Creating simple quantum circuit...")
    
    # Create quantum and classical registers
    qr = QuantumRegister(2, 'q')
    cr = ClassicalRegister(2, 'c')
    
    # Create quantum circuit
    circuit = QuantumCircuit(qr, cr)
    
    # Add gates
    circuit.h(0)        # Apply Hadamard gate to qubit 0
    circuit.cx(0, 1)    # Apply CNOT gate
    circuit.measure_all() # Measure all qubits
    
    return circuit

def analyze_circuit(circuit):
    """Analyze the quantum circuit."""
    print("\n🎨 Quantum Circuit Diagram:")
    print("=" * 40)
    print(circuit.draw(output='text'))
    
    print(f"\n📋 Circuit Information:")
    print(f"   Qubits: {circuit.num_qubits}")
    print(f"   Classical bits: {circuit.num_clbits}")
    print(f"   Gates: {circuit.depth()}")
    
    print(f"\n🔬 Quantum Gates Used:")
    for instruction in circuit.data:
        gate_name = instruction.operation.name
        qubits = [circuit.qubits[i] for i in instruction.qubits]
        print(f"   {gate_name} on qubits {qubits}")

def explain_quantum_concepts():
    """Explain the quantum concepts in the circuit."""
    print("\n💡 Quantum Concepts Explained:")
    print("=" * 40)
    print("1. Hadamard Gate (H):")
    print("   • Creates quantum superposition")
    print("   • |0⟩ → (|0⟩ + |1⟩)/√2")
    print("   • Qubit exists in both states simultaneously")
    
    print("\n2. CNOT Gate (CX):")
    print("   • Creates quantum entanglement")
    print("   • If control qubit is |1⟩, target qubit flips")
    print("   • Creates correlated quantum states")
    
    print("\n3. Measurement:")
    print("   • Collapses quantum superposition")
    print("   • Returns classical bits (0 or 1)")
    print("   • Destroys quantum information")

def main():
    """Main function."""
    print("🚀 QuantumViz Agent - Simple Quantum Circuit")
    print("=" * 50)
    
    try:
        # Create circuit
        circuit = create_simple_circuit()
        
        # Analyze circuit
        analyze_circuit(circuit)
        
        # Explain concepts
        explain_quantum_concepts()
        
        print("\n🎉 Success! Your quantum circuit is ready!")
        print("💡 Next steps:")
        print("   • Add quantum simulation")
        print("   • Connect to Amazon Braket")
        print("   • Create 3D visualizations")
        
        return circuit
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    circuit = main()

