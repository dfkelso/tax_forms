import reflex as rx
from datetime import date, datetime
from typing import List, Dict, Any, Optional

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
        """Create a test job."""
        # In a real implementation, this would create a job in the database
        # For now, we'll just set job_created to True and populate available_forms
        self.job_created = True
        self.job_id = 1  # Simulated job ID
        
        # Load available forms for the selected entity type
        self.available_forms = [
            {"id": 1, "form_number": "1040", "form_name": "U.S. Individual Income Tax Return", "entity_type": "individual", "locality_type": "federal", "locality": "United States"},
            {"id": 2, "form_number": "1120", "form_name": "U.S. Corporation Income Tax Return", "entity_type": "corporation", "locality_type": "federal", "locality": "United States"},
        ]
        
        # Filter forms by entity type
        self.available_forms = [form for form in self.available_forms if form["entity_type"] == self.entity_type]
    
    def add_form_to_job(self, form_id: int):
        """Add a form to the test job."""
        # In a real implementation, this would add the form to the job in the database
        # For now, we'll just set forms_added to True and populate due_dates
        self.forms_added = True
        
        # Find the form in available_forms
        form = next((f for f in self.available_forms if f["id"] == form_id), None)
        if not form:
            return
        
        # Calculate due dates
        # In a real implementation, this would use the DueDateCalculator
        self.due_dates.append({
            "form_number": form["form_number"],
            "form_name": form["form_name"],
            "due_date": "2025-04-15",
            "extension_due_date": "2025-10-15"
        })