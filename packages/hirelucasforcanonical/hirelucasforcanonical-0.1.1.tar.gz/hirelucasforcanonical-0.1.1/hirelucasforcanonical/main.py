import typer


app = typer.Typer()


@app.callback()
def callback():
    """
    Interview with canonical
    """


@app.command()
def why_hire():
    """
    Why should we hire you?
    """
    typer.echo("Because I'm a very good developer and learn fast!")


@app.command()
def when_start():
    """
    when could you start?
    """
    typer.echo("I would like to start around february, if possible!")
