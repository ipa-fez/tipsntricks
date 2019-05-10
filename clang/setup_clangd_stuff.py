#!/usr/bin/env python

from subprocess import Popen
import os.path
from catkin_tools.context import Context
from catkin_pkg.packages import find_packages
import click

def setup_workspace(workspace):
    ctx = Context.load(workspace_hint=workspace, load_env=False)
    if not ctx.source_space_exists():
        print("Source space doesn't exist at {}".format(ctx.source_space_abs))
        return
    for path, package in find_packages(ctx.source_space_abs).items():
        Popen(['ln', '-s', '{}{}{}{}compile_commands.json'.format(ctx.build_space_abs, os.path.sep, package.name, os.path.sep), '{}{}{}'.format(ctx.source_space_abs, os.path.sep, path)])

@click.command()
@click.argument('workspace', nargs=1, required=False, type=click.Path(exists=True, file_okay=False, dir_okay=True, readable=True))
def main(workspace = None):
    setup_workspace(workspace)

if __name__ == '__main__':
    main()
