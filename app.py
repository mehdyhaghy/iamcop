import streamlit as st
import json
import boto3
from datetime import datetime
import uuid
from streamlit_ace import st_ace

# Configure page
st.set_page_config(
    page_title="IAM Cop - IAM Policy Reviewer",
    page_icon="🔒",
    layout="wide"
)

# Model configurations
MODELS = {
    "Amazon Nova Pro": "us.amazon.nova-pro-v1:0",
    "Anthropic Claude 3.7 Sonnet": "us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    "Anthropic Claude 4 Sonnet": "us.anthropic.claude-sonnet-4-20250514-v1:0"
}

# Initialize Bedrock client
@st.cache_resource
def init_bedrock_client():
    try:
        return boto3.client('bedrock-runtime', region_name='us-east-1')
    except Exception as e:
        st.error(f"Failed to initialize Bedrock client: {str(e)}")
        return None

def get_risk_color(risk_score):
    """Return color based on risk score"""
    if risk_score <= 1:
        return "#006400"  # Dark Green
    elif risk_score <= 2:
        return "#90EE90"  # Light Green
    elif risk_score <= 3:
        return "#ffc107"  # Yellow
    elif risk_score <= 4:
        return "#ff8c00"  # Orange
    else:
        return "#8b0000"  # Dark Red

def get_risk_category(risk_score):
    """Return risk category based on score"""
    if risk_score <= 1:
        return "Low"
    elif risk_score <= 2:
        return "Medium-Low"
    elif risk_score <= 3:
        return "Medium"
    elif risk_score <= 4:
        return "Medium-High"
    else:
        return "Critical"

def analyze_policy_with_bedrock(policy_json, bedrock_client, model_id):
    """Analyze IAM policy using Amazon Bedrock Converse API"""
    
    prompt = f"""You are a cloud security engineer tasked with reviewing AWS IAM policies for security risks.

First, identify the policy type (Identity-based, Resource-based, Trust policy, Permissions boundary, etc.) and include this in your analysis.

Input: {policy_json}

Review Criteria:
Evaluate the policy for the following security red flags:

1. Overly Permissive Actions
   - Wildcard usage in actions (e.g., "*", "s3:*")
   - Administrative privileges (e.g., "iam:*", "organizations:*")
   - Dangerous actions (e.g., "iam:PassRole", "sts:AssumeRole")

2. Resource Scope Issues
   - Wildcard resources ("*")
   - Overly broad resource patterns
   - Cross-account access without proper controls

3. Missing Security Controls
   - Lack of condition statements
   - No MFA requirements for sensitive actions
   - Missing IP restrictions for privileged operations
   - No time-based access controls

4. Policy Structure Issues
   - Mixing Allow and Deny statements improperly
   - Redundant or conflicting permissions
   - Policy size and complexity

5. Compliance Violations
   - Violations of least privilege principle
   - Non-compliance with organizational standards
   - Potential data exposure risks

Risk Scoring Scale:
- 1 (Low Risk)
- 2 (Medium-Low Risk)
- 3 (Medium Risk)
- 4 (Medium-High Risk)
- 5 (Critical Risk)

Provide the analysis in the following JSON structure:
{{
  "ticket_id": "string",
  "review_timestamp": "ISO 8601 timestamp",
  "policy_type": "string (Identity-based|Resource-based|Trust policy|Permissions boundary|etc.)",
  "overall_risk_score": "number (1-5)",
  "risk_category": "Low|Medium-Low|Medium|Medium-High|Critical",
  "findings": [
    {{
      "finding_id": "string",
      "category": "string (from review criteria)",
      "severity": "number (1-5)",
      "description": "string",
      "affected_elements": {{
        "actions": ["string"],
        "resources": ["string"],
        "conditions": ["string"]
      }},
      "recommendation": "string",
      "references": ["string"]
    }}
  ],
  "summary": {{
    "total_findings": "number",
    "critical_findings": "number",
    "high_findings": "number",
    "medium_findings": "number",
    "low_findings": "number"
  }},
  "recommendations": {{
    "immediate_actions": ["string"],
    "short_term_improvements": ["string"],
    "long_term_considerations": ["string"]
  }},
  "compliant_with_standards": {{
    "least_privilege": "boolean",
    "zero_trust": "boolean",
    "organizational_policies": "boolean"
  }},
  "auto_remediation_possible": "boolean",
  "suggested_policy": "object (optional - provide improved version if applicable)"
}}

Return only the JSON response without any additional text."""

    try:
        # Set max tokens based on model
        if "nova" in model_id:
            max_tokens = 10000
        elif "claude-3-sonnet" in model_id:
            max_tokens = 32000
        else:
            max_tokens = 32000
        
        response = bedrock_client.converse(
            modelId=model_id,
            messages=[
                {
                    "role": "user",
                    "content": [{"text": prompt}]
                }
            ],
            inferenceConfig={
                "maxTokens": max_tokens,
                "temperature": 0.5
            }
        )
        
        analysis_text = response['output']['message']['content'][0]['text']
        
        # Extract JSON from response
        start_idx = analysis_text.find('{')
        end_idx = analysis_text.rfind('}') + 1
        json_str = analysis_text[start_idx:end_idx]
        
        return json.loads(json_str)
    
    except Exception as e:
        st.error(f"Error analyzing policy: {str(e)}")
        return None

