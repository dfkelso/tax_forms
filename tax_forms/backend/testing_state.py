# tax_forms/state/testing_state.py
import reflex as rx
from datetime import date, datetime
from typing import List, Optional

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
    
    def create_job(self):
        """Create a test job."""
        self.job_created = True
        self.job_id = 1  # Simulated job ID
        
        # In a real app, this would load forms from a repository
        # For now, we'll add dummy data
        self.available_forms = [
            FormInfo(
                id=1,
                form_number="1040",
                form_name="U.S. Individual Income Tax Return",
                entity_type="individual",
                locality_type="federal",
                locality="United States"
            )
        ]
    
    def add_form_to_job(self, form_id: int):
        """Add a form to the test job and calculate due dates."""
        def add_form():
            form = next((f for f in self.available_forms if f.id == form_id), None)
            if form:
                self.due_dates.append(
                    DueDateInfo(
                        form_number=form.form_number,
                        form_name=form.form_name,
                        due_date="2025-04-15",
                        extension_due_date="2025-10-15"
                    )
                )
                self.forms_added = True
        
        return add_form
    
    def clear_results(self):
        """Clear all results."""
        self.forms_added = False
        self.due_dates = []
    
    def set_entity_type(self, value: str):
        self.entity_type = value
    
    def set_start_date(self, value: str):
        self.start_date = value
    
    def set_end_date(self, value: str):
        self.end_date = value