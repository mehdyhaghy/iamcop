"""Configuration settings for IAM COP application"""

# AWS Bedrock Configuration
BEDROCK_REGION = 'us-east-1'
BEDROCK_MODEL_ID = 'anthropic.claude-3-sonnet-20240229-v1:0'

# Risk Score Colors
RISK_COLORS = {
    1: "#28a745",  # Green - Low
    2: "#ffc107",  # Yellow - Medium-Low
    3: "#fd7e14",  # Orange - Medium
    4: "#dc3545",  # Red - Medium-High
    5: "#6f42c1"   # Purple - Critical
}

# Risk Categories
RISK_CATEGORIES = {
    1: "Low",
    2: "Medium-Low", 
    3: "Medium",
    4: "Medium-High",
    5: "Critical"
}