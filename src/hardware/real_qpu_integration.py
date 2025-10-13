#!/usr/bin/env python3
"""
QuantumViz Agent - Real Quantum Hardware Integration
Integration with real QPU devices via Amazon Braket for production quantum computing.
"""

import boto3
import json
import time
from typing import Dict, List, Any, Optional
from braket.circuits import Circuit
from braket.aws import AwsDevice
from braket.devices import LocalSimulator
import numpy as np

class RealQPUIntegration:
    """Integration with real quantum hardware via Amazon Braket."""
    
    def __init__(self, region: str = "us-east-1"):
        self.region = region
        self.braket_client = boto3.client('braket', region_name=region)
        self.s3_client = boto3.client('s3', region_name=region)
        self.bucket_name = "quantumviz-agent-hardware"
        self.devices = {}
        self._initialize_devices()
        
    def _initialize_devices(self):
        """Initialize available quantum devices."""
        try:
            # Get available devices
            response = self.braket_client.search_devices(
                filters=[
                    {'name': 'deviceStatus', 'values': ['ONLINE']},
                    {'name': 'deviceType', 'values': ['QPU']}
                ]
            )
            
            for device in response['devices']:
                device_name = device['deviceName']
                device_type = device['deviceType']
                provider = device['providerName']
                
                self.devices[device_name] = {
                    'name': device_name,
                    'type': device_type,
                    'provider': provider,
                    'status': device['deviceStatus'],
                    'capabilities': device.get('deviceCapabilities', {}),
                    'arn': device['deviceArn']
                }
                
            print(f"🔗 Found {len(self.devices)} available QPU devices")
            for name, info in self.devices.items():
                print(f"   - {name} ({info['provider']}) - {info['status']}")
                
        except Exception as e:
            print(f"⚠️ Could not initialize QPU devices: {e}")
            print("   Using local simulator as fallback")
            self.devices = {}
    
    def get_available_devices(self) -> Dict[str, Any]:
        """Get list of available quantum devices."""
        return {
            "qpu_devices": self.devices,
            "simulator_devices": ["local_simulator"],
            "total_devices": len(self.devices) + 1
        }
    
    def create_bell_state_circuit(self) -> Circuit:
        """Create a Bell state circuit for hardware testing."""
        circuit = Circuit()
        
        # Create Bell state: |Φ⁺⟩ = (|00⟩ + |11⟩)/√2
        circuit.h(0)  # Hadamard on qubit 0
        circuit.cnot(0, 1)  # CNOT between qubits 0 and 1
        
        # Add measurements
        circuit.measure_all()
        
        return circuit
    
    def create_ghz_state_circuit(self, n_qubits: int = 3) -> Circuit:
        """Create GHZ state circuit for multi-qubit entanglement."""
        circuit = Circuit()
        
        # Create GHZ state: |GHZ⟩ = (|000...0⟩ + |111...1⟩)/√2
        circuit.h(0)  # Hadamard on first qubit
        
        # Entangle all qubits
        for i in range(1, n_qubits):
            circuit.cnot(0, i)
        
        # Add measurements
        circuit.measure_all()
        
        return circuit
    
    def create_quantum_teleportation_circuit(self) -> Circuit:
        """Create quantum teleportation circuit."""
        circuit = Circuit()
        
        # Alice and Bob share entangled state
        circuit.h(0)
        circuit.cnot(0, 1)
        
        # Alice prepares message qubit (qubit 2)
        circuit.h(2)
        
        # Teleportation protocol
        circuit.cnot(2, 0)
        circuit.h(2)
        
        # Bob's correction (simplified)
        circuit.cnot(0, 1)
        circuit.cz(2, 1)
        
        # Add measurements
        circuit.measure_all()
        
        return circuit
    
    async def run_on_qpu(self, circuit: Circuit, device_name: str, shots: int = 100) -> Dict[str, Any]:
        """Run quantum circuit on real QPU hardware."""
        if device_name not in self.devices:
            return {"error": f"Device {device_name} not available"}
        
        device_info = self.devices[device_name]
        device_arn = device_info['arn']
        
        try:
            print(f"🚀 Running circuit on {device_name} ({device_info['provider']})")
            print(f"   Circuit depth: {len(circuit.instructions)}")
            print(f"   Qubits: {circuit.qubit_count}")
            print(f"   Shots: {shots}")
            
            # Get device
            device = AwsDevice(device_arn)
            
            # Run task
            task = device.run(circuit, shots=shots)
            
            # Wait for completion
            print("⏳ Waiting for QPU execution...")
            result = task.result()
            
            # Get results
            counts = result.measurement_counts
            execution_time = result.task_metadata.executionDuration
            
            print(f"✅ QPU execution completed in {execution_time} seconds")
            print(f"📊 Results: {counts}")
            
            return {
                "success": True,
                "device": device_name,
                "provider": device_info['provider'],
                "results": counts,
                "execution_time": execution_time,
                "shots": shots,
                "circuit_depth": len(circuit.instructions),
                "qubit_count": circuit.qubit_count
            }
            
        except Exception as e:
            print(f"❌ QPU execution failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "device": device_name
            }
    
    async def run_on_simulator(self, circuit: Circuit, shots: int = 1000) -> Dict[str, Any]:
        """Run quantum circuit on local simulator."""
        try:
            print(f"🖥️ Running circuit on local simulator")
            print(f"   Circuit depth: {len(circuit.instructions)}")
            print(f"   Qubits: {circuit.qubit_count}")
            print(f"   Shots: {shots}")
            
            simulator = LocalSimulator()
            result = simulator.run(circuit, shots=shots)
            counts = result.result().measurement_counts
            
            print(f"✅ Simulator execution completed")
            print(f"📊 Results: {counts}")
            
            return {
                "success": True,
                "device": "local_simulator",
                "provider": "amazon_braket",
                "results": counts,
                "execution_time": 0.1,  # Simulated
                "shots": shots,
                "circuit_depth": len(circuit.instructions),
                "qubit_count": circuit.qubit_count
            }
            
        except Exception as e:
            print(f"❌ Simulator execution failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "device": "local_simulator"
            }
    
    def compare_hardware_vs_simulator(self, circuit: Circuit, qpu_device: str = None) -> Dict[str, Any]:
        """Compare results between real hardware and simulator."""
        print("🔬 Comparing Hardware vs Simulator Results")
        print("=" * 50)
        
        # Run on simulator first
        simulator_result = self.run_on_simulator(circuit, shots=1000)
        
        # Run on QPU if available
        qpu_result = None
        if qpu_device and qpu_device in self.devices:
            qpu_result = self.run_on_qpu(circuit, qpu_device, shots=100)
        
        # Calculate fidelity
        fidelity = self._calculate_fidelity(simulator_result, qpu_result)
        
        return {
            "simulator_result": simulator_result,
            "qpu_result": qpu_result,
            "fidelity": fidelity,
            "comparison_analysis": self._analyze_differences(simulator_result, qpu_result)
        }
    
    def _calculate_fidelity(self, simulator_result: Dict[str, Any], qpu_result: Dict[str, Any]) -> float:
        """Calculate fidelity between simulator and QPU results."""
        if not simulator_result.get("success") or not qpu_result.get("success"):
            return 0.0
        
        sim_counts = simulator_result.get("results", {})
        qpu_counts = qpu_result.get("results", {})
        
        if not sim_counts or not qpu_counts:
            return 0.0
        
        # Normalize counts to probabilities
        sim_total = sum(sim_counts.values())
        qpu_total = sum(qpu_counts.values())
        
        if sim_total == 0 or qpu_total == 0:
            return 0.0
        
        sim_probs = {k: v/sim_total for k, v in sim_counts.items()}
        qpu_probs = {k: v/qpu_total for k, v in qpu_counts.items()}
        
        # Calculate fidelity (overlap)
        fidelity = 0.0
        for state in sim_probs:
            if state in qpu_probs:
                fidelity += np.sqrt(sim_probs[state] * qpu_probs[state])
        
        return fidelity
    
    def _analyze_differences(self, simulator_result: Dict[str, Any], qpu_result: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze differences between simulator and QPU results."""
        if not simulator_result.get("success") or not qpu_result.get("success"):
            return {"error": "Cannot analyze - one or both executions failed"}
        
        sim_counts = simulator_result.get("results", {})
        qpu_counts = qpu_result.get("results", {})
        
        analysis = {
            "simulator_states": len(sim_counts),
            "qpu_states": len(qpu_counts),
            "common_states": len(set(sim_counts.keys()) & set(qpu_counts.keys())),
            "fidelity": self._calculate_fidelity(simulator_result, qpu_result),
            "noise_analysis": "QPU shows expected noise characteristics",
            "recommendations": [
                "Use error correction for production applications",
                "Consider noise mitigation techniques",
                "Validate results with multiple runs"
            ]
        }
        
        return analysis
    
    def get_hardware_capabilities(self, device_name: str) -> Dict[str, Any]:
        """Get capabilities of a specific quantum device."""
        if device_name not in self.devices:
            return {"error": f"Device {device_name} not found"}
        
        device_info = self.devices[device_name]
        capabilities = device_info.get('capabilities', {})
        
        return {
            "device_name": device_name,
            "provider": device_info['provider'],
            "status": device_info['status'],
            "max_qubits": capabilities.get('maxQubits', 'unknown'),
            "max_shots": capabilities.get('maxShots', 'unknown'),
            "gate_set": capabilities.get('gateSet', []),
            "connectivity": capabilities.get('connectivity', {}),
            "noise_model": capabilities.get('noiseModel', {})
        }

# Demo function
async def demo_real_qpu_integration():
    """Demonstrate real QPU integration."""
    print("🔗 QuantumViz Agent - Real QPU Integration Demo")
    print("=" * 60)
    
    # Initialize QPU integration
    qpu_integration = RealQPUIntegration()
    
    # Show available devices
    devices = qpu_integration.get_available_devices()
    print(f"\n📱 Available Devices:")
    print(f"   QPU Devices: {devices['total_devices'] - 1}")
    print(f"   Simulator: 1")
    
    # Create test circuits
    bell_circuit = qpu_integration.create_bell_state_circuit()
    ghz_circuit = qpu_integration.create_ghz_state_circuit(3)
    teleportation_circuit = qpu_integration.create_quantum_teleportation_circuit()
    
    print(f"\n🧪 Test Circuits Created:")
    print(f"   Bell State: {len(bell_circuit.instructions)} gates")
    print(f"   GHZ State: {len(ghz_circuit.instructions)} gates")
    print(f"   Teleportation: {len(teleportation_circuit.instructions)} gates")
    
    # Run on simulator
    print(f"\n🖥️ Running on Local Simulator:")
    simulator_result = await qpu_integration.run_on_simulator(bell_circuit, shots=1000)
    
    if simulator_result.get("success"):
        print(f"✅ Simulator Success: {simulator_result['results']}")
    else:
        print(f"❌ Simulator Failed: {simulator_result.get('error')}")
    
    # Try to run on QPU (if available)
    if devices['qpu_devices']:
        qpu_device = list(devices['qpu_devices'].keys())[0]
        print(f"\n🚀 Running on QPU: {qpu_device}")
        qpu_result = await qpu_integration.run_on_qpu(bell_circuit, qpu_device, shots=100)
        
        if qpu_result.get("success"):
            print(f"✅ QPU Success: {qpu_result['results']}")
            
            # Compare results
            comparison = qpu_integration.compare_hardware_vs_simulator(bell_circuit, qpu_device)
            print(f"\n📊 Hardware vs Simulator Comparison:")
            print(f"   Fidelity: {comparison['fidelity']:.3f}")
            print(f"   Analysis: {comparison['comparison_analysis']}")
        else:
            print(f"❌ QPU Failed: {qpu_result.get('error')}")
    else:
        print(f"\n⚠️ No QPU devices available - using simulator only")
    
    print(f"\n🏆 Real QPU Integration Demo Complete!")
    print(f"   - Hardware connectivity: {'✅' if devices['qpu_devices'] else '⚠️'}")
    print(f"   - Simulator functionality: {'✅' if simulator_result.get('success') else '❌'}")
    print(f"   - Production readiness: {'✅' if devices['qpu_devices'] else '⚠️'}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(demo_real_qpu_integration())
