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
        
        # Generate beautiful quantum circuit representation
        max_qubit = max(gate.get('target', gate['qubit']) for gate in current_circuit)
        n_qubits = max_qubit + 1
        
        circuit_str = f"Quantum Circuit ({len(current_circuit)} gates, {n_qubits} qubits):\n\n"
        
        # Create ASCII quantum circuit
        for q in range(n_qubits):
            line = f"q{q} |0⟩ ─"
            for gate in current_circuit:
                if gate['qubit'] == q:
                    if gate['type'] == 'H':
                        line += "─[H]─"
                    elif gate['type'] == 'X':
                        line += "─[X]─"
                    elif gate['type'] == 'Y':
                        line += "─[Y]─"
                    elif gate['type'] == 'Z':
                        line += "─[Z]─"
                    elif gate['type'] == 'CNOT' and 'target' in gate:
                        line += "─●───"
                    else:
                        line += "─────"
                elif 'target' in gate and gate['target'] == q:
                    line += "─⊕───"
                else:
                    line += "─────"
            circuit_str += line + "\n"
        
        circuit_str += f"\nGate Sequence:\n"
        for i, gate in enumerate(current_circuit):
            if 'target' in gate:
                circuit_str += f"  {i+1}. {gate['type']} q{gate['qubit']} → q{gate['target']}\n"
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
    
    # Detailed AI explanation based on gates
    gate_types = [gate['type'] for gate in current_circuit]
    max_qubit = max(gate.get('target', gate['qubit']) for gate in current_circuit)
    n_qubits = max_qubit + 1
    
    explanation = "🤖 QuantumViz AI Circuit Analysis\n\n"
    explanation += f"📊 Circuit Statistics:\n"
    explanation += f"   • {len(current_circuit)} quantum gates\n"
    explanation += f"   • {n_qubits} qubits involved\n"
    explanation += f"   • Circuit depth: {len(current_circuit)}\n\n"
    
    explanation += "🔬 Quantum Operations Detected:\n"
    
    if 'H' in gate_types and 'CNOT' in gate_types:
        explanation += "🎯 ENTANGLEMENT PATTERN DETECTED!\n"
        explanation += "   • This circuit creates quantum entanglement\n"
        explanation += "   • Bell state formation: |00⟩ + |11⟩ superposition\n"
        explanation += "   • Qubits become correlated - measuring one affects the other\n\n"
    
    if 'H' in gate_types:
        explanation += "✓ Hadamard (H) Gates:\n"
        explanation += "   • Creates quantum superposition: |0⟩ → (|0⟩ + |1⟩)/√2\n"
        explanation += "   • Enables quantum parallelism\n"
        explanation += "   • Foundation of quantum algorithms\n\n"
    
    if 'CNOT' in gate_types:
        explanation += "✓ CNOT Gates:\n"
        explanation += "   • Controlled-NOT operation\n"
        explanation += "   • Creates quantum entanglement between qubits\n"
        explanation += "   • Essential for quantum error correction\n\n"
    
    if 'X' in gate_types:
        explanation += "✓ Pauli-X Gates:\n"
        explanation += "   • Quantum NOT gate: |0⟩ ↔ |1⟩\n"
        explanation += "   • Bit-flip operation\n\n"
    
    if 'Y' in gate_types:
        explanation += "✓ Pauli-Y Gates:\n"
        explanation += "   • Combined bit-flip and phase-flip\n"
        explanation += "   • Rotation around Y-axis on Bloch sphere\n\n"
    
    if 'Z' in gate_types:
        explanation += "✓ Pauli-Z Gates:\n"
        explanation += "   • Phase-flip operation: |1⟩ → -|1⟩\n"
        explanation += "   • Leaves |0⟩ unchanged\n\n"
    
    explanation += "📈 Expected Measurement Results:\n"
    if 'H' in gate_types and 'CNOT' in gate_types:
        explanation += "   • 50% probability: |00⟩ state\n"
        explanation += "   • 50% probability: |11⟩ state\n"
        explanation += "   • Never: |01⟩ or |10⟩ (due to entanglement)\n"
    elif 'H' in gate_types:
        explanation += "   • Equal superposition of all computational basis states\n"
        explanation += "   • Demonstrates quantum randomness\n"
    
    explanation += "\n💡 Applications:\n"
    if 'CNOT' in gate_types:
        explanation += "   • Quantum cryptography (QKD)\n"
        explanation += "   • Quantum teleportation protocols\n"
        explanation += "   • Quantum error correction codes\n"
    
    explanation += "\n🎓 Educational Value:\n"
    explanation += "   • Demonstrates core quantum mechanics principles\n"
    explanation += "   • Shows difference from classical computing\n"
    explanation += "   • Foundation for understanding quantum algorithms"
    
    return jsonify({
        'status': 'success',
        'explanation': explanation
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)