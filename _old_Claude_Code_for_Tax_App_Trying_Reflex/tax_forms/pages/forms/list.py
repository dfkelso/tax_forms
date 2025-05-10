# tax_forms/pages/forms/list.py
import reflex as rx
from tax_forms.state.forms_state import FormsState
from tax_forms.templates import template

@template(route="/forms", title="Tax Forms")
def list():
    """Forms list page."""
    return rx.container(
        rx.vstack(
            rx.hstack(
                rx.heading("Tax Forms", size="3"),
                rx.spacer(),
                rx.button(
                    "Add Form", 
                    on_click=rx.redirect("/forms/new"),
                    color_scheme="blue",
                ),
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
                rx.button(
                    "Filter", 
                    on_click=FormsState.filter_forms,
                    color_scheme="blue",
                ),
                spacing="4",
                width="100%",
                mb=4,
            ),
            rx.cond(
                FormsState.forms,
                rx.data_table(
                    data=FormsState.forms,
                    columns=[
                        {"field": "id", "header": "ID", "cell": lambda data: rx.text(data["id"])},
                        {"field": "formNumber", "header": "Form Number", "cell": lambda data: rx.text(data["formNumber"])},
                        {"field": "formName", "header": "Form Name", "cell": lambda data: rx.text(data["formName"])},
                        {"field": "entityType", "header": "Entity Type", "cell": lambda data: rx.text(data["entityType"])},
                        {"field": "localityType", "header": "Locality Type", "cell": lambda data: rx.text(data["localityType"])},
                        {"field": "locality", "header": "Locality", "cell": lambda data: rx.text(data["locality"])},
                        {
                            "field": "id", 
                            "header": "Actions",
                            "cell": lambda data: rx.hstack(
                                rx.button(
                                    "Edit", 
                                    on_click=rx.redirect(f"/forms/{data['id']}/edit"),
                                    size="sm",
                                    color_scheme="blue",
                                ),
                                rx.button(
                                    "Delete", 
                                    on_click=FormsState.delete_form(data["id"]),
                                    size="sm",
                                    color_scheme="red",
                                ),
                                spacing="2",
                            )
                        }
                    ],
                    pagination=True,
                    search=True,
                    width="100%",
                ),
                rx.center(
                    rx.vstack(
                        rx.icon("alert-circle", size="xl", color="gray"),
                        rx.text("No forms found", color="gray"),
                        spacing="4",
                        padding="8",
                    )
                ),
            ),
            width="100%",
            align_items="stretch",
        ),
        width="100%",
        padding="0",
    )