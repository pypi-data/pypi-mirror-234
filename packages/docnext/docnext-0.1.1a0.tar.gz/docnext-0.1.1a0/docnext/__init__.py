import nextpy as xt

from . import templates
from .docnext import Docnext
from .document import Document


# The default Docnext instance.
docnext = Docnext()


def parse(source) -> Document:
    """Parse a Docnext document.

    Args:
        source: The source code of the Docnext document.

    Returns:
        The parsed Docnext document.
    """
    return Document.from_source(source)


def parse_file(path: str) -> Document:
    """Parse a Docnext file.

    Args:
        path: The path to the Docnext file.

    Returns:
        The parsed Docnext document.
    """
    return Document.from_file(path)


def render(source: str, **kwargs) -> xt.Component:
    """Render Docnext source code into a Nextpy component.

    Args:
        source: The source code of the Docnext file.
        **kwargs: The keyword arguments to pass to the Docnext constructor.

    Returns:
        The Nextpy component representing the Docnext file.
    """
    return Docnext(**kwargs).render(source)


def render_file(path: str, **kwargs) -> xt.Component:
    """Render a Docnext file into a Nextpy component.

    Args:
        path: The path to the Docnext file.
        **kwargs: The keyword arguments to pass to the Docnext constructor.

    Returns:
        The Nextpy component representing the Docnext file.
    """
    return Docnext(**kwargs).render_file(path)


def app(path: str, **kwargs) -> xt.App:
    """Create a Nextpy app from a directory of Docnext files.

    Args:
        path: The path to the directory of Docnext files.
        **kwargs: The keyword arguments to pass to the Docnext constructor.

    Returns:
        The Nextpy app representing the directory of Docnext files.
    """

    class State(xt.State):
        pass

    return Docnext(**kwargs).create_app(path)
