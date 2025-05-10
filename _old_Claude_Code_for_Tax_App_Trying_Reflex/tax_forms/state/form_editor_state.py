# tax_forms/state/form_editor_state.py
import reflex as rx
import json
from typing import List, Dict, Any, Optional
from tax_forms.services.forms_repository import FormsRepository
from tax_forms.services.claude_service import ClaudeService

class DueDateInfo(rx.Base):
    months_after_year_end: int = 0
    day_of_month: int = 15
    fiscal_year_exceptions: Dict[str, Any] = {}

class CalculationRule(rx.Base):
    effective_years: List[int] = []
    due_date: DueDateInfo = DueDateInfo()
    extension_due_date: DueDateInfo = DueDateInfo()

class FormDataFull(rx.Base):
    id: Optional[int] = None
    form_number: str = ""
    form_name: str = ""
    entity_type: str = "individual"
    locality_type: str = "federal"
    locality: str = "United States"
    parent_form_numbers: List[str] = []
    owner: str = "MPM"
    calculation_base: str = "end"
    extension: Dict[str, Any] = {}

class FormEditorState(rx.State):
    """State for editing forms."""
    form_data: FormDataFull = FormDataFull()
    calculation_rules: List[CalculationRule] = []
    ai_loading: bool = False
    ai_results: str = ""
    
    def __init__(self):
        super().__init__()
        self.repository = FormsRepository()
        self.claude_service = ClaudeService()
    
    def on_mount(self):
        """Load form data when the component mounts."""
        form_id = self.router.page.params.get("form_id")
        if form_id:
            self.load_form(int(form_id))
    
    def load_form(self, form_id: int):
        """Load a form by ID."""
        form = self.repository.find_form(form_id)
        if form:
            # Convert from raw form to FormDataFull
            self.form_data = FormDataFull(
                id=form.get('id', form_id),
                form_number=form.get('formNumber', ''),
                form_name=form.get('formName', ''),
                entity_type=form.get('entityType', 'individual'),
                locality_type=form.get('localityType', 'federal'),
                locality=form.get('locality', 'United States'),
                parent_form_numbers=form.get('parentFormNumbers', []),
                owner=form.get('owner', 'MPM'),
                calculation_base=form.get('calculationBase', 'end'),
                extension=form.get('extension', {})
            )
            
            # Load calculation rules
            self.calculation_rules = []
            for rule in form.get('calculationRules', []):
                due_date = rule.get('dueDate', {})
                extension_due_date = rule.get('extensionDueDate', {})
                
                self.calculation_rules.append(
                    CalculationRule(
                        effective_years=rule.get('effectiveYears', []),
                        due_date=DueDateInfo(
                            months_after_year_end=due_date.get('monthsAfterCalculationBase', 0),
                            day_of_month=due_date.get('dayOfMonth', 15),
                            fiscal_year_exceptions=due_date.get('fiscalYearExceptions', {})
                        ),
                        extension_due_date=DueDateInfo(
                            months_after_year_end=extension_due_date.get('monthsAfterCalculationBase', 0),
                            day_of_month=extension_due_date.get('dayOfMonth', 15),
                            fiscal_year_exceptions=extension_due_date.get('fiscalYearExceptions', {})
                        )
                    )
                )
    
    def save_form(self):
        """Save the form."""
        # Convert from FormDataFull to raw form
        form_data = {
            'formNumber': self.form_data.form_number,
            'formName': self.form_data.form_name,
            'entityType': self.form_data.entity_type,
            'localityType': self.form_data.locality_type,
            'locality': self.form_data.locality,
            'parentFormNumbers': self.form_data.parent_form_numbers,
            'owner': self.form_data.owner,
            'calculationBase': self.form_data.calculation_base,
            'extension': self.form_data.extension,
            'calculationRules': self._convert_rules_to_dict()
        }
        
        if self.form_data.id:
            self.repository.update_form(self.form_data.id, form_data)
        else:
            new_form = self.repository.add_form(form_data)
            self.form_data.id = new_form.get('id')
    
    def _convert_rules_to_dict(self) -> List[Dict[str, Any]]:
        """Convert calculation rules to dictionary format."""
        rules = []
        for rule in self.calculation_rules:
            rules.append({
                'effectiveYears': rule.effective_years,
                'dueDate': {
                    'monthsAfterCalculationBase': rule.due_date.months_after_year_end,
                    'dayOfMonth': rule.due_date.day_of_month,
                    'fiscalYearExceptions': rule.due_date.fiscal_year_exceptions
                },
                'extensionDueDate': {
                    'monthsAfterCalculationBase': rule.extension_due_date.months_after_year_end,
                    'dayOfMonth': rule.extension_due_date.day_of_month,
                    'fiscalYearExceptions': rule.extension_due_date.fiscal_year_exceptions
                }
            })
        return rules
    
    def add_empty_rule(self):
        """Add an empty rule."""
        self.calculation_rules.append(CalculationRule())
    
    def delete_rule(self, index: int):
        """Delete a rule."""
        def delete():
            if 0 <= index < len(self.calculation_rules):
                self.calculation_rules.pop(index)
        
        return delete
    
    def save_rules(self):
        """Save all rules."""
        self.save_form()
    
    def generate_ai_rules(self):
        """Generate calculation rules using Claude AI."""
        self.ai_loading = True
        self.ai_results = ""
        
        # Prepare form data for Claude
        form_data = {
            'form_number': self.form_data.form_number,
            'form_name': self.form_data.form_name,
            'entity_type': self.form_data.entity_type,
            'locality_type': self.form_data.locality_type,
            'locality': self.form_data.locality
        }
        
        # Call Claude service
        result = self.claude_service.generate_tax_rules(form_data)
        
        self.ai_loading = False
        if result:
            self.ai_results = json.dumps(result, indent=2)
    
    def apply_ai_rules(self):
        """Apply AI-generated rules."""
        if not self.ai_results:
            return
        
        try:
            rules_data = json.loads(self.ai_results)
            if 'calculationRules' in rules_data:
                # Convert the rules to our format
                self.calculation_rules = []
                for rule in rules_data['calculationRules']:
                    due_date = rule.get('dueDate', {})
                    extension_due_date = rule.get('extensionDueDate', {})
                    
                    self.calculation_rules.append(
                        CalculationRule(
                            effective_years=rule.get('effectiveYears', []),
                            due_date=DueDateInfo(
                                months_after_year_end=due_date.get('monthsAfterCalculationBase', 0),
                                day_of_month=due_date.get('dayOfMonth', 15),
                                fiscal_year_exceptions=due_date.get('fiscalYearExceptions', {})
                            ),
                            extension_due_date=DueDateInfo(
                                months_after_year_end=extension_due_date.get('monthsAfterCalculationBase', 0),
                                day_of_month=extension_due_date.get('dayOfMonth', 15),
                                fiscal_year_exceptions=extension_due_date.get('fiscalYearExceptions', {})
                            )
                        )
                    )
                
                # Save the form with the new rules
                self.save_form()
        except Exception as e:
            print(f"Error applying AI rules: {e}")
    
    # Field setters
    def set_form_number(self, value: str):
        self.form_data.form_number = value
    
    def set_form_name(self, value: str):
        self.form_data.form_name = value
    
    def set_entity_type(self, value: str):
        self.form_data.entity_type = value
    
    def set_locality_type(self, value: str):
        self.form_data.locality_type = value
    
    def set_locality(self, value: str):
        self.form_data.locality = value
    
    def set_parent_form_numbers(self, value: str):
        self.form_data.parent_form_numbers = [v.strip() for v in value.split(',') if v.strip()]
    
    def set_owner(self, value: str):
        self.form_data.owner = value
    
    # Rule update methods
    def update_rule_years(self, index: int, years_str: str):
        if 0 <= index < len(self.calculation_rules):
            try:
                years = [int(y.strip()) for y in years_str.split(',') if y.strip()]
                self.calculation_rules[index].effective_years = years
            except ValueError:
                pass
    
    def update_rule_due_date_months(self, index: int, months: int):
        if 0 <= index < len(self.calculation_rules):
            self.calculation_rules[index].due_date.months_after_year_end = months
    
    def update_rule_due_date_day(self, index: int, day: int):
        if 0 <= index < len(self.calculation_rules):
            self.calculation_rules[index].due_date.day_of_month = day
    
    def update_rule_extension_months(self, index: int, months: int):
        if 0 <= index < len(self.calculation_rules):
            self.calculation_rules[index].extension_due_date.months_after_year_end = months
    
    def update_rule_extension_day(self, index: int, day: int):
        if 0 <= index < len(self.calculation_rules):
            self.calculation_rules[index].extension_due_date.day_of_month = day