"""
QuantumViz Agent - Configuration Module
Centralized configuration management for the QuantumViz Agent.
"""

import os
import logging
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Config:
    """Configuration class for QuantumViz Agent."""
    
    # AWS Configuration
    AWS_REGION = os.getenv('AWS_REGION', 'eu-central-1')
    AWS_ACCOUNT_ID = os.getenv('AWS_ACCOUNT_ID', '082979152822')
    
    # Agent Configuration
    AGENT_NAME = os.getenv('AGENT_NAME', 'QuantumViz-Agent')
    AGENT_ROLE_NAME = os.getenv('AGENT_ROLE_NAME', 'AgentExecutionRole')
    
    # Model Configuration
    FOUNDATION_MODEL = os.getenv('FOUNDATION_MODEL', 'anthropic.claude-3-5-sonnet-20240620-v1:0')
    EMBEDDING_MODEL_ARN = os.getenv('EMBEDDING_MODEL_ARN', 
                                  f'arn:aws:bedrock:{AWS_REGION}::foundation-model/amazon.titan-embed-text-v1')
    
    # Knowledge Base Configuration
    KB_NAME = os.getenv('KB_NAME', 'QuantumComputing-KnowledgeBase')
    KB_COLLECTION_ARN = os.getenv('KB_COLLECTION_ARN', 
                                f'arn:aws:aoss:{AWS_REGION}:{AWS_ACCOUNT_ID}:collection/quantumviz-collection')
    
    # OpenSearch Configuration
    VECTOR_INDEX_NAME = os.getenv('VECTOR_INDEX_NAME', 'quantum-knowledge-index')
    
    # S3 Configuration
    S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME', 'quantumviz-agent-assets')
    
    @classmethod
    def get_agent_role_arn(cls) -> str:
        """Get the full ARN for the agent execution role."""
        return f'arn:aws:iam::{cls.AWS_ACCOUNT_ID}:role/{cls.AGENT_ROLE_NAME}'
    
    @classmethod
    def get_kb_collection_arn(cls) -> str:
        """Get the full ARN for the knowledge base collection."""
        return f'arn:aws:aoss:{cls.AWS_REGION}:{cls.AWS_ACCOUNT_ID}:collection/quantumviz-collection'
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate critical configuration values."""
        errors = []
        
        # Validate AWS region
        valid_regions = ['us-east-1', 'us-west-2', 'eu-central-1', 'eu-west-1', 'ap-southeast-1']
        if cls.AWS_REGION not in valid_regions:
            logger.warning(f"AWS_REGION '{cls.AWS_REGION}' may not be valid. Valid regions: {valid_regions}")
        
        # Validate AWS account ID format (12 digits)
        if not cls.AWS_ACCOUNT_ID.isdigit() or len(cls.AWS_ACCOUNT_ID) != 12:
            errors.append(f"Invalid AWS_ACCOUNT_ID format: {cls.AWS_ACCOUNT_ID}")
        
        # Log configuration loaded
        logger.info(f"Configuration loaded: Region={cls.AWS_REGION}, Account={cls.AWS_ACCOUNT_ID}")
        
        if errors:
            for error in errors:
                logger.error(error)
            return False
        
        return True
