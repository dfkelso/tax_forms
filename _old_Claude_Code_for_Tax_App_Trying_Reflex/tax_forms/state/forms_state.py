# tax_forms/state/forms_state.py
import reflex as rx
from typing import List, Dict, Any, Optional
from tax_forms.services.forms_repository import FormsRepository

class FormData(rx.Base):
    id: int
    form_number: str
    form_name: str
    entity_type: str
    locality_type: str
    locality: str

class FormsState(rx.State):
    """State for managing forms."""
    forms: List[FormData] = []
    search_text: str = ""
    entity_filter: str = "All"
    
    def __init__(self):
        super().__init__()
        self.repository = FormsRepository()
    
    def on_mount(self):
        """Load forms when the component mounts."""
        self.load_forms()
    
    def load_forms(self):
        """Load forms from the repository."""
        forms_data = self.repository.get_all_forms()
        self.forms = [
            FormData(
                id=form.get('id', i+1),
                form_number=form.get('formNumber', ''),
                form_name=form.get('formName', ''),
                entity_type=form.get('entityType', ''),
                locality_type=form.get('localityType', ''),
                locality=form.get('locality', '')
            )
            for i, form in enumerate(forms_data)
        ]
    
    def filter_forms(self):
        """Filter forms based on search text and entity filter."""
        self.load_forms()
        filtered_forms = self.forms
        
        # Apply entity filter
        if self.entity_filter != "All":
            filtered_forms = [
                form for form in filtered_forms 
                if form.entity_type.lower() == self.entity_filter.lower()
            ]
        
        # Apply search filter
        if self.search_text:
            search_lower = self.search_text.lower()
            filtered_forms = [
                form for form in filtered_forms 
                if (search_lower in form.form_number.lower() or
                    search_lower in form.form_name.lower() or
                    search_lower in form.locality.lower())
            ]
        
        self.forms = filtered_forms
    
    def delete_form(self, form_id: int):
        """Delete a form."""
        def delete():
            success = self.repository.delete_form(form_id)
            if success:
                self.load_forms()
        
        return delete