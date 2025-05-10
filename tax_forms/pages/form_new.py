"""The form new page."""

import reflex as rx

from ..templates import template


class FormNewState(rx.State):
    """State for creating a new form."""
    form_number: str = ""
    form_name: str = ""
    entity_type: str = "individual"
    locality_type: str = "federal"
    locality: str = ""
    
    def create_form(self):
        """Create a new form."""
        # For now, just navigate back to the forms list
        return rx.navigate("/forms")


@template(route="/forms/new", title="New Form")
def form_new() -> rx.Component:
    """The form new page.

    Returns:
        The UI for creating a new form.
    """
    return rx.vstack(
        rx.heading("Create New Form", size="5"),
        rx.card(
            rx.form(
                rx.vstack(
                    rx.hstack(
                        rx.form_control(
                            rx.form_label("Form Number"),
                            rx.input(
                                value=FormNewState.form_number,
                                on_change=FormNewState.set_form_number,
                                placeholder="e.g. 1040"
                            ),
                            is_required=True,
                        ),
                        rx.form_control(
                            rx.form_label("Form Name"),
                            rx.input(
                                value=FormNewState.form_name,
                                on_change=FormNewState.set_form_name,
                                placeholder="e.g. U.S. Individual Income Tax Return"
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
                                value=FormNewState.entity_type,
                                on_change=FormNewState.set_entity_type,
                            ),
                            is_required=True,
                        ),
                        rx.form_control(
                            rx.form_label("Locality Type"),
                            rx.select(
                                ["federal", "state", "city"],
                                value=FormNewState.locality_type,
                                on_change=FormNewState.set_locality_type,
                            ),
                            is_required=True,
                        ),
                        rx.form_control(
                            rx.form_label("Locality"),
                            rx.input(
                                value=FormNewState.locality,
                                on_change=FormNewState.set_locality,
                                placeholder="e.g. United States or California"
                            ),
                            is_required=True,
                        ),
                        width="100%",
                    ),
                    rx.hstack(
                        rx.button("Create Form", type="submit"),
                        rx.button("Cancel", on_click=rx.navigate("/forms"), color_scheme="gray", variant="soft"),
                        justify="end",
                        width="100%",
                    ),
                    width="100%",
                    spacing="4",
                    padding="1em",
                ),
                on_submit=FormNewState.create_form,
            ),
            width="100%",
        ),
        spacing="8",
        width="100%",
    )