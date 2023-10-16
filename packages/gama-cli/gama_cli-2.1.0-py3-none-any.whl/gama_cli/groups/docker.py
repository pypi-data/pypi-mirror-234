import click

from gama_cli.helpers import call


@click.group(help="Docker convenience methods")
def docker():
    pass


@click.command(name="clearlogs")
def clearlogs():  # type: ignore
    """Clears all the docker logs"""
    command = 'sudo sh -c "truncate -s 0 /var/lib/docker/containers/*/*-json.log"'
    call(command)
