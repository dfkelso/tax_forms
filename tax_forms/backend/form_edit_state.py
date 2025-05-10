# tax_forms/backend/form_edit_state.py
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

import reflex as rx


class FormEditState(rx.State):
    """State for form editing."""
    
    # Modal visibility
    show_edit_modal: bool = False
    
    # Form data
    edit_form_id: int = -1
    form_number: str = ""
    form_name: str = ""
    entity_type: str = "individual"
    locality_type: str = "federal"
    locality: str = ""
    is_parent_form: bool = False
    parent_form_number: str = ""
    owner: str = "MPM"
    calculation_base: str = "end"
    
    # Extension data
    extension_form_number: str = ""
    extension_form_name: str = ""
    piggyback_fed: bool = False
    
    # Calculation rules
    calculation_rules: List[Dict[str, Any]] = []
    
    # Available options
    entity_types: List[str] = ["individual", "corporation", "partnership", "scorp", "smllc"]
    locality_types: List[str] = ["federal", "state", "city"]
    parent_forms: List[str] = []
    
    # Error messages
    error_message: str = ""
    
    def open_edit_modal(self, form_id: int):
        """Open the edit modal with form data."""
        # Load forms from JSON
        json_path = Path("assets/forms.json")
        if json_path.exists():
            with open(json_path, 'r') as f:
                data = json.load(f)
                forms = data.get("forms", [])
                
                if 0 <= form_id - 1 < len(forms):
                    form = forms[form_id - 1]
                    
                    # Load form data
                    self.edit_form_id = form_id
                    self.form_number = form.get("formNumber", "")
                    self.form_name = form.get("formName", "")
                    self.entity_type = form.get("entityType", "individual")
                    self.locality_type = form.get("localityType", "federal")
                    self.locality = form.get("locality", "")
                    self.owner = form.get("owner", "MPM")
                    self.calculation_base = form.get("calculationBase", "end")
                    
                    # Check if parent form
                    parent_form_numbers = form.get("parentFormNumbers", [])
                    self.is_parent_form = self.form_number in parent_form_numbers
                    if not self.is_parent_form and parent_form_numbers:
                        self.parent_form_number = parent_form_numbers[0]
                    else:
                        self.parent_form_number = ""
                    
                    # Load extension data
                    extension = form.get("extension", {})
                    self.extension_form_number = extension.get("formNumber", "")
                    self.extension_form_name = extension.get("formName", "")
                    self.piggyback_fed = extension.get("piggybackFed", False)
                    
                    # Load calculation rules
                    self.calculation_rules = form.get("calculationRules", [])
                    
                    # Get available parent forms
                    self.parent_forms = [
                        f.get("formNumber", "") 
                        for f in forms 
                        if f.get("formNumber") != self.form_number
                    ]
                    
                    self.show_edit_modal = True
                    self.error_message = ""
    
    def close_modal(self):
        """Close the modal without saving."""
        self.show_edit_modal = False
        self.error_message = ""
    
    def save_form(self):
        """Save the form data."""
        # Validate required fields
        if not self.form_number or not self.form_name:
            self.error_message = "Form number and name are required."
            return
        
        # Load current data
        json_path = Path("assets/forms.json")
        if not json_path.exists():
            self.error_message = "Forms data file not found."
            return
        
        with open(json_path, 'r') as f:
            data = json.load(f)
            forms = data.get("forms", [])
        
        if 0 <= self.edit_form_id - 1 < len(forms):
            # Update form data
            form = {
                "formNumber": self.form_number,
                "formName": self.form_name,
                "entityType": self.entity_type,
                "localityType": self.locality_type,
                "locality": self.locality,
                "parentFormNumbers": [self.form_number] if self.is_parent_form else ([self.parent_form_number] if self.parent_form_number else []),
                "owner": self.owner,
                "calculationBase": self.calculation_base,
                "calculationRules": self.calculation_rules
            }
            
            # Add extension if provided
            if self.extension_form_number:
                form["extension"] = {
                    "formNumber": self.extension_form_number,
                    "formName": self.extension_form_name,
                    "piggybackFed": self.piggyback_fed
                }
            
            # Update form in array
            forms[self.edit_form_id - 1] = form
            
            # For this demo, we'll just update in memory
            # In a real app, you would save to the JSON file
            # with open(json_path, 'w') as f:
            #     json.dump(data, f, indent=2)
            
            # Close modal and refresh table
            self.show_edit_modal = False
            
            # Trigger table reload by updating the parent state
            yield rx.call_script("window.location.reload()")
    
    # Rule management methods
    def add_calculation_rule(self):
        """Add a new empty calculation rule."""
        new_rule = {
            "effectiveYears": [],
            "dueDate": {
                "monthsAfterCalculationBase": 0,
                "dayOfMonth": 15
            },
            "extensionDueDate": {
                "monthsAfterCalculationBase": 0,
                "dayOfMonth": 15
            }
        }
        self.calculation_rules.append(new_rule)
    
    def delete_rule(self, index: int):
        """Delete a calculation rule."""
        if 0 <= index < len(self.calculation_rules):
            self.calculation_rules.pop(index)
    
    def update_rule_years(self, index: int, years_str: str):
        """Update effective years for a rule."""
        if 0 <= index < len(self.calculation_rules):
            try:
                years = [int(y.strip()) for y in years_str.split(",") if y.strip()]
                self.calculation_rules[index]["effectiveYears"] = years
            except ValueError:
    # Getter methods for calculation rules (needed for Reflex vars)
    def get_effective_years_string(self, index: int) -> str:
        """Get effective years as comma-separated string."""
        if 0 <= index < len(self.calculation_rules):
            years = self.calculation_rules[index].get("effectiveYears", [])
            return ",".join(map(str, years))
        return ""
    
    def get_due_months(self, index: int) -> str:
        """Get due date months."""
        if 0 <= index < len(self.calculation_rules):
            return str(self.calculation_rules[index].get("dueDate", {}).get("monthsAfterCalculationBase", 0))
        return "0"
    
    def get_due_day(self, index: int) -> str:
        """Get due date day."""
        if 0 <= index < len(self.calculation_rules):
            return str(self.calculation_rules[index].get("dueDate", {}).get("dayOfMonth", 15))
        return "15"
    
    def get_extension_months(self, index: int) -> str:
        """Get extension due date months."""
        if 0 <= index < len(self.calculation_rules):
            return str(self.calculation_rules[index].get("extensionDueDate", {}).get("monthsAfterCalculationBase", 0))
        return "0"
    
    def get_extension_day(self, index: int) -> str:
        """Get extension due date day."""
        if 0 <= index < len(self.calculation_rules):
            return str(self.calculation_rules[index].get("extensionDueDate", {}).get("dayOfMonth", 15))
        return "15"
    
    def update_due_months(self, index: int, months: str):
        """Update due date months for a rule."""
        if 0 <= index < len(self.calculation_rules):
            try:
                self.calculation_rules[index]["dueDate"]["monthsAfterCalculationBase"] = int(months)
            except ValueError:
                pass
    
    def update_due_day(self, index: int, day: str):
        """Update due date day for a rule."""
        if 0 <= index < len(self.calculation_rules):
            try:
                self.calculation_rules[index]["dueDate"]["dayOfMonth"] = int(day)
            except ValueError:
                pass
    
    def update_extension_months(self, index: int, months: str):
        """Update extension due date months for a rule."""
        if 0 <= index < len(self.calculation_rules):
            try:
                self.calculation_rules[index]["extensionDueDate"]["monthsAfterCalculationBase"] = int(months)
            except ValueError:
                pass
    
    def update_extension_day(self, index: int, day: str):
        """Update extension due date day for a rule."""
        if 0 <= index < len(self.calculation_rules):
            try:
                self.calculation_rules[index]["extensionDueDate"]["dayOfMonth"] = int(day)
            except ValueError:
                pass