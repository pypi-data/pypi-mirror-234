"""Welcome to Dotreact! This file outlines the steps to create a basic app."""
from drconfig import config

import dotreact as dr

docs_url = "https://dotagent.dev/docs/getting-started/introduction"
filename = f"{config.app_name}/{config.app_name}.py"


class State(dr.State):
    """The app state."""

    pass


def index() -> dr.Component:
    return dr.fragment(
        dr.color_mode_button(dr.color_mode_icon(), float="right"),
        dr.vstack(
            dr.heading("Welcome to Dotreact!", font_size="2em"),
            dr.box("Get started by editing ", dr.code(filename, font_size="1em")),
            dr.link(
                "Check out our docs!",
                href=docs_url,
                border="0.1em solid",
                padding="0.5em",
                border_radius="0.5em",
                _hover={
                    "color": dr.color_mode_cond(
                        light="rgb(107,99,246)",
                        dark="rgb(179, 175, 255)",
                    )
                },
            ),
            spacing="1.5em",
            font_size="2em",
            padding_top="10%",
        ),
    )


# Add state and page to the app.
app = dr.App()
app.add_page(index)
app.compile()
