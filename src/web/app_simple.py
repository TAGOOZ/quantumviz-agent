#!/usr/bin/env python3
"""
QuantumViz Agent - Simple Demo Version
Minimal Flask app for demo purposes.
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
import random

app = Flask(__name__)
CORS(app, origins=["*"])

# Simple in-memory circuit storage
current_circuit = []

@app.route('/')
def index():
    return jsonify({
        'message': 'QuantumViz Agent API',
        'status': 'running',
        'endpoints': ['/api/health', '/api/add_gate', '/api/simulate', '/api/reset']
    })

@app.route('/api/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'QuantumViz Agent API',
        'version': '1.0.0',
        'aws_available': False,
        'gemini_available': False
    })

@app.route('/api/add_gate', methods=['POST', 'OPTIONS'])
def add_gate():
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        data = request.json
        gate_type = data.get('gate_type')
        qubit = data.get('qubit')
        target = data.get('target')
        
        # Add gate to circuit
        gate = {'type': gate_type, 'qubit': qubit}
        if target is not None:
            gate['target'] = target
        
        current_circuit.append(gate)
        
        # Generate simple circuit representation
        circuit_str = f"Circuit with {len(current_circuit)} gates:\n"
        for i, gate in enumerate(current_circuit):
            if 'target' in gate:
                circuit_str += f"  {i+1}. {gate['type']} q{gate['qubit']} -> q{gate['target']}\n"
            else:
                circuit_str += f"  {i+1}. {gate['type']} q{gate['qubit']}\n"
        
        return jsonify({
            'status': 'success',
            'circuit': circuit_str,
            'gate_count': len(current_circuit)
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

@app.route('/api/simulate', methods=['POST', 'OPTIONS'])
def simulate():
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        if not current_circuit:
            return jsonify({
                'status': 'error',
                'message': 'No gates in circuit'
            }), 400
        
        # Simple simulation - generate random results based on circuit
        results = {}
        
        # Determine number of qubits
        max_qubit = 0
        for gate in current_circuit:
            max_qubit = max(max_qubit, gate['qubit'])
            if 'target' in gate:
                max_qubit = max(max_qubit, gate['target'])
        
        n_qubits = max_qubit + 1
        
        # Generate realistic quantum results
        if any(gate['type'] == 'H' and any(g['type'] == 'CNOT' for g in current_circuit) for gate in current_circuit):
            # Bell state pattern
            results['00'] = random.randint(480, 520)
            results['11'] = 1024 - results['00']
        elif any(gate['type'] == 'H' for gate in current_circuit):
            # Superposition
            for i in range(2**n_qubits):
                state = format(i, f'0{n_qubits}b')
                results[state] = random.randint(200, 300)
        else:
            # Classical states
            results['0' * n_qubits] = 1024
        
        # Create simple visualization data
        states = list(results.keys())
        counts = list(results.values())
        
        visualization = {
            'data': [{
                'x': states,
                'y': counts,
                'type': 'bar',
                'marker': {'color': '#4ECDC4'}
            }],
            'layout': {
                'title': 'Quantum Measurement Results',
                'xaxis': {'title': 'Quantum States'},
                'yaxis': {'title': 'Counts'}
            }
        }
        
        return jsonify({
            'status': 'success',
            'results': results,
            'visualization': json.dumps(visualization),
            'gate_count': len(current_circuit),
            'qubit_count': n_qubits
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

@app.route('/api/reset', methods=['POST', 'OPTIONS'])
def reset():
    if request.method == 'OPTIONS':
        return '', 200
    
    global current_circuit
    current_circuit = []
    
    return jsonify({
        'status': 'success',
        'message': 'Circuit reset'
    })

@app.route('/api/ai/explain', methods=['POST', 'OPTIONS'])
def ai_explain():
    if request.method == 'OPTIONS':
        return '', 200
    
    if not current_circuit:
        return jsonify({
            'status': 'error',
            'message': 'No circuit to explain'
        }), 400
    
    # Simple AI explanation based on gates
    explanation = "🤖 QuantumViz AI Analysis\n\n"
    explanation += f"📊 Circuit Overview:\n"
    explanation += f"   • {len(current_circuit)} quantum gates\n"
    explanation += f"   • Quantum circuit simulation\n\n"
    
    gate_types = [gate['type'] for gate in current_circuit]
    
    if 'H' in gate_types:
        explanation += "✓ Hadamard (H) gates: Create quantum superposition\n"
    if 'CNOT' in gate_types:
        explanation += "✓ CNOT gates: Create quantum entanglement\n"
    if 'X' in gate_types:
        explanation += "✓ Pauli-X gates: Quantum NOT operation\n"
    
    explanation += "\n🔬 This circuit demonstrates fundamental quantum computing principles!"
    
    return jsonify({
        'status': 'success',
        'explanation': explanation
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)