# tax_forms/state/forms_state.py
import reflex as rx
from typing import List, Dict, Any, Optional
from tax_forms.services.forms_repository import FormsRepository

class FormsState(rx.State):
    """State for the forms list page."""
    forms: List[Dict[str, Any]] = []
    search_text: str = ""
    entity_filter: str = "All"  # Default to "All" instead of empty string
    
    def on_mount(self):
        """Initialize the state when component mounts."""
        self.load_forms()
    
    def load_forms(self):
        """Load forms from the repository."""
        forms_repo = FormsRepository()
        self.forms = forms_repo.get_all_forms()
    
    def filter_forms(self):
        """Filter forms based on search text and entity filter."""
        # Start fresh
        self.load_forms()
        
        # Apply entity filter (skip if "All" is selected)
        if self.entity_filter and self.entity_filter != "All":
            self.forms = [form for form in self.forms if form.get("entityType") == self.entity_filter]
        
        # Apply search filter
        if self.search_text:
            search_lower = self.search_text.lower()
            self.forms = [
                form for form in self.forms 
                if (search_lower in form.get("formNumber", "").lower() or
                    search_lower in form.get("formName", "").lower() or
                    search_lower in form.get("locality", "").lower())
            ]
    
    def delete_form(self, form_id: int):
        """Delete a form and refresh the list."""
        def delete():
            forms_repo = FormsRepository()
            success = forms_repo.delete_form(form_id)
            if success:
                # Reload the forms list
                self.load_forms()
        
        return delete