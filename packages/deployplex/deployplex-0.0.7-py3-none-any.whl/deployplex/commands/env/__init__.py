import click
from deployplex.commands.env.set import set
from deployplex.commands.env.list import list


@click.group("env", help="Environment variables commands")
def env():
    pass


env.add_command(set)
env.add_command(list)
