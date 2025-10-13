# QuantumViz Agent - Main Package
"""
QuantumViz Agent: An AI-powered autonomous agent that converts quantum code 
into interactive 3D visualizations with natural language explanations.

This package contains the core implementation of the QuantumViz Agent system,
including quantum circuit processing, AI agent orchestration, and visualization
generation capabilities.
"""

__version__ = "1.0.0"
__author__ = "QuantumViz Team"
__email__ = "team@quantumviz.ai"

# Package imports
from .agent import QuantumVizAgent
from .quantum import CircuitProcessor, BraketConnector
from .visualization import VisualizationEngine

__all__ = [
    "QuantumVizAgent",
    "CircuitProcessor", 
    "BraketConnector",
    "VisualizationEngine"
]

