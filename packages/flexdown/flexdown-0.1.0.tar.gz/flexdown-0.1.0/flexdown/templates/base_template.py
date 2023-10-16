import reflex as rx


def base_template(content: rx.Component) -> rx.Component:
    return rx.container(
        content,
        margin_y="5em",
    )
