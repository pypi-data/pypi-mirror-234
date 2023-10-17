# Please note that the following line, has security checks disabled.
# The security check is disabled, because I read the security guides
# on this topic, so im pretty confident it is suitable for production.
import subprocess  # nosec
import typing
from importlib.metadata import version as get_version
from pathlib import Path

import typer
from slugify import slugify as awslugify
from toolcat import project

package_name = "groundsupport"
app = typer.Typer(add_completion=False, help=project.summary(package_name))


@app.command()
def slugify(
    text: str = typer.Argument(..., help="The string to slugify, between commas."),
):
    """
    Slugifies a string to lower case by default.
    """
    print(f"\n\t{awslugify(text, to_lower=True)}")


@app.command()
def version():
    """
    Shows the current version.
    """
    typer.echo(get_version(package_name))


projects_app = typer.Typer()
app.add_typer(projects_app, name="projects", help="Project management commands.")


@projects_app.command(
    help="Cleans all projects found in the specified path, acconrding to the project Makefile."
)
def clean(path: str = typer.Argument(".", help="The path to the projects.")):
    """
    Run clean executes 'make clean' in all subdirectories from the execution
    of the command.
    """

    for path in Path(path).glob("*/Makefile"):
        typer.echo(f"Running make clean in {path.parent}")
        _run_command(["make", "-C", path.parent, "clean"])


def _run_command(cmd: typing.List) -> subprocess.CompletedProcess:
    # Please note that the following line, has security checks disabled.
    # The security check is disabled, because I read the security guides
    # on this topic, so im pretty confident it is suitable for production.
    # If you wish to change this, please run the security check again.
    # Some security tips:
    #   - https://security.openstack.org/guidelines/dg_use-subprocess-securely.html
    #   - https://security.openstack.org/guidelines/dg_avoid-shell-true.html
    #   - https://docs.python.org/3.9/library/subprocess.html#security-considerations
    completed_process = subprocess.run(
        cmd, capture_output=True, text=True, check=True
    )  # nosec
    return completed_process


if __name__ == "__main__":
    app()
