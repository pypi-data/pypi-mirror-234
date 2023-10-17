import nextpy as xt

from docnext import types
from docnext.blocks.block import Block


class EvalBlock(Block):
    """A block that evaluates a Nextpy component to display."""

    type = "eval"
    starting_indicator = "```python eval"
    ending_indicator = "```"

    def render(self, env: types.Env, **_) -> xt.Component:
        return eval(self.get_content(env), env, env)
