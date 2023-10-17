"""The Docnext CLI.""" ""
import os

from nextpy.nextpy import typer
from nextpy.utils.processes import new_process

from docnext import constants


# The command line app.
app = typer.Typer()


@app.command()
def run(path: str):
    # Create a .docnext directory in the current directory.
    os.makedirs(constants.DOCNEXT_DIR, exist_ok=True)

    # Create a nextpy project.
    new_process(
        ["nextpy", "init"], cwd=constants.DOCNEXT_DIR, show_logs=True, run=True
    )

    # Replace the app file with a template.
    with open(constants.DOCNEXT_FILE, "w") as f:
        f.write(constants.APP_TEMPLATE.format(path=f"../../{path}"))

    # Run the nextpy project.
    new_process(["nextpy", "run"], cwd=constants.DOCNEXT_DIR, show_logs=True, run=True)
