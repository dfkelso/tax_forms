# tax_forms/pages/forms/edit.py
import reflex as rx
from tax_forms.state.form_editor_state import FormEditorState
from tax_forms.templates import template

@template(route="/forms/:form_id/edit", title="Edit Form")
def form_edit():
    form_id = rx.State.router.page.params.form_id
    
    return rx.vstack(
        rx.heading(f"Edit Form: {FormEditorState.form_data.form_number}", size="lg"),
        rx.tabs(
            rx.tab_list(
                rx.tab("Basic Info"),
                rx.tab("Calculation Rules"),
                rx.tab("AI Assistant"),
            ),
            rx.tab_panels(
                rx.tab_panel(
                    # Basic form info panel
                    rx.form(
                        rx.vstack(
                            rx.hstack(
                                rx.form_control(
                                    rx.form_label("Form Number"),
                                    rx.input(
                                        value=FormEditorState.form_data.form_number,
                                        on_change=FormEditorState.set_form_number,
                                    ),
                                    is_required=True,
                                ),
                                rx.form_control(
                                    rx.form_label("Form Name"),
                                    rx.input(
                                        value=FormEditorState.form_data.form_name,
                                        on_change=FormEditorState.set_form_name,
                                    ),
                                    is_required=True,
                                ),
                                width="100%",
                            ),
                            rx.hstack(
                                rx.form_control(
                                    rx.form_label("Entity Type"),
                                    rx.select(
                                        ["individual", "corporation", "partnership", "scorp", "smllc"],
                                        value=FormEditorState.form_data.entity_type,
                                        on_change=FormEditorState.set_entity_type,
                                    ),
                                ),
                                rx.form_control(
                                    rx.form_label("Locality Type"),
                                    rx.select(
                                        ["federal", "state", "city"],
                                        value=FormEditorState.form_data.locality_type,
                                        on_change=FormEditorState.set_locality_type,
                                    ),
                                ),
                                rx.form_control(
                                    rx.form_label("Locality"),
                                    rx.input(
                                        value=FormEditorState.form_data.locality,
                                        on_change=FormEditorState.set_locality,
                                    ),
                                ),
                                width="100%",
                            ),
                            rx.hstack(
                                rx.form_control(
                                    rx.form_label("Parent Form"),
                                    rx.input(
                                        value=FormEditorState.form_data.parent_form_numbers,
                                        on_change=FormEditorState.set_parent_form_numbers,
                                    ),
                                ),
                                rx.form_control(
                                    rx.form_label("Owner"),
                                    rx.input(
                                        value=FormEditorState.form_data.owner,
                                        on_change=FormEditorState.set_owner,
                                    ),
                                ),
                                width="100%",
                            ),
                            rx.button("Save", on_click=FormEditorState.save_form),
                            width="100%",
                            spacing="4",
                        ),
                        on_submit=FormEditorState.save_form,
                    ),
                ),
                rx.tab_panel(
                    # Calculation rules panel
                    rx.vstack(
                        rx.heading("Calculation Rules", size="md"),
                        rx.button(
                            "Add Rule", 
                            on_click=FormEditorState.add_empty_rule
                        ),
                        rx.foreach(
                            FormEditorState.calculation_rules,
                            lambda rule, i: rx.box(
                                rx.vstack(
                                    rx.hstack(
                                        rx.heading(f"Rule #{i+1}", size="sm"),
                                        rx.spacer(),
                                        rx.button(
                                            "Delete", 
                                            on_click=FormEditorState.delete_rule(i),
                                            size="sm",
                                            color_scheme="red",
                                        ),
                                        width="100%",
                                    ),
                                    rx.form_control(
                                        rx.form_label("Effective Years (comma separated)"),
                                        rx.input(
                                            value=",".join(map(str, rule.effective_years)),
                                            on_change=lambda val: FormEditorState.update_rule_years(i, val),
                                        ),
                                    ),
                                    rx.heading("Due Date", size="xs"),
                                    rx.hstack(
                                        rx.form_control(
                                            rx.form_label("Months After Year End"),
                                            rx.number_input(
                                                value=rule.due_date.months_after_year_end,
                                                on_change=lambda val: FormEditorState.update_rule_due_date_months(i, val),
                                                min=0,
                                                max=24,
                                            ),
                                        ),
                                        rx.form_control(
                                            rx.form_label("Day of Month"),
                                            rx.number_input(
                                                value=rule.due_date.day_of_month,
                                                on_change=lambda val: FormEditorState.update_rule_due_date_day(i, val),
                                                min=1,
                                                max=31,
                                            ),
                                        ),
                                    ),
                                    rx.heading("Extension Due Date", size="xs"),
                                    rx.hstack(
                                        rx.form_control(
                                            rx.form_label("Months After Year End"),
                                            rx.number_input(
                                                value=rule.extension_due_date.months_after_year_end,
                                                on_change=lambda val: FormEditorState.update_rule_extension_months(i, val),
                                                min=0,
                                                max=24,
                                            ),
                                        ),
                                        rx.form_control(
                                            rx.form_label("Day of Month"),
                                            rx.number_input(
                                                value=rule.extension_due_date.day_of_month,
                                                on_change=lambda val: FormEditorState.update_rule_extension_day(i, val),
                                                min=1,
                                                max=31,
                                            ),
                                        ),
                                    ),
                                    width="100%",
                                    spacing="4",
                                    padding="4",
                                    border="1px solid",
                                    border_color="gray.200",
                                    border_radius="md",
                                    mb="4",
                                ),
                            )
                        ),
                        rx.button("Save All Rules", on_click=FormEditorState.save_rules),
                        width="100%",
                        spacing="4",
                    ),
                ),
                rx.tab_panel(
                    # AI Assistant panel
                    rx.vstack(
                        rx.heading("AI Due Date Assistant", size="md"),
                        rx.text(
                            "Let our AI assistant generate calculation rules for this form by researching past 7 years of due dates."
                        ),
                        rx.button(
                            "Generate Calculation Rules", 
                            on_click=FormEditorState.generate_ai_rules,
                            size="lg",
                            color_scheme="blue",
                        ),
                        rx.cond(
                            FormEditorState.ai_loading,
                            rx.center(
                                rx.spinner(size="xl"),
                                rx.text("Generating rules..."),
                            ),
                        ),
                        rx.cond(
                            FormEditorState.ai_results != "",
                            rx.vstack(
                                rx.heading("Generated Rules", size="md"),
                                rx.code_block(
                                    FormEditorState.ai_results,
                                    language="json",
                                ),
                                rx.button(
                                    "Apply Rules", 
                                    on_click=FormEditorState.apply_ai_rules,
                                ),
                            ),
                        ),
                        width="100%",
                        spacing="4",
                        padding="4",
                        border="1px solid",
                        border_color="blue.100",
                        border_radius="md",
                        background="blue.50",
                    ),
                ),
            ),
            width="100%",
        ),
        width="100%",
        spacing="6",
    )