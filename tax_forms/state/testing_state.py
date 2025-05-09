# tax_forms/state/testing_state.py
import reflex as rx
from datetime import date, datetime
from typing import List, Dict, Any, Optional
from tax_forms.services.forms_repository import FormsRepository
from tax_forms.services.due_date_calculator import DueDateCalculator

class TestingState(rx.State):
    """State for testing due dates."""
    entity_type: str = "individual"
    start_date: str = datetime.now().strftime("%Y-01-01")
    end_date: str = datetime.now().strftime("%Y-12-31")
    job_created: bool = False
    forms_added: bool = False
    job_id: Optional[int] = None
    available_forms: List[Dict[str, Any]] = []
    due_dates: List[Dict[str, Any]] = []
    
    def create_job(self):
        """Create a test job for due date calculations."""
        # Reset any previous data
        self.job_created = True
        self.forms_added = False
        self.job_id = 1  # Simple job ID for testing
        self.due_dates = []
        
        # Load forms that match the entity type
        forms_repo = FormsRepository()
        forms = forms_repo.get_all_forms()
        
        # Filter forms by entity type
        self.available_forms = [
            form for form in forms 
            if form.get("entityType") == self.entity_type
        ]
    
    def add_form_to_job(self, form_id: int):
        """Add a form to the job and calculate its due dates."""
        def add_form():
            # Find the form by ID
            forms_repo = FormsRepository()
            form = forms_repo.find_form(form_id)
            
            if not form:
                return
            
            # Parse dates
            try:
                start_date = date.fromisoformat(self.start_date)
                end_date = date.fromisoformat(self.end_date)
            except ValueError:
                return
            
            # Calculate due dates
            calculator = DueDateCalculator()
            dates = calculator.calculate_dates(
                form_number=form.get("formNumber"),
                entity_type=form.get("entityType"),
                locality_type=form.get("localityType"),
                locality=form.get("locality"),
                coverage_start_date=start_date,
                coverage_end_date=end_date
            )
            
            # If calculation successful, add to due dates
            if dates:
                self.forms_added = True
                
                due_date_str = dates.get("due_date").strftime("%Y-%m-%d") if dates.get("due_date") else "N/A"
                ext_date_str = dates.get("extension_due_date").strftime("%Y-%m-%d") if dates.get("extension_due_date") else "N/A"
                
                self.due_dates.append({
                    "id": len(self.due_dates) + 1,
                    "formNumber": form.get("formNumber"),
                    "formName": form.get("formName"),
                    "due_date": due_date_str,
                    "extension_due_date": ext_date_str,
                    "approximated": dates.get("approximated", False)
                })
        
        return add_form