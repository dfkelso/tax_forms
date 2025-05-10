# tax_forms/templates.py
import reflex as rx
from tax_forms.components.sidebar import sidebar

def template(route, title=""):
    """The template for each page of the app."""
    def decorator(component_fn):
        # Create the wrapper function that adds the layout
        def wrapper(*args, **kwargs):
            # Get the content from the component function
            content = component_fn(*args, **kwargs)
            
            # Create the layout with sidebar and content
            return rx.hstack(
                sidebar(),
                rx.box(
                    rx.box(
                        content,
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
        wrapper.__name__ = component_fn.__name__
        wrapper.__qualname__ = component_fn.__qualname__
        wrapper.__module__ = component_fn.__module__
        
        # This is a crucial step: In Reflex, we need to use add_page_to_app directly
        from reflex.app import App
        App.add_page_to_app(wrapper, route=route, title=title)
        
        return component_fn  # Return the original function
    
    return decorator