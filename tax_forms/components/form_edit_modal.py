# tax_forms/components/form_edit_modal.py
import reflex as rx
from ..backend.form_edit_state import FormEditState, CalculationRule


def form_field(label: str, field_component: rx.Component) -> rx.Component:
    """Create a form field with label."""
    return rx.vstack(
        rx.text(label, weight="bold", size="2"),
        field_component,
        spacing="1",
        width="100%",
    )


def _format_years(rule: CalculationRule) -> str:
    """Helper to format effective years as string."""
    return rx.cond(
        rule.effective_years.length() > 0,
        rx.Var.create(rule.effective_years).to(str).join(", "),
        ""
    )


def _get_due_months(rule: CalculationRule) -> str:
    """Helper to get due months value."""
    return rx.cond(
        rule.due_date.get("monthsAfterCalculationBase"),
        rule.due_date.get("monthsAfterCalculationBase").to(str),
        "0"
    )


def _get_due_day(rule: CalculationRule) -> str:
    """Helper to get due day value."""
    return rx.cond(
        rule.due_date.get("dayOfMonth"),
        rule.due_date.get("dayOfMonth").to(str),
        "15"
    )


def _get_extension_months(rule: CalculationRule) -> str:
    """Helper to get extension months value."""
    return rx.cond(
        rule.extension_due_date.get("monthsAfterCalculationBase"),
        rule.extension_due_date.get("monthsAfterCalculationBase").to(str),
        "0"
    )


def _get_extension_day(rule: CalculationRule) -> str:
    """Helper to get extension day value."""
    return rx.cond(
        rule.extension_due_date.get("dayOfMonth"),
        rule.extension_due_date.get("dayOfMonth").to(str),
        "15"
    )


def calculation_rule_item(rule: CalculationRule, index: int) -> rx.Component:
    """Single calculation rule component."""
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.heading(f"Rule #{index + 1}", size="3"),
                rx.spacer(),
                rx.button(
                    rx.icon("trash-2", size=16),
                    color_scheme="red",
                    size="1",
                    on_click=FormEditState.delete_rule(index),
                ),
                width="100%",
            ),
            
            # Effective Years
            form_field(
                "Effective Years (comma separated)",
                rx.input(
                    value=_format_years(rule),
                    on_change=FormEditState.update_rule_years(index),
                    placeholder="e.g. 2023, 2024, 2025",
                ),
            ),
            
            # Due Date
            rx.heading("Due Date", size="2", margin_top="1em"),
            rx.hstack(
                form_field(
                    "Months After Year End",
                    rx.input(
                        type="number",
                        value=_get_due_months(rule),
                        on_change=FormEditState.update_due_months(index),
                        min=0,
                        max=24,
                    ),
                ),
                form_field(
                    "Day of Month",
                    rx.input(
                        type="number",
                        value=_get_due_day(rule),
                        on_change=FormEditState.update_due_day(index),
                        min=1,
                        max=31,
                    ),
                ),
                spacing="4",
                width="100%",
            ),
            
            # Extension Due Date
            rx.heading("Extension Due Date", size="2", margin_top="1em"),
            rx.hstack(
                form_field(
                    "Months After Year End",
                    rx.input(
                        type="number",
                        value=_get_extension_months(rule),
                        on_change=FormEditState.update_extension_months(index),
                        min=0,
                        max=24,
                    ),
                ),
                form_field(
                    "Day of Month",
                    rx.input(
                        type="number",
                        value=_get_extension_day(rule),
                        on_change=FormEditState.update_extension_day(index),
                        min=1,
                        max=31,
                    ),
                ),
                spacing="4",
                width="100%",
            ),
            spacing="3",
            width="100%",
        ),
        width="100%",
    )


