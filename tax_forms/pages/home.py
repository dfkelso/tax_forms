import reflex as rx
from tax_forms.templates import template

@template(route="/", title="Home")
def home():
    return rx.redirect("/forms")