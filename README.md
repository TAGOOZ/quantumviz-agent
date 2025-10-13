# QuantumViz Agent

An AI-powered platform that transforms quantum circuits into interactive 3D visualizations with natural language explanations. Built for quantum computing education and research.

## Overview

QuantumViz Agent bridges the gap between complex quantum computing concepts and accessible learning by providing:

- Interactive 3D visualization of quantum circuits and states
- AI-driven explanations adapted to user expertise level
- Real quantum simulations using Amazon Braket
- Multi-agent collaboration system for comprehensive analysis
- Integration with real quantum hardware (IonQ QPU)

## Architecture

The system follows a modular pipeline architecture:

```
User Input → AgentCore Runtime → Circuit Parser → Braket Simulator → 3D Visualizer
     ↓              ↓                    ↓              ↓              ↓
Claude 3.5 → Memory/Gateway → Circuit Analysis → State Vectors → Plotly 3D
```

### Key Components

**AgentCore Integration**
- Runtime environment for AI agent orchestration
- Memory management and gateway services
- Real-time observability and monitoring

**Quantum Processing Pipeline**
- Circuit parsing for QASM, Qiskit, and Cirq formats
- Simulation using Amazon Braket Local Simulator and QPU
- State vector analysis and measurement processing

**AI Reasoning Engine**
- Multi-step analysis using Claude 3.5 Sonnet
- Context-aware explanations based on user expertise
- Educational content generation and adaptation

**Visualization System**
- Real-time 3D rendering with Plotly
- Interactive Bloch sphere representations
- Circuit diagram generation and animation

## Features

### Multi-Agent Collaboration
- Teacher Agent for educational content and assessments
- Debugger Agent for circuit analysis and error detection
- Optimizer Agent for performance enhancement
- Coordinated problem-solving across specialized agents

### Quantum Hardware Integration
- Support for IonQ quantum processing units
- Fidelity comparison between simulator and hardware
- Real-time quantum state measurement
- Hardware-specific circuit optimization

### Educational Platform
- Gamified learning with challenge system
- Community circuit gallery and sharing
- Progress tracking and analytics
- Structured learning paths

### AI-Powered Debugging
- Automatic error detection in quantum circuits
- Optimization suggestions for gate reduction
- Performance analysis and complexity scoring
- Personalized debugging assistance

### Analytics Dashboard
- Student progress tracking for educators
- Concept difficulty analysis
- Engagement metrics and patterns
- AI-driven learning recommendations

## REST API

The platform provides a comprehensive REST API with the following endpoints:

**Circuit Operations**
- `POST /api/circuit/simulate` - Simulate quantum circuits
- `POST /api/visualize/bloch` - Generate Bloch sphere visualizations
- `POST /api/visualize/circuit` - Create circuit diagrams

**Quantum Algorithms**
- `POST /api/algorithms/grover` - Grover's search algorithm
- `POST /api/algorithms/shor` - Shor's factorization
- `POST /api/algorithms/vqe` - Variational quantum eigensolver

**AI Services**
- `POST /api/ai/explain` - Get AI explanations of quantum concepts
- `GET /api/education/modules` - Access educational content
- `GET /api/education/module/<id>` - Retrieve specific learning modules

**System**
- `GET /api/health` - Health check endpoint

All POST endpoints require API key authentication via the `X-API-Key` header.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- AWS account with Bedrock and Braket access
- AWS CLI configured with appropriate credentials

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/quantumviz-agent.git
cd quantumviz-agent
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r src/requirements.txt
```

4. Configure environment variables:
```bash
cp src/.env.example src/.env
# Edit src/.env with your AWS credentials and configuration
```

5. Generate secure keys:
```bash
python3 -c "import secrets; print('API_KEY=' + secrets.token_hex(32))"
python3 -c "import secrets; print('FLASK_SECRET_KEY=' + secrets.token_hex(32))"
# Add these to your src/.env file
```

### Running the Application

**Web Interface:**
```bash
./start_web.sh
# Access at http://localhost:5000
```

**API Server:**
```bash
./start_api.sh
# Access at http://localhost:5001
```

**Manual Start:**
```bash
source venv/bin/activate
cd src
python web/app.py  # or python api/quantum_api.py
```

## Project Structure

```
quantumviz-agent/
├── src/
│   ├── agent/              # AgentCore integration and AI services
│   ├── agents/             # Multi-agent collaboration system
│   ├── ai/                 # AI-powered debugging and optimization
│   ├── algorithms/         # Quantum algorithm implementations
│   ├── analytics/          # Educational analytics dashboard
│   ├── api/                # REST API endpoints
│   ├── demo/               # Demo scenarios and examples
│   ├── gamification/       # Learning platform and challenges
│   ├── hardware/           # Quantum hardware integration
│   ├── quantum/            # Core quantum computing logic
│   ├── sdk/                # SDK and integrations
│   ├── visualization/      # 3D visualization engine
│   ├── web/                # Web interface
│   ├── config.py           # Configuration management
│   └── requirements.txt    # Python dependencies
├── venv/                   # Virtual environment
├── start_api.sh            # API server startup script
├── start_web.sh            # Web interface startup script
└── README.md               # This file
```

## Security

The application implements several security measures:

- API key authentication for all POST endpoints
- Secure session management with HttpOnly cookies
- Input validation on all user inputs
- Environment-based configuration for sensitive data
- Comprehensive request logging and monitoring
- IAM roles following principle of least privilege

For detailed security information, see the security audit documentation in the `docs/` directory.

## Configuration

Key configuration options in `src/.env`:

- `AWS_REGION` - AWS region for services (default: eu-central-1)
- `AWS_ACCOUNT_ID` - Your AWS account ID
- `AGENT_ID` - Bedrock Agent ID
- `API_KEY` - API authentication key
- `FLASK_SECRET_KEY` - Flask session secret
- `FLASK_ENV` - Environment (development/production)
- `S3_BUCKET_NAME` - S3 bucket for visualizations

## Testing

Run the test suite:
```bash
source venv/bin/activate
python -m pytest tests/
```

Validate configuration:
```bash
python -c "from src.config import Config; Config.validate_config()"
```

## Contributing

Contributions are welcome. Please ensure:

- Code follows existing style and patterns
- All tests pass before submitting
- Security best practices are maintained
- Documentation is updated as needed

## License

This project is part of the AWS AI Agent Global Hackathon.

## Acknowledgments

- Built using AWS Bedrock AgentCore
- Quantum simulations powered by Amazon Braket
- AI explanations generated by Claude 3.5 Sonnet
- 3D visualizations created with Plotly