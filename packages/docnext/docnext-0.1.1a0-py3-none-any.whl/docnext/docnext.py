"""The main docnext module."""
from typing import Callable

import nextpy as xt

from docnext import errors, utils, types
from docnext.blocks import block, Block, MarkdownBlock, CodeBlock, ExecBlock, EvalBlock
from docnext.document import Document

component_map = {
    "code": lambda source: xt.code(source, color="#1F1944", bg="#EAE4FD"),
}


class Docnext(xt.Base):
    """Class to parse and render docnext files."""

    # The list of accepted block types to parse.
    blocks: list[type[Block]] = [
        ExecBlock,
        EvalBlock,
        CodeBlock,
        MarkdownBlock,
    ]

    # The default block type.
    default_block_type: type[Block] = MarkdownBlock

    # List of processors to apply to blocks before rendering.
    block_processors: list[block.BlockProcessor] = [
        ExecBlock.process_blocks,
    ]

    # The template to use when rendering pages.
    page_template: Callable[[xt.Component], xt.Component] = xt.fragment

    # Mapping from markdown tag to a rendering function for Nextpy components.
    component_map: types.ComponentMap = component_map

    def _get_block(self, line: str, line_number: int) -> Block:
        """Get the block type for a line of text.

        Args:
            line: The line of text to check.
            line_number: The line number of the line.

        Returns:
            The block type for the line of text.
        """
        # Search for a block type that can parse the line.
        for block_type in self.blocks:

            # Try to create a block from the line.
            block = block_type.from_line(line, line_number=line_number)

            # If a block was created, then return it.
            if block is not None:
                return block

        # If no block was created, then return the default block type.
        return self.default_block_type().append(line)

    def get_blocks(self, source: str) -> list[Block]:
        """Parse a Docnext file into blocks.

        Args:
            source: The source code of the Docnext file.

        Returns:
            The list of blocks in the Docnext file.
        """
        # The list of parsed blocks.
        blocks: list[Block] = []
        current_block = None

        # Iterate over each line in the source code.
        for line_number, line in enumerate(source.splitlines()):

            # If there is no current block, then create a new block.
            if current_block is None:
                # If the line is empty, then skip it.
                if line == "":
                    continue

                # Otherwise, create a new block.
                current_block = self._get_block(line, line_number)

            else:
                # Add the line to the current block.
                current_block.append(line)

            # Check if the current block is finished.
            if current_block.is_finished():
                blocks.append(current_block)
                current_block = None

        # Add the final block if it exists.
        if current_block is not None:
            blocks.append(current_block)

        # Return the list of blocks.
        return blocks

    def process_blocks(self, blocks: list[Block], env: types.Env) -> list[Block]:
        """Process a list of blocks to execute any side effects.

        Args:
            blocks: The list of blocks to process.
            env: The environment variables to use for processing.

        Returns:
            The list of processed blocks.
        """
        for processor in self.block_processors:
            processor(blocks, env)

    def render(self, source: str | Document) -> xt.Component:
        """Render a Docnext file into a Nextpy component.

        Args:
            source: The source code of the Docnext file.

        Returns:
            The Nextpy component representing the Docnext file.
        """
        # Convert the source to a document.
        if isinstance(source, str):
            source = Document.from_source(source)

        # The environment used for execing and evaling code.
        env: types.Env = source.metadata

        # Get the content of the document.
        source = source.content

        # Get the blocks in the source code.
        blocks = self.get_blocks(source)
        self.process_blocks(blocks, env)

        # Render each block.
        out: list[xt.Component] = []
        for block in blocks:
            try:
                out.append(block.render(env=env, component_map=self.component_map))
            except Exception as e:
                raise errors.RenderError(
                    f"Error while rendering block {block.type} on line {block.start_line_number}. "
                    f"\n{block.get_content(env)}"
                ) from e

        # Wrap the output in the page template.
        return self.page_template(xt.fragment(*out))

    def render_file(self, path: str) -> xt.Component:
        """Render a Docnext file into a Nextpy component.

        Args:
            path: The path to the Docnext file.

        Returns:
            The Nextpy component representing the Docnext file.
        """
        # Render the source code.
        return self.render(Document.from_file(path))

    def create_app(self, path: str) -> xt.App:
        """Create a Nextpy app from a directory of Docnext files.

        Args:
            path: The path to the directory of Docnext files.

        Returns:
            The Nextpy app representing the directory of Docnext files.
        """
        # Get all the docnext files in the directory.
        files = utils.get_docnext_files(path)

        # Create the Nextpy app.
        app = xt.App()

        # Create a base state.
        class State(xt.State):
            pass

        # Add each page to the app.
        for file in files:
            route = file.replace(path, "").replace(".md", "")
            app.add_page(self.render_file(file), route=route)

        # Compile the app.
        app.compile()

        # Return the app.
        return app
