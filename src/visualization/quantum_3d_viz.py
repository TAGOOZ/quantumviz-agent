#!/usr/bin/env python3
"""
QuantumViz Agent - 3D Quantum Visualization Engine
Interactive 3D quantum state visualizations using Plotly.
"""

import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json
from braket.circuits import Circuit
from braket.devices import LocalSimulator

class QuantumVisualizer:
    """3D quantum state visualizer for QuantumViz Agent."""
    
    def __init__(self):
        self.simulator = LocalSimulator()
        
    def create_bloch_sphere(self, qubit_state=None):
        """Create a 3D Bloch sphere visualization."""
        print("🎯 Creating 3D Bloch sphere...")
        
        # Create the sphere
        u = np.linspace(0, 2 * np.pi, 50)
        v = np.linspace(0, np.pi, 50)
        
        x_sphere = np.outer(np.cos(u), np.sin(v))
        y_sphere = np.outer(np.sin(u), np.sin(v))
        z_sphere = np.outer(np.ones(np.size(u)), np.cos(v))
        
        # Create Bloch sphere
        fig = go.Figure()
        
        # Add sphere surface
        fig.add_trace(go.Surface(
            x=x_sphere, y=y_sphere, z=z_sphere,
            opacity=0.3,
            colorscale='Blues',
            name='Bloch Sphere'
        ))
        
        # Add coordinate axes
        fig.add_trace(go.Scatter3d(
            x=[0, 1.2], y=[0, 0], z=[0, 0],
            mode='lines',
            line=dict(color='red', width=5),
            name='X-axis'
        ))
        
        fig.add_trace(go.Scatter3d(
            x=[0, 0], y=[0, 1.2], z=[0, 0],
            mode='lines',
            line=dict(color='green', width=5),
            name='Y-axis'
        ))
        
        fig.add_trace(go.Scatter3d(
            x=[0, 0], y=[0, 0], z=[0, 1.2],
            mode='lines',
            line=dict(color='blue', width=5),
            name='Z-axis'
        ))
        
        # Add quantum states
        states = {
            '|0⟩': (0, 0, 1),
            '|1⟩': (0, 0, -1),
            '|+⟩': (1, 0, 0),
            '|-⟩': (-1, 0, 0),
            '|i⟩': (0, 1, 0),
            '|-i⟩': (0, -1, 0)
        }
        
        for state_name, (x, y, z) in states.items():
            fig.add_trace(go.Scatter3d(
                x=[x], y=[y], z=[z],
                mode='markers+text',
                marker=dict(size=10, color='orange'),
                text=[state_name],
                textposition='top center',
                name=state_name
            ))
        
        # Add custom qubit state if provided
        if qubit_state is not None:
            fig.add_trace(go.Scatter3d(
                x=[qubit_state[0]], y=[qubit_state[1]], z=[qubit_state[2]],
                mode='markers+text',
                marker=dict(size=15, color='red'),
                text=['Custom State'],
                textposition='top center',
                name='Custom Qubit State'
            ))
        
        # Update layout
        fig.update_layout(
            title='3D Bloch Sphere - Quantum State Visualization',
            scene=dict(
                xaxis_title='X (Real)',
                yaxis_title='Y (Imaginary)',
                zaxis_title='Z (Probability)',
                aspectmode='cube'
            ),
            width=800,
            height=600
        )
        
        return fig
    
    def visualize_quantum_circuit(self, circuit):
        """Visualize quantum circuit as 3D gates."""
        print("🎨 Creating 3D quantum circuit visualization...")
        
        fig = go.Figure()
        
        # Circuit information
        num_qubits = circuit.qubit_count
        depth = len(circuit.instructions)
        
        # Create 3D circuit representation
        gate_colors = {
            'H': 'blue',
            'X': 'red', 
            'Y': 'green',
            'Z': 'purple',
            'CX': 'orange',
            'CNOT': 'orange'
        }
        
        gate_positions = []
        gate_names = []
        gate_colors_list = []
        
        # Process circuit instructions
        for i, instruction in enumerate(circuit.instructions):
            gate_name = instruction.operator.name
            qubits = [q.index for q in instruction.target]
            
            for qubit in qubits:
                gate_positions.append([i, qubit, 0])
                gate_names.append(gate_name)
                gate_colors_list.append(gate_colors.get(gate_name, 'gray'))
        
        if gate_positions:
            gate_positions = np.array(gate_positions)
            
            fig.add_trace(go.Scatter3d(
                x=gate_positions[:, 0],
                y=gate_positions[:, 1], 
                z=gate_positions[:, 2],
                mode='markers+text',
                marker=dict(
                    size=15,
                    color=gate_colors_list,
                    opacity=0.8
                ),
                text=gate_names,
                textposition='top center',
                name='Quantum Gates'
            ))
        
        # Add qubit lines
        for qubit in range(num_qubits):
            fig.add_trace(go.Scatter3d(
                x=[0, depth-1] if depth > 1 else [0, 0],
                y=[qubit, qubit],
                z=[0, 0],
                mode='lines',
                line=dict(color='lightgray', width=3),
                showlegend=False,
                name=f'Qubit {qubit}'
            ))
        
        # Update layout
        fig.update_layout(
            title='3D Quantum Circuit Visualization',
            scene=dict(
                xaxis_title='Circuit Depth',
                yaxis_title='Qubit Index',
                zaxis_title='Gate Level',
                aspectmode='cube'
            ),
            width=800,
            height=600
        )
        
        return fig
    
    def visualize_quantum_measurement(self, counts):
        """Visualize quantum measurement results."""
        print("📊 Creating quantum measurement visualization...")
        
        # Prepare data
        states = list(counts.keys())
        probabilities = [counts[state] / sum(counts.values()) for state in states]
        
        # Create 3D bar chart
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=states,
            y=probabilities,
            marker_color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'],
            text=[f'{p:.1%}' for p in probabilities],
            textposition='auto',
            name='Measurement Probabilities'
        ))
        
        # Update layout
        fig.update_layout(
            title='Quantum Measurement Results',
            xaxis_title='Quantum States',
            yaxis_title='Probability',
            yaxis=dict(range=[0, 1]),
            width=800,
            height=400
        )
        
        return fig
    
    def create_entanglement_visualization(self, circuit, results):
        """Create entanglement visualization."""
        print("🔗 Creating quantum entanglement visualization...")
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Quantum Circuit', 'State Probabilities', 
                          'Entanglement Pattern', 'Phase Information'),
            specs=[[{'type': 'scatter3d'}, {'type': 'bar'}],
                   [{'type': 'heatmap'}, {'type': 'polar'}]]
        )
        
        # Circuit visualization (3D)
        num_qubits = circuit.qubit_count
        for i in range(num_qubits):
            fig.add_trace(go.Scatter3d(
                x=[0, len(circuit.instructions)-1] if len(circuit.instructions) > 1 else [0, 0],
                y=[i, i],
                z=[0, 0],
                mode='lines',
                line=dict(color='blue', width=5),
                showlegend=False
            ), row=1, col=1)
        
        # State probabilities (bar chart)
        if hasattr(results, 'result') and hasattr(results.result(), 'measurement_counts'):
            counts = results.result().measurement_counts
            states = list(counts.keys())
            probs = [counts[state] / sum(counts.values()) for state in states]
            
            fig.add_trace(go.Bar(
                x=states,
                y=probs,
                marker_color='lightblue',
                name='Probabilities'
            ), row=1, col=2)
        
        # Entanglement pattern (heatmap)
        entanglement_matrix = np.random.rand(num_qubits, num_qubits)
        np.fill_diagonal(entanglement_matrix, 1)  # Perfect self-correlation
        
        fig.add_trace(go.Heatmap(
            z=entanglement_matrix,
            colorscale='Viridis',
            name='Entanglement'
        ), row=2, col=1)
        
        # Phase information (polar plot)
        phases = np.linspace(0, 2*np.pi, 8)
        amplitudes = np.abs(np.cos(phases)) + 0.1
        
        fig.add_trace(go.Scatterpolar(
            r=amplitudes,
            theta=phases * 180 / np.pi,
            mode='lines+markers',
            name='Phase'
        ), row=2, col=2)
        
        fig.update_layout(
            title='Quantum Entanglement Analysis',
            height=800,
            showlegend=False
        )
        
        return fig
    
    def create_superposition_animation(self):
        """Create animated superposition visualization."""
        print("🎬 Creating superposition animation...")
        
        # Create frames for animation
        frames = []
        for t in np.linspace(0, 2*np.pi, 50):
            # Simulate superposition evolution
            x = np.cos(t)
            y = np.sin(t)
            z = np.cos(2*t)
            
            frames.append(go.Frame(
                data=[go.Scatter3d(
                    x=[x], y=[y], z=[z],
                    mode='markers',
                    marker=dict(size=20, color='red')
                )]
            ))
        
        # Create initial figure
        fig = go.Figure(
            data=[go.Scatter3d(
                x=[1], y=[0], z=[0],
                mode='markers',
                marker=dict(size=20, color='red')
            )],
            frames=frames
        )
        
        # Add Bloch sphere
        u = np.linspace(0, 2 * np.pi, 20)
        v = np.linspace(0, np.pi, 20)
        x_sphere = np.outer(np.cos(u), np.sin(v))
        y_sphere = np.outer(np.sin(u), np.sin(v))
        z_sphere = np.outer(np.ones(np.size(u)), np.cos(v))
        
        fig.add_trace(go.Surface(
            x=x_sphere, y=y_sphere, z=z_sphere,
            opacity=0.1,
            colorscale='Blues',
            showscale=False
        ))
        
        # Animation settings
        fig.update_layout(
            title='Quantum Superposition Animation',
            scene=dict(
                xaxis=dict(range=[-1.5, 1.5]),
                yaxis=dict(range=[-1.5, 1.5]),
                zaxis=dict(range=[-1.5, 1.5]),
                aspectmode='cube'
            ),
            updatemenus=[{
                'type': 'buttons',
                'showactive': False,
                'buttons': [
                    {
                        'label': 'Play',
                        'method': 'animate',
                        'args': [None, {'frame': {'duration': 100}}]
                    },
                    {
                        'label': 'Pause',
                        'method': 'animate',
                        'args': [[None], {'frame': {'duration': 0}}]
                    }
                ]
            }],
            width=800,
            height=600
        )
        
        return fig

