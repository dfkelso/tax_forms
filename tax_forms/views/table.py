# tax_forms/views/table.py
import reflex as rx

from ..backend.table_state import TaxForm, TableState
from ..backend.form_edit_state import FormEditState

def _header_cell(text: str, icon: str) -> rx.Component:
    return rx.table.column_header_cell(
        rx.hstack(
            rx.icon(icon, size=18),
            rx.text(text),
            align="center",
            spacing="2",
        ),
    )

def _show_item(item: TaxForm, index: int) -> rx.Component:
    bg_color = rx.cond(
        index % 2 == 0,
        rx.color("gray", 1),
        rx.color("accent", 2),
    )
    hover_color = rx.cond(
        index % 2 == 0,
        rx.color("gray", 3),
        rx.color("accent", 3),
    )
    
    return rx.table.row(
        rx.table.row_header_cell(
            rx.link(
                item.form_number,
                on_click=lambda: FormEditState.open_edit_modal(item.id),
                color=rx.color("blue", 9),
                text_decoration="none",
                _hover={"text_decoration": "underline", "cursor": "pointer"},
            )
        ),
        rx.table.cell(item.form_name),
        rx.table.cell(item.entity_type.title()),
        rx.table.cell(item.locality_type.title()),
        rx.table.cell(item.locality),
        rx.table.cell(
            rx.text(rx.cond(item.due_date, item.due_date, "N/A"))
        ),
        rx.table.cell(
            rx.text(rx.cond(item.extension_due_date, item.extension_due_date, "N/A"))
        ),
        rx.table.cell(
            rx.hstack(
                rx.icon_button(
                    rx.icon("square-check", size=20),
                    on_click=lambda: FormEditState.open_edit_modal(item.id),
                    size="2",
                    color_scheme="green",
                    variant="soft",
                ),
                rx.icon_button(
                    rx.icon("pencil", size=20),
                    on_click=lambda: FormEditState.open_edit_modal(item.id),
                    size="2",
                    color_scheme="blue",
                    variant="soft",
                ),
                rx.icon_button(
                    rx.icon("trash", size=20),
                    on_click=lambda: TableState.show_delete_confirmation(item.id),
                    size="2",
                    color_scheme="red",
                    variant="soft",
                ),
                spacing="2",
            )
        ),
        style={"_hover": {"bg": hover_color}, "bg": bg_color},
        align="center",
    )

def delete_modal() -> rx.Component:
    return rx.alert_dialog.root(
        rx.alert_dialog.content(
            rx.alert_dialog.title("Confirm Delete"),
            rx.alert_dialog.description(
                "Are you sure you want to delete this form? This action cannot be undone."
            ),
            rx.flex(
                rx.alert_dialog.cancel(
                    rx.button("Cancel", variant="soft", color_scheme="gray"),
                ),
                rx.alert_dialog.action(
                    rx.button(
                        "Delete",
                        color_scheme="red",
                        on_click=TableState.confirm_delete,
                    ),
                ),
                spacing="3",
                justify="end",
            ),
        ),
        open=TableState.show_delete_modal,
    )

def _pagination_view() -> rx.Component:
    return (
        rx.hstack(
            rx.text(
                "Page ",
                rx.code(TableState.page_number),
                f" of {TableState.total_pages}",
                justify="end",
            ),
            rx.hstack(
                rx.icon_button(
                    rx.icon("chevrons-left", size=18),
                    on_click=TableState.first_page,
                    opacity=rx.cond(TableState.page_number == 1, 0.6, 1),
                    color_scheme=rx.cond(TableState.page_number == 1, "gray", "accent"),
                    variant="soft",
                ),
                rx.icon_button(
                    rx.icon("chevron-left", size=18),
                    on_click=TableState.prev_page,
                    opacity=rx.cond(TableState.page_number == 1, 0.6, 1),
                    color_scheme=rx.cond(TableState.page_number == 1, "gray", "accent"),
                    variant="soft",
                ),
                rx.icon_button(
                    rx.icon("chevron-right", size=18),
                    on_click=TableState.next_page,
                    opacity=rx.cond(
                        TableState.page_number == TableState.total_pages, 0.6, 1
                    ),
                    color_scheme=rx.cond(
                        TableState.page_number == TableState.total_pages,
                        "gray",
                        "accent",
                    ),
                    variant="soft",
                ),
                rx.icon_button(
                    rx.icon("chevrons-right", size=18),
                    on_click=TableState.last_page,
                    opacity=rx.cond(
                        TableState.page_number == TableState.total_pages, 0.6, 1
                    ),
                    color_scheme=rx.cond(
                        TableState.page_number == TableState.total_pages,
                        "gray",
                        "accent",
                    ),
                    variant="soft",
                ),
                align="center",
                spacing="2",
                justify="end",
            ),
            spacing="5",
            margin_top="1em",
            align="center",
            width="100%",
            justify="end",
        ),
    )

def main_table() -> rx.Component:
    return rx.box(
        rx.flex(
            rx.flex(
                rx.cond(
                    TableState.sort_reverse,
                    rx.icon(
                        "arrow-down-z-a",
                        size=28,
                        stroke_width=1.5,
                        cursor="pointer",
                        flex_shrink="0",
                        on_click=TableState.toggle_sort,
                    ),
                    rx.icon(
                        "arrow-down-a-z",
                        size=28,
                        stroke_width=1.5,
                        cursor="pointer",
                        flex_shrink="0",
                        on_click=TableState.toggle_sort,
                    ),
                ),
                rx.select(
                    [
                        "form_number",
                        "form_name",
                        "entity_type",
                        "locality_type",
                        "locality",
                    ],
                    placeholder="Sort By: Form Number",
                    size="3",
                    on_change=TableState.set_sort_value,
                ),
                rx.input(
                    rx.input.slot(rx.icon("search")),
                    rx.input.slot(
                        rx.icon("x"),
                        justify="end",
                        cursor="pointer",
                        on_click=TableState.setvar("search_value", ""),
                        display=rx.cond(TableState.search_value, "flex", "none"),
                    ),
                    value=TableState.search_value,
                    placeholder="Search forms...",
                    size="3",
                    max_width=["150px", "150px", "200px", "250px"],
                    width="100%",
                    variant="surface",
                    color_scheme="gray",
                    on_change=TableState.set_search_value,
                ),
                align="center",
                justify="end",
                spacing="3",
            ),
            rx.hstack(
                rx.text("Preview Year: "),
                rx.input(
                    type="number",
                    value=TableState.preview_year,
                    on_change=TableState.set_preview_year,
                    width="100px",
                    size="2",
                ),
                rx.button(
                    rx.icon("plus", size=20),
                    "Add Form",
                    size="3",
                    variant="surface",
                    on_click=rx.redirect("/forms/new"),
                ),
                spacing="3",
            ),
            spacing="3",
            justify="between",
            wrap="wrap",
            width="100%",
            padding_bottom="1em",
        ),
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    _header_cell("Form Number", "file-text"),
                    _header_cell("Form Name", "text"),
                    _header_cell("Entity Type", "users"),
                    _header_cell("Locality Type", "map"),
                    _header_cell("Locality", "map-pin"),
                    _header_cell("Due Date", "calendar"),
                    _header_cell("Extension Due Date", "calendar-plus"),
                    _header_cell("Actions", "settings"),
                ),
            ),
            rx.table.body(
                rx.foreach(
                    TableState.get_current_page,
                    lambda item, index: _show_item(item, index),
                )
            ),
            variant="surface",
            size="3",
            width="100%",
        ),
        _pagination_view(),
        delete_modal(),
        width="100%",
    )