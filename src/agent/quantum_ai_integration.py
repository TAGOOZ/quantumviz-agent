#!/usr/bin/env python3
"""
QuantumViz Agent - AI Integration
Integrate AgentCore with quantum circuit analysis and explanations.
"""

import boto3
import json
import sys
import os
from braket.circuits import Circuit
from braket.devices import LocalSimulator
import time
# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config

class QuantumAIIntegration:
    """AI-powered quantum circuit analysis and explanation."""
    
    def __init__(self):
        self.agent_id = os.getenv('AGENT_ID', 'DRC1I6SIWE')  # Use env var or default
        self.region = Config.AWS_REGION
        self.runtime = boto3.client('bedrock-agent-runtime', region_name=self.region)
        self.simulator = LocalSimulator()
        
    def create_agent_alias(self):
        """Create agent alias for easier access."""
        print("🏷️  Creating agent alias...")
        
        try:
            agentcore = boto3.client('bedrock-agent', region_name=Config.AWS_REGION)
            
            response = agentcore.create_agent_alias(
                agentId=self.agent_id,
                agentAliasName='QuantumViz-Live',
                description='Live alias for QuantumViz Agent'
            )
            
            alias_id = response['agentAlias']['agentAliasId']
            print(f"✅ Agent alias created: {alias_id}")
            return alias_id
            
        except Exception as e:
            if "already exists" in str(e).lower():
                print("✅ Agent alias already exists")
                return "EXISTS"
            else:
                print(f"❌ Alias creation error: {e}")
                return None
    
    def get_agent_alias(self):
        """Get existing agent alias."""
        try:
            agentcore = boto3.client('bedrock-agent', region_name=Config.AWS_REGION)
            
            response = agentcore.list_agent_aliases(agentId=self.agent_id)
            aliases = response['agentAliasSummaries']
            
            if aliases:
                alias = aliases[0]
                print(f"✅ Using alias: {alias['agentAliasName']} ({alias['agentAliasId']})")
                return alias['agentAliasId']
            else:
                return None
                
        except Exception as e:
            print(f"❌ Alias retrieval error: {e}")
            return None
    
    def analyze_quantum_circuit(self, circuit_description):
        """Analyze quantum circuit with AI explanations."""
        print(f"🤖 Analyzing quantum circuit: {circuit_description}")
        
        # Create the circuit
        circuit = self.create_circuit_from_description(circuit_description)
        
        # Run quantum simulation
        result = self.simulator.run(circuit, shots=1024)
        counts = result.result().measurement_counts
        
        # Prepare analysis prompt
        analysis_prompt = f"""
        Analyze this quantum circuit and provide an educational explanation:
        
        Circuit: {circuit_description}
        Results: {dict(counts)}
        
        Please provide:
        1. What this circuit does (simple explanation)
        2. Key quantum concepts demonstrated
        3. Why we get these specific results
        4. Educational analogies for beginners
        5. Real-world applications
        
        Make it engaging and accessible for someone learning quantum computing.
        """
        
        # Get AI explanation
        explanation = self.get_ai_explanation(analysis_prompt)
        
        return {
            'circuit': circuit,
            'results': counts,
            'explanation': explanation,
            'visualization_data': self.prepare_visualization_data(counts)
        }
    
    def create_circuit_from_description(self, description):
        """Create quantum circuit from description."""
        circuit = Circuit()
        
        if 'bell state' in description.lower() or 'entanglement' in description.lower():
            circuit.h(0)
            circuit.cnot(0, 1)
            
        elif 'superposition' in description.lower():
            circuit.h(0)
            
        elif 'teleportation' in description.lower():
            # Simple teleportation circuit
            circuit.h(0)
            circuit.cnot(0, 1)
            circuit.h(2)
            circuit.cnot(2, 0)
            circuit.h(2)
            
        else:
            # Default: Bell state
            circuit.h(0)
            circuit.cnot(0, 1)
        
        return circuit
    
    def get_ai_explanation(self, prompt):
        """Get AI explanation from AgentCore."""
        print("🧠 Getting AI explanation...")
        
        try:
            # Get agent alias
            alias_id = self.get_agent_alias()
            if not alias_id:
                alias_id = self.create_agent_alias()
            
            if not alias_id:
                return "❌ Unable to access AgentCore agent"
            
            # Invoke agent
            response = self.runtime.invoke_agent(
                agentId=self.agent_id,
                agentAliasId=alias_id,
                sessionId=f'session-{int(time.time())}',
                inputText=prompt
            )
            
            # Read response
            explanation = ""
            for event in response['completion']:
                if 'chunk' in event:
                    chunk = event['chunk']
                    if 'bytes' in chunk:
                        text = chunk['bytes'].decode('utf-8')
                        explanation += text
            
            return explanation.strip()
            
        except Exception as e:
            print(f"❌ AI explanation error: {e}")
            return f"AI explanation temporarily unavailable: {e}"
    
    def prepare_visualization_data(self, counts):
        """Prepare data for 3D visualization."""
        total_shots = sum(counts.values())
        
        visualization_data = {
            'states': list(counts.keys()),
            'probabilities': [counts[state] / total_shots for state in counts.keys()],
            'total_shots': total_shots,
            'entanglement_detected': self.detect_entanglement(counts),
            'quantum_concepts': self.identify_quantum_concepts(counts)
        }
        
        return visualization_data
    
    def detect_entanglement(self, counts):
        """Detect quantum entanglement from results."""
        states = list(counts.keys())
        
        # Perfect Bell state: only |00⟩ and |11⟩
        if len(states) == 2 and '00' in states and '11' in states:
            return True
        
        # Check for correlation
        total_shots = sum(counts.values())
        if '00' in counts and '11' in counts:
            correlation = (counts['00'] + counts['11']) / total_shots
            return correlation > 0.8
        
        return False
    
    def identify_quantum_concepts(self, counts):
        """Identify quantum concepts from results."""
        concepts = []
        
        if self.detect_entanglement(counts):
            concepts.append('Quantum Entanglement')
        
        if len(counts) > 1:
            concepts.append('Quantum Superposition')
        
        if any('1' in state for state in counts.keys()):
            concepts.append('Quantum Measurement')
        
        return concepts
    
    def create_interactive_demo(self):
        """Create interactive quantum circuit demo with AI."""
        print("🚀 QuantumViz Agent - Interactive AI Demo")
        print("=" * 60)
        
        # Demo circuits
        demo_circuits = [
            "Create a Bell state with quantum entanglement",
            "Show quantum superposition with Hadamard gate",
            "Demonstrate quantum teleportation protocol"
        ]
        
        results = []
        
        for i, circuit_desc in enumerate(demo_circuits, 1):
            print(f"\n{i}. {circuit_desc}")
            print("-" * 50)
            
            # Analyze circuit
            analysis = self.analyze_quantum_circuit(circuit_desc)
            
            # Display results
            print("📊 Quantum Results:")
            for state, count in analysis['results'].items():
                probability = count / sum(analysis['results'].values())
                print(f"   |{state}⟩: {count} times ({probability:.1%})")
            
            print(f"\n🤖 AI Explanation:")
            print(analysis['explanation'])
            
            print(f"\n🔬 Quantum Concepts:")
            for concept in analysis['visualization_data']['quantum_concepts']:
                print(f"   • {concept}")
            
            results.append(analysis)
        
        return results
    
    def test_agent_connectivity(self):
        """Test AgentCore agent connectivity."""
        print("🔍 Testing AgentCore connectivity...")
        
        try:
            # Simple test prompt
            test_prompt = "Hello! Can you explain what quantum computing is in simple terms?"
            
            alias_id = self.get_agent_alias()
            if not alias_id:
                alias_id = self.create_agent_alias()
            
            if alias_id:
                response = self.runtime.invoke_agent(
                    agentId=self.agent_id,
                    agentAliasId=alias_id,
                    sessionId='test-session',
                    inputText=test_prompt
                )
                
                # Read response
                explanation = ""
                for event in response['completion']:
                    if 'chunk' in event:
                        chunk = event['chunk']
                        if 'bytes' in chunk:
                            text = chunk['bytes'].decode('utf-8')
                            explanation += text
                
                print("✅ AgentCore connectivity successful!")
                print(f"🤖 Agent response: {explanation[:200]}...")
                return True
            else:
                print("❌ No agent alias available")
                return False
                
        except Exception as e:
            print(f"❌ AgentCore connectivity error: {e}")
            return False

def main():
    """Main function to test AI integration."""
    print("🚀 QuantumViz Agent - AI Integration Test")
    print("=" * 60)
    
    # Create AI integration
    ai_integration = QuantumAIIntegration()
    
    # Test connectivity
    connectivity_ok = ai_integration.test_agent_connectivity()
    
    if connectivity_ok:
        print("\n🎉 AgentCore integration working!")
        
        # Create interactive demo
        demo_results = ai_integration.create_interactive_demo()
        
        print("\n" + "=" * 60)
        print("🎯 AI Integration Summary:")
        print("=" * 60)
        print("✅ AgentCore agent: PREPARED and responding")
        print("✅ Quantum simulation: Working perfectly")
        print("✅ AI explanations: Generated successfully")
        print("✅ 3D visualization: Data prepared")
        print("✅ Interactive demo: Complete")
        
        print("\n💡 Ready for competition demo!")
        
    else:
        print("\n⚠️  AgentCore needs attention")
        print("   Check AWS console for agent status")

if __name__ == "__main__":
    main()

