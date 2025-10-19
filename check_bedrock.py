#!/usr/bin/env python3
"""
Test which Bedrock models are available in your region
"""
import boto3
import json

def test_bedrock_models(region='eu-central-1'):
    """Test available Bedrock models."""
    bedrock = boto3.client('bedrock-runtime', region_name=region)
    
    # Models to test
    test_models = [
        ('openai.gpt-oss-120b', 'OpenAI GPT OSS 120B'),
        ('openai.gpt-oss-20b', 'OpenAI GPT OSS 20B'),
        ('anthropic.claude-3-5-sonnet-20240620-v1:0', 'Claude 3.5 Sonnet'),
        ('anthropic.claude-3-sonnet-20240229-v1:0', 'Claude 3 Sonnet'),
        ('anthropic.claude-v2:1', 'Claude 2.1'),
        ('anthropic.claude-instant-v1', 'Claude Instant'),
        ('amazon.titan-text-express-v1', 'Titan Text Express'),
        ('amazon.titan-text-lite-v1', 'Titan Text Lite'),
        ('ai21.jamba-instruct-v1:0', 'AI21 Jamba'),
        ('ai21.j2-ultra-v1', 'AI21 Jurassic-2 Ultra'),
        ('meta.llama3-70b-instruct-v1:0', 'Llama 3 70B'),
        ('cohere.command-text-v14', 'Cohere Command'),
    ]
    
    print(f"Testing Bedrock Models in {region}...\n")
    available_models = []
    
    for model_id, model_name in test_models:
        try:
            # Try a simple test prompt
            if 'openai' in model_id:
                body = json.dumps({
                    'prompt': 'Hi',
                    'max_tokens': 10
                })
            elif 'claude' in model_id:
                body = json.dumps({
                    'anthropic_version': 'bedrock-2023-05-31',
                    'max_tokens': 10,
                    'messages': [{'role': 'user', 'content': 'Hi'}]
                })
            elif 'titan' in model_id:
                body = json.dumps({
                    'inputText': 'Hi',
                    'textGenerationConfig': {'maxTokenCount': 10}
                })
            elif 'ai21' in model_id:
                body = json.dumps({
                    'prompt': 'Hi',
                    'maxTokens': 10
                })
            elif 'llama' in model_id:
                body = json.dumps({
                    'prompt': 'Hi',
                    'max_gen_len': 10
                })
            elif 'cohere' in model_id:
                body = json.dumps({
                    'prompt': 'Hi',
                    'max_tokens': 10
                })
            
            response = bedrock.invoke_model(
                modelId=model_id,
                body=body
            )
            
            print(f"✅ {model_name}: AVAILABLE")
            available_models.append((model_id, model_name))
            
        except Exception as e:
            error_msg = str(e)
            if 'ValidationException' in error_msg:
                print(f"❌ {model_name}: NOT AVAILABLE (not enabled)")
            elif 'AccessDeniedException' in error_msg:
                print(f"⚠️  {model_name}: ACCESS DENIED (check IAM permissions)")
            else:
                print(f"❌ {model_name}: ERROR - {error_msg[:50]}")
    
    print(f"\n{'='*60}")
    print(f"Summary: {len(available_models)}/{len(test_models)} models available")
    print(f"{'='*60}")
    
    if available_models:
        print("\nAvailable models:")
        for model_id, model_name in available_models:
            print(f"  - {model_name} ({model_id})")
    else:
        print("\n⚠️  No models available. Check:")
        print("  1. AWS credentials configured")
        print("  2. IAM permissions for bedrock:InvokeModel")
        print("  3. Region supports Bedrock (eu-central-1)")

if __name__ == '__main__':
    import sys
    region = sys.argv[1] if len(sys.argv) > 1 else 'eu-central-1'
    test_bedrock_models(region)