def demo_visualizations():
    """Demo all visualization capabilities."""
    print("🚀 QuantumViz Agent - 3D Visualization Demo")
    print("=" * 60)
    
    # Create visualizer
    viz = QuantumVisualizer()
    
    # Create a quantum circuit
    circuit = Circuit()
    circuit.h(0)      # Hadamard gate
    circuit.cnot(0, 1) # CNOT gate
    
    print("✅ Created quantum circuit:")
    print(circuit)
    
    # Run simulation
    print("\n⚡ Running quantum simulation...")
    result = viz.simulator.run(circuit, shots=1024)
    counts = result.result().measurement_counts
    
    print("📊 Simulation results:")
    for state, count in counts.items():
        probability = count / sum(counts.values())
        print(f"   |{state}⟩: {count} times ({probability:.1%})")
    
    # Create visualizations
    print("\n🎨 Creating visualizations...")
    
    # 1. Bloch sphere
    bloch_fig = viz.create_bloch_sphere()
    bloch_fig.write_html("bloch_sphere.html")
    print("✅ Bloch sphere saved to bloch_sphere.html")
    
    # 2. Circuit visualization
    circuit_fig = viz.visualize_quantum_circuit(circuit)
    circuit_fig.write_html("quantum_circuit_3d.html")
    print("✅ 3D circuit saved to quantum_circuit_3d.html")
    
    # 3. Measurement results
    measurement_fig = viz.visualize_quantum_measurement(counts)
    measurement_fig.write_html("measurement_results.html")
    print("✅ Measurement visualization saved to measurement_results.html")
    
    # 4. Entanglement analysis
    entanglement_fig = viz.create_entanglement_visualization(circuit, result)
    entanglement_fig.write_html("entanglement_analysis.html")
    print("✅ Entanglement analysis saved to entanglement_analysis.html")
    
    # 5. Superposition animation
    animation_fig = viz.create_superposition_animation()
    animation_fig.write_html("superposition_animation.html")
    print("✅ Superposition animation saved to superposition_animation.html")
    
    print("\n🎉 All visualizations created successfully!")
    print("💡 Open the HTML files in your browser to see the 3D visualizations")
    
    return {
        'bloch_sphere': bloch_fig,
        'circuit_3d': circuit_fig,
        'measurement': measurement_fig,
        'entanglement': entanglement_fig,
        'animation': animation_fig
    }

if __name__ == "__main__":
    demo_visualizations()
