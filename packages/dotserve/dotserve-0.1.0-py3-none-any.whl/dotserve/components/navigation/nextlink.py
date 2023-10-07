"""A link component."""

from dotserve.components.component import Component
from dotserve.vars import Var


class NextLink(Component):
    """Links are accessible elements used primarily for navigation. This component is styled to resemble a hyperlink and semantically renders an <a>."""

    library = "next/link"

    tag = "NextLink"

    is_default = True

    # The page to link to.
    href: Var[str]

    # Whether to pass the href prop to the child.
    pass_href: Var[bool] = True  # type: ignore
