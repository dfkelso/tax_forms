# tax_forms/tax_forms.py
import reflex as rx
from tax_forms import styles

# Create the app
app = rx.App(
    style=styles.base_style,
    stylesheets=styles.base_stylesheets,
)

# Define a basic home page directly
@app.add_page(route="/", title="Home")
def home():
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