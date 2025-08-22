# IAM COP - IAM Policy Security Analyzer

A Streamlit application that analyzes AWS IAM policies for security risks using Amazon Bedrock.

## Features

- **JSON Syntax Highlighting**: Input and output editors with JSON syntax highlighting
- **AI-Powered Analysis**: Uses Amazon Bedrock (Claude 3 Sonnet) for intelligent policy analysis
- **Risk Scoring**: Color-coded risk assessment (1-5 scale)
- **Detailed Findings**: Comprehensive security analysis with recommendations
- **Real-time Validation**: JSON validation and error handling

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure AWS Credentials**:
   Ensure you have AWS credentials configured with access to Amazon Bedrock:
   ```bash
   aws configure
   ```
   
   Or set environment variables:
   ```bash
   export AWS_ACCESS_KEY_ID=your_access_key
   export AWS_SECRET_ACCESS_KEY=your_secret_key
   export AWS_DEFAULT_REGION=us-east-1
   ```

3. **Enable Bedrock Model Access**:
   - Go to AWS Console → Amazon Bedrock → Model access
   - Request access to "Claude 3 Sonnet" model

## Usage

1. **Run the Application**:
   ```bash
   streamlit run app.py
   ```

2. **Analyze IAM Policies**:
   - Paste your IAM policy JSON in the input editor
   - Click "Analyze Policy"
   - Review the risk score and detailed analysis

## Risk Levels

- 🟢 **Low (1)**: Minor issues, best practice improvements recommended
- 🟡 **Medium-Low (2)**: Some concerns, should be addressed but not critical
- 🟠 **Medium (3)**: Notable security gaps, requires remediation
- 🔴 **Medium-High (4)**: Significant security concerns, urgent remediation needed
- 🟣 **Critical (5)**: Severe security vulnerabilities, immediate action required

## Example Policy

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "*",
      "Resource": "*"
    }
  ]
}
```

## License

This project uses MIT-licensed libraries only:
- Streamlit (Apache 2.0)
- streamlit-ace (MIT)
- boto3 (Apache 2.0)