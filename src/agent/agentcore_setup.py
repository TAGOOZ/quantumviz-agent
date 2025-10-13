#!/usr/bin/env python3
"""
QuantumViz Agent - AgentCore Runtime Setup
Deploy and configure the core AI agent runtime.
"""

import boto3
import json
import time
import sys
import os
import logging
from botocore.exceptions import ClientError
# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_agentcore_agent():
    """Create the AgentCore agent for QuantumViz."""
    logger.info("Creating AgentCore agent for QuantumViz...")
    print("🤖 Creating AgentCore agent for QuantumViz...")
    
    try:
        # Initialize AgentCore client
        logger.debug(f"Initializing Bedrock Agent client in region: {Config.AWS_REGION}")
        agentcore = boto3.client('bedrock-agent', region_name=Config.AWS_REGION)
        
        # Agent configuration
        agent_config = {
            'agentName': 'QuantumViz-Agent',
            'description': 'AI agent that converts quantum code into interactive 3D visualizations with natural language explanations',
            'foundationModel': Config.FOUNDATION_MODEL,
            'instruction': """
            You are QuantumViz, an AI agent specialized in quantum computing education. Your mission is to:

            1. Parse and analyze quantum circuits written in QASM, Qiskit, or Cirq
            2. Explain quantum concepts in simple, accessible language
            3. Generate educational analogies for complex quantum phenomena
            4. Adapt explanations based on user expertise level (beginner/intermediate/advanced)
            5. Provide step-by-step guidance for quantum circuit understanding

            Always be educational, encouraging, and accurate in your quantum explanations.
            """.strip(),
            'idleSessionTTLInSeconds': 1800,  # 30 minutes
            'agentResourceRoleArn': Config.get_agent_role_arn()
        }
        
        # Create the agent
        logger.info("Creating agent with Bedrock Agent service...")
        response = agentcore.create_agent(**agent_config)
        agent_id = response['agent']['agentId']
        
        logger.info(f"Agent created successfully with ID: {agent_id}")
        print(f"✅ AgentCore agent created successfully!")
        print(f"   Agent ID: {agent_id}")
        print(f"   Agent Name: {agent_config['agentName']}")
        
        return agent_id
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        logger.error(f"AWS ClientError during agent creation: {error_code} - {error_message}")
        print(f"❌ AgentCore agent creation error: {error_message}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error during agent creation: {str(e)}", exc_info=True)
        print(f"❌ AgentCore agent creation error: {e}")
        return None

def create_agent_execution_role():
    """Create IAM role for AgentCore execution."""
    print("\n🔐 Creating AgentCore execution role...")
    
    try:
        iam = boto3.client('iam', region_name=Config.AWS_REGION)
        
        # Trust policy for AgentCore
        trust_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "bedrock.amazonaws.com"
                    },
                    "Action": "sts:AssumeRole"
                }
            ]
        }
        
        # Create the role
        role_response = iam.create_role(
            RoleName=Config.AGENT_ROLE_NAME,
            AssumeRolePolicyDocument=json.dumps(trust_policy),
            Description='Role for QuantumViz AgentCore execution'
        )
        
        # Attach more restrictive policies
        policies = [
            'arn:aws:iam::aws:policy/AmazonBedrockReadOnlyAccess',
        ]
        
        # Only attach write policies if explicitly configured
        if os.getenv('AGENT_FULL_ACCESS', 'false').lower() == 'true':
            policies.extend([
                'arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess',
                'arn:aws:iam::aws:policy/AmazonDynamoDBReadOnlyAccess'
            ])
        
        for policy_arn in policies:
            iam.attach_role_policy(
                RoleName=Config.AGENT_ROLE_NAME,
                PolicyArn=policy_arn
            )
        
        print("✅ AgentCore execution role created")
        print("   Role: AgentExecutionRole")
        print("   Policies: Bedrock, S3, DynamoDB access")
        
        return True
        
    except Exception as e:
        if "EntityAlreadyExists" in str(e):
            print("✅ AgentCore execution role already exists")
            return True
        else:
            print(f"❌ Role creation error: {e}")
            return False

