#!/usr/bin/env python3
"""
QuantumViz Agent - Web Interface
Interactive quantum circuit builder with real-time visualization.
"""

from flask import Flask, render_template, request, jsonify
import json
from braket.circuits import Circuit
from braket.devices import LocalSimulator
import plotly.graph_objects as go
import plotly.utils
import numpy as np

app = Flask(__name__)

class QuantumCircuitBuilder:
    """Interactive quantum circuit builder."""
    
    def __init__(self):
        self.simulator = LocalSimulator()
        self.circuit = Circuit()
        
    def add_gate(self, gate_type, qubit, target=None):
        """Add quantum gate to circuit."""
        if gate_type == 'H':
            self.circuit.h(qubit)
        elif gate_type == 'X':
            self.circuit.x(qubit)
        elif gate_type == 'Y':
            self.circuit.y(qubit)
        elif gate_type == 'Z':
            self.circuit.z(qubit)
        elif gate_type == 'CNOT':
            self.circuit.cnot(qubit, target)
        elif gate_type == 'CZ':
            self.circuit.cz(qubit, target)
        elif gate_type == 'SWAP':
            self.circuit.swap(qubit, target)
            
    def run_simulation(self, shots=1024):
        """Run quantum simulation."""
        result = self.simulator.run(self.circuit, shots=shots)
        counts = result.result().measurement_counts
        return counts
        
    def create_visualization(self, counts):
        """Create 3D visualization of results."""
        states = list(counts.keys())
        probabilities = [counts[state] / sum(counts.values()) for state in states]
        
        fig = go.Figure(data=[
            go.Bar(x=states, y=probabilities, 
                   marker_color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])
        ])
        
        fig.update_layout(
            title='Quantum Measurement Results',
            xaxis_title='Quantum States',
            yaxis_title='Probability',
            height=400
        )
        
        return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

# Initialize circuit builder
circuit_builder = QuantumCircuitBuilder()

@app.route('/')
def index():
    """Main quantum circuit builder interface."""
    return render_template('index.html')

@app.route('/api/add_gate', methods=['POST'])
def add_gate():
    """Add quantum gate to circuit."""
    data = request.json
    gate_type = data['gate_type']
    qubit = data['qubit']
    target = data.get('target')
    
    try:
        circuit_builder.add_gate(gate_type, qubit, target)
        return jsonify({'status': 'success', 'circuit': str(circuit_builder.circuit)})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/simulate', methods=['POST'])
def simulate():
    """Run quantum simulation."""
    try:
        counts = circuit_builder.run_simulation()
        visualization = circuit_builder.create_visualization(counts)
        return jsonify({
            'status': 'success',
            'results': counts,
            'visualization': visualization
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/reset', methods=['POST'])
def reset():
    """Reset quantum circuit."""
    circuit_builder.circuit = Circuit()
    return jsonify({'status': 'success', 'message': 'Circuit reset'})

@app.route('/api/circuit_info')
def circuit_info():
    """Get circuit information."""
    return jsonify({
        'qubits': circuit_builder.circuit.qubit_count,
        'gates': len(circuit_builder.circuit.instructions),
        'circuit': str(circuit_builder.circuit)
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
