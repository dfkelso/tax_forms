from datetime import date, timedelta
from typing import Dict, Any, Optional, List, Tuple

class DueDateCalculator:
    """Calculator for determining tax form due dates."""
    
    def __init__(self, forms_repository=None):
        """Initialize the calculator with a forms repository."""
        self.forms_repository = forms_repository
    
    def calculate_dates(
        self, 
        form_number: str, 
        entity_type: str, 
        locality_type: str, 
        locality: str, 
        coverage_start_date: date, 
        coverage_end_date: date
    ) -> Optional[Dict[str, date]]:
        """Calculate due dates for a specific form and time period."""
        # Find the form in the repository
        form = self._find_form(form_number, entity_type, locality_type, locality)
        if not form:
            return None
        
        # Determine base date based on calculation base
        calculation_base = form.get('calculationBase', 'end')
        base_date = coverage_end_date if calculation_base == 'end' else coverage_start_date
        
        # Find rule for the specific tax year
        tax_year = coverage_end_date.year
        rule = self._find_applicable_rule(form, tax_year)
        
        if not rule:
            return None
        
        # Calculate dates using the rule
        return self._calculate_specific_dates(rule, coverage_start_date, coverage_end_date, base_date)
    
    def _find_form(
        self, 
        form_number: str, 
        entity_type: str, 
        locality_type: str, 
        locality: str
    ) -> Optional[Dict[str, Any]]:
        """Find a form in the repository by its attributes."""
        if not self.forms_repository:
            return None
            
        forms = self.forms_repository.get_all_forms()
        for form in forms:
            if (form.get('formNumber') == form_number and
                form.get('entityType') == entity_type and
                form.get('localityType') == locality_type and
                form.get('locality') == locality):
                return form
        return None
    
    def _find_applicable_rule(
        self, 
        form: Dict[str, Any], 
        tax_year: int
    ) -> Optional[Dict[str, Any]]:
        """Find the applicable rule for a specific tax year."""
        calculation_rules = form.get('calculationRules', [])
        if not calculation_rules:
            return None
            
        # Look for exact match first
        for rule in calculation_rules:
            effective_years = rule.get('effectiveYears', [])
            if tax_year in effective_years:
                return rule
                
        # If no exact match, find closest year
        closest_rule = None
        closest_year_diff = float('inf')
        
        for rule in calculation_rules:
            effective_years = rule.get('effectiveYears', [])
            for year in effective_years:
                year_diff = abs(year - tax_year)
                if year_diff < closest_year_diff:
                    closest_year_diff = year_diff
                    closest_rule = rule.copy()
                    if 'approximated' not in closest_rule:
                        closest_rule['approximated'] = True
                        
        return closest_rule
    
    def _calculate_specific_dates(
        self, 
        rule: Dict[str, Any], 
        start_date: date, 
        end_date: date, 
        base_date: date = None
    ) -> Dict[str, date]:
        """Calculate specific dates based on a rule."""
        # Default to end date as base if not specified
        base_date = base_date or end_date
        
        # Get month of base date for fiscal year exception checking
        base_month = str(base_date.month).zfill(2)
        
        # Calculate due date
        due_date = None
        if 'dueDate' in rule:
            due_date = self._calculate_date(rule['dueDate'], base_date, base_month, end_date.year)
        
        # Calculate extension date
        extension_due_date = None
        if 'extensionDueDate' in rule:
            extension_due_date = self._calculate_date(rule['extensionDueDate'], base_date, base_month, end_date.year)
        
        # Include the approximated flag if it exists
        result = {
            'due_date': due_date,
            'extension_due_date': extension_due_date
        }
        
        if rule.get('approximated'):
            result['approximated'] = True
            
        return result
    
    def _calculate_date(
        self, 
        date_rule: Dict[str, Any], 
        base_date: date, 
        base_month: str, 
        year: int
    ) -> date:
        """Calculate a specific date based on a rule."""
        # Default values
        months_to_add = 0
        day_of_month = date_rule.get('dayOfMonth', 15)
        reference_date = base_date
        
        # Check for fiscal year exceptions first
        fiscal_exceptions = date_rule.get('fiscalYearExceptions', {})
        if base_month in fiscal_exceptions:
            exception = fiscal_exceptions[base_month]
            
            if 'monthsAfterCalculationBase' in exception:
                months_to_add = exception['monthsAfterCalculationBase']
            elif 'monthsAfterYearStart' in exception:
                months_to_add = exception['monthsAfterYearStart']
                reference_date = date(year, 1, 1)
                
            if 'dayOfMonth' in exception:
                day_of_month = exception['dayOfMonth']
        else:
            # Use standard rules
            if 'monthsAfterCalculationBase' in date_rule:
                months_to_add = date_rule['monthsAfterCalculationBase']
            elif 'monthsAfterYearStart' in date_rule:
                months_to_add = date_rule['monthsAfterYearStart']
                reference_date = date(year, 1, 1)
        
        # Calculate the result date using date arithmetic
        return self._calculate_result_date(reference_date, months_to_add, day_of_month)
    
    def _calculate_result_date(
        self, 
        reference_date: date, 
        months_to_add: int, 
        day_of_month: int
    ) -> date:
        """Calculate a result date with month and day adjustments."""
        # Calculate year and month
        year = reference_date.year + ((reference_date.month + months_to_add - 1) // 12)
        month = ((reference_date.month + months_to_add - 1) % 12) + 1
        
        # Adjust day for month length
        max_day = self._get_month_last_day(year, month)
        day = min(day_of_month, max_day)
        
        # Create date
        result_date = date(year, month, day)
        
        # Adjust for weekends and holidays
        while self._is_weekend(result_date) or self._is_holiday(result_date):
            result_date += timedelta(days=1)
            
        return result_date
    
    def _get_month_last_day(self, year: int, month: int) -> int:
        """Get the last day of a month."""
        if month == 12:
            next_month = date(year + 1, 1, 1)
        else:
            next_month = date(year, month + 1, 1)
        return (next_month - timedelta(days=1)).day
    
    def _is_weekend(self, d: date) -> bool:
        """Check if a date is a weekend."""
        return d.weekday() >= 5  # 5 = Saturday, 6 = Sunday
    
    def _is_holiday(self, d: date) -> bool:
        """Check if a date is a holiday."""
        # Placeholder for holiday checking
        # In a real implementation, this would check against a holiday calendar
        return False