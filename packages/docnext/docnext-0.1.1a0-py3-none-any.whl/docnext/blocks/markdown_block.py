import nextpy as xt

from docnext import types, utils
from docnext.blocks.block import Block


class MarkdownBlock(Block):
    """A block of Markdown."""

    type = "markdown"
    line_transforms = [
        utils.evaluate_templates,
    ]

    def render(self, env: types.Env, component_map: types.ComponentMap) -> xt.Component:
        return xt.markdown(self.get_content(env), component_map=component_map)
