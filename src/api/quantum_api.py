#!/usr/bin/env python3
"""
QuantumViz Agent - REST API
RESTful API for quantum circuit processing and visualization.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import numpy as np
import logging
from datetime import datetime
from braket.circuits import Circuit
from braket.devices import LocalSimulator
from src.algorithms.quantum_algorithms import QuantumAlgorithms
from src.visualization.simple_3d_viz import QuantumVisualizer
import boto3
import os
import sys
# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Request logging decorator
def log_request(f):
    def decorated_function(*args, **kwargs):
        logger.info(f"API Request: {request.method} {request.path} from {request.remote_addr}")
        start_time = datetime.now()
        
        result = f(*args, **kwargs)
        
        duration = (datetime.now() - start_time).total_seconds()
        logger.info(f"API Response: {request.path} completed in {duration:.3f}s")
        
        return result
    decorated_function.__name__ = f.__name__
    return decorated_function

# Simple authentication decorator
def require_api_key(f):
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        expected_key = os.getenv('API_KEY')
        
        # In production, you would use a more secure authentication method
        if expected_key and api_key != expected_key:
            logger.warning(f"Unauthorized API access attempt from {request.remote_addr}")
            return jsonify({'status': 'error', 'message': 'Invalid API key'}), 401
        
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

app = Flask(__name__)
CORS(app)

# Initialize services
simulator = LocalSimulator()
algorithms = QuantumAlgorithms()
visualizer = QuantumVisualizer()

# AWS clients
bedrock_client = boto3.client('bedrock-runtime', region_name=Config.AWS_REGION)
s3_client = boto3.client('s3', region_name=Config.AWS_REGION)

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
    @require_api_key
    @log_request
    def simulate_circuit():
        """Simulate quantum circuit."""
        try:
            data = request.json
            
            # Input validation
            if not data:
                return jsonify({'status': 'error', 'message': 'No data provided'}), 400
            
            circuit_data = data.get('circuit', {})
            if not isinstance(circuit_data, dict):
                return jsonify({'status': 'error', 'message': 'Invalid circuit data'}), 400
            
            gates = circuit_data.get('gates', [])
            if not isinstance(gates, list):
                return jsonify({'status': 'error', 'message': 'Invalid gates format'}), 400
            
            # Validate each gate
            valid_gates = ['H', 'X', 'Y', 'Z', 'CNOT', 'CZ', 'SWAP']
            for i, gate in enumerate(gates):
                if not isinstance(gate, dict):
                    return jsonify({'status': 'error', 'message': f'Invalid gate format at index {i}'}), 400
                
                gate_type = gate.get('type')
                if gate_type not in valid_gates:
                    return jsonify({'status': 'error', 'message': f'Invalid gate type \'{gate_type}\' at index {i}. Valid gates: {valid_gates}'}), 400
                
                qubit = gate.get('qubit')
                if not isinstance(qubit, int) or qubit < 0:
                    return jsonify({'status': 'error', 'message': f'Invalid qubit index at index {i}'}), 400
                
                target = gate.get('target')
                if target is not None and (not isinstance(target, int) or target < 0):
                    return jsonify({'status': 'error', 'message': f'Invalid target qubit index at index {i}'}), 400
            
            # Create circuit from JSON
            circuit = Circuit()
            for gate in gates:
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
            return jsonify({'status': 'error', 'message': str(e)}), 500
    
    @app.route('/api/algorithms/grover', methods=['POST'])
    @require_api_key
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
    @require_api_key
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
    @require_api_key
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
    
    @app.route('/api/algorithms/teleport', methods=['POST'])
    @require_api_key
    def quantum_teleportation():
        """Run quantum teleportation protocol."""
        try:
            data = request.json
            message_qubit = data.get('message_qubit', 2)
            
            result = algorithms.quantum_teleportation(message_qubit)
            
            return jsonify({
                'status': 'success',
                'results': result['results'],
                'teleportation_success': result['teleportation_success'],
                'protocol': 'quantum_teleportation'
            })
            
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)})
    
    @app.route('/api/visualize/bloch', methods=['POST'])
    @require_api_key
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
                Bucket=Config.S3_BUCKET_NAME,
                Key=s3_key,
                Body=html_content,
                ContentType='text/html'
            )
            
            return jsonify({
                'status': 'success',
                'visualization_url': f"https://{Config.S3_BUCKET_NAME}.s3.{Config.AWS_REGION}.amazonaws.com/{s3_key}",
                's3_key': s3_key
            })
            
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)})
    
    @app.route('/api/visualize/circuit', methods=['POST'])
    @require_api_key
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
                Bucket=Config.S3_BUCKET_NAME,
                Key=s3_key,
                Body=html_content,
                ContentType='text/html'
            )
            
            return jsonify({
                'status': 'success',
                'visualization_url': f"https://{Config.S3_BUCKET_NAME}.s3.{Config.AWS_REGION}.amazonaws.com/{s3_key}",
                's3_key': s3_key
            })
            
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)})
    
    @app.route('/api/ai/explain', methods=['POST'])
    @require_api_key
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
                modelId=Config.FOUNDATION_MODEL,
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
    # Only run in debug mode in development
    debug_mode = os.getenv('FLASK_ENV', 'production') == 'development'
    app.run(debug=debug_mode, host='127.0.0.1', port=5001)
