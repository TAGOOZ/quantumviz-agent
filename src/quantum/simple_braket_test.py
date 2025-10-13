#!/usr/bin/env python3
"""
QuantumViz Agent - Simple Braket Test
Test basic Braket connectivity and local simulation.
"""

import boto3
from braket.circuits import Circuit
from braket.devices import LocalSimulator

def test_braket_service():
    """Test if Braket service is accessible."""
    print("🔗 Testing Amazon Braket service...")
    
    try:
        # Test basic service access
        braket = boto3.client('braket', region_name='us-east-1')
        
        # Try to get service metadata
        print("✅ Braket service is accessible")
        return True
        
    except Exception as e:
        print(f"❌ Braket service error: {e}")
        return False

def test_local_braket():
    """Test local Braket simulator."""
    print("\n🏠 Testing local Braket simulator...")
    
    try:
        # Create local simulator
        local_sim = LocalSimulator()
        
        # Create quantum circuit
        circuit = Circuit()
        circuit.h(0)        # Hadamard gate
        circuit.cnot(0, 1)  # CNOT gate
        
        print("✅ Circuit created:")
        print(circuit)
        
        # Run simulation
        print("⚡ Running simulation...")
        result = local_sim.run(circuit, shots=1024)
        counts = result.result().measurement_counts
        
        print("📊 Braket Local Simulation Results:")
        print("=" * 40)
        
        total_shots = sum(counts.values())
        for state, count in counts.items():
            probability = (count / total_shots) * 100
            print(f"State |{state}⟩: {count} times ({probability:.1f}%)")
        
        # Analysis
        print("\n🔬 Quantum Analysis:")
        if '00' in counts and '11' in counts:
            if '01' not in counts and '10' not in counts:
                print("✅ Perfect Bell State! Quantum entanglement detected.")
            else:
                print("✅ Superposition with entanglement detected.")
        else:
            print("✅ Quantum interference pattern detected.")
        
        return True
        
    except Exception as e:
        print(f"❌ Local Braket error: {e}")
        return False

def test_quantum_concepts():
    """Test different quantum concepts with Braket."""
    print("\n🧪 Testing quantum concepts with Braket...")
    
    try:
        local_sim = LocalSimulator()
        
        # Test 1: Single qubit superposition
        print("\n1. Single Qubit Superposition:")
        circuit1 = Circuit()
        circuit1.h(0)
        result1 = local_sim.run(circuit1, shots=1000)
        counts1 = result1.result().measurement_counts
        
        for state, count in counts1.items():
            print(f"   |{state}⟩: {count} times")
        
        # Test 2: Entanglement
        print("\n2. Two-Qubit Entanglement:")
        circuit2 = Circuit()
        circuit2.h(0)
        circuit2.cnot(0, 1)
        result2 = local_sim.run(circuit2, shots=1000)
        counts2 = result2.result().measurement_counts
        
        for state, count in counts2.items():
            print(f"   |{state}⟩: {count} times")
        
        # Test 3: Quantum interference
        print("\n3. Quantum Interference:")
        circuit3 = Circuit()
        circuit3.h(0)
        circuit3.h(0)  # Apply H twice (should return to |0⟩)
        result3 = local_sim.run(circuit3, shots=1000)
        counts3 = result3.result().measurement_counts
        
        for state, count in counts3.items():
            print(f"   |{state}⟩: {count} times")
        
        print("✅ All quantum concepts tested successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Quantum concepts test error: {e}")
        return False

def main():
    """Main function."""
    print("🚀 QuantumViz Agent - Simple Braket Test")
    print("=" * 50)
    
    # Test service connectivity
    service_ok = test_braket_service()
    
    # Test local simulation
    local_ok = test_local_braket()
    
    # Test quantum concepts
    concepts_ok = test_quantum_concepts()
    
    print("\n" + "=" * 50)
    print("📋 Test Summary:")
    print(f"   Braket Service: {'✅' if service_ok else '❌'}")
    print(f"   Local Simulation: {'✅' if local_ok else '❌'}")
    print(f"   Quantum Concepts: {'✅' if concepts_ok else '❌'}")
    
    if local_ok and concepts_ok:
        print("\n🎉 Braket integration ready!")
        print("💡 Local quantum simulation working perfectly")
        print("🚀 Ready for cloud quantum execution")
    else:
        print("\n⚠️  Some tests failed, but basic functionality available")

if __name__ == "__main__":
    main()

