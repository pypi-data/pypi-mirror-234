import typer

from artorias.commands import create

app = typer.Typer(help="Some utilites")
app.add_typer(create.app)
