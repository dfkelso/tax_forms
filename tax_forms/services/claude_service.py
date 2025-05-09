# tax_forms/services/claude_service.py
import os
import json
from typing import Dict, Any, Optional
import anthropic

class ClaudeService:
    """Service for interacting with Claude AI to generate tax rules."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the Claude service with an API key."""
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY", "")
        
        if not self.api_key:
            print("Warning: ANTHROPIC_API_KEY not set. AI features will not work.")
    
    def generate_tax_rules(self, form_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Generate tax form rules using Claude AI."""
        if not self.api_key:
            return None
            
        try:
            client = anthropic.Anthropic(api_key=self.api_key)
            
            # Create prompt for Claude
            prompt = self._build_tax_rule_prompt(form_data)
            
            # Call Claude API
            message = client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=4000,
                temperature=0,
                system="You are a tax expert who provides JSON responses containing tax form calculation rules.",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            # Parse the response
            response_text = message.content[0].text
            return self._parse_response(response_text)
            
        except Exception as e:
            print(f"Error calling Claude API: {e}")
            return None
    
    def _build_tax_rule_prompt(self, form_data: Dict[str, Any]) -> str:
        """Build the prompt for generating tax rules."""
        current_year = 2025  # Fixed for now, could use datetime
        seven_years_ago = current_year - 6

        return f"""
        You are a senior tax compliance specialist with expert knowledge of filing deadlines across all IRS forms, state tax forms, and local tax forms. 

        I need you to research and determine the exact due dates and extension due dates for the following tax form for each year from {seven_years_ago} through {current_year}:

        Form Number: {form_data.get('form_number')}
        Form Name: {form_data.get('form_name')}
        Entity Type: {form_data.get('entity_type')}
        Locality Type: {form_data.get('locality_type')}
        Locality: {form_data.get('locality')}

        RESEARCH GUIDELINES:
        1. Use multiple official sources to verify deadlines. Primary sources like IRS.gov, state tax department websites, and official tax calendars are most reliable.
        2. For each year, determine both the standard filing deadline and the maximum extension deadline.
        3. Pay special attention to any COVID-19 related changes in 2020-2021, as many tax deadlines were extended.
        4. Account for any changes to standard filing deadlines that occurred over the past 7 years.
        5. Consider any special rules that apply to the specific entity type ({form_data.get('entity_type')}).
        6. For fiscal year entities, note any different rules that apply to different fiscal year ends.
        7. Account for weekend/holiday adjustments in your base calculations.
        8. For foreign entity forms, take into account any special international filing rules.

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
              "effectiveYears": [2019, 2021, 2022, 2023, 2024, 2025],
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

        GROUPING RULES:
        - Group years that have identical filing requirements together.
        - Years with different requirements (like 2020 COVID extensions) should be in separate rule objects.
        - If certain fiscal year endings have different rules (common for corporate returns), use fiscalYearExceptions like:
        ```
        "fiscalYearExceptions": {{
          "06": {{  // For June fiscal year end
            "monthsAfterCalculationBase": 4,
            "dayOfMonth": 15
          }}
        }}
        ```

        CALCULATION BASES:
        - Most tax due dates are calculated as "monthsAfterCalculationBase" 
        - If you discover that dates should be calculated from the beginning of the year, use "monthsAfterYearStart" instead

        RULES FOR DETERMINING CALCULATIONS:
        - Use standard tax calculation practices - typically X months after the end of the tax year
        - If a form uses a different calculation approach, implement it according to official guidance
        - Always include the day of the month when the form is due
        - For forms with unusual timing requirements, ensure the calculation method accurately reflects official deadlines

        Provide ONLY the JSON result with no additional explanation. The JSON must be valid, properly formatted, and contain accurate tax filing information based on thorough research.
        """
    
    def _parse_response(self, response_text: str) -> Optional[Dict[str, Any]]:
        """Parse the response from Claude to extract the JSON data."""
        try:
            # Extract JSON from the response
            json_text = ""
            
            # Look for JSON block
            if "```json" in response_text:
                # Extract text between ```json and ```
                start_marker = "```json"
                end_marker = "```"
                start_index = response_text.find(start_marker) + len(start_marker)
                end_index = response_text.find(end_marker, start_index)
                if end_index > start_index:
                    json_text = response_text[start_index:end_index].strip()
            elif "```" in response_text:
                # Try generic code block
                start_marker = "```"
                end_marker = "```"
                start_index = response_text.find(start_marker) + len(start_marker)
                end_index = response_text.find(end_marker, start_index)
                if end_index > start_index:
                    json_text = response_text[start_index:end_index].strip()
            else:
                # Try to find JSON object directly
                start_index = response_text.find("{")
                end_index = response_text.rfind("}") + 1
                if start_index >= 0 and end_index > start_index:
                    json_text = response_text[start_index:end_index].strip()
            
            if json_text:
                return json.loads(json_text)
            return None
            
        except json.JSONDecodeError as e:
            print(f"Error parsing Claude response: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error processing Claude response: {e}")
            return None