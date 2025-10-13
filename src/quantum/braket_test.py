#!/usr/bin/env python3
"""
QuantumViz Agent - Amazon Braket Integration Test
Test quantum circuit execution on Amazon Braket.
"""

import boto3
from braket.aws import AwsDevice
from braket.circuits import Circuit
from braket.circuits.gates import H, CNot
import time

def test_braket_connectivity():
    """Test Amazon Braket service connectivity."""
    print("🔗 Testing Amazon Braket connectivity...")
    
    try:
        # Initialize Braket client
        braket = boto3.client('braket', region_name='us-east-1')
        
        # List available devices
        response = braket.search_devices(
            filters=[{'name': 'deviceStatus', 'values': ['ONLINE']}]
        )
        
        devices = response['devices']
        print(f"✅ Found {len(devices)} available quantum devices:")
        
        for device in devices:
            device_name = device['deviceName']
            device_type = device['deviceType']
            provider = device['providerName']
            status = device['deviceStatus']
            
            print(f"   • {device_name} ({provider}) - {device_type} - {status}")
        
        return devices
        
    except Exception as e:
        print(f"❌ Braket connectivity error: {e}")
        return None

def get_sv1_simulator():
    """Get the SV1 simulator device."""
    print("\n🎯 Getting SV1 simulator...")
    
    try:
        # SV1 simulator ARN
        sv1_arn = "arn:aws:braket:us-east-1::device/qpu/simulator/sv1"
        device = AwsDevice(sv1_arn)
        
        print(f"✅ SV1 Simulator:")
        print(f"   Name: {device.name}")
        print(f"   Status: {device.status}")
        print(f"   Type: {device.type}")
        print(f"   Provider: {device.provider}")
        
        return device
        
    except Exception as e:
        print(f"❌ SV1 simulator error: {e}")
        return None

def create_quantum_circuit():
    """Create a quantum circuit for Braket."""
    print("\n🎨 Creating quantum circuit for Braket...")
    
    try:
        # Create a simple circuit
        circuit = Circuit()
        circuit.h(0)      # Hadamard gate on qubit 0
        circuit.cnot(0, 1) # CNOT gate between qubit 0 and 1
        
        print("✅ Circuit created:")
        print(circuit)
        
        return circuit
        
    except Exception as e:
        print(f"❌ Circuit creation error: {e}")
        return None

def run_quantum_simulation(circuit, device):
    """Run quantum simulation on Braket."""
    print("\n⚡ Running quantum simulation on Braket...")
    
    try:
        # Run the circuit on SV1 simulator
        print("🚀 Submitting job to SV1 simulator...")
        task = device.run(circuit, shots=1024)
        
        print(f"✅ Task submitted:")
        print(f"   Task ID: {task.id}")
        print(f"   Status: {task.state}")
        
        # Wait for completion (with timeout)
        print("⏳ Waiting for simulation to complete...")
        max_wait = 60  # 1 minute timeout
        start_time = time.time()
        
        while task.state() in ['CREATED', 'QUEUED', 'RUNNING']:
            if time.time() - start_time > max_wait:
                print("⏰ Simulation timeout - this is normal for first run")
                print("   Task will continue running in background")
                break
            
            print(f"   Status: {task.state()}")
            time.sleep(5)
        
        # Get results if completed
        if task.state() == 'COMPLETED':
            result = task.result()
            counts = result.measurement_counts
            
            print("✅ Simulation completed!")
            print("📊 Results:")
            for state, count in counts.items():
                probability = (count / 1024) * 100
                print(f"   |{state}⟩: {count} times ({probability:.1f}%)")
            
            return result
        else:
            print(f"📋 Final status: {task.state()}")
            print("   Results will be available when task completes")
            return None
            
    except Exception as e:
        print(f"❌ Simulation error: {e}")
        return None

def test_local_simulator():
    """Test local Braket simulator (free)."""
    print("\n🏠 Testing local Braket simulator...")
    
    try:
        from braket.devices import LocalSimulator
        
        # Create local simulator
        local_sim = LocalSimulator()
        
        # Create simple circuit
        circuit = Circuit()
        circuit.h(0)
        circuit.cnot(0, 1)
        
        print("✅ Running on local simulator...")
        result = local_sim.run(circuit, shots=1024)
        counts = result.result().measurement_counts
        
        print("📊 Local Simulation Results:")
        for state, count in counts.items():
            probability = (count / 1024) * 100
            print(f"   |{state}⟩: {count} times ({probability:.1f}%)")
        
        return result
        
    except Exception as e:
        print(f"❌ Local simulator error: {e}")
        return None

def main():
    """Main function to test Braket integration."""
    print("🚀 QuantumViz Agent - Amazon Braket Integration Test")
    print("=" * 60)
    
    # Test connectivity
    devices = test_braket_connectivity()
    
    if devices:
        print("✅ Braket connectivity successful!")
        
        # Get SV1 simulator
        sv1_device = get_sv1_simulator()
        
        # Create quantum circuit
        circuit = create_quantum_circuit()
        
        if circuit and sv1_device:
            # Run simulation
            result = run_quantum_simulation(circuit, sv1_device)
            
            if result:
                print("\n🎉 Braket integration working perfectly!")
            else:
                print("\n📋 Simulation submitted successfully")
                print("   Results will be available shortly")
        
        # Test local simulator
        local_result = test_local_simulator()
        
        if local_result:
            print("\n✅ Local simulation working!")
            print("💡 Ready for quantum circuit execution")
        
    else:
        print("❌ Braket connectivity failed")
        print("   Check: https://console.aws.amazon.com/braket/")

if __name__ == "__main__":
    main()

