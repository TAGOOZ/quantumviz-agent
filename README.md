# QuantumViz Agent

**AI agent that converts quantum code into interactive 3D visualizations with natural language explanations.**

## What It Does

- Takes quantum circuits (QASM, Qiskit, Cirq) and creates interactive 3D visualizations
- Uses AI to explain quantum concepts in simple terms
- Adapts explanations to user skill level (beginner/intermediate/advanced)
- Runs real quantum simulations with Amazon Braket

## Technical Stack

- **AgentCore Runtime** (eu-central-1) - AI agent orchestration
- **Amazon Braket** (us-east-1) - Quantum simulation
- **Claude 3.5 Sonnet** - Natural language explanations
- **Plotly** - 3D visualizations
- **Python** - Backend logic

## Live Demo

Open these HTML files in your browser:
- `quantumviz_bloch_sphere.html` - Interactive 3D Bloch sphere
- `quantumviz_circuit_analysis.html` - Quantum circuit visualization
- `quantumviz_teleportation.html` - Quantum teleportation animation

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run quantum simulation
python src/quantum/first_circuit.py

# Create 3D visualizations
python src/visualization/simple_3d_viz.py

# Test AWS integration
python src/agent/aws_integration_test.py
```

## Results

- **Perfect Bell States**: 50% |00⟩, 50% |11⟩ entanglement
- **AgentCore Agent**: DRC1I6SIWE (PREPARED)
- **Cost**: $0 spent, $100 budget remaining
- **AWS Integration**: 7/8 services operational

## Competition Highlights

- **Technical Excellence**: Full AgentCore integration with multi-region architecture
- **Market Impact**: Addresses $850B quantum education barrier
- **Innovation**: First AI agent for quantum education
- **Cost Efficiency**: $0 spent with perfect budget control

## Files

- `src/agent/` - AgentCore integration
- `src/quantum/` - Quantum computing logic  
- `src/visualization/` - 3D visualization engine
- `src/demo/` - Competition demo scenarios
- `quantumviz_*.html` - Interactive visualizations