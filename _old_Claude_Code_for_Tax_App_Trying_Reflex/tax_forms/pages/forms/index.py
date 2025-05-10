# tax_forms/pages/forms/index.py
import reflex as rx
from tax_forms.state.forms_state import FormsState
from tax_forms.templates import template

@template(route="/forms", title="Forms")
def forms_index():
    return rx.vstack(
        rx.hstack(
            rx.heading("Tax Forms", size="lg"),
            rx.spacer(),
            rx.button("Add Form", on_click=rx.navigate("/forms/new")),
            width="100%",
            mb=4,
        ),
        rx.hstack(
            rx.input(
                placeholder="Search forms...",
                on_change=FormsState.set_search_text,
                value=FormsState.search_text,
                width="300px",
            ),
            rx.select(
                ["All", "individual", "corporation", "partnership", "scorp", "smllc"],
                placeholder="Entity Type",
                on_change=FormsState.set_entity_filter,
                value=FormsState.entity_filter,
            ),
            rx.button("Search", on_click=FormsState.filter_forms),
            spacing="4",
            width="100%",
            mb=4,
        ),
        rx.table(
            rx.thead(
                rx.tr(
                    rx.th("Form Number"),
                    rx.th("Form Name"),
                    rx.th("Entity Type"),
                    rx.th("Locality"),
                    rx.th("Actions"),
                )
            ),
            rx.tbody(
                rx.foreach(
                    FormsState.forms,
                    lambda form: rx.tr(
                        rx.td(form.form_number),
                        rx.td(form.form_name),
                        rx.td(form.entity_type),
                        rx.td(f"{form.locality_type} - {form.locality}"),
                        rx.td(
                            rx.hstack(
                                rx.button(
                                    "Edit",
                                    on_click=rx.navigate(f"/forms/{form.id}/edit"),
                                    size="sm",
                                ),
                                rx.button(
                                    "Delete",
                                    on_click=FormsState.delete_form(form.id),
                                    size="sm",
                                    color_scheme="red",
                                ),
                                spacing="2",
                            )
                        ),
                    )
                )
            ),
            width="100%",
        ),
        width="100%",
        spacing="4",
    )