# tax_forms/pages/home.py
import reflex as rx
from tax_forms.templates import template

@template(route="/", title="Tax Forms")
def home():
    """Home page that redirects to forms."""
    return rx.redirect("/forms")