def main():
    st.title("🔒 IAM Cop - IAM Policy Security Reviewer")
    st.markdown("Analyze AWS IAM policies for security risks using Amazon Bedrock")
    
    # Initialize Bedrock client
    bedrock_client = init_bedrock_client()
    
    if not bedrock_client:
        st.error("Cannot proceed without Bedrock client. Please check your AWS credentials and region.")
        return
    
    # Create sidebar for model selection
    with st.sidebar:
        selected_model = st.selectbox(
            "🤖 Select AI Model",
            options=list(MODELS.keys()),
            index=1
        )
        
        st.markdown("---")
        st.markdown("## ℹ️ About IAM COP")
        st.markdown("""
        IAM COP helps you analyze AWS IAM policies for security risks using Amazon Bedrock's AI capabilities.
        
        **Features:**
        - Real-time policy analysis
        - Risk scoring (1-5 scale)
        - Detailed security findings
        - Remediation recommendations
        """)
        
        st.markdown("**Risk Levels:**")
        st.markdown(
            "<span style='color: #006400;'>●</span> Low (1)<br>"
            "<span style='color: #90EE90;'>●</span> Medium-Low (2)<br>"
            "<span style='color: #ffc107;'>●</span> Medium (3)<br>"
            "<span style='color: #ff8c00;'>●</span> High (4)<br>"
            "<span style='color: #8b0000;'>●</span> Critical (5)",
            unsafe_allow_html=True
        )
    
    st.subheader("📝 IAM Policy Input")
    
    # JSON editor with syntax highlighting
    policy_input = st_ace(
        value='{\n  "Version": "2012-10-17",\n  "Statement": [\n    {\n      "Effect": "Allow",\n      "Action": "*",\n      "Resource": "*"\n    }\n  ]\n}',
        language='json',
        theme='monokai',
        key="policy_editor",
        height=300,
        auto_update=False
    )
    
    analyze_button = st.button("🔍 Analyze Policy", type="primary")
    
    st.subheader("📊 Security Analysis Results")
    
    if analyze_button and policy_input:
            try:
                # Validate JSON
                json.loads(policy_input)
                
                with st.spinner(f"Analyzing policy with {selected_model}..."):
                    model_id = MODELS[selected_model]
                    analysis = analyze_policy_with_bedrock(policy_input, bedrock_client, model_id)
                
                if analysis:
                    # Risk Score Display
                    risk_score = analysis.get('overall_risk_score', 0)
                    risk_category = analysis.get('risk_category', 'Unknown')
                    
                    st.markdown("### 🎯 Risk Assessment")
                    
                    # Risk score with color coding (smaller)
                    risk_color = get_risk_color(risk_score)
                    st.markdown(
                        f"""
                        <div style="
                            background-color: {risk_color}; 
                            color: white; 
                            padding: 10px; 
                            border-radius: 5px; 
                            text-align: center;
                            margin: 5px 0;
                        ">
                            <h4 style="margin: 0;">Risk Score: {risk_score}/5 - {risk_category}</h4>
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )
                    
                    # Human readable summary
                    st.markdown("### 📋 Analysis Summary")
                    summary_text = ""
                    if 'findings' in analysis and analysis['findings']:
                        summary_text += f"**Total Findings:** {len(analysis['findings'])}\n\n"
                        for finding in analysis['findings']:  # Show all findings
                            summary_text += f"• **{finding.get('category', 'Security Issue')}** (Severity {finding.get('severity', 'N/A')}): {finding.get('description', 'No description')}\n\n"
                            if finding.get('recommendation'):
                                summary_text += f"  **Recommendation:** {finding.get('recommendation')}\n\n"
                            else:
                                summary_text += "\n"
                    
                    if 'recommendations' in analysis and 'immediate_actions' in analysis['recommendations']:
                        summary_text += "**Immediate Actions:**\n"
                        for action in analysis['recommendations']['immediate_actions']:  # Show all actions
                            summary_text += f"• {action}\n"
                    
                    st.markdown(summary_text)
                    
                    # JSON Analysis Results
                    st.markdown("### 📄 Detailed JSON Analysis")
                    st_ace(
                        value=json.dumps(analysis, indent=2),
                        language='json',
                        theme='monokai',
                        key="analysis_output",
                        height=300,
                        readonly=True
                    )
                    
                    # Summary metrics
                    if 'summary' in analysis:
                        summary = analysis['summary']
                        st.markdown("### 📈 Findings Summary")
                        
                        metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
                        with metrics_col1:
                            st.metric("Total Findings", summary.get('total_findings', 0))
                        with metrics_col2:
                            st.metric("Critical", summary.get('critical_findings', 0))
                        with metrics_col3:
                            st.metric("High Risk", summary.get('high_findings', 0))
                
            except json.JSONDecodeError:
                st.error("❌ Invalid JSON format. Please check your policy syntax.")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    elif not policy_input and analyze_button:
        st.warning("⚠️ Please enter an IAM policy to analyze.")

if __name__ == "__main__":
    main()