
import click
import terrascope.cli.lib.workflow as wf
import terrascope.cli.lib.utils as tsu
from terrascope.cli.lib.aliased_group import AliasedGroup


@click.command(cls=AliasedGroup, help="'environment' command group")
@click.pass_context
def environment(ctx):
    pass


@environment.command('check')
@click.pass_context
def env_check(ctx):

    is_complete = wf.check_environment_complete(raise_on_failure=False, print_missing=True)
    knot = ''
    if is_complete:
        fg = 'green'
    else:
        fg = 'red'
        knot = 'NOT '
    click.secho(f"Environment is {knot}complete", fg=fg)
