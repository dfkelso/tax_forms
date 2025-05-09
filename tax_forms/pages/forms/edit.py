# tax_forms/pages/forms/edit.py
import reflex as rx
from tax_forms.state.form_editor_state import FormEditorState
from tax_forms.templates import template

@template(route="/forms/edit/{form_id}", title="Edit Form")
def edit():
    """Edit an existing form."""
    return form_editor()

@template(route="/forms/new", title="New Form")
def new():
    """Create a new form."""
    return form_editor(is_new=True)

def form_editor(is_new=False):
    """Form editor component."""
    return rx.container(
        rx.vstack(
            rx.heading(
                "New Tax Form" if is_new else "Edit Tax Form", 
                size="3",
            ),
            
            # Basic form information card
            rx.card(
                rx.vstack(
                    rx.hstack(
                        rx.vstack(
                            rx.text("Form Number", as_="strong"),
                            rx.input(
                                placeholder="e.g. 1040",
                                value=FormEditorState.form_number,
                                on_change=FormEditorState.set_form_number,
                                width="100%",
                            ),
                            width="100%",
                        ),
                        rx.vstack(
                            rx.text("Form Name", as_="strong"),
                            rx.input(
                                placeholder="e.g. U.S. Individual Income Tax Return",
                                value=FormEditorState.form_name,
                                on_change=FormEditorState.set_form_name,
                                width="100%",
                            ),
                            width="100%",
                        ),
                        spacing="4",
                        width="100%",
                    ),
                    
                    rx.hstack(
                        rx.vstack(
                            rx.text("Entity Type", as_="strong"),
                            rx.select(
                                ["individual", "corporation", "partnership", "scorp", "smllc"],
                                placeholder="Select entity type",
                                value=FormEditorState.entity_type,
                                on_change=FormEditorState.set_entity_type,
                                width="100%",
                            ),
                            width="100%",
                        ),
                        rx.vstack(
                            rx.text("Locality Type", as_="strong"),
                            rx.select(
                                ["federal", "state", "city"],
                                placeholder="Select locality type",
                                value=FormEditorState.locality_type,
                                on_change=FormEditorState.set_locality_type,
                                width="100%",
                            ),
                            width="100%",
                        ),
                        rx.vstack(
                            rx.text("Locality", as_="strong"),
                            rx.input(
                                placeholder="e.g. United States, California",
                                value=FormEditorState.locality,
                                on_change=FormEditorState.set_locality,
                                width="100%",
                            ),
                            width="100%",
                        ),
                        spacing="4",
                        width="100%",
                    ),
                    
                    rx.hstack(
                        rx.vstack(
                            rx.text("Parent Relationship", as_="strong"),
                            rx.checkbox(
                                "This is a parent form",
                                value=FormEditorState.is_parent,
                                on_change=FormEditorState.set_is_parent,
                            ),
                            rx.cond(
                                ~FormEditorState.is_parent,
                                rx.input(
                                    placeholder="Parent form number",
                                    value=FormEditorState.parent_form_number,
                                    on_change=FormEditorState.set_parent_form_number,
                                    width="100%",
                                ),
                            ),
                            width="100%",
                        ),
                        rx.vstack(
                            rx.text("Owner", as_="strong"),
                            rx.input(
                                value=FormEditorState.owner,
                                on_change=FormEditorState.set_owner,
                                width="100%",
                            ),
                            width="100%",
                        ),
                        rx.vstack(
                            rx.text("Calculation Base", as_="strong"),
                            rx.select(
                                ["end", "start"],
                                placeholder="Select calculation base",
                                value=FormEditorState.calculation_base,
                                on_change=FormEditorState.set_calculation_base,
                                width="100%",
                            ),
                            width="100%",
                        ),
                        spacing="4",
                        width="100%",
                    ),
                    
                    # Extension information
                    rx.divider(),
                    rx.heading("Extension Information", size="4"),
                    
                    rx.hstack(
                        rx.vstack(
                            rx.text("Extension Form Number", as_="strong"),
                            rx.input(
                                placeholder="e.g. 4868",
                                value=FormEditorState.extension_form_number,
                                on_change=FormEditorState.set_extension_form_number,
                                width="100%",
                            ),
                            width="100%",
                        ),
                        rx.vstack(
                            rx.text("Extension Form Name", as_="strong"),
                            rx.input(
                                placeholder="e.g. Application for Automatic Extension",
                                value=FormEditorState.extension_form_name,
                                on_change=FormEditorState.set_extension_form_name,
                                width="100%",
                            ),
                            width="100%",
                        ),
                        rx.vstack(
                            rx.text("Piggyback Fed", as_="strong"),
                            rx.checkbox(
                                "Accepts federal extension",
                                value=FormEditorState.piggyback_fed,
                                on_change=FormEditorState.set_piggyback_fed,
                            ),
                            width="100%",
                        ),
                        spacing="4",
                        width="100%",
                    ),
                    
                    width="100%",
                    spacing="4",
                ),
                width="100%",
            ),
            
            # Calculation Rules
            rx.card(
                rx.vstack(
                    rx.hstack(
                        rx.heading("Calculation Rules", size="4"),
                        rx.spacer(),
                        rx.button(
                            "Generate with AI",
                            on_click=FormEditorState.generate_rules_with_ai,
                            color_scheme="teal",
                        ),
                        width="100%",
                    ),
                    
                    # Rules Table
                    rx.cond(
                        FormEditorState.calculation_rules,
                        rx.vstack(
                            rx.foreach(
                                FormEditorState.calculation_rules,
                                lambda rule, i: rx.card(
                                    rx.vstack(
                                        rx.hstack(
                                            rx.text(f"Years: {', '.join(map(str, rule['effectiveYears']))}", as_="strong"),
                                            rx.spacer(),
                                            rx.button(
                                                "Delete",
                                                on_click=lambda: FormEditorState.delete_rule(i),
                                                color_scheme="red",
                                                size="sm",
                                            ),
                                            width="100%",
                                        ),
                                        rx.text(f"Due Date: {rule['dueDate']['monthsAfterCalculationBase']} months after year end, day {rule['dueDate']['dayOfMonth']}"),
                                        rx.text(f"Extension Due Date: {rule['extensionDueDate']['monthsAfterCalculationBase']} months after year end, day {rule['extensionDueDate']['dayOfMonth']}"),
                                        rx.cond(
                                            "fiscalYearExceptions" in rule["dueDate"],
                                            rx.card(
                                                rx.vstack(
                                                    rx.text("Fiscal Year Exceptions:", as_="strong"),
                                                    rx.foreach(
                                                        rule["dueDate"]["fiscalYearExceptions"].items(),
                                                        lambda exception: rx.text(f"Month {exception[0]}: {exception[1]['monthsAfterCalculationBase']} months after year end, day {exception[1]['dayOfMonth']}"),
                                                    ),
                                                    spacing="1",
                                                ),
                                                padding="2",
                                                background_color="gray.50",
                                            ),
                                        ),
                                        width="100%",
                                        spacing="2",
                                    ),
                                    padding="3",
                                ),
                            ),
                            rx.button(
                                "Add Rule",
                                on_click=FormEditorState.add_rule,
                                color_scheme="blue",
                                variant="outline",
                            ),
                            width="100%",
                            spacing="3",
                        ),
                        rx.vstack(
                            rx.text("No calculation rules added yet."),
                            rx.button(
                                "Add Rule",
                                on_click=FormEditorState.add_rule,
                                color_scheme="blue",
                                variant="outline",
                            ),
                            spacing="3",
                        ),
                    ),
                    
                    width="100%",
                    spacing="4",
                ),
                width="100%",
            ),
            
            # Save buttons
            rx.hstack(
                rx.button(
                    "Save Form",
                    on_click=FormEditorState.save_form,
                    color_scheme="green",
                ),
                rx.button(
                    "Cancel",
                    on_click=rx.redirect("/forms"),
                    color_scheme="gray",
                ),
                spacing="4",
                mt="4",
            ),
            
            width="100%",
            spacing="4",
            align_items="stretch",
        ),
        width="100%",
        padding="0",
    )