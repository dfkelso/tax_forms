import reflex as rx
from tax_forms.components.sidebar import sidebar

def template(route, title=""):
    """The template for each page of the app."""
    def decorator(component):
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
            )
        
        # Add the page to the app
        rx.App.add_page(
            wrapper,
            route=route,
            title=title,
        )
        
        return wrapper
    
    return decorator