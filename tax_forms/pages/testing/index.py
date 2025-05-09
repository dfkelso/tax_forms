# tax_forms/pages/testing/index.py
import reflex as rx
from tax_forms.state.testing_state import TestingState
from tax_forms.templates import template

@template(route="/testing", title="Test Due Dates")
def index():
    """Testing page for due date calculations."""
    return rx.container(
        rx.vstack(
            rx.heading("Test Due Dates", size="3"),
            rx.card(
                rx.vstack(
                    rx.form(
                        rx.vstack(
                            rx.hstack(
                                rx.select(
                                    ["individual", "corporation", "partnership", "scorp", "smllc"],
                                    label="Entity Type",
                                    value=TestingState.entity_type,
                                    on_change=TestingState.set_entity_type,
                                    width="100%",
                                ),
                                rx.vstack(
                                    rx.text("Coverage Start Date"),
                                    rx.input(
                                        type_="date",
                                        value=TestingState.start_date,
                                        on_change=TestingState.set_start_date,
                                        width="100%",
                                    ),
                                    width="100%",
                                ),
                                rx.vstack(
                                    rx.text("Coverage End Date"),
                                    rx.input(
                                        type_="date",
                                        value=TestingState.end_date,
                                        on_change=TestingState.set_end_date,
                                        width="100%",
                                    ),
                                    width="100%",
                                ),
                                width="100%",
                                spacing="4",
                            ),
                            rx.button(
                                "Create Test Job",
                                type_="submit",
                                on_click=TestingState.create_job,
                                width="full",
                                color_scheme="blue",
                            ),
                            width="100%",
                            spacing="4",
                        ),
                        on_submit=TestingState.create_job,
                    ),
                    width="100%",
                ),
                width="100%",
            ),
            
            # Conditional display of forms table
            rx.cond(
                TestingState.job_created,
                rx.vstack(
                    rx.heading("Available Forms", size="4", mt="6"),
                    rx.data_table(
                        data=TestingState.available_forms,
                        columns=[
                            {"field": "formNumber", "header": "Form Number"},
                            {"field": "formName", "header": "Form Name"},
                            {"field": "localityType", "header": "Locality Type"},
                            {"field": "locality", "header": "Locality"},
                            {
                                "field": "id",
                                "header": "Actions",
                                "cell": lambda data: rx.button(
                                    "Add to Job", 
                                    on_click=TestingState.add_form_to_job(data["id"]),
                                    size="sm",
                                    color_scheme="blue",
                                ),
                            }
                        ],
                        pagination=True,
                        search=True,
                        width="100%",
                    ),
                    width="100%",
                ),
            ),
            
            # Conditional display of due dates table
            rx.cond(
                TestingState.forms_added,
                rx.vstack(
                    rx.heading("Due Dates", size="4", mt="6"),
                    rx.data_table(
                        data=TestingState.due_dates,
                        columns=[
                            {"field": "formNumber", "header": "Form Number"},
                            {"field": "formName", "header": "Form Name"},
                            {"field": "due_date", "header": "Due Date"},
                            {"field": "extension_due_date", "header": "Extension Due Date"},
                        ],
                        pagination=True,
                        width="100%",
                    ),
                    width="100%",
                ),
            ),
            
            width="100%",
            align_items="flex-start",
            spacing="4",
        ),
        width="100%",
        padding="0",
    )