def create_agent_knowledge_base():
    """Create knowledge base for quantum computing information."""
    print("\n📚 Creating quantum computing knowledge base...")
    
    try:
        agentcore = boto3.client('bedrock-agent', region_name=Config.AWS_REGION)
        
        # Knowledge base configuration
        kb_config = {
            'name': 'QuantumComputing-KnowledgeBase',
            'description': 'Knowledge base containing quantum computing concepts, algorithms, and educational materials',
            'knowledgeBaseConfiguration': {
                'type': 'VECTOR',
                'vectorKnowledgeBaseConfiguration': {
                    'embeddingModelArn': Config.EMBEDDING_MODEL_ARN
                }
            },
            'storageConfiguration': {
                'type': 'OPENSEARCH_SERVERLESS',
                'opensearchServerlessConfiguration': {
                    'collectionArn': Config.get_kb_collection_arn(),
                    'vectorIndexName': Config.VECTOR_INDEX_NAME,
                    'fieldMapping': {
                        'vectorField': 'vector',
                        'textField': 'text',
                        'metadataField': 'metadata'
                    }
                }
            }
        }
        
        # Create knowledge base
        response = agentcore.create_knowledge_base(**kb_config)
        kb_id = response['knowledgeBase']['knowledgeBaseId']
        
        print(f"✅ Knowledge base created successfully!")
        print(f"   Knowledge Base ID: {kb_id}")
        print(f"   Name: {kb_config['name']}")
        
        return kb_id
        
    except Exception as e:
        print(f"❌ Knowledge base creation error: {e}")
        print("   Note: This requires OpenSearch Serverless setup")
        return None

def test_agentcore_agent():
    """Test the created AgentCore agent."""
    print("\n🧪 Testing AgentCore agent...")
    
    try:
        agentcore = boto3.client('bedrock-agent', region_name=Config.AWS_REGION)
        
        # List agents
        response = agentcore.list_agents()
        agents = response['agentSummaries']
        
        print(f"✅ Found {len(agents)} AgentCore agents:")
        
        for agent in agents:
            print(f"   • {agent['agentName']} ({agent['agentId']})")
            print(f"     Status: {agent['agentStatus']}")
            print(f"     Created: {agent['createdAt']}")
        
        return len(agents) > 0
        
    except Exception as e:
        print(f"❌ AgentCore test error: {e}")
        return False

def create_agent_alias():
    """Create an alias for the agent for easier access."""
    print("\n🏷️  Creating agent alias...")
    
    try:
        agentcore = boto3.client('bedrock-agent', region_name=Config.AWS_REGION)
        
        # List agents to get the latest agent ID
        response = agentcore.list_agents()
        agents = response['agentSummaries']
        
        if not agents:
            print("❌ No agents found to create alias for")
            return None
        
        agent_id = agents[0]['agentId']  # Use the first agent
        
        # Create alias
        alias_config = {
            'agentId': agent_id,
            'agentAliasName': 'QuantumViz-Live',
            'description': 'Live alias for QuantumViz Agent'
        }
        
        response = agentcore.create_agent_alias(**alias_config)
        alias_id = response['agentAlias']['agentAliasId']
        
        print(f"✅ Agent alias created!")
        print(f"   Alias: {alias_config['agentAliasName']}")
        print(f"   Alias ID: {alias_id}")
        
        return alias_id
        
    except Exception as e:
        print(f"❌ Alias creation error: {e}")
        return None

def main():
    """Main function to set up AgentCore runtime."""
    print("🚀 QuantumViz Agent - AgentCore Runtime Setup")
    print("=" * 60)
    
    # Create execution role
    role_ok = create_agent_execution_role()
    
    if role_ok:
        # Create agent
        agent_id = create_agentcore_agent()
        
        if agent_id:
            # Test agent
            test_ok = test_agentcore_agent()
            
            if test_ok:
                # Create alias
                alias_id = create_agent_alias()
                
                # Create knowledge base (optional)
                kb_id = create_agent_knowledge_base()
                
                print("\n" + "=" * 60)
                print("🎉 AgentCore Runtime Setup Complete!")
                print("=" * 60)
                print(f"✅ Agent ID: {agent_id}")
                if alias_id:
                    print(f"✅ Alias ID: {alias_id}")
                if kb_id:
                    print(f"✅ Knowledge Base ID: {kb_id}")
                
                print("\n💡 Next Steps:")
                print("   1. Deploy agent to runtime")
                print("   2. Test agent with quantum circuit queries")
                print("   3. Integrate with Bedrock and Braket")
                
            else:
                print("\n⚠️  AgentCore agent created but testing failed")
        else:
            print("\n❌ AgentCore agent creation failed")
    else:
        print("\n❌ IAM role creation failed")

if __name__ == "__main__":
    main()

