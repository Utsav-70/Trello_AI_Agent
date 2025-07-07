import os
from typing import List, Dict
import json
import requests
import time
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from huggingface_hub import InferenceClient
import torch

class TrelloAgent:
    def __init__(self):
        self.hf_api_key = os.getenv('HUGGINGFACE_API_KEY')
        self.model_name = os.getenv('HF_MODEL_NAME', 'microsoft/DialoGPT-medium')
        
        if not self.hf_api_key:
            raise ValueError("Please set HUGGINGFACE_API_KEY in your .env file")
        
        # Initialize Hugging Face client
        self.client = InferenceClient(
            model=self.model_name,
            token=self.hf_api_key
        )
        
        # Alternative: Local model setup (uncomment if you want to run locally)
        # self.setup_local_model()
        
        print(f"🤖 Initialized Hugging Face agent with model: {self.model_name}")
    
    def setup_local_model(self):
        """Setup local Hugging Face model (optional)"""
        try:
            print("🔄 Loading local Hugging Face model...")
            
            # Check if CUDA is available
            device = "cuda" if torch.cuda.is_available() else "cpu"
            print(f"🖥️ Using device: {device}")
            
            # Load tokenizer and model
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float16 if device == "cuda" else torch.float32,
                device_map="auto" if device == "cuda" else None
            )
            
            # Create text generation pipeline
            self.pipeline = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                device=0 if device == "cuda" else -1,
                max_length=512,
                temperature=0.7,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
            
            print("✅ Local model loaded successfully!")
            self.use_local_model = True
            
        except Exception as e:
            print(f"⚠️ Could not load local model: {str(e)}")
            print("📡 Will use Hugging Face Inference API instead")
            self.use_local_model = False
    
    async def analyze_members_with_api(self, members_data: List[Dict]) -> str:
        """Analyze member data using Hugging Face Inference API"""
        try:
            members_json = json.dumps(members_data, indent=2)
            
            # Create analysis prompt
            prompt = f"""
Task: Analyze the following Trello team member data and provide insights.

Team Member Data:
{members_json}

Please provide a comprehensive analysis including:
1. Team composition summary
2. Data quality assessment
3. Security recommendations
4. User management suggestions
5. Any anomalies or concerns

Analysis:
"""
            
            # Use Hugging Face Inference API
            response = self.client.text_generation(
                prompt,
                max_new_tokens=500,
                temperature=0.7,
                do_sample=True,
                return_full_text=False
            )
            
            return response
            
        except Exception as e:
            print(f"❌ Error with Hugging Face API: {str(e)}")
            return self.fallback_analysis(members_data)
    
    def analyze_members_with_local_model(self, members_data: List[Dict]) -> str:
        """Analyze member data using local Hugging Face model"""
        try:
            members_json = json.dumps(members_data, indent=2)
            
            prompt = f"""
Analyze this Trello team data:

{members_json}

Provide insights on team composition, security, and user management:
"""
            
            # Generate response using local model
            response = self.pipeline(
                prompt,
                max_new_tokens=300,
                temperature=0.7,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
            
            # Extract generated text
            generated_text = response[0]['generated_text']
            
            # Remove the prompt from the response
            analysis = generated_text.replace(prompt, "").strip()
            
            return analysis
            
        except Exception as e:
            print(f"❌ Error with local model: {str(e)}")
            return self.fallback_analysis(members_data)
    
    async def analyze_members(self, members_data: List[Dict]) -> str:
        """Main analysis method that tries different approaches"""
        print("🔍 Analyzing member data with Hugging Face...")
        
        # Try API first
        try:
            return await self.analyze_members_with_api(members_data)
        except Exception as e:
            print(f"⚠️ API analysis failed: {str(e)}")
            
            # Try local model if available
            if hasattr(self, 'use_local_model') and self.use_local_model:
                print("🔄 Trying local model...")
                return self.analyze_members_with_local_model(members_data)
            
            # Fallback to rule-based analysis
            return self.fallback_analysis(members_data)
    
    def fallback_analysis(self, members_data: List[Dict]) -> str:
        """Fallback analysis using rule-based approach"""
        print("🔄 Using fallback rule-based analysis...")
        
        total_members = len(members_data)
        
        # Count members with email data
        members_with_email = len([m for m in members_data if m['email'] != 'Not available in free tier'])
        
        # Basic analysis
        analysis = f"""
🔍 TRELLO TEAM ANALYSIS REPORT
{'=' * 50}

📊 TEAM COMPOSITION:
- Total Members: {total_members}
- Members with Email Data: {members_with_email}
- Members without Email Data: {total_members - members_with_email}

👥 MEMBER DETAILS:
"""
        
        for i, member in enumerate(members_data, 1):
            analysis += f"\n{i}. {member['name']}"
            analysis += f"\n   Email: {member['email']}"
            analysis += f"\n   Role: {member['role']}"
            analysis += f"\n   Last Login: {member['last_login']}\n"
        
        analysis += f"""
📋 DATA QUALITY ASSESSMENT:
- Email Availability: {(members_with_email/total_members)*100:.1f}% of members
- Role Information: Limited (Free tier restriction)
- Activity Data: Limited (Free tier restriction)

🔐 SECURITY RECOMMENDATIONS:
1. Upgrade to Trello paid plan for better user management
2. Regular access reviews for team members
3. Enable two-factor authentication for all members
4. Monitor board access and permissions

⚙️ USER MANAGEMENT SUGGESTIONS:
1. Review member access levels regularly
2. Remove inactive members to reduce security risks
3. Use proper naming conventions for team organization
4. Consider board-specific permissions

⚠️ LIMITATIONS NOTED:
- Free Trello tier provides limited member data
- Role and activity information requires paid plan
- Email data may not be available for all members
"""
        
        return analysis
    
    def generate_provisioning_recommendations(self, members_data: List[Dict]) -> Dict:
        """Generate specific provisioning/deprovisioning recommendations"""
        recommendations = {
            'provision': [],
            'deprovision': [],
            'review': [],
            'upgrade_needed': []
        }
        
        for member in members_data:
            if member['email'] == 'Not available in free tier':
                recommendations['review'].append({
                    'name': member['name'],
                    'reason': 'Email not available - manual review required',
                    'action': 'Verify member access and contact information'
                })
            
            if member['last_login'] == 'Not available in free tier':
                recommendations['upgrade_needed'].append({
                    'name': member['name'],
                    'reason': 'Activity data requires paid plan',
                    'action': 'Consider upgrading Trello plan for better user management'
                })
            
            if member['role'] == 'Member' and member['name'] != 'Current User':
                recommendations['review'].append({
                    'name': member['name'],
                    'reason': 'Role verification needed',
                    'action': 'Confirm appropriate access level'
                })
        
        return recommendations
    
    def generate_security_report(self, members_data: List[Dict]) -> str:
        """Generate a security-focused report"""
        report = f"""
🔒 SECURITY ANALYSIS REPORT
{'=' * 40}

Team Size: {len(members_data)} members

🚨 SECURITY CONCERNS:
"""
        
        concerns = []
        
        # Check for data availability issues
        no_email_count = len([m for m in members_data if m['email'] == 'Not available in free tier'])
        if no_email_count > 0:
            concerns.append(f"- {no_email_count} members without email data")
        
        # Check for unknown members
        unknown_count = len([m for m in members_data if 'Unknown' in m['name']])
        if unknown_count > 0:
            concerns.append(f"- {unknown_count} members with unknown names")
        
        if concerns:
            report += "\n".join(concerns)
        else:
            report += "- No major security concerns identified"
        
        report += f"""

✅ RECOMMENDATIONS:
1. Enable audit logging (requires paid plan)
2. Regular access reviews
3. Implement least privilege access
4. Monitor for unusual activity
5. Use strong authentication methods

📈 NEXT STEPS:
- Consider upgrading to paid Trello plan for better security features
- Implement regular user access reviews
- Set up automated monitoring for team changes
"""
        
        return report