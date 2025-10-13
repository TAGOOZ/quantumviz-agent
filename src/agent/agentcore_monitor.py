#!/usr/bin/env python3
"""
QuantumViz Agent - AgentCore Status Monitor
Monitor AgentCore agent status and test when ready.
"""

import boto3
import json
import time

def check_agent_status():
    """Check the status of our AgentCore agent."""
    print("🔍 Checking AgentCore agent status...")
    
    try:
        agentcore = boto3.client('bedrock-agent', region_name='eu-central-1')
        
        # Get agent details
        response = agentcore.get_agent(agentId='DRC1I6SIWE')
        agent = response['agent']
        
        print(f"✅ Agent Status:")
        print(f"   Name: {agent['agentName']}")
        print(f"   Status: {agent['agentStatus']}")
        print(f"   Model: {agent['foundationModel']}")
        print(f"   Created: {agent['createdAt']}")
        
        if 'updatedAt' in agent:
            print(f"   Updated: {agent['updatedAt']}")
        
        return agent['agentStatus']
        
    except Exception as e:
        print(f"❌ Agent status check error: {e}")
        return None

def list_agent_versions():
    """List agent versions and their status."""
    print("\n📋 Checking agent versions...")
    
    try:
        agentcore = boto3.client('bedrock-agent', region_name='eu-central-1')
        
        response = agentcore.list_agent_versions(agentId='DRC1I6SIWE')
        versions = response['agentVersionSummaries']
        
        print(f"✅ Found {len(versions)} agent versions:")
        
        for version in versions:
            print(f"   • Version {version['agentVersion']}: {version['agentStatus']}")
            print(f"     Created: {version['createdAt']}")
        
        return versions
        
    except Exception as e:
        print(f"❌ Version list error: {e}")
        return []

def create_agent_alias_if_ready():
    """Create agent alias if agent is ready."""
    print("\n🏷️  Checking if agent alias can be created...")
    
    try:
        agentcore = boto3.client('bedrock-agent', region_name='eu-central-1')
        
        # Check if agent is ready
        agent_status = check_agent_status()
        
        if agent_status == 'PREPARED':
            print("✅ Agent is ready! Creating alias...")
            
            # Create alias
            alias_response = agentcore.create_agent_alias(
                agentId='DRC1I6SIWE',
                agentAliasName='QuantumViz-Live',
                description='Live alias for QuantumViz Agent'
            )
            
            alias_id = alias_response['agentAlias']['agentAliasId']
            print(f"✅ Alias created: {alias_id}")
            
            return alias_id
            
        else:
            print(f"⏳ Agent not ready yet (Status: {agent_status})")
            return None
            
    except Exception as e:
        if "already exists" in str(e).lower():
            print("✅ Agent alias already exists")
            return "EXISTS"
        else:
            print(f"❌ Alias creation error: {e}")
            return None

def test_agent_invocation():
    """Test agent invocation if ready."""
    print("\n🧪 Testing agent invocation...")
    
    try:
        # Check if we have an alias
        agentcore = boto3.client('bedrock-agent', region_name='eu-central-1')
        
        # List aliases
        aliases_response = agentcore.list_agent_aliases(agentId='DRC1I6SIWE')
        aliases = aliases_response['agentAliasSummaries']
        
        if not aliases:
            print("❌ No aliases found. Agent may not be ready yet.")
            return False
        
        alias = aliases[0]
        print(f"✅ Using alias: {alias['agentAliasName']} ({alias['agentAliasId']})")
        
        # Test invocation
        runtime = boto3.client('bedrock-agent-runtime', region_name='eu-central-1')
        
        test_prompt = "Hello! Can you explain what quantum entanglement is?"
        
        response = runtime.invoke_agent(
            agentId='DRC1I6SIWE',
            agentAliasId=alias['agentAliasId'],
            sessionId='test-session-001',
            inputText=test_prompt
        )
        
        print("✅ Agent invocation successful!")
        print(f"   Session: {response['sessionId']}")
        
        # Read the response
        for event in response['completion']:
            if 'chunk' in event:
                chunk = event['chunk']
                if 'bytes' in chunk:
                    text = chunk['bytes'].decode('utf-8')
                    print(f"   Response: {text}")
        
        return True
        
    except Exception as e:
        print(f"❌ Agent invocation error: {e}")
        return False

def main():
    """Main function to monitor AgentCore status."""
    print("🚀 QuantumViz Agent - AgentCore Status Monitor")
    print("=" * 60)
    
    # Check agent status
    status = check_agent_status()
    
    if status:
        print(f"\n📊 Current Status: {status}")
        
        if status == 'PREPARED':
            print("🎉 Agent is ready for use!")
            
            # Create alias if needed
            alias_id = create_agent_alias_if_ready()
            
            if alias_id:
                # Test invocation
                test_ok = test_agent_invocation()
                
                if test_ok:
                    print("\n✅ AgentCore integration complete!")
                    print("💡 Ready for quantum circuit explanations")
                else:
                    print("\n⚠️  Agent created but invocation needs work")
            
        elif status == 'CREATING':
            print("⏳ Agent is still being created...")
            print("   This usually takes 2-5 minutes")
            print("   Check again in a few minutes")
            
        elif status == 'FAILED':
            print("❌ Agent creation failed")
            print("   Check AWS console for details")
            
        else:
            print(f"📋 Agent status: {status}")
            print("   Monitor progress in AWS console")
    
    # List versions for additional info
    versions = list_agent_versions()
    
    print(f"\n📋 Summary:")
    print(f"   Agent Status: {status}")
    print(f"   Versions: {len(versions)}")

if __name__ == "__main__":
    main()

