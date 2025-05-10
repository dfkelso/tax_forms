# tax_forms/backend/table_state.py
import json
import os
from datetime import date, datetime
from pathlib import Path
from typing import List, Optional

import reflex as rx


class TaxForm(rx.Base):
    """The tax form class."""
    id: int
    form_number: str
    form_name: str
    entity_type: str
    locality_type: str
    locality: str
    due_date: Optional[str] = None
    extension_due_date: Optional[str] = None
    approximated: bool = False


class TableState(rx.State):
    """The state class."""
    items: List[TaxForm] = []
    search_value: str = ""
    entity_filter: str = "All"
    sort_value: str = ""
    sort_reverse: bool = False
    total_items: int = 0
    offset: int = 0
    limit: int = 25  # Increased to match Rails app
    preview_year: int = datetime.now().year
    show_delete_modal: bool = False
    form_to_delete: Optional[int] = None

    @rx.var(cache=True)
    def filtered_sorted_items(self) -> List[TaxForm]:
        items = self.items

        # Filter by entity type
        if self.entity_filter != "All":
            items = [item for item in items if item.entity_type.lower() == self.entity_filter.lower()]

        # Filter by search value
        if self.search_value:
            search_value = self.search_value.lower()
            items = [
                item
                for item in items
                if any(
                    search_value in str(getattr(item, attr)).lower()
                    for attr in ["form_number", "form_name", "entity_type", "locality_type", "locality"]
                )
            ]

        # Sort items
        if self.sort_value:
            items = sorted(
                items,
                key=lambda item: str(getattr(item, self.sort_value)).lower(),
                reverse=self.sort_reverse,
            )

        return items

    @rx.var(cache=True)
    def page_number(self) -> int:
        return (self.offset // self.limit) + 1

    @rx.var(cache=True)
    def total_pages(self) -> int:
        filtered_count = len(self.filtered_sorted_items)
        return (filtered_count // self.limit) + (1 if filtered_count % self.limit else 0)

    @rx.var(cache=True, initial_value=[])
    def get_current_page(self) -> list[TaxForm]:
        start_index = self.offset
        end_index = start_index + self.limit
        return self.filtered_sorted_items[start_index:end_index]

    def prev_page(self):
        if self.page_number > 1:
            self.offset -= self.limit

    def next_page(self):
        if self.page_number < self.total_pages:
            self.offset += self.limit

    def first_page(self):
        self.offset = 0

    def last_page(self):
        self.offset = (self.total_pages - 1) * self.limit

    def set_preview_year(self, value: str):
        try:
            self.preview_year = int(value)
            self.load_entries()  # Reload with new dates
        except ValueError:
            pass

    def show_delete_confirmation(self, form_id: int):
        self.form_to_delete = form_id
        self.show_delete_modal = True

    def hide_delete_modal(self):
        self.show_delete_modal = False
        self.form_to_delete = None

    def confirm_delete(self):
        if self.form_to_delete:
            # In Rails app, this would delete from JSON
            # For now, just remove from display
            self.items = [item for item in self.items if item.id != self.form_to_delete]
            self.total_items = len(self.items)
        self.hide_delete_modal()

    def load_entries(self):
        """Load entries from forms.json with due date calculations."""
        json_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "forms.json")
        
        try:
            with open(json_path, 'r') as f:
                data = json.load(f)
                forms_data = data.get('forms', [])
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading forms.json: {e}")
            forms_data = []
        
        # Convert to TaxForm objects with due date calculations
        self.items = []
        for i, form in enumerate(forms_data):
            # Calculate due dates if preview_year is set
            due_date = None
            extension_due_date = None
            approximated = False
            
            if self.preview_year:
                dates = self._calculate_dates(form)
                if dates:
                    due_date = dates.get('due_date')
                    extension_due_date = dates.get('extension_due_date')
                    approximated = dates.get('approximated', False)
            
            self.items.append(
                TaxForm(
                    id=i + 1,
                    form_number=form.get("formNumber", ""),
                    form_name=form.get("formName", ""),
                    entity_type=form.get("entityType", ""),
                    locality_type=form.get("localityType", ""),
                    locality=form.get("locality", ""),
                    due_date=due_date,
                    extension_due_date=extension_due_date,
                    approximated=approximated
                )
            )
        
        self.total_items = len(self.items)

    def _calculate_dates(self, form):
        """Simplified due date calculation."""
        rules = form.get('calculationRules', [])
        if not rules:
            return None
        
        # Find rule for preview year or closest
        applicable_rule = None
        for rule in rules:
            if self.preview_year in rule.get('effectiveYears', []):
                applicable_rule = rule
                break
        
        # If no exact match, use first rule as approximation
        if not applicable_rule and rules:
            applicable_rule = rules[0]
            approximated = True
        else:
            approximated = False
        
        if not applicable_rule:
            return None
        
        # Calculate dates
        base_date = date(self.preview_year, 12, 31)  # Year end
        
        due_date_info = applicable_rule.get('dueDate', {})
        months_after = due_date_info.get('monthsAfterCalculationBase', 0)
        day_of_month = due_date_info.get('dayOfMonth', 15)
        
        # Simple calculation - add months
        month = base_date.month + months_after
        year = base_date.year + (month - 1) // 12
        month = ((month - 1) % 12) + 1
        
        try:
            due_date = date(year, month, day_of_month).strftime('%m/%d/%Y')
        except ValueError:
            due_date = None
        
        # Extension date
        ext_info = applicable_rule.get('extensionDueDate', {})
        if ext_info:
            ext_months = ext_info.get('monthsAfterCalculationBase', 0)
            ext_day = ext_info.get('dayOfMonth', 15)
            
            ext_month = base_date.month + ext_months
            ext_year = base_date.year + (ext_month - 1) // 12
            ext_month = ((ext_month - 1) % 12) + 1
            
            try:
                extension_due_date = date(ext_year, ext_month, ext_day).strftime('%m/%d/%Y')
            except ValueError:
                extension_due_date = None
        else:
            extension_due_date = None
        
        return {
            'due_date': due_date,
            'extension_due_date': extension_due_date,
            'approximated': approximated
        }

    def toggle_sort(self):
        self.sort_reverse = not self.sort_reverse