#!/usr/bin/env python3
"""
QuantumViz Agent - Web Interface
Interactive quantum circuit builder with real-time visualization.
"""

from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import json
import os
import sys
import secrets
import re
import time
from braket.circuits import Circuit
from braket.devices import LocalSimulator
import plotly.graph_objects as go
import plotly.utils
import numpy as np
import boto3
from datetime import datetime
from botocore.exceptions import ClientError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import Google Generative AI after environment variables are loaded
try:
    import google.generativeai as genai
    GEMINI_IMPORTED = True
except ImportError:
    GEMINI_IMPORTED = False

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from config import Config
except ImportError:
    # Fallback config if import fails
    class Config:
        AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
        S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME', 'quantumviz-agent-assets')

def retry_on_failure(max_attempts=3, backoff_factor=1.0):
    """Decorator for retrying AWS API calls with exponential backoff."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except ClientError as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        # Check if error is retryable
                        error_code = e.response['Error']['Code']
                        if error_code in ['ThrottlingException', 'ServiceUnavailableException', 'InternalServerException']:
                            sleep_time = backoff_factor * (2 ** attempt)
                            time.sleep(sleep_time)
                            continue
                    raise e
                except Exception as e:
                    # Don't retry for non-AWS errors
                    raise e
            raise last_exception
        return wrapper
    return decorator


def _extract_gemini_text(response):
    if getattr(response, "text", None):
        return response.text
    parts = []
    for candidate in getattr(response, "candidates", []) or []:
        content = getattr(candidate, "content", None)
        if not content:
            continue
        for part in getattr(content, "parts", []):
            text = getattr(part, "text", None)
            if text:
                parts.append(text)
    if parts:
        return "\n".join(parts).strip()
    raise Exception("Empty response from Gemini")


def _extract_openai_text(payload):
    choices = payload.get('choices') if isinstance(payload, dict) else None
    if isinstance(choices, list) and choices:
        first = choices[0]
        if isinstance(first, dict):
            text_field = first.get('text')
            if isinstance(text_field, str) and text_field.strip():
                return text_field
            message = first.get('message')
            if isinstance(message, dict):
                content = message.get('content')
                if isinstance(content, str) and content.strip():
                    return content
                if isinstance(content, list):
                    parts = [part.get('text') for part in content if isinstance(part, dict) and part.get('text')]
                    if parts:
                        return "\n".join(parts).strip()
    text = payload.get('text') if isinstance(payload, dict) else None
    if isinstance(text, str) and text.strip():
        return text
    output_text = payload.get('outputText') if isinstance(payload, dict) else None
    if isinstance(output_text, str) and output_text.strip():
        return output_text
    return str(payload)


def _gemini_safety_settings():
    if not hasattr(genai, "types"):
        return []
    SafetySetting = getattr(genai.types, "SafetySetting", None)
    HarmCategory = getattr(genai.types, "HarmCategory", None)
    HarmBlockThreshold = getattr(genai.types, "HarmBlockThreshold", None)
    if None in (SafetySetting, HarmCategory, HarmBlockThreshold):
        return []
    try:
        return [
            SafetySetting(category=HarmCategory.HARM_CATEGORY_HARASSMENT, threshold=HarmBlockThreshold.BLOCK_NONE),
            SafetySetting(category=HarmCategory.HARM_CATEGORY_HATE_SPEECH, threshold=HarmBlockThreshold.BLOCK_NONE),
            SafetySetting(category=HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT, threshold=HarmBlockThreshold.BLOCK_NONE),
            SafetySetting(category=HarmCategory.HARM_CATEGORY_SEXUAL, threshold=HarmBlockThreshold.BLOCK_NONE),
        ]
    except Exception:
        return []

def validate_circuit_input(data):
    """Comprehensive input validation for circuit data."""
    if not isinstance(data, dict):
        raise ValueError("Invalid input format: expected JSON object")

    # Validate gate_type
    gate_type = data.get('gate_type')
    if not gate_type:
        raise ValueError("Missing required field: gate_type")

    valid_gates = ['H', 'X', 'Y', 'Z', 'CNOT', 'CZ', 'SWAP', 'T']
    if gate_type not in valid_gates:
        raise ValueError(f"Invalid gate type '{gate_type}'. Valid gates: {valid_gates}")

    # Validate qubit index
    qubit = data.get('qubit')
    if qubit is None:
        raise ValueError("Missing required field: qubit")

    if not isinstance(qubit, int) or qubit < 0 or qubit > 100:  # Reasonable upper limit
        raise ValueError("Invalid qubit index: must be non-negative integer ≤ 100")

    # Validate target qubit for multi-qubit gates
    target = data.get('target')
    if gate_type in ['CNOT', 'CZ', 'SWAP']:
        if target is None:
            raise ValueError(f"Gate '{gate_type}' requires a target qubit")
        if not isinstance(target, int) or target < 0 or target > 100:
            raise ValueError("Invalid target qubit index: must be non-negative integer ≤ 100")
        if target == qubit:
            raise ValueError("Target qubit cannot be the same as control qubit")
    elif target is not None:
        raise ValueError(f"Gate '{gate_type}' does not require a target qubit")

    # Sanitize any string inputs to prevent injection
    for key, value in data.items():
        if isinstance(value, str):
            # Remove any potentially dangerous characters
            data[key] = re.sub(r'[^\w\s\-\.]', '', value)

    return data

app = Flask(__name__)

# Enable CORS for all routes
CORS(app, origins=["*"], methods=["GET", "POST", "OPTIONS"], 
     allow_headers=["Content-Type", "Authorization"])

# Set secret key for session management
app.secret_key = os.getenv('FLASK_SECRET_KEY', secrets.token_hex(32))
# Configure session
app.config['SESSION_COOKIE_SECURE'] = os.getenv('FLASK_ENV', 'production') == 'production'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Configure rate limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"  # Use Redis in production: "redis://localhost:6379"
)

# Initialize AWS clients
try:
    bedrock_runtime = boto3.client('bedrock-runtime', region_name=Config.AWS_REGION)
    s3_client = boto3.client('s3', region_name=Config.AWS_REGION)
    AWS_AVAILABLE = True
except Exception as e:
    print(f"AWS services not available: {e}")
    bedrock_runtime = None
    s3_client = None
    AWS_AVAILABLE = False

# Initialize Google Gemini client
GEMINI_AVAILABLE = False
SUPPORTED_GEMINI_MODEL = None
if GEMINI_IMPORTED:
    try:
        gemini_api_key = os.getenv('GEMINI_API_KEY')
        if gemini_api_key and gemini_api_key.strip():
            genai.configure(api_key=gemini_api_key)
            # Find a supported model, preferring gemini-2.5-pro
            preferred_model = 'models/gemini-2.5-flash'
            supported_model = None
            # First check if preferred model is available
            for model in genai.list_models():
                if model.name == preferred_model and 'generateContent' in model.supported_generation_methods:
                    supported_model = preferred_model
                    break
            # If preferred not found, take the first available
            if not supported_model:
                for model in genai.list_models():
                    if 'generateContent' in model.supported_generation_methods:
                        supported_model = model.name
                        break
            if supported_model:
                # Test the configuration
                genai.GenerativeModel(supported_model)
                GEMINI_AVAILABLE = True
                SUPPORTED_GEMINI_MODEL = supported_model
                print(f"✅ Google Gemini API initialized successfully with model: {supported_model}")
            else:
                print("⚠️  No supported Gemini model found")
        else:
            print("⚠️  GEMINI_API_KEY is empty or not set in environment variables")
    except Exception as e:
        print(f"❌ Google Gemini API initialization failed: {str(e)}")
        GEMINI_AVAILABLE = False
else:
    print("⚠️  google-generativeai package not installed. Run: pip install google-generativeai")

class QuantumCircuitBuilder:
    """Interactive quantum circuit builder."""
    
    def __init__(self):
        self.simulator = LocalSimulator()
        self.circuit = Circuit()
        
    def add_gate(self, gate_type, qubit, target=None):
        """Add quantum gate to circuit."""
        if gate_type == 'H':
            self.circuit.h(qubit)
        elif gate_type == 'X':
            self.circuit.x(qubit)
        elif gate_type == 'Y':
            self.circuit.y(qubit)
        elif gate_type == 'Z':
            self.circuit.z(qubit)
        elif gate_type == 'CNOT':
            self.circuit.cnot(qubit, target)
        elif gate_type == 'CZ':
            self.circuit.cz(qubit, target)
        elif gate_type == 'SWAP':
            self.circuit.swap(qubit, target)
            
    def run_simulation(self, shots=1024):
        """Run quantum simulation."""
        result = self.simulator.run(self.circuit, shots=shots)
        counts = result.result().measurement_counts
        return counts
        
    def create_visualization(self, counts):
        """Create 3D visualization of results."""
        states = list(counts.keys())
        probabilities = [counts[state] / sum(counts.values()) for state in states]
        
        fig = go.Figure(data=[
            go.Bar(x=states, y=probabilities, 
                   marker_color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])
        ])
        
        fig.update_layout(
            title='Quantum Measurement Results',
            xaxis_title='Quantum States',
            yaxis_title='Probability',
            height=400
        )
        
        return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

# Initialize circuit builder
circuit_builder = QuantumCircuitBuilder()

@app.route('/')
def index():
    """Main quantum circuit builder interface."""
    return render_template('index.html')

@app.route('/api/add_gate', methods=['POST'])
@limiter.limit("30 per minute")
def add_gate():
    """Add quantum gate to circuit."""
    try:
        data = request.json

        # Comprehensive input validation
        if not data:
            return jsonify({'status': 'error', 'message': 'No data provided'})

        validated_data = validate_circuit_input(data)

        circuit_builder.add_gate(
        validated_data['gate_type'],
        validated_data['qubit'],
        validated_data.get('target')
        )
        return jsonify({'status': 'success', 'circuit': str(circuit_builder.circuit)})
    except ValueError as e:
        return jsonify({'status': 'error', 'message': str(e)})
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Internal error: {str(e)}'})

@app.route('/api/simulate', methods=['POST'])
@limiter.limit("10 per minute")
def simulate():
    """Run quantum simulation."""
    try:
        # Validate circuit is not empty
        if len(circuit_builder.circuit.instructions) == 0:
            return jsonify({'status': 'error', 'message': 'No gates in circuit'})
        
        counts = circuit_builder.run_simulation()
        visualization = circuit_builder.create_visualization(counts)
        return jsonify({
            'status': 'success',
            'results': counts,
            'visualization': visualization
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/reset', methods=['POST'])
def reset():
    """Reset quantum circuit."""
    circuit_builder.circuit = Circuit()
    return jsonify({'status': 'success', 'message': 'Circuit reset'})

@app.route('/api/circuit_info')
def circuit_info():
    """Get circuit information."""
    return jsonify({
        'qubits': circuit_builder.circuit.qubit_count,
        'gates': len(circuit_builder.circuit.instructions),
        'circuit': str(circuit_builder.circuit),
        'aws_available': AWS_AVAILABLE
    })

@app.route('/api/ai/explain', methods=['POST'])
@limiter.limit("5 per minute")
def ai_explain():
    """Get AI explanation of the current circuit using AWS Bedrock."""
    print("DEBUG: AI explain endpoint called")
    print(f"DEBUG: AWS_AVAILABLE = {AWS_AVAILABLE}, GEMINI_AVAILABLE = {GEMINI_AVAILABLE}")
    # Temporarily bypass AWS check for testing
    # if not AWS_AVAILABLE:
    #     return jsonify({
    #         'status': 'error',
    #         'message': 'AWS Bedrock not available. Configure AWS credentials to use AI features.'
    #     })
    
    try:
        print("DEBUG: Entered try block")
        circuit_str = str(circuit_builder.circuit)
        gate_count = len(circuit_builder.circuit.instructions)
        print(f"DEBUG: Circuit has {gate_count} gates")
        
        if gate_count == 0:
            return jsonify({
                'status': 'error',
                'message': 'No circuit to explain. Add some gates first.'
            })
        
        # Create prompt for AI models (use safer prompt for Gemini)
        print(f"DEBUG: Creating prompt for circuit with {gate_count} gates", file=sys.stderr)
        prompt = f"""Explain this quantum circuit in simple terms:

