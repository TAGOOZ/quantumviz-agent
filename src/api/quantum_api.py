#!/usr/bin/env python3
"""
QuantumViz Agent - REST API
RESTful API for quantum circuit processing and visualization.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import numpy as np
from braket.circuits import Circuit
from braket.devices import LocalSimulator
from src.algorithms.quantum_algorithms import QuantumAlgorithms
from src.visualization.simple_3d_viz import QuantumVisualizer
import boto3
import os

app = Flask(__name__)
CORS(app)

# Initialize services
simulator = LocalSimulator()
algorithms = QuantumAlgorithms()
visualizer = QuantumVisualizer()

# AWS clients
bedrock_client = boto3.client('bedrock-runtime', region_name='eu-central-1')
s3_client = boto3.client('s3', region_name='eu-central-1')

class QuantumAPI:
    """REST API for quantum processing."""
    
    @app.route('/api/health', methods=['GET'])
    def health_check():
        """Health check endpoint."""
        return jsonify({
            'status': 'healthy',
            'service': 'QuantumViz Agent API',
            'version': '1.0.0'
        })
    
    @app.route('/api/circuit/simulate', methods=['POST'])
    def simulate_circuit():
        """Simulate quantum circuit."""
        try:
            data = request.json
            circuit_data = data.get('circuit', {})
            
            # Create circuit from JSON
            circuit = Circuit()
            for gate in circuit_data.get('gates', []):
                gate_type = gate['type']
                qubit = gate['qubit']
                target = gate.get('target')
                
                if gate_type == 'H':
                    circuit.h(qubit)
                elif gate_type == 'X':
                    circuit.x(qubit)
                elif gate_type == 'Y':
                    circuit.y(qubit)
                elif gate_type == 'Z':
                    circuit.z(qubit)
                elif gate_type == 'CNOT':
                    circuit.cnot(qubit, target)
                elif gate_type == 'CZ':
                    circuit.cz(qubit, target)
                elif gate_type == 'SWAP':
                    circuit.swap(qubit, target)
            
            # Run simulation
            result = simulator.run(circuit, shots=1024)
            counts = result.result().measurement_counts
            
            return jsonify({
                'status': 'success',
                'results': counts,
                'circuit_depth': len(circuit.instructions),
                'qubit_count': circuit.qubit_count
            })
            
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)})
    
    @app.route('/api/algorithms/grover', methods=['POST'])
    def grover_search():
        """Run Grover's search algorithm."""
        try:
            data = request.json
            search_space = data.get('search_space', 8)
            targets = data.get('targets', [3, 5])
            iterations = data.get('iterations')
            
            result = algorithms.grover_search(search_space, targets, iterations)
            
            return jsonify({
                'status': 'success',
                'results': result['results'],
                'success_rate': result['success_rate'],
                'iterations': result['iterations']
            })
            
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)})
    
    @app.route('/api/algorithms/shor', methods=['POST'])
    def shor_factorization():
        """Run Shor's factorization algorithm."""
        try:
            data = request.json
            n = data.get('number', 15)
            a = data.get('random_base', 7)
            
            result = algorithms.shor_algorithm(n, a)
            
            return jsonify({
                'status': 'success',
                'results': result['results'],
                'period': result['period'],
                'factors': result['factors']
            })
            
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)})
    
    @app.route('/api/algorithms/vqe', methods=['POST'])
    def vqe_optimization():
        """Run VQE optimization."""
        try:
            data = request.json
            hamiltonian_matrix = data.get('hamiltonian', [[1, 0], [0, -1]])
            depth = data.get('ansatz_depth', 3)
            
            hamiltonian = np.array(hamiltonian_matrix)
            result = algorithms.vqe_optimization(hamiltonian, depth)
            
            return jsonify({
                'status': 'success',
                'ground_state_energy': result['ground_state_energy'],
                'expectation_value': result['expectation_value'],
                'ansatz_depth': result['ansatz_depth']
            })
            
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)})
    
    @app.route('/api/visualize/bloch', methods=['POST'])
    def visualize_bloch_sphere():
        """Create Bloch sphere visualization."""
        try:
            data = request.json
            qubit_state = data.get('qubit_state', [1, 0])  # |0⟩ state
            
            # Create visualization
            html_content = visualizer.create_bloch_sphere_visualization(qubit_state)
            
            # Save to S3
            s3_key = f"visualizations/bloch_sphere_{np.random.randint(1000, 9999)}.html"
            s3_client.put_object(
                Bucket='quantumviz-agent-assets',
                Key=s3_key,
                Body=html_content,
                ContentType='text/html'
            )
            
            return jsonify({
                'status': 'success',
                'visualization_url': f"https://quantumviz-agent-assets.s3.eu-central-1.amazonaws.com/{s3_key}",
                's3_key': s3_key
            })
            
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)})
    
    @app.route('/api/visualize/circuit', methods=['POST'])
    def visualize_circuit():
        """Create circuit visualization."""
        try:
            data = request.json
            circuit_data = data.get('circuit', {})
            
            # Create circuit visualization
            html_content = visualizer.create_circuit_analysis_visualization(circuit_data)
            
            # Save to S3
            s3_key = f"visualizations/circuit_analysis_{np.random.randint(1000, 9999)}.html"
            s3_client.put_object(
                Bucket='quantumviz-agent-assets',
                Key=s3_key,
                Body=html_content,
                ContentType='text/html'
            )
            
            return jsonify({
                'status': 'success',
                'visualization_url': f"https://quantumviz-agent-assets.s3.eu-central-1.amazonaws.com/{s3_key}",
                's3_key': s3_key
            })
            
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)})
    
    @app.route('/api/ai/explain', methods=['POST'])
    def ai_explanation():
        """Get AI explanation of quantum concept."""
        try:
            data = request.json
            concept = data.get('concept', 'quantum superposition')
            level = data.get('level', 'beginner')
            
            # Create prompt for Claude
            prompt = f"""
            Explain the quantum concept '{concept}' for a {level} audience.
            Include:
            1. Simple definition
            2. Real-world analogy
            3. Mathematical representation
            4. Why it's important for quantum computing
            
            Keep it concise and engaging.
            """
            
            # Call Claude via Bedrock
            response = bedrock_client.invoke_model(
                modelId='anthropic.claude-3-5-sonnet-20241022-v2:0',
                body=json.dumps({
                    'prompt': prompt,
                    'max_tokens': 500,
                    'temperature': 0.7
                })
            )
            
            explanation = json.loads(response['body'].read())['completion']
            
            return jsonify({
                'status': 'success',
                'explanation': explanation,
                'concept': concept,
                'level': level
            })
            
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)})
    
    @app.route('/api/education/modules', methods=['GET'])
    def get_education_modules():
        """Get available education modules."""
        modules = [
            {
                'id': 'superposition',
                'title': 'Quantum Superposition',
                'description': 'Learn about quantum superposition and the double-slit experiment',
                'difficulty': 'beginner',
                'duration': '15 minutes'
            },
            {
                'id': 'entanglement',
                'title': 'Quantum Entanglement',
                'description': 'Understand quantum entanglement and Bell states',
                'difficulty': 'intermediate',
                'duration': '20 minutes'
            },
            {
                'id': 'algorithms',
                'title': 'Quantum Algorithms',
                'description': 'Explore Grover\'s search and Shor\'s factorization',
                'difficulty': 'advanced',
                'duration': '30 minutes'
            },
            {
                'id': 'teleportation',
                'title': 'Quantum Teleportation',
                'description': 'Learn about quantum teleportation protocol',
                'difficulty': 'intermediate',
                'duration': '25 minutes'
            }
        ]
        
        return jsonify({
            'status': 'success',
            'modules': modules
        })
    
    @app.route('/api/education/module/<module_id>', methods=['GET'])
    def get_education_module(module_id):
        """Get specific education module content."""
        modules = {
            'superposition': {
                'title': 'Quantum Superposition',
                'content': {
                    'theory': 'Quantum superposition is the fundamental principle that quantum particles can exist in multiple states simultaneously.',
                    'experiment': 'Double-slit experiment demonstrates wave-particle duality.',
                    'mathematics': '|ψ⟩ = α|0⟩ + β|1⟩ where |α|² + |β|² = 1',
                    'visualization': 'Bloch sphere representation of qubit states'
                },
                'interactive_demo': '/api/visualize/bloch',
                'quiz': [
                    {
                        'question': 'What is quantum superposition?',
                        'options': ['A', 'B', 'C', 'D'],
                        'correct': 'A'
                    }
                ]
            },
            'entanglement': {
                'title': 'Quantum Entanglement',
                'content': {
                    'theory': 'Quantum entanglement is a phenomenon where particles become correlated and share quantum states.',
                    'experiment': 'Bell test experiments prove quantum non-locality.',
                    'mathematics': '|Φ⁺⟩ = (|00⟩ + |11⟩)/√2',
                    'visualization': 'Bell state visualization and measurement correlations'
                },
                'interactive_demo': '/api/algorithms/teleportation',
                'quiz': [
                    {
                        'question': 'What is quantum entanglement?',
                        'options': ['A', 'B', 'C', 'D'],
                        'correct': 'A'
                    }
                ]
            }
        }
        
        if module_id not in modules:
            return jsonify({'status': 'error', 'message': 'Module not found'})
        
        return jsonify({
            'status': 'success',
            'module': modules[module_id]
        })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
