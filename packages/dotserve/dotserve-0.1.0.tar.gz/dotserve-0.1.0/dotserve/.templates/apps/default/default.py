"""Welcome to Dotserve! This file outlines the steps to create a basic app."""
from dsconfig import config

import dotserve as ds

docs_url = "https://dotagent.dev/docs/getting-started/introduction"
filename = f"{config.app_name}/{config.app_name}.py"


class State(ds.State):
    """The app state."""

    pass


def index() -> ds.Component:
    return ds.fragment(
        ds.color_mode_button(ds.color_mode_icon(), float="right"),
        ds.vstack(
            ds.heading("Welcome to Dotserve!", font_size="2em"),
            ds.box("Get started by editing ", ds.code(filename, font_size="1em")),
            ds.link(
                "Check out our docs!",
                href=docs_url,
                border="0.1em solid",
                padding="0.5em",
                border_radius="0.5em",
                _hover={
                    "color": ds.color_mode_cond(
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
app = ds.App()
app.add_page(index)
app.compile()
