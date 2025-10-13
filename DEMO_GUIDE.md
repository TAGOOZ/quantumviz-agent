# QuantumViz Agent - Demo Guide for Judges

## Quick Start (5 Minutes)

### Prerequisites
- Python 3.8+ installed
- Git installed

### One-Command Setup
```bash
# Clone and setup
git clone https://github.com/yourusername/quantumviz-agent.git
cd quantumviz-agent
python3 -m venv venv
source venv/bin/activate
pip install -r src/requirements.txt

# Configure (uses demo mode, no AWS required)
cp src/.env.example src/.env
```

### Run Demo Scenarios

**Scenario 1: Interactive Web Interface (No AWS Required)**
```bash
./start_web.sh
# Open http://localhost:5000
# Try: Add H gate on qubit 0, then CNOT on qubits 0,1
# Click "Simulate" to see Bell state visualization
```

**Scenario 2: REST API Demo (No AWS Required)**
```bash
./start_api.sh
# In another terminal:
curl http://localhost:5001/api/health
```

**Scenario 3: Quantum Algorithms**
```bash
source venv/bin/activate
cd src
python algorithms/quantum_algorithms.py
# Watch: Grover's search, Shor's algorithm, VQE optimization
```

## Demo Scenarios with Sample Data

### Demo 1: Bell State Creation
**What it shows:** Quantum entanglement visualization

```bash
curl -X POST http://localhost:5001/api/circuit/simulate \
  -H "Content-Type: application/json" \
  -d '{
    "circuit": {
      "gates": [
        {"type": "H", "qubit": 0},
        {"type": "CNOT", "qubit": 0, "target": 1}
      ]
    }
  }'
```

**Expected Result:** 50% |00⟩ and 50% |11⟩ (perfect entanglement)

### Demo 2: Grover's Search Algorithm
**What it shows:** Quantum speedup O(√N)

```bash
curl -X POST http://localhost:5001/api/algorithms/grover \
  -H "Content-Type: application/json" \
  -d '{
    "search_space": 8,
    "targets": [3, 5]
  }'
```

**Expected Result:** Finds targets 3 and 5 with high probability

### Demo 3: Multi-Agent Collaboration
**What it shows:** Teacher, Debugger, and Optimizer agents working together

```bash
source venv/bin/activate
cd src
python agents/multi_agent_system.py
```

**Expected Result:** See agents collaborating to analyze and optimize circuits

### Demo 4: AI-Powered Debugging
**What it shows:** Automatic error detection and suggestions

```bash
source venv/bin/activate
cd src
python ai/quantum_debugger.py
```

**Expected Result:** Detects 6 types of quantum circuit errors with AI explanations

## Sample Configuration Files

All sample configs are pre-configured in `src/.env.example`:
- No AWS credentials needed for local demos
- Demo mode uses local simulator
- Sample data included in `src/demo/` directory

## Key Features to Highlight

### 1. Real QPU Integration
- File: `src/hardware/ionq_integration.py`
- Shows actual quantum hardware execution
- Compares simulator vs real hardware results

### 2. Multi-Agent Collaboration
- File: `src/agents/multi_agent_system.py`
- Teacher, Debugger, Optimizer agents
- Real-time inter-agent communication

### 3. Arabic Accessibility
- File: `src/accessibility/arabic_support.py`
- RTL text support
- Arabic voice commands
- Cultural adaptations

## Troubleshooting

**Issue: Port already in use**
```bash
# Kill existing process
lsof -ti:5000 | xargs kill -9
```

**Issue: Module not found**
```bash
# Reinstall dependencies
pip install -r src/requirements.txt
```

## Demo Video Script

**0:00-0:30** - Problem: Quantum computing education barrier
**0:30-1:00** - Solution: QuantumViz Agent with AI explanations
**1:00-1:30** - Unique Feature 1: Real QPU integration (show IonQ execution)
**1:30-2:00** - Unique Feature 2: Multi-agent collaboration (show agents working)
**2:00-2:30** - Unique Feature 3: Arabic accessibility (show RTL interface)
**2:30-3:00** - Live Demo: Bell state creation and visualization
**3:00-3:30** - Impact: Making quantum computing accessible globally

## Contact for Judges

If you encounter any issues running the demos:
- Check `docs/SETUP_COMPLETE.md` for detailed setup
- All demos work without AWS credentials
- Sample data provided in `src/demo/` directory
