# tax_forms/pages/home.py
import reflex as rx

def home_content():
    """The home page content."""
    return rx.vstack(
        rx.heading("Tax Forms Calculator", size="lg"),
        rx.text("Welcome to the Tax Forms Calculator application."),
        rx.hstack(
            rx.button("View Forms", on_click=rx.navigate("/forms")),
            rx.button("Test Due Dates", on_click=rx.navigate("/testing")),
            spacing="4",
        ),
        width="100%",
        spacing="6",
        align_items="center",
        justify_content="center",
    )