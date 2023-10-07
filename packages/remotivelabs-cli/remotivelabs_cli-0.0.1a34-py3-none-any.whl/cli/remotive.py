import typer
import base64
from .broker.brokers import app as broker_app
from .cloud.cloud_cli import app as cloud_app
from rich import print
import pkg_resources

app = typer.Typer(rich_markup_mode="rich", help="""
Welcome to RemotiveLabs CLI - Simplify and automate tasks for cloud resources and brokers

For documentation - https://docs.remotivelabs.com
""")


def version_callback(value: bool):
    if value:
        my_version = pkg_resources.get_distribution('remotivelabs-cli')
        typer.echo(my_version)
        raise typer.Exit()


def test_callback(value: int):
    if value:
        print(value)
        raise typer.Exit()
    # if value:
    #    typer.echo(f"Awesome CLI Version: 0.0.22a")
    #    raise typer.Exit()


@app.callback()
def main(
        version: bool = typer.Option(None, callback=version_callback, is_eager=False, help="Print current version"),
):
    # Do other global stuff, handle other global options here
    # print(f"version {version}")
    return


app.add_typer(broker_app, name="broker", help="Manage a single broker - local or cloud")
app.add_typer(cloud_app, name="cloud", help="Manage resources in RemotiveCloud", )
