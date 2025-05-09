# tax_forms/services/due_date_calculator.py
from datetime import date, timedelta
from typing import Dict, Any, Optional
from tax_forms.services.forms_repository import FormsRepository

class DueDateCalculator:
    """Calculator for determining tax form due dates."""
    
    def __init__(self, forms_repository=None):
        """Initialize the calculator with a forms repository."""
        self.forms_repository = forms_repository or FormsRepository()
    
    def calculate_dates(
        self, 
        form_number: str, 
        entity_type: str, 
        locality_type: str, 
        locality: str, 
        coverage_start_date: date, 
        coverage_end_date: date
    ) -> Optional[Dict[str, Any]]:
        """Calculate due dates for a specific form and time period."""
        # Find the form by its attributes
        forms = self.forms_repository.get_all_forms()
        form = None
        
        for f in forms:
            if (f.get("formNumber") == form_number and
                f.get("entityType") == entity_type and
                f.get("localityType") == locality_type and
                f.get("locality") == locality):
                form = f
                break
        
        if not form:
            return None
        
        # Determine base date based on calculation base
        calculation_base = form.get("calculationBase", "end")
        base_date = coverage_end_date if calculation_base == "end" else coverage_start_date
        
        # Find rule for the specific tax year
        tax_year = coverage_end_date.year
        rule = self._find_applicable_rule(form, tax_year)
        
        if not rule:
            return None
        
        # Calculate dates using the rule
        return self._calculate_specific_dates(rule, coverage_start_date, coverage_end_date, base_date)
    
    def _find_applicable_rule(self, form: Dict[str, Any], tax_year: int) -> Optional[Dict[str, Any]]:
        """Find the applicable rule for a specific tax year."""
        calculation_rules = form.get("calculationRules", [])
        if not calculation_rules:
            return None
        
        # Look for exact match first
        for rule in calculation_rules:
            effective_years = rule.get("effectiveYears", [])
            if tax_year in effective_years:
                return rule
        
        # If no exact match, find closest year
        closest_rule = None
        closest_year_diff = float('inf')
        
        for rule in calculation_rules:
            effective_years = rule.get("effectiveYears", [])
            for year in effective_years:
                year_diff = abs(year - tax_year)
                if year_diff < closest_year_diff:
                    closest_year_diff = year_diff
                    closest_rule = rule.copy()
                    closest_rule["approximated"] = True
        
        return closest_rule
    
    def _calculate_specific_dates(
        self, 
        rule: Dict[str, Any], 
        start_date: date, 
        end_date: date, 
        base_date: date = None
    ) -> Dict[str, Any]:
        """Calculate specific dates based on a rule."""
        # Default to end date as base if not specified
        base_date = base_date or end_date
        
        # Get month of base date for fiscal year exception checking
        base_month = f"{base_date.month:02d}"
        
        # Calculate due date
        due_date = None
        if "dueDate" in rule:
            due_date = self._calculate_date(rule["dueDate"], base_date, base_month, end_date.year)
        
        # Calculate extension date
        extension_due_date = None
        if "extensionDueDate" in rule:
            extension_due_date = self._calculate_date(rule["extensionDueDate"], base_date, base_month, end_date.year)
        
        # Prepare result
        result = {
            "due_date": due_date,
            "extension_due_date": extension_due_date
        }
        
        # Include approximated flag if present
        if rule.get("approximated"):
            result["approximated"] = True
            
        return result
    
    def _calculate_date(
        self, 
        date_rule: Dict[str, Any], 
        base_date: date, 
        base_month: str, 
        year: int
    ) -> Optional[date]:
        """Calculate a specific date based on a rule."""
        # Default values
        months_to_add = 0
        day_of_month = date_rule.get("dayOfMonth", 15)
        reference_date = base_date
        
        # Check for fiscal year exceptions first
        fiscal_exceptions = date_rule.get("fiscalYearExceptions", {})
        exception = fiscal_exceptions.get(base_month)
        
        if exception:
            # If there's an exception for this month
            if "monthsAfterCalculationBase" in exception:
                months_to_add = exception["monthsAfterCalculationBase"]
            elif "monthsAfterYearStart" in exception:
                months_to_add = exception["monthsAfterYearStart"]
                reference_date = date(year, 1, 1)
            
            if "dayOfMonth" in exception:
                day_of_month = exception["dayOfMonth"]
        else:
            # Use standard rules
            if "monthsAfterCalculationBase" in date_rule:
                months_to_add = date_rule["monthsAfterCalculationBase"]
            elif "monthsAfterYearStart" in date_rule:
                months_to_add = date_rule["monthsAfterYearStart"]
                reference_date = date(year, 1, 1)
        
        # Calculate the result date
        return self._calculate_result_date(reference_date, months_to_add, day_of_month)
    
    def _calculate_result_date(
        self, 
        reference_date: date, 
        months_to_add: int, 
        day_of_month: int
    ) -> date:
        """Calculate a result date with month and day adjustments."""
        # Calculate year and month
        target_month = reference_date.month + months_to_add
        target_year = reference_date.year + (target_month - 1) // 12
        target_month = ((target_month - 1) % 12) + 1
        
        # Calculate the max day for the month
        if target_month == 2:
            # February - check for leap year
            if (target_year % 4 == 0 and target_year % 100 != 0) or target_year % 400 == 0:
                max_day = 29
            else:
                max_day = 28
        elif target_month in [4, 6, 9, 11]:
            # April, June, September, November
            max_day = 30
        else:
            max_day = 31
        
        # Ensure day is valid
        actual_day = min(day_of_month, max_day)
        
        # Create date
        result_date = date(target_year, target_month, actual_day)
        
        # Adjust for weekends
        while result_date.weekday() >= 5:  # 5 = Saturday, 6 = Sunday
            result_date += timedelta(days=1)
        
        return result_date