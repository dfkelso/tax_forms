# tax_forms/templates.py
import reflex as rx
from tax_forms.components.sidebar import sidebar

def template(route, title=""):
    """The template for each page of the app."""
    def decorator(component):
        @rx.page(route=route, title=title)
        def wrapper(*args, **kwargs):
            return rx.hstack(
                sidebar(),
                rx.box(
                    rx.box(
                        component(*args, **kwargs),
                        padding="20px",
                        width="100%",
                    ),
                    width="100%",
                    height="100vh",
                    overflow="auto",
                ),
                height="100vh",
                width="100%",
                spacing="0",  # Remove spacing between sidebar and content
            )
        
        return wrapper
    
    return decorator