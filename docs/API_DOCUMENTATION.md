# QuantumViz Agent - API Documentation

## Overview
RESTful API for quantum circuit processing, algorithm execution, and 3D visualization generation.

## Base URL
```
http://localhost:5001/api
```

## Endpoints

### Health Check
```http
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "QuantumViz Agent API",
  "version": "1.0.0"
}
```

### Quantum Circuit Simulation
```http
POST /api/circuit/simulate
```

**Request Body:**
```json
{
  "circuit": {
    "gates": [
      {"type": "H", "qubit": 0},
      {"type": "CNOT", "qubit": 0, "target": 1}
    ]
  }
}
```

**Response:**
```json
{
  "status": "success",
  "results": {"00": 512, "11": 512},
  "circuit_depth": 2,
  "qubit_count": 2
}
```

### Grover's Search Algorithm
```http
POST /api/algorithms/grover
```

**Request Body:**
```json
{
  "search_space": 8,
  "targets": [3, 5],
  "iterations": 2
}
```

**Response:**
```json
{
  "status": "success",
  "results": {"011": 256, "101": 256, "000": 128, "111": 128},
  "success_rate": 0.5,
  "iterations": 2
}
```

### Shor's Factorization Algorithm
```http
POST /api/algorithms/shor
```

**Request Body:**
```json
{
  "number": 15,
  "random_base": 7
}
```

**Response:**
```json
{
  "status": "success",
  "results": {"000": 256, "001": 256, "010": 256, "011": 256},
  "period": 4,
  "factors": [3, 5]
}
```

### VQE Optimization
```http
POST /api/algorithms/vqe
```

**Request Body:**
```json
{
  "hamiltonian": [[1, 0], [0, -1]],
  "ansatz_depth": 3
}
```

**Response:**
```json
{
  "status": "success",
  "ground_state_energy": -1.0,
  "expectation_value": -1.0,
  "ansatz_depth": 3
}
```

### Bloch Sphere Visualization
```http
POST /api/visualize/bloch
```

**Request Body:**
```json
{
  "qubit_state": [1, 0]
}
```

**Response:**
```json
{
  "status": "success",
  "visualization_url": "https://quantumviz-agent-assets.s3.eu-central-1.amazonaws.com/visualizations/bloch_sphere_1234.html",
  "s3_key": "visualizations/bloch_sphere_1234.html"
}
```

### Circuit Analysis Visualization
```http
POST /api/visualize/circuit
```

**Request Body:**
```json
{
  "circuit": {
    "gates": [
      {"type": "H", "qubit": 0},
      {"type": "CNOT", "qubit": 0, "target": 1}
    ]
  }
}
```

**Response:**
```json
{
  "status": "success",
  "visualization_url": "https://quantumviz-agent-assets.s3.eu-central-1.amazonaws.com/visualizations/circuit_analysis_5678.html",
  "s3_key": "visualizations/circuit_analysis_5678.html"
}
```

### AI Explanation
```http
POST /api/ai/explain
```

**Request Body:**
```json
{
  "concept": "quantum superposition",
  "level": "beginner"
}
```

**Response:**
```json
{
  "status": "success",
  "explanation": "Quantum superposition is like a coin spinning in the air...",
  "concept": "quantum superposition",
  "level": "beginner"
}
```

### Education Modules
```http
GET /api/education/modules
```

**Response:**
```json
{
  "status": "success",
  "modules": [
    {
      "id": "superposition",
      "title": "Quantum Superposition",
      "description": "Learn about quantum superposition and the double-slit experiment",
      "difficulty": "beginner",
      "duration": "15 minutes"
    }
  ]
}
```

### Specific Education Module
```http
GET /api/education/module/superposition
```

**Response:**
```json
{
  "status": "success",
  "module": {
    "title": "Quantum Superposition",
    "content": {
      "theory": "Quantum superposition is the fundamental principle...",
      "experiment": "Double-slit experiment demonstrates...",
      "mathematics": "|ψ⟩ = α|0⟩ + β|1⟩ where |α|² + |β|² = 1",
      "visualization": "Bloch sphere representation of qubit states"
    },
    "interactive_demo": "/api/visualize/bloch",
    "quiz": [
      {
        "question": "What is quantum superposition?",
        "options": ["A", "B", "C", "D"],
        "correct": "A"
      }
    ]
  }
}
```

## Error Responses

All endpoints return error responses in the following format:

```json
{
  "status": "error",
  "message": "Error description"
}
```

## Rate Limiting

- 100 requests per minute per IP
- 1000 requests per hour per API key

## Authentication

Currently no authentication required for demo purposes.

## SDK Examples

### Python
```python
import requests

# Simulate quantum circuit
response = requests.post('http://localhost:5001/api/circuit/simulate', json={
    'circuit': {
        'gates': [
            {'type': 'H', 'qubit': 0},
            {'type': 'CNOT', 'qubit': 0, 'target': 1}
        ]
    }
})
result = response.json()
print(result['results'])
```

### JavaScript
```javascript
// Simulate quantum circuit
fetch('http://localhost:5001/api/circuit/simulate', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        circuit: {
            gates: [
                {type: 'H', qubit: 0},
                {type: 'CNOT', qubit: 0, target: 1}
            ]
        }
    })
})
.then(response => response.json())
.then(data => console.log(data.results));
```

## WebSocket Support

Real-time quantum simulation updates via WebSocket:

```javascript
const ws = new WebSocket('ws://localhost:5001/ws');
ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('Quantum simulation update:', data);
};
```
