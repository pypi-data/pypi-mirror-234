import nextpy as xt

from docnext import types
from docnext.blocks.markdown_block import MarkdownBlock


class CodeBlock(MarkdownBlock):
    """A block of code."""

    type = "code"
    starting_indicator = "```"
    ending_indicator = "```"
    include_indicators = True
