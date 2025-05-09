# tax_forms/services/forms_repository.py
import json
import os
from typing import List, Dict, Any, Optional
from pathlib import Path

class FormsRepository:
    """Repository for managing tax forms data."""
    
    def __init__(self, json_path: Optional[str] = None):
        """Initialize the repository with a path to the JSON file."""
        self.json_path = json_path or os.path.join(os.getcwd(), "assets", "forms.json")
        self.data = self._load_json()
    
    def _load_json(self) -> Dict[str, Any]:
        """Load JSON data from file."""
        try:
            path = Path(self.json_path)
            if path.exists():
                with open(path, 'r') as f:
                    return json.load(f)
            else:
                print(f"Warning: JSON file not found at {self.json_path}")
                return {"forms": []}
        except Exception as e:
            print(f"Error loading JSON: {e}")
            return {"forms": []}
    
    def _save_json(self) -> bool:
        """Save JSON data to file."""
        try:
            # Create directories if they don't exist
            os.makedirs(os.path.dirname(self.json_path), exist_ok=True)
            
            with open(self.json_path, 'w') as f:
                json.dump(self.data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving JSON: {e}")
            return False
    
    def get_all_forms(self) -> List[Dict[str, Any]]:
        """Get all forms."""
        forms = self.data.get('forms', [])
        # Add an ID for each form (position in array + 1)
        for i, form in enumerate(forms):
            form['id'] = i + 1
        return forms
    
    def find_form(self, form_id: int) -> Optional[Dict[str, Any]]:
        """Find a form by ID."""
        forms = self.data.get('forms', [])
        index = form_id - 1
        if 0 <= index < len(forms):
            form = forms[index].copy()
            form['id'] = form_id
            return form
        return None
    
    def find_form_by_attributes(
        self, 
        form_number: str, 
        entity_type: str, 
        locality_type: str, 
        locality: str
    ) -> Optional[Dict[str, Any]]:
        """Find a form by its attributes."""
        for i, form in enumerate(self.data.get('forms', [])):
            if (form.get('formNumber') == form_number and
                form.get('entityType') == entity_type and
                form.get('localityType') == locality_type and
                form.get('locality') == locality):
                form_copy = form.copy()
                form_copy['id'] = i + 1
                return form_copy
        return None
    
    def add_form(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new form."""
        # Convert from our form format to the JSON schema format
        json_form = {
            'formNumber': form_data.get('formNumber', ''),
            'formName': form_data.get('formName', ''),
            'entityType': form_data.get('entityType', 'individual'),
            'localityType': form_data.get('localityType', 'federal'),
            'locality': form_data.get('locality', 'United States'),
            'parentFormNumbers': form_data.get('parentFormNumbers', []),
            'owner': form_data.get('owner', 'MPM'),
            'calculationBase': form_data.get('calculationBase', 'end'),
            'extension': form_data.get('extension', {}),
            'calculationRules': form_data.get('calculationRules', [])
        }
        
        forms = self.data.get('forms', [])
        forms.append(json_form)
        self._save_json()
        
        # Return the new form with an ID
        json_form['id'] = len(forms)
        return json_form
    
    def update_form(self, form_id: int, form_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update an existing form."""
        forms = self.data.get('forms', [])
        index = form_id - 1
        
        if 0 <= index < len(forms):
            # Convert from our form format to the JSON schema format
            json_form = {
                'formNumber': form_data.get('formNumber', ''),
                'formName': form_data.get('formName', ''),
                'entityType': form_data.get('entityType', 'individual'),
                'localityType': form_data.get('localityType', 'federal'),
                'locality': form_data.get('locality', 'United States'),
                'parentFormNumbers': form_data.get('parentFormNumbers', []),
                'owner': form_data.get('owner', 'MPM'),
                'calculationBase': form_data.get('calculationBase', 'end'),
                'extension': form_data.get('extension', {}),
                'calculationRules': form_data.get('calculationRules', [])
            }
            
            forms[index] = json_form
            self._save_json()
            
            # Return the updated form with an ID
            json_form['id'] = form_id
            return json_form
        
        return None
    
    def delete_form(self, form_id: int) -> bool:
        """Delete a form."""
        forms = self.data.get('forms', [])
        index = form_id - 1
        
        if 0 <= index < len(forms):
            forms.pop(index)
            return self._save_json()
        
        return False