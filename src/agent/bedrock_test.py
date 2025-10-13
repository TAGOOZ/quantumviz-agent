#!/usr/bin/env python3
"""
QuantumViz Agent - Bedrock Integration Test
Test Amazon Bedrock Claude 3.5 Sonnet for quantum explanations.
"""

import json
import boto3
from botocore.exceptions import ClientError

def test_bedrock_connection():
    """Test basic Bedrock connectivity."""
    print("🔗 Testing Amazon Bedrock connection...")
    
    try:
        # Initialize Bedrock client
        bedrock = boto3.client('bedrock-runtime', region_name='eu-central-1')
        
        # Test model availability
        bedrock_models = boto3.client('bedrock', region_name='eu-central-1')
        models = bedrock_models.list_foundation_models()
        
        claude_models = [model for model in models['modelSummaries'] 
                        if 'claude' in model['modelId'].lower()]
        
        print(f"✅ Found {len(claude_models)} Claude models available:")
        for model in claude_models:
            print(f"   • {model['modelName']} ({model['modelId']})")
        
        return True
        
    except Exception as e:
        print(f"❌ Bedrock connection error: {e}")
        return False

def generate_quantum_explanation():
    """Generate quantum explanation using Claude 3.5 Sonnet."""
    print("\n🤖 Testing quantum explanation generation...")
    
    try:
        # Initialize Bedrock client
        bedrock = boto3.client('bedrock-runtime', region_name='eu-central-1')
        
        # Prepare the prompt
        prompt = """
        Explain quantum entanglement in simple terms for a beginner. 
        Use analogies and avoid complex mathematics. 
        Focus on how two quantum particles can be connected even when far apart.
        """
        
        # Claude 3.5 Sonnet model ID
        model_id = "anthropic.claude-3-5-sonnet-20240620-v1:0"
        
        # Prepare the request body
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 500,
            "temperature": 0.7,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        })
        
        # Invoke the model
        response = bedrock.invoke_model(
            modelId=model_id,
            body=body,
            contentType="application/json"
        )
        
        # Parse response
        response_body = json.loads(response['body'].read())
        explanation = response_body['content'][0]['text']
        
        print("✅ Quantum Explanation Generated:")
        print("=" * 50)
        print(explanation)
        print("=" * 50)
        
        return explanation
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'AccessDeniedException':
            print("❌ Access denied. You may need to request model access.")
            print("   Go to: https://console.aws.amazon.com/bedrock/")
            print("   Request access to Claude 3.5 Sonnet")
        else:
            print(f"❌ Bedrock error: {e}")
        return None
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None

def test_different_models():
    """Test different available models."""
    print("\n🧪 Testing different Bedrock models...")
    
    models_to_test = [
        "anthropic.claude-3-5-sonnet-20240620-v1:0",
        "anthropic.claude-3-haiku-20240307-v1:0",
        "amazon.nova-pro-v1:0"
    ]
    
    bedrock = boto3.client('bedrock-runtime', region_name='eu-central-1')
    
    for model_id in models_to_test:
        try:
            print(f"\n📝 Testing {model_id}...")
            
            prompt = "What is quantum superposition? Explain in one sentence."
            
            body = json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 100,
                "temperature": 0.5,
                "messages": [{"role": "user", "content": prompt}]
            })
            
            response = bedrock.invoke_model(
                modelId=model_id,
                body=body,
                contentType="application/json"
            )
            
            response_body = json.loads(response['body'].read())
            result = response_body['content'][0]['text']
            
            print(f"✅ {model_id}: {result[:100]}...")
            
        except Exception as e:
            print(f"❌ {model_id}: {e}")

def main():
    """Main function to test Bedrock integration."""
    print("🚀 QuantumViz Agent - Bedrock Integration Test")
    print("=" * 60)
    
    # Test connection
    if test_bedrock_connection():
        print("✅ Bedrock connection successful!")
        
        # Generate quantum explanation
        explanation = generate_quantum_explanation()
        
        if explanation:
            print("\n🎉 Bedrock integration working perfectly!")
            print("💡 Ready for quantum explanation generation")
            
            # Test different models
            test_different_models()
            
        else:
            print("\n⚠️  Model access may need to be requested")
            print("   Check: https://console.aws.amazon.com/bedrock/")
            
    else:
        print("❌ Bedrock connection failed")

if __name__ == "__main__":
    main()