def form_edit_modal() -> rx.Component:
    """Form edit modal component."""
    return rx.dialog.root(
        rx.dialog.content(
            rx.vstack(
                # Header
                rx.hstack(
                    rx.heading(
                        rx.text("Edit Form: ", display="inline"),
                        rx.text(FormEditState.form_number, display="inline", weight="bold"),
                        size="5",
                    ),
                    rx.spacer(),
                    rx.dialog.close(
                        rx.button(
                            rx.icon("x", size=20),
                            variant="ghost",
                            on_click=FormEditState.close_modal,
                        ),
                    ),
                    width="100%",
                ),
                
                # Error message
                rx.cond(
                    FormEditState.error_message != "",
                    rx.callout(
                        FormEditState.error_message,
                        icon="alert-circle",
                        color_scheme="red",
                        width="100%",
                    ),
                ),
                
                # Form content with tabs
                rx.tabs.root(
                    rx.tabs.list(
                        rx.tabs.trigger("Basic Info", value="basic"),
                        rx.tabs.trigger("Calculation Rules", value="rules"),
                    ),
                    
                    # Basic Info Tab
                    rx.tabs.content(
                        rx.divider(),
                        rx.scroll_area(
                            
                            rx.vstack(
                                rx.spacer(),
                                rx.form(
                                    rx.vstack(
                                        rx.hstack(
                                            rx.text.strong("Form Number:", size="2"),
                                            rx.input(
                                                value=FormEditState.form_number,
                                                on_change=FormEditState.set_form_number,
                                                placeholder="e.g. 1040",    
                                                name="Form Number",
                                                required=True,                                       
                                            ), 
                                            rx.spacer(spacing="5"),
                                            rx.text.strong("Form Name:", size="2"),
                                            rx.input(
                                                value=FormEditState.form_name,
                                                on_change=FormEditState.set_form_name,
                                                placeholder="e.g. U.S. Individual Income Tax Return",
                                                required=True,                                       
                                            ),
                                            align="center"
                                        ),
                                    ),
                                ),
                                rx.spacer(),
                                rx.divider(),
                                # Form Number and Name row
                                rx.hstack(
                                    form_field(
                                        "Form Number*",
                                        rx.input(
                                            value=FormEditState.form_number,
                                            on_change=FormEditState.set_form_number,
                                            placeholder="e.g. 1040",
                                        ),
                                    ),
                                    form_field(
                                        "Form Name*",
                                        rx.input(
                                            value=FormEditState.form_name,
                                            on_change=FormEditState.set_form_name,
                                            placeholder="e.g. U.S. Individual Income Tax Return",
                                        ),
                                    ),
                                    spacing="4",
                                    width="100%",
                                ),
                                
                                # Entity Type, Locality Type, Locality row
                                rx.hstack(
                                    form_field(
                                        "Entity Type",
                                        rx.select.root(
                                            rx.select.trigger(placeholder="Select entity type"),
                                            rx.select.content(
                                                rx.foreach(
                                                    FormEditState.entity_types,
                                                    lambda entity: rx.select.item(entity, value=entity),
                                                ),
                                            ),
                                            value=FormEditState.entity_type,
                                            on_change=FormEditState.set_entity_type,
                                        ),
                                    ),
                                    form_field(
                                        "Locality Type",
                                        rx.select.root(
                                            rx.select.trigger(placeholder="Select locality type"),
                                            rx.select.content(
                                                rx.foreach(
                                                    FormEditState.locality_types,
                                                    lambda locality: rx.select.item(locality, value=locality),
                                                ),
                                            ),
                                            value=FormEditState.locality_type,
                                            on_change=FormEditState.set_locality_type,
                                        ),
                                    ),
                                    form_field(
                                        "Locality",
                                        rx.input(
                                            value=FormEditState.locality,
                                            on_change=FormEditState.set_locality,
                                            placeholder="e.g. United States",
                                        ),
                                    ),
                                    spacing="4",
                                    width="100%",
                                ),
                                
                                # Parent Form row
                                rx.hstack(
                                    rx.checkbox(
                                        "Is Parent Form?",
                                        checked=FormEditState.is_parent_form,
                                        on_change=FormEditState.set_is_parent_form,
                                    ),
                                    rx.cond(
                                        ~FormEditState.is_parent_form,
                                        form_field(
                                            "Parent Form",
                                            rx.select.root(
                                                rx.select.trigger(placeholder="Select parent form"),
                                                rx.select.content(
                                                    rx.foreach(
                                                        FormEditState.parent_forms,
                                                        lambda form: rx.select.item(form, value=form),
                                                    ),
                                                ),
                                                value=FormEditState.parent_form_number,
                                                on_change=FormEditState.set_parent_form_number,
                                            ),
                                        ),
                                    ),
                                    spacing="4",
                                    align="center",
                                    width="100%",
                                ),
                                
                                # Owner and Calculation Base row
                                rx.hstack(
                                    form_field(
                                        "Owner",
                                        rx.input(
                                            value=FormEditState.owner,
                                            on_change=FormEditState.set_owner,
                                            placeholder="MPM",
                                        ),
                                    ),
                                    form_field(
                                        "Calculation Base",
                                        rx.select.root(
                                            rx.select.trigger(placeholder="Select calculation base"),
                                            rx.select.content(
                                                rx.select.item("End", value="end"),
                                                rx.select.item("Start", value="start"),
                                            ),
                                            value=FormEditState.calculation_base,
                                            on_change=FormEditState.set_calculation_base,
                                        ),
                                    ),
                                    spacing="4",
                                    width="100%",
                                ),
                                
                                # Extension Information section
                                rx.heading("Extension Information", size="4", margin_top="1.5em"),
                                rx.hstack(
                                    form_field(
                                        "Extension Form Number",
                                        rx.input(
                                            value=FormEditState.extension_form_number,
                                            on_change=FormEditState.set_extension_form_number,
                                            placeholder="e.g. 4868",
                                        ),
                                    ),
                                    form_field(
                                        "Extension Form Name",
                                        rx.input(
                                            value=FormEditState.extension_form_name,
                                            on_change=FormEditState.set_extension_form_name,
                                            placeholder="e.g. Application for Automatic Extension",
                                        ),
                                    ),
                                    spacing="4",
                                    width="100%",
                                ),
                                rx.checkbox(
                                    "Piggyback Fed?",
                                    checked=FormEditState.piggyback_fed,
                                    on_change=FormEditState.set_piggyback_fed,
                                    margin_top="0.5em",
                                ),
                                
                                spacing="4",
                                width="100%",
                            ),
                            height="400px",
                            width="100%",
                        ),
                        value="basic",
                        width="100%",
                    ),
                    
                    # Calculation Rules Tab
                    rx.tabs.content(
                        rx.vstack(
                            rx.hstack(
                                # rx.heading("Calculation Rules", size="4"),
                                rx.spacer(),
                                rx.button(
                                    rx.icon("plus", size=16),
                                    "Add Rule",
                                    on_click=FormEditState.add_calculation_rule,
                                    size="2",
                                ),
                                width="100%",
                            ),
                            rx.scroll_area(
                                rx.vstack(
                                    rx.foreach(
                                        FormEditState.calculation_rules,
                                        calculation_rule_item,
                                    ),
                                    spacing="3",
                                    width="100%",
                                ),
                                height="350px",
                                width="100%",
                            ),
                            spacing="3",
                            width="100%",
                        ),
                        value="rules",
                        width="100%",
                    ),
                    
                    default_value="basic",
                    width="100%",
                ),
                
                # Footer with buttons
                rx.hstack(
                    rx.spacer(),
                    rx.button(
                        "Cancel",
                        variant="soft",
                        on_click=FormEditState.close_modal,
                    ),
                    rx.button(
                        "Save Form",
                        on_click=FormEditState.save_form,
                    ),
                    spacing="2",
                    width="100%",
                    padding_top="1em",
                ),
                
                spacing="4",
                width="100%",
            ),
            max_width="900px",
            padding="1.5em",
        ),
        open=FormEditState.show_edit_modal,
    )