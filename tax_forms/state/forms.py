import reflex as rx
from typing import List, Dict, Any, Optional

class FormsState(rx.State):
    """State for the forms list page."""
    forms: List[Dict[str, Any]] = []
    search_text: str = ""
    entity_filter: str = "All"  # Default to "All" instead of empty string
    
    def init(self):
        """Initialize the state."""
        self.load_forms()
    
    def load_forms(self):
        """Load forms from the repository."""
        # This is a placeholder - will be replaced with actual DB queries
        self.forms = [
            {"id": 1, "form_number": "1040", "form_name": "U.S. Individual Income Tax Return", "entity_type": "individual", "locality_type": "federal", "locality": "United States"},
            {"id": 2, "form_number": "1120", "form_name": "U.S. Corporation Income Tax Return", "entity_type": "corporation", "locality_type": "federal", "locality": "United States"},
        ]
    
    def filter_forms(self):
        """Filter forms based on search text and entity filter."""
        # This is a placeholder - will be replaced with actual filtering logic
        self.load_forms()
        
        # Apply entity filter (skip if "All" is selected)
        if self.entity_filter and self.entity_filter != "All":
            self.forms = [form for form in self.forms if form.get("entity_type") == self.entity_filter]
        
        # Apply search filter
        if self.search_text:
            search_lower = self.search_text.lower()
            self.forms = [
                form for form in self.forms 
                if search_lower in form.get("form_number", "").lower() 
                or search_lower in form.get("form_name", "").lower()
                or search_lower in form.get("locality", "").lower()
            ]