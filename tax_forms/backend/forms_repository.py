# tax_forms/backend/forms_repository.py
import json
import os
from typing import List, Dict, Any, Optional
from pathlib import Path

class FormsRepository:
    """Repository for managing tax forms data."""
    
    def __init__(self, json_path: Optional[str] = None):
        """Initialize the repository with a path to the JSON file."""
        self.json_path = json_path or os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "forms.json")
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
    
    def get_all_forms(self) -> List[Dict[str, Any]]:
        """Get all forms."""
        forms = self.data.get('forms', [])
        # Add an ID for each form (position in array + 1)
        for i, form in enumerate(forms):
            form['id'] = i + 1
        return forms