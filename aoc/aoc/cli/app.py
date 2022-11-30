import typer
from .prep import prep_today

app = typer.Typer()


@app.command()
def prep():
    """
    Prepares for a new day of AOC.
    """
    prep_today()
