"""Types for Docnext.""" ""
from typing import Any, Callable

import nextpy as xt

# An environment for executing and evaluating code.
Env = dict[str, Any]

# The frontmatter of a Docnext document.
Frontmatter = dict[str, Any]

# Mapping from markdown tag to a rendering function for Nextpy components.
ComponentMap = dict[str, Callable[[str], xt.Component]]
