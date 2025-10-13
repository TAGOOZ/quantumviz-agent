# QuantumViz Agent

**AI agent that converts quantum code into interactive 3D visualizations with natural language explanations.**

## What It Does

- Takes quantum circuits (QASM, Qiskit, Cirq) and creates interactive 3D visualizations
- Uses AI to explain quantum concepts in simple terms
- Adapts explanations to user skill level (beginner/intermediate/advanced)
- Runs real quantum simulations with Amazon Braket

## Engineering Approach

### Architecture
```
User Input → AgentCore Runtime → Quantum Circuit Parser → Braket Simulator → 3D Visualizer
     ↓              ↓                    ↓                    ↓              ↓
Claude 3.5 → Memory/Gateway → Circuit Analysis → State Vectors → Plotly 3D
```

### Multi-Region Design
- **eu-central-1**: AgentCore Runtime, Bedrock models, S3 storage
- **us-east-1**: Amazon Braket quantum processing, results storage
- **Cross-region**: Optimized for global access and cost efficiency

### Technical Implementation
- **AgentCore Integration**: Runtime, Memory, Gateway, Observability
- **Quantum Pipeline**: Circuit parsing → Simulation → State analysis → Visualization
- **AI Reasoning**: Multi-step analysis with Claude 3.5 Sonnet
- **3D Rendering**: Real-time quantum state visualization with Plotly
- **Cost Optimization**: Local development + cloud execution strategy

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

## Engineering Challenges Solved

### 1. Quantum State Visualization
- **Problem**: Converting abstract quantum states to interactive 3D
- **Solution**: Custom Plotly integration with real-time state updates
- **Result**: Perfect Bell states (50% |00⟩, 50% |11⟩) visualized

### 2. Multi-Region AWS Architecture
- **Problem**: Quantum processing in us-east-1, AI in eu-central-1
- **Solution**: Cross-region S3 sync + optimized data transfer
- **Result**: 7/8 services operational, $0 spent

### 3. AgentCore Integration
- **Problem**: Complex quantum reasoning with AI agent
- **Solution**: Custom prompt engineering + circuit analysis pipeline
- **Result**: Agent DRC1I6SIWE (PREPARED) with quantum expertise

### 4. Cost Optimization
- **Problem**: $100 budget for quantum + AI services
- **Solution**: Local development + cloud execution strategy
- **Result**: $0 spent, $100 remaining, full monitoring active

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