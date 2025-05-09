# tax_forms/styles.py
import reflex as rx

border_radius = "0.375rem"
accent_color = "rgb(107, 99, 246)"
accent_dark = "rgb(86, 77, 242)"

base_style = {
    "font_family": "Inter, -apple-system, BlinkMacSystemFont, sans-serif",
    "background_color": "white",
    "color": "black",
    rx.heading: {
        "font_weight": "600",
    },
    rx.button: {
        "border_radius": border_radius,
        "_hover": {
            "opacity": 0.8,
        },
    },
    rx.link: {
        "text_decoration": "none",
        "_hover": {
            "text_decoration": "underline",
        },
    },
    rx.card: {
        "border_radius": border_radius,
        "padding": "1rem",
        "shadow": "md",
        "border": "1px solid rgb(230, 230, 230)",  # Using direct RGB instead of rx.color
    },
}

base_stylesheets = [
    "https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;600;700;800;900&display=swap",
]