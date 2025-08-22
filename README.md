# IAM COP - IAM Policy Security Analyzer

An AI-powered Streamlit application that analyzes AWS IAM policies for security risks using Amazon Bedrock.

## Features

- **AI-Powered Analysis**: Uses Amazon Bedrock (Claude 3.7 Sonnet, Claude 4 Sonnet, Nova Pro) for intelligent policy analysis
- **Policy Type Detection**: Automatically identifies policy type (Identity-based, Resource-based, Trust policy, etc.)
- **Risk Scoring**: Color-coded risk assessment (1-5 scale) with detailed findings
- **JSON Syntax Highlighting**: Input and output editors with syntax highlighting
- **Individual Recommendations**: Specific remediation guidance for each security finding
- **Real-time Validation**: JSON validation and error handling

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/mehdyhaghy/iamcop.git
   cd iamcop
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure AWS credentials**:
   ```bash
   aws configure
   ```
   Or set environment variables:
   ```bash
   export AWS_ACCESS_KEY_ID=your_access_key
   export AWS_SECRET_ACCESS_KEY=your_secret_key
   export AWS_DEFAULT_REGION=us-east-1
   ```

4. **Enable Bedrock model access**:
   - Go to AWS Console → Amazon Bedrock → Model access
   - Request access to Claude and Nova models

## Usage

1. **Run the application**:
   ```bash
   streamlit run app.py
   ```

2. **Analyze policies**:
   - Select AI model from sidebar
   - Paste IAM policy JSON in the editor
   - Click "Analyze Policy"
   - Review risk assessment and recommendations

## Risk Levels

- 🟢 **Low (1)**: Minor issues
- 🟢 **Medium-Low (2)**: Some concerns
- 🟡 **Medium (3)**: Notable gaps
- 🟠 **High (4)**: Significant concerns
- 🔴 **Critical (5)**: Severe vulnerabilities

## Requirements

- Python 3.8+
- AWS account with Bedrock access
- Streamlit
- boto3