# tax_forms/state/form_editor_state.py
import reflex as rx
from typing import Dict, Any, List, Optional
from tax_forms.services.forms_repository import FormsRepository
from tax_forms.services.claude_service import ClaudeService

class FormEditorState(rx.State):
    """State for the form editor."""
    form_id: Optional[int] = None
    form_data: Dict[str, Any] = {}
    
    # Form fields
    form_number: str = ""
    form_name: str = ""
    entity_type: str = "individual"
    locality_type: str = "federal"
    locality: str = ""
    is_parent: bool = False
    parent_form_number: str = ""
    owner: str = "MPM"
    calculation_base: str = "end"
    
    # Extension fields
    extension_form_number: str = ""
    extension_form_name: str = ""
    piggyback_fed: bool = False
    
    # Rules
    calculation_rules: List[Dict[str, Any]] = []
    
    def on_mount(self):
        """Load form data if editing an existing form."""
        if self.form_id:
            self.load_form()
    
    def load_form(self):
        """Load form data when editing."""
        repo = FormsRepository()
        form = repo.find_form(self.form_id)
        
        if form:
            self.form_data = form
            
            # Populate form fields
            self.form_number = form.get("formNumber", "")
            self.form_name = form.get("formName", "")
            self.entity_type = form.get("entityType", "individual")
            self.locality_type = form.get("localityType", "federal")
            self.locality = form.get("locality", "")
            
            # Determine if is parent
            parent_forms = form.get("parentFormNumbers", [])
            self.is_parent = len(parent_forms) > 0 and parent_forms[0] == self.form_number
            if not self.is_parent and len(parent_forms) > 0:
                self.parent_form_number = parent_forms[0]
            
            self.owner = form.get("owner", "MPM")
            self.calculation_base = form.get("calculationBase", "end")
            
            # Extension data
            extension = form.get("extension", {})
            self.extension_form_number = extension.get("formNumber", "")
            self.extension_form_name = extension.get("formName", "")
            self.piggyback_fed = extension.get("piggybackFed", False)
            
            # Rules
            self.calculation_rules = form.get("calculationRules", [])
    
    def save_form(self):
        """Save form data."""
        repo = FormsRepository()
        
        # Build form data
        form_data = {
            "formNumber": self.form_number,
            "formName": self.form_name,
            "entityType": self.entity_type,
            "localityType": self.locality_type,
            "locality": self.locality,
            "parentFormNumbers": [self.form_number] if self.is_parent else [self.parent_form_number],
            "owner": self.owner,
            "calculationBase": self.calculation_base,
            "calculationRules": self.calculation_rules
        }
        
        # Add extension if provided
        if self.extension_form_number:
            form_data["extension"] = {
                "formNumber": self.extension_form_number,
                "formName": self.extension_form_name,
                "piggybackFed": self.piggyback_fed
            }
        
        # Save to repository
        if self.form_id:
            repo.update_form(self.form_id, form_data)
        else:
            saved_form = repo.add_form(form_data)
            self.form_id = saved_form.get("id")
        
        return rx.redirect(f"/forms")
    
    def generate_rules_with_ai(self):
        """Generate calculation rules using the AI service."""
        form_data = {
            "form_number": self.form_number,
            "form_name": self.form_name,
            "entity_type": self.entity_type,
            "locality_type": self.locality_type,
            "locality": self.locality
        }
        
        service = ClaudeService()
        result = service.generate_tax_rules(form_data)
        
        if result and "calculationRules" in result:
            self.calculation_rules = result["calculationRules"]
    
    def add_rule(self):
        """Add a new empty calculation rule."""
        new_rule = {
            "effectiveYears": [2023],
            "dueDate": {
                "monthsAfterCalculationBase": 4,
                "dayOfMonth": 15
            },
            "extensionDueDate": {
                "monthsAfterCalculationBase": 10,
                "dayOfMonth": 15
            }
        }
        
        self.calculation_rules.append(new_rule)
    
    def update_rule(self, index: int, rule: Dict[str, Any]):
        """Update a calculation rule."""
        if 0 <= index < len(self.calculation_rules):
            self.calculation_rules[index] = rule
    
    def delete_rule(self, index: int):
        """Delete a calculation rule."""
        if 0 <= index < len(self.calculation_rules):
            self.calculation_rules.pop(index)