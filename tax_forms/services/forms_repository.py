# tax_forms/services/forms_repository.py
import json
import os
from typing import List, Dict, Any, Optional
from pathlib import Path

class FormsRepository:
    """Repository for managing tax forms data."""
    
    def __init__(self, json_path: Optional[str] = None):
        """Initialize the repository with a path to the JSON file."""
        self.json_path = json_path or os.path.join(os.path.dirname(__file__), '../../assets/forms.json')
        self.data = self._load_json()
    
    def _load_json(self) -> Dict[str, Any]:
        """Load JSON data from file."""
        try:
            path = Path(self.json_path)
            if path.exists():
                with open(path, 'r') as f:
                    return json.load(f)
            else:
                # If file doesn't exist, return an empty forms object
                return {"forms": []}
        except Exception as e:
            print(f"Error loading JSON: {e}")
            return {"forms": []}
    
    def get_all_forms(self) -> List[Dict[str, Any]]:
        """Get all forms with added ID property."""
        forms = self.data.get('forms', [])
        
        # Add an ID for each form (position in array + 1)
        for i, form in enumerate(forms):
            form_copy = form.copy()
            form_copy['id'] = i + 1
            forms[i] = form_copy
            
        return forms
    
    def find_form(self, form_id: int) -> Optional[Dict[str, Any]]:
        """Find a form by ID."""
        forms = self.data.get('forms', [])
        index = form_id - 1  # Convert ID to array index
        
        if 0 <= index < len(forms):
            form = forms[index].copy()
            form['id'] = form_id
            return form
        return None
    
    def add_form(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new form."""
        # Remove id from form_data if present
        if 'id' in form_data:
            del form_data['id']
            
        forms = self.data.get('forms', [])
        forms.append(form_data)
        
        self._save_json()
        
        # Return the form with the new ID
        form_data_copy = form_data.copy()
        form_data_copy['id'] = len(forms)
        return form_data_copy
    
    def update_form(self, form_id: int, form_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update an existing form."""
        # Remove id from form_data if present
        if 'id' in form_data:
            del form_data['id']
            
        forms = self.data.get('forms', [])
        index = form_id - 1  # Convert ID to array index
        
        if 0 <= index < len(forms):
            forms[index] = form_data
            self._save_json()
            
            # Return the form with the ID
            form_data_copy = form_data.copy()
            form_data_copy['id'] = form_id
            return form_data_copy
        return None
    
    def delete_form(self, form_id: int) -> bool:
        """Delete a form."""
        forms = self.data.get('forms', [])
        index = form_id - 1  # Convert ID to array index
        
        if 0 <= index < len(forms):
            forms.pop(index)
            self._save_json()
            return True
        return False