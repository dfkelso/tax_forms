import reflex as rx
from tax_forms.state.testing_state import TestingState
from tax_forms.templates import template

@template(route="/testing", title="Testing")
def testing_page():
    return rx.container(
        rx.vstack(
            rx.heading("Test Due Dates", size="3"),
            rx.card(
                rx.vstack(
                    rx.hstack(
                        rx.vstack(
                            rx.text("Entity Type", as_="strong"),
                            rx.select(
                                ["individual", "corporation", "partnership", "scorp", "smllc"],
                                placeholder="Select entity type",
                                on_change=TestingState.set_entity_type,
                                value=TestingState.entity_type,
                                width="100%",
                            ),
                            width="100%",
                        ),
                        rx.vstack(
                            rx.text("Coverage Period Start", as_="strong"),
                            rx.input(
                                type_="date",
                                on_change=TestingState.set_start_date,
                                value=TestingState.start_date,
                                width="100%",
                            ),
                            width="100%",
                        ),
                        rx.vstack(
                            rx.text("Coverage Period End", as_="strong"),
                            rx.input(
                                type_="date",
                                on_change=TestingState.set_end_date,
                                value=TestingState.end_date,
                                width="100%",
                            ),
                            width="100%",
                        ),
                        width="100%",
                        spacing="4",
                    ),
                    rx.divider(),
                    rx.hstack(
                        rx.button("Create Test Job", on_click=TestingState.create_job),
                        rx.spacer(),
                        width="100%",
                    ),
                    width="100%",
                    spacing="4",
                ),
                width="100%",
            ),
            rx.cond(
                TestingState.job_created,
                rx.vstack(
                    rx.heading("Select Form", size="3"),
                    rx.data_table(
                        data=TestingState.available_forms,
                        columns=[
                            {"field": "form_number", "header": "Form Number"},
                            {"field": "form_name", "header": "Form Name"},
                            {"field": "locality_type", "header": "Locality Type"},
                            {"field": "locality", "header": "Locality"},
                            {
                                "field": "id",
                                "header": "Actions",
                                "cell": lambda data: rx.button(
                                    "Add to Job", 
                                    on_click=TestingState.add_form_to_job(data['id']),
                                    size="1",
                                )
                            }
                        ],
                        pagination=True,
                        search=True,
                        sort=True,
                        width="100%",
                    ),
                    rx.cond(
                        TestingState.forms_added,
                        rx.vstack(
                            rx.heading("Due Dates", size="3"),
                            rx.data_table(
                                data=TestingState.due_dates,
                                columns=[
                                    {"field": "form_number", "header": "Form Number"},
                                    {"field": "form_name", "header": "Form Name"},
                                    {"field": "due_date", "header": "Due Date"},
                                    {"field": "extension_due_date", "header": "Extension Due Date"},
                                ],
                                pagination=True,
                                search=True,
                                sort=True,
                                width="100%",
                            ),
                            width="100%",
                        ),
                    ),
                    width="100%",
                ),
            ),
            width="100%",
            align_items="flex-start",
        ),
        width="100%",
        padding="0",
    )