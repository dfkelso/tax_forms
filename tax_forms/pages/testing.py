"""The testing page."""

import reflex as rx

from ..templates import template


class TestingState(rx.State):
    """State for testing due dates."""
    entity_type: str = "individual"
    start_date: str = ""
    end_date: str = ""
    job_created: bool = False
    
    def create_job(self):
        """Create a test job."""
        self.job_created = True


@template(route="/testing", title="Testing")
def testing() -> rx.Component:
    """The testing page.

    Returns:
        The UI for the testing page.
    """
    return rx.vstack(
        rx.heading("Test Due Dates", size="5"),
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
                rx.heading("Job Created", size="md"),
                rx.text("In a future update, you'll see available forms here."),
                width="100%",
                spacing="4",
                mt="6",
            ),
        ),
        spacing="8",
        width="100%",
    )