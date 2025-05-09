# tax_forms/tax_forms.py
import reflex as rx

# Import styles
from . import styles

# Import pages explicitly to ensure they're registered
from .pages import home
from .pages.forms import list, edit
from .pages.testing import index

# Create the app instance
app = rx.App(
    style=styles.base_style,
    stylesheets=styles.base_stylesheets,
)