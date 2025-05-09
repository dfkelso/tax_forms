import reflex as rx
from tax_forms.state.forms_state import FormsState
from tax_forms.templates import template

@template(route="/forms", title="Forms")
def forms_list():
    return rx.container(
        rx.vstack(
            rx.hstack(
                rx.heading("Tax Forms", size="3"),
                rx.spacer(),
                rx.button("Add Form", on_click=rx.redirect("/forms/new"), color_scheme="blue"),
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
            rx.data_table(
                data=FormsState.forms,
                columns=[
                    {"field": "id", "header": "ID"},
                    {"field": "form_number", "header": "Form Number"},
                    {"field": "form_name", "header": "Form Name"},
                    {"field": "entity_type", "header": "Entity Type"},
                    {"field": "locality_type", "header": "Locality Type"},
                    {"field": "locality", "header": "Locality"},
                    {
                        "field": "id", 
                        "header": "Actions",
                        "cell": lambda data: rx.hstack(
                            rx.button("Edit", on_click=rx.redirect(f"/forms/{data['id']}/edit"), size="1"),
                            rx.button("Delete", color_scheme="red", size="1",
                                     on_click=FormsState.delete_form(data['id'])),
                            spacing="2",
                        )
                    }
                ],
                pagination=True,
                search=True,
                sort=True,
                width="100%",
            ),
            width="100%",
            align_items="flex-start",
        ),
        width="100%",
        padding="0",
    )