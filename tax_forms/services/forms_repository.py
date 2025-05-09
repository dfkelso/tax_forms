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
                return {"forms": []}
        except Exception as e:
            print(f"Error loading JSON: {e}")
            return {"forms": []}
    
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
    
    def add_form(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new form."""
        forms = self.data.get('forms', [])
        forms.append(form_data)
        self._save_json()
        form_data['id'] = len(forms)
        return form_data
    
    def update_form(self, form_id: int, form_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update an existing form."""
        forms = self.data.get('forms', [])
        index = form_id - 1
        if 0 <= index < len(forms):
            forms[index] = form_data
            self._save_json()
            form_data['id'] = form_id
            return form_data
        return None
    
    def delete_form(self, form_id: int) -> bool:
        """Delete a form."""
        forms = self.data.get('forms', [])
        index = form_id - 1
        if 0 <= index < len(forms):
            forms.pop(index)
            self._save_json()
            return True
        return False
    
    def _save_json(self) -> None:
        """Save JSON data to file."""
        try:
            with open(self.json_path, 'w') as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            print(f"Error saving JSON: {e}")