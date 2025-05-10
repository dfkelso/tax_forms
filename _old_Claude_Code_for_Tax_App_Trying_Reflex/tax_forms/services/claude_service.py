# tax_forms/services/claude_service.py
import os
import json
from typing import Dict, Any, Optional
import requests

class ClaudeService:
    """Service for interacting with the Claude AI API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the service with an API key."""
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            print("Warning: No Claude API key provided. AI features will not work.")
    
    def generate_tax_rules(self, form_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Generate tax rules for a form using Claude AI."""
        if not self.api_key:
            print("Error: No Claude API key provided.")
            return None
        
        prompt = self._build_tax_rule_prompt(form_data)
        
        try:
            response = self._make_claude_request(prompt)
            if response:
                return self._parse_json_response(response)
            return None
        except Exception as e:
            print(f"Error generating tax rules: {e}")
            return None
    
    def _make_claude_request(self, prompt: str) -> Optional[str]:
        """Make a request to the Claude AI API."""
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        
        data = {
            "model": "claude-3-haiku-20240307",
            "max_tokens": 4000,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            
            response_data = response.json()
            content = response_data.get("content", [])
            
            if content and len(content) > 0:
                return content[0].get("text", "")
            
            return None
        except requests.exceptions.RequestException as e:
            print(f"API request error: {e}")
            return None
    
    def _parse_json_response(self, response: str) -> Optional[Dict[str, Any]]:
        """Parse a JSON response from Claude AI."""
        try:
            # Look for JSON content in the response
            json_start = response.find("{")
            json_end = response.rfind("}")
            
            if json_start >= 0 and json_end >= 0:
                json_str = response[json_start:json_end + 1]
                return json.loads(json_str)
            
            # Alternative: Try to find JSON inside code blocks
            import re
            json_match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", response)
            
            if json_match:
                json_str = json_match.group(1)
                return json.loads(json_str)
            
            print("No JSON found in response")
            return None
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            return None
    
    def _build_tax_rule_prompt(self, form_data: Dict[str, Any]) -> str:
        """Build a prompt for generating tax rules."""
        return f"""
        You are a senior tax compliance specialist with expert knowledge of filing deadlines.
        
        I need you to research and determine the exact due dates and extension due dates for the following tax form:
        
        Form Number: {form_data.get('form_number', '')}
        Form Name: {form_data.get('form_name', '')}
        Entity Type: {form_data.get('entity_type', '')}
        Locality Type: {form_data.get('locality_type', '')}
        Locality: {form_data.get('locality', '')}
        
        Provide the tax filing deadlines for the last 7 years. For each year, determine both the standard filing deadline 
        and the maximum extension deadline.
        
        FORMAT YOUR RESPONSE AS VALID JSON:
        ```json
        {{
          "calculationRules": [
            {{
              "effectiveYears": [2020],
              "dueDate": {{
                "monthsAfterCalculationBase": 7,
                "dayOfMonth": 15
              }},
              "extensionDueDate": {{
                "monthsAfterCalculationBase": 11,
                "dayOfMonth": 15
              }}
            }},
            {{
              "effectiveYears": [2019, 2021, 2022, 2023, 2024],
              "dueDate": {{
                "monthsAfterCalculationBase": 5,
                "dayOfMonth": 15
              }},
              "extensionDueDate": {{
                "monthsAfterCalculationBase": 11,
                "dayOfMonth": 15
              }}
            }}
          ]
        }}
        ```
        
        Group years that have identical filing requirements together. Years with different requirements should be 
        in separate rule objects.
        
        If certain fiscal year endings have different rules (common for corporate returns), use fiscalYearExceptions.
        
        Provide ONLY the JSON result with no additional explanation.
        """