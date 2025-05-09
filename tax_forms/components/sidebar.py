# tax_forms/components/sidebar.py
import reflex as rx

def sidebar():
    """Sidebar component for navigation."""
    return rx.box(
        rx.vstack(
            rx.heading("Tax Forms", size="3"),  # Changed from "lg" to "3"
            rx.divider(mb=4),
            rx.link(
                rx.hstack(
                    rx.icon("file-text"),
                    rx.text("Forms"),
                    spacing="3",
                ),
                href="/forms",
                width="100%",
                padding="10px",
                border_radius="md",
                _hover={"bg": "rgb(243, 244, 246)"},
                color="black",
                text_decoration="none",
            ),
            rx.link(
                rx.hstack(
                    rx.icon("check-circle"),
                    rx.text("Testing"),
                    spacing="3",
                ),
                href="/testing",
                width="100%",
                padding="10px",
                border_radius="md",
                _hover={"bg": "rgb(243, 244, 246)"},
                color="black",
                text_decoration="none",
            ),
            align_items="flex-start",
            width="100%",
            padding="10px",
        ),
        width="250px",
        height="100vh",
        border_right="1px solid rgb(229, 231, 235)",
        background_color="rgb(249, 250, 251)",
    )