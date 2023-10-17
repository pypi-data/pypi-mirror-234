import nextpy as xt


def base_template(content: xt.Component) -> xt.Component:
    return xt.container(
        content,
        margin_y="5em",
    )
