import click
from deployplex.commands.env import env
from deployplex.commands.login import login
from deployplex.commands.logout import logout
from deployplex.commands.logs import logs
from deployplex.commands.project import project
from deployplex.config import Config

config = Config()


@click.group()
@click.version_option(None, *("-v", "--version"), package_name="deployplex")
@click.help_option(*("-h", "--help"))
def cli():
    pass


cli.add_command(login)
cli.add_command(logout)
cli.add_command(logs)
cli.add_command(env)
cli.add_command(project)

if __name__ == '__main__':
    cli()
