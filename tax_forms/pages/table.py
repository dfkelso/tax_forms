# reflex_app/pages/table.py
"""The forms page."""

import reflex as rx

from ..backend.table_state import TableState
from ..templates import template
from ..views.table import main_table


@template(route="/forms", title="Forms", on_load=TableState.load_entries)
def table() -> rx.Component:
    """The forms page.

    Returns:
        The UI for the forms page.

    """
    return rx.vstack(
        rx.hstack(
            rx.heading("Tax Forms", size="5"),
            rx.spacer(),
            rx.button("Add Form", on_click=rx.redirect("/forms/new")),
            width="100%",
        ),
        main_table(),
        spacing="8",
        width="100%",
    )