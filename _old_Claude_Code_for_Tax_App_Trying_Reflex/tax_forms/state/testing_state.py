# tax_forms/state/testing_state.py
import reflex as rx
from datetime import date, datetime
from typing import List, Dict, Any, Optional
from tax_forms.services.forms_repository import FormsRepository
from tax_forms.services.due_date_calculator import DueDateCalculator

class FormInfo(rx.Base):
    """Basic form information."""
    id: int
    form_number: str
    form_name: str
    entity_type: str
    locality_type: str
    locality: str

class DueDateInfo(rx.Base):
    """Due date information for a form."""
    form_number: str
    form_name: str
    due_date: str
    extension_due_date: Optional[str] = None

class TestingState(rx.State):
    """State for testing due dates."""
    entity_type: str = "individual"
    start_date: str = datetime.now().strftime("%Y-01-01")
    end_date: str = datetime.now().strftime("%Y-12-31")
    job_created: bool = False
    forms_added: bool = False
    job_id: Optional[int] = None
    available_forms: List[FormInfo] = []
    due_dates: List[DueDateInfo] = []
    
    def __init__(self):
        super().__init__()
        self.repository = FormsRepository()
        self.calculator = DueDateCalculator(self.repository)
    
    def create_job(self):
        """Create a test job."""
        self.job_created = True
        self.job_id = 1  # Simulated job ID
        
        # Load available forms for the selected entity type
        forms_data = self.repository.get_all_forms()
        
        # Convert forms to FormInfo objects and filter by entity type
        self.available_forms = []
        for form in forms_data:
            if form.get("entityType") == self.entity_type:
                self.available_forms.append(
                    FormInfo(
                        id=form.get("id", 1),
                        form_number=form.get("formNumber", ""),
                        form_name=form.get("formName", ""),
                        entity_type=form.get("entityType", ""),
                        locality_type=form.get("localityType", ""),
                        locality=form.get("locality", "")
                    )
                )
    
    def add_form_to_job(self, form_id: int):
        """Add a form to the test job and calculate due dates."""
        def add_form():
            # Find the form in available forms
            form = next((f for f in self.available_forms if f.id == form_id), None)
            if not form:
                return
            
            # Parse dates
            try:
                start_date = datetime.strptime(self.start_date, "%Y-%m-%d").date()
                end_date = datetime.strptime(self.end_date, "%Y-%m-%d").date()
            except ValueError:
                # Use current year if dates are invalid
                current_year = datetime.now().year
                start_date = date(current_year, 1, 1)
                end_date = date(current_year, 12, 31)
            
            # Calculate due dates using the calculator
            dates = self.calculator.calculate_dates(
                form.form_number,
                form.entity_type,
                form.locality_type,
                form.locality,
                start_date,
                end_date
            )
            
            if dates:
                due_date_str = dates.get("due_date", "").strftime("%Y-%m-%d") if dates.get("due_date") else "N/A"
                ext_date_str = dates.get("extension_due_date", "").strftime("%Y-%m-%d") if dates.get("extension_due_date") else "N/A"
                
                # Check if this form is already in the results
                existing = next((d for d in self.due_dates if d.form_number == form.form_number), None)
                
                if existing:
                    # Update existing entry
                    existing.due_date = due_date_str
                    existing.extension_due_date = ext_date_str
                else:
                    # Add new entry
                    self.due_dates.append(
                        DueDateInfo(
                            form_number=form.form_number,
                            form_name=form.form_name,
                            due_date=due_date_str,
                            extension_due_date=ext_date_str
                        )
                    )
                
                self.forms_added = True
        
        return add_form
    
    def clear_results(self):
        """Clear all results."""
        self.forms_added = False
        self.due_dates = []
    
    # Setters
    def set_entity_type(self, value: str):
        self.entity_type = value
        # Reset job when entity type changes
        self.job_created = False
        self.forms_added = False
        self.due_dates = []
    
    def set_start_date(self, value: str):
        self.start_date = value
    
    def set_end_date(self, value: str):
        self.end_date = value