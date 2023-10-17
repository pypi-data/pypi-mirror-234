"""Constants used in docnext."""

# The extension for Docnext files.
DOCNEXT_EXTENSION = ".md"

# The Docnext app directory.
DOCNEXT_DIR = ".docnext/flexd"
DOCNEXT_FILE = f"{DOCNEXT_DIR}/flexd/flexd.py"
DOCNEXT_MODULES_DIR = "modules"

# Regex for front matter.
FRONT_MATTER_REGEX = r"^---\s*\n(.+?)\n---\s*\n(.*)$"
# Regex for template placeholders.
TEMPLATE_REGEX = r"(?<!\\)(?<!\\\\){(?!\\)(.*?)(?<!\\)}"

# The default app template.
APP_TEMPLATE = """import docnext
import nextpy as xt
component_map = {{
    "a": lambda value, **props: xt.link(value, color="blue", **props),
}}
app = docnext.app(
    '{path}',
    page_template=docnext.templates.base_template,
    component_map=component_map
)
"""
