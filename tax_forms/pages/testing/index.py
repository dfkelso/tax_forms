# tax_forms/pages/testing/index.py
import reflex as rx
from tax_forms.state.testing_state import TestingState
from tax_forms.templates import template

@template(route="/testing", title="Testing")
def testing_page():
    return rx.vstack(
        rx.heading("Test Due Dates", size="lg"),
        rx.card(
            rx.vstack(
                rx.text("Create a test job to verify due date calculations."),
                rx.form(
                    rx.vstack(
                        rx.hstack(
                            rx.form_control(
                                rx.form_label("Entity Type"),
                                rx.select(
                                    ["individual", "corporation", "partnership", "scorp", "smllc"],
                                    value=TestingState.entity_type,
                                    on_change=TestingState.set_entity_type,
                                ),
                                is_required=True,
                            ),
                            rx.form_control(
                                rx.form_label("Start Date"),
                                rx.input(
                                    type_="date",
                                    value=TestingState.start_date,
                                    on_change=TestingState.set_start_date,
                                ),
                                is_required=True,
                            ),
                            rx.form_control(
                                rx.form_label("End Date"),
                                rx.input(
                                    type_="date",
                                    value=TestingState.end_date,
                                    on_change=TestingState.set_end_date,
                                ),
                                is_required=True,
                            ),
                            width="100%",
                        ),
                        rx.button("Create Test Job", on_click=TestingState.create_job),
                        width="100%",
                        spacing="4",
                    ),
                    on_submit=TestingState.create_job,
                ),
                width="100%",
            ),
            width="100%",
        ),
        rx.cond(
            TestingState.job_created,
            rx.vstack(
                rx.heading("Available Forms", size="md"),
                rx.text("Select forms to add to your test job:"),
                rx.table(
                    rx.thead(
                        rx.tr(
                            rx.th("Form Number"),
                            rx.th("Form Name"),
                            rx.th("Locality"),
                            rx.th("Actions"),
                        )
                    ),
                    rx.tbody(
                        rx.foreach(
                            TestingState.available_forms,
                            lambda form: rx.tr(
                                rx.td(form.form_number),
                                rx.td(form.form_name),
                                rx.td(f"{form.locality_type} - {form.locality}"),
                                rx.td(
                                    rx.button(
                                        "Add to Job",
                                        on_click=TestingState.add_form_to_job(form.id),
                                        size="sm",
                                    )
                                ),
                            )
                        )
                    ),
                    width="100%",
                ),
                rx.cond(
                    TestingState.forms_added,
                    rx.vstack(
                        rx.heading("Calculated Due Dates", size="md"),
                        rx.table(
                            rx.thead(
                                rx.tr(
                                    rx.th("Form Number"),
                                    rx.th("Form Name"),
                                    rx.th("Due Date"),
                                    rx.th("Extension Due Date"),
                                )
                            ),
                            rx.tbody(
                                rx.foreach(
                                    TestingState.due_dates,
                                    lambda date_info: rx.tr(
                                        rx.td(date_info.form_number),
                                        rx.td(date_info.form_name),
                                        rx.td(date_info.due_date),
                                        rx.td(date_info.extension_due_date),
                                    )
                                )
                            ),
                            width="100%",
                        ),
                        rx.button(
                            "Clear Results", 
                            on_click=TestingState.clear_results,
                            color_scheme="red",
                        ),
                        width="100%",
                        spacing="4",
                    ),
                ),
                width="100%",
                spacing="6",
                mt="6",
            ),
        ),
        width="100%",
        spacing="6",
    )