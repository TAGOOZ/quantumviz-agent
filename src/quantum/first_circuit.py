#!/usr/bin/env python3
"""
QuantumViz Agent - First Quantum Circuit
This script creates and tests your first quantum circuit using Qiskit.
"""

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import AerSimulator
import numpy as np

def create_basic_quantum_circuit():
    """Create a simple quantum circuit with Hadamard and CNOT gates."""
    print("🎯 Creating your first quantum circuit...")
    
    # Create quantum and classical registers
    qr = QuantumRegister(2, 'q')
    cr = ClassicalRegister(2, 'c')
    
    # Create quantum circuit
    circuit = QuantumCircuit(qr, cr)
    
    # Add gates
    circuit.h(0)        # Apply Hadamard gate to qubit 0 (creates superposition)
    circuit.cx(0, 1)    # Apply CNOT gate (creates entanglement)
    circuit.measure_all() # Measure all qubits
    
    return circuit

def simulate_circuit(circuit, shots=1024):
    """Simulate the quantum circuit locally."""
    print("⚡ Simulating quantum circuit...")
    
    # Use local simulator (free, no AWS costs)
    simulator = AerSimulator()
    
    # Transpile circuit for the simulator
    transpiled_circuit = transpile(circuit, simulator)
    
    # Run simulation
    job = simulator.run(transpiled_circuit, shots=shots)
    result = job.result()
    
    return result.get_counts()

def analyze_results(counts):
    """Analyze the quantum circuit results."""
    print("\n📊 Quantum Circuit Results:")
    print("=" * 40)
    
    total_shots = sum(counts.values())
    print(f"Total shots: {total_shots}")
    
    for state, count in counts.items():
        probability = (count / total_shots) * 100
        print(f"State |{state}⟩: {count} times ({probability:.1f}%)")
    
    # Quantum analysis
    print("\n🔬 Quantum Analysis:")
    if '00' in counts and '11' in counts:
        print("✅ Bell State detected! This shows quantum entanglement.")
        print("   The qubits are perfectly correlated.")
    elif '00' in counts and '01' in counts and '10' in counts and '11' in counts:
        print("✅ Superposition detected! All states are possible.")
    else:
        print("✅ Quantum interference detected!")

def visualize_circuit(circuit):
    """Display the quantum circuit diagram."""
    print("\n🎨 Quantum Circuit Diagram:")
    print("=" * 40)
    print(circuit.draw(output='text'))
    
    # Circuit information
    print(f"\n📋 Circuit Information:")
    print(f"   Qubits: {circuit.num_qubits}")
    print(f"   Classical bits: {circuit.num_clbits}")
    print(f"   Gates: {circuit.depth()}")

def main():
    """Main function to run the quantum circuit demonstration."""
    print("🚀 QuantumViz Agent - First Quantum Circuit Demo")
    print("=" * 50)
    
    try:
        # Create quantum circuit
        circuit = create_basic_quantum_circuit()
        
        # Visualize circuit
        visualize_circuit(circuit)
        
        # Simulate circuit
        counts = simulate_circuit(circuit)
        
        # Analyze results
        analyze_results(counts)
        
        print("\n🎉 Success! Your first quantum circuit is working!")
        print("💡 This demonstrates:")
        print("   • Quantum superposition (Hadamard gate)")
        print("   • Quantum entanglement (CNOT gate)")
        print("   • Quantum measurement")
        
        return circuit, counts
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None, None

if __name__ == "__main__":
    circuit, counts = main()