{circuit_str}

The circuit has {gate_count} gates. Provide:
1. What this circuit does
2. The quantum concepts involved
3. Expected behavior when measured

Keep the explanation concise and beginner-friendly.

Note: Focus on educational aspects of quantum computing."""
        print(f"DEBUG: Prompt created, length: {len(prompt)}", file=sys.stderr)

        # Try different models based on availability in eu-central-1
        # Most commonly available models across regions
        all_models = [
            # Prioritized Google Gemini models (test first!)
            ('models/gemini-2.5-flash', 'gemini'),
            # AWS models
            ('openai.gpt-oss-20b-1:0', 'openai'),
            ('openai.gpt-oss-120b-1:0', 'openai'),
            # Claude models
            ('anthropic.claude-3-5-sonnet-20240620-v1:0', 'claude'),
            ('anthropic.claude-3-sonnet-20240229-v1:0', 'claude'),
            ('anthropic.claude-v2:1', 'claude'),
            ('anthropic.claude-v2', 'claude'),
            ('anthropic.claude-instant-v1', 'claude'),
            # Amazon Titan models (various ID formats)
            ('amazon.titan-text-express-v1', 'titan'),
            ('amazon.titan-text-lite-v1', 'titan'),
            ('amazon.titan-tg1-large', 'titan'),
            # AI21 models
            ('ai21.j2-ultra-v1', 'ai21'),
            ('ai21.j2-mid-v1', 'ai21'),
            ('ai21.jamba-instruct-v1:0', 'ai21'),
            # Meta Llama
            ('meta.llama3-70b-instruct-v1:0', 'llama'),
            ('meta.llama2-70b-chat-v1', 'llama'),
            # Cohere
            ('cohere.command-text-v14', 'cohere'),
            ('cohere.command-light-text-v14', 'cohere')
        ]
        
        response = None
        last_error = None
        used_model = None
        
        @retry_on_failure(max_attempts=3, backoff_factor=1.0)
        def call_bedrock_model(model_id, model_type, prompt):
            """Call Bedrock model with retry logic."""
            if model_type == 'openai':
                body = json.dumps({
                    'prompt': prompt,
                    'max_tokens': 500,
                    'temperature': 0.7
                })
            elif model_type == 'claude':
                body = json.dumps({
                    'anthropic_version': 'bedrock-2023-05-31',
                    'max_tokens': 500,
                    'messages': [{
                        'role': 'user',
                        'content': prompt
                    }]
                })
            elif model_type == 'titan':
                body = json.dumps({
                    'inputText': prompt,
                    'textGenerationConfig': {
                        'maxTokenCount': 500,
                        'temperature': 0.7
                    }
                })
            elif model_type == 'ai21':
                body = json.dumps({
                    'prompt': prompt,
                    'maxTokens': 500,
                    'temperature': 0.7
                })
            elif model_type == 'llama':
                body = json.dumps({
                    'prompt': prompt,
                    'max_gen_len': 500,
                    'temperature': 0.7
                })
            elif model_type == 'cohere':
                body = json.dumps({
                    'prompt': prompt,
                    'max_tokens': 500,
                    'temperature': 0.7
                })
            elif model_type == 'gemini':
                """Call Google Gemini API"""
                if not GEMINI_AVAILABLE:
                    raise Exception("Gemini API not available")

                try:
                    if not SUPPORTED_GEMINI_MODEL:
                        raise Exception("Gemini model not configured")
                    model = genai.GenerativeModel(SUPPORTED_GEMINI_MODEL)
                    gemini_prompt = [{
                        'role': 'user',
                        'parts': [{'text': f"This is a safe educational quantum computing request. Respond with beginner-friendly guidance.\n\n{prompt}"}]
                    }]
                    response = model.generate_content(
                        contents=gemini_prompt,
                        safety_settings=_gemini_safety_settings(),
                        generation_config=genai.types.GenerationConfig(
                            temperature=0.7,
                            max_output_tokens=500
                        )
                    )

                    text = _extract_gemini_text(response)
                    if not text:
                        raise Exception("Empty response from Gemini")

                    return text
                except Exception as e:
                    print(f"Gemini API error: {str(e)}")
                    raise Exception(f"Gemini API error: {str(e)}")
            else:
                """Call Bedrock model"""
                response = bedrock_runtime.invoke_model(
                    ModelId=model_id,
                    Body=body.encode('utf-8')
                )
                response_body = response.get('body')
                if hasattr(response_body, 'read'):
                    response_body = response_body.read()
                if isinstance(response_body, bytes):
                    response_body = response_body.decode('utf-8')
                if not response_body:
                    return {}
                try:
                    return json.loads(response_body)
                except json.JSONDecodeError:
                    return {'text': response_body}
            
        for model_id, model_type in all_models:
            try:
                print(f"DEBUG: Trying model {model_id} ({model_type})", file=sys.stderr)
                response = call_bedrock_model(model_id, model_type, prompt)
                used_model = (model_id, model_type)
                print(f"DEBUG: Success with model {model_id} ({model_type})", file=sys.stderr)
                break  # Success, exit loop
            except ClientError as e:
                last_error = e
                error_code = e.response['Error']['Code']
                if error_code in ['ValidationException', 'AccessDeniedException']:
                    # Don't retry these errors, try next model
                    continue
                continue  # Try next model
            except Exception as e:
                last_error = e
                continue  # Try next model
        
        if response is None:
            raise last_error or Exception("No AI models available in your region")
        
        try:
            if not isinstance(response, dict):
                if isinstance(response, str):
                    try:
                        response = json.loads(response)
                    except json.JSONDecodeError:
                        response = {'text': response}
                else:
                    response = {'text': str(response)}

            if used_model[1] == 'openai':
                explanation = _extract_openai_text(response)
            elif used_model[1] == 'claude':
                explanation = response['content'][0]['text']
            elif used_model[1] == 'titan':
                explanation = response['results'][0]['outputText']
            elif used_model[1] == 'ai21':
                explanation = response['completions'][0]['data']['text']
            elif used_model[1] == 'llama':
                explanation = response['generation']
            elif used_model[1] == 'cohere':
                explanation = response['generations'][0]['text']
            elif used_model[1] == 'gemini':
                explanation = response
            else:
                explanation = str(response)
            
            print(f"DEBUG: Final explanation type: {used_model[1]}, length: {len(explanation)}")
            
            return jsonify({
                'status': 'success',
                'explanation': explanation,
                'model_used': used_model[0]
            })
        except Exception as parsing_error:
            print(f"DEBUG: Parsing failed for {used_model}: {str(parsing_error)}")
            raise parsing_error
        
    except Exception as e:
        # Fallback to rule-based explanation if Bedrock fails
        error_msg = str(e)
        
        # Analyze circuit gates
        gates_used = []
        for instruction in circuit_builder.circuit.instructions:
            gate_name = instruction.operator.name
            gates_used.append(gate_name)
        
        # Generate intelligent explanation based on gates
        explanation_parts = [
            f"🤖 QuantumViz AI Analysis",
            f"\n📊 Circuit Overview:",
            f"   • {gate_count} quantum gates",
            f"   • {circuit_builder.circuit.qubit_count} qubits",
            f"   • Depth: {gate_count} (sequential operations)\n"
        ]
        
        # Gate-specific explanations
        if 'H' in gates_used:
            explanation_parts.append("✓ Hadamard (H) gates: Create quantum superposition - qubit becomes 50/50 |0⟩ and |1⟩")
        if 'X' in gates_used:
            explanation_parts.append("✓ Pauli-X gates: Quantum NOT gate - flips |0⟩ to |1⟩ and vice versa")
        if 'Y' in gates_used:
            explanation_parts.append("✓ Pauli-Y gates: Rotation around Y-axis with phase flip")
        if 'Z' in gates_used:
            explanation_parts.append("✓ Pauli-Z gates: Phase flip - changes sign of |1⟩ state")
        if 'CNot' in gates_used or 'CNOT' in gates_used:
            explanation_parts.append("✓ CNOT gates: Creates entanglement between qubits - flips target if control is |1⟩")
        if 'T' in gates_used:
            explanation_parts.append("✓ T gates: π/4 phase rotation - used in quantum algorithms")
        
        # Pattern detection and quantum concepts
        explanation_parts.append("\n🔬 Quantum Concepts:")
        if 'H' in gates_used and ('CNot' in gates_used or 'CNOT' in gates_used):
            explanation_parts.append("   🎯 ENTANGLEMENT: This circuit creates quantum entanglement!")
            explanation_parts.append("   • Bell State pattern detected")
            explanation_parts.append("   • Qubits become correlated - measuring one affects the other")
            explanation_parts.append("   • Foundation of quantum teleportation and quantum cryptography")
        elif gates_used.count('H') > 1:
            explanation_parts.append("   🎯 SUPERPOSITION: Multiple qubits in superposition")
            explanation_parts.append("   • Creates 2^n possible states simultaneously")
            explanation_parts.append("   • Enables quantum parallelism")
        elif 'H' in gates_used:
            explanation_parts.append("   🎯 SUPERPOSITION: Qubit exists in multiple states")
            explanation_parts.append("   • Equal probability of measuring |0⟩ or |1⟩")
        
        # Expected measurement results
        explanation_parts.append("\n📈 Expected Measurement:")
        if 'H' in gates_used and ('CNot' in gates_used or 'CNOT' in gates_used):
            explanation_parts.append("   • 50% chance: |00⟩ (both qubits 0)")
            explanation_parts.append("   • 50% chance: |11⟩ (both qubits 1)")
            explanation_parts.append("   • Never: |01⟩ or |10⟩ (due to entanglement)")
        elif 'H' in gates_used:
            explanation_parts.append("   • Equal probability for all basis states")
            explanation_parts.append("   • Demonstrates quantum randomness")
        
        # Applications
        if 'CNot' in gates_used or 'CNOT' in gates_used:
            explanation_parts.append("\n💡 Real-World Applications:")
            explanation_parts.append("   • Quantum cryptography (QKD)")
            explanation_parts.append("   • Quantum error correction")
            explanation_parts.append("   • Quantum teleportation protocols")
        
        explanation_parts.append(f"\n📝 Circuit Diagram:\n{circuit_str[:250]}")
        explanation_parts.append(f"\n💬 Powered by QuantumViz Local AI Engine")
        
        fallback_explanation = "\n".join(explanation_parts)
        
        return jsonify({
            'status': 'success',
            'explanation': fallback_explanation
        })

@app.route('/api/save_to_s3', methods=['POST'])
def save_to_s3():
    """Save circuit visualization to S3."""
    if not AWS_AVAILABLE:
        return jsonify({
            'status': 'error',
            'message': 'AWS S3 not available. Configure AWS credentials to use cloud storage.'
        })
    
    try:
        data = request.json
        visualization_html = data.get('html')
        
        if not visualization_html:
            return jsonify({'status': 'error', 'message': 'No visualization data provided'})
        
        # Check if bucket exists, create if not
        try:
            s3_client.head_bucket(Bucket=Config.S3_BUCKET_NAME)
        except:
            try:
                # Create bucket
                if Config.AWS_REGION == 'us-east-1':
                    s3_client.create_bucket(Bucket=Config.S3_BUCKET_NAME)
                else:
                    s3_client.create_bucket(
                        Bucket=Config.S3_BUCKET_NAME,
                        CreateBucketConfiguration={'LocationConstraint': Config.AWS_REGION}
                    )
                print(f"Created S3 bucket: {Config.S3_BUCKET_NAME}")
            except Exception as create_error:
                return jsonify({
                    'status': 'error',
                    'message': f'Bucket does not exist and could not be created: {str(create_error)}'
                })
        
        # Generate unique filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        s3_key = f"visualizations/circuit_{timestamp}.html"
        
        # Upload to S3 (without ACL for better compatibility)
        s3_client.put_object(
            Bucket=Config.S3_BUCKET_NAME,
            Key=s3_key,
            Body=visualization_html,
            ContentType='text/html'
        )
        
        # Generate presigned URL (works without public access)
        try:
            url = s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': Config.S3_BUCKET_NAME, 'Key': s3_key},
                ExpiresIn=86400  # 24 hours
            )
        except:
            url = f"https://{Config.S3_BUCKET_NAME}.s3.{Config.AWS_REGION}.amazonaws.com/{s3_key}"
        
        return jsonify({
            'status': 'success',
            'url': url,
            's3_key': s3_key,
            'note': 'File uploaded successfully. Link valid for 24 hours.'
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'S3 upload failed: {str(e)}'
        })

@app.route('/api/aws_status')
def aws_status():
    """Check AWS services availability."""
    return jsonify({
        'aws_available': AWS_AVAILABLE,
        'bedrock': bedrock_runtime is not None,
        's3': s3_client is not None,
        'region': Config.AWS_REGION
    })

@app.route('/api/health')
def health_check():
    """Health check endpoint for Render."""
    return jsonify({
        'status': 'healthy',
        'service': 'QuantumViz Agent API',
        'version': '1.0.0',
        'aws_available': AWS_AVAILABLE,
        'gemini_available': GEMINI_AVAILABLE
    })

if __name__ == '__main__':
    # Get port from environment (Render sets PORT)
    port = int(os.getenv('PORT', 5000))
    host = '0.0.0.0'  # Always bind to all interfaces for deployment
    debug_mode = os.getenv('FLASK_ENV', 'development') == 'development'
    app.run(host=host, port=port, debug=debug_mode)
