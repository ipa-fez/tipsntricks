from __future__ import print_function
import sys
import os

from catkin_tools.argument_parsing import add_context_args
from catkin_tools.metadata import find_enclosing_workspace
from catkin_tools.context import Context
from catkin_pkg.packages import find_packages
from subprocess import Popen

def runClangTidy(clang_binary, pkg_root, filenames, cfg, compile_db, fix = False, dry_run = False):
    cmd = [clang_binary]
    cmd += ['-p={}'.format(compile_db)]
    #cmd += ['-config={}'.format(cfg)]
    if fix:
        cmd += ['--fix']
    cmd += filenames
    if dry_run:
        print(" ".join(cmd))
    else:
        s = Popen(cmd, cwd=pkg_root)
        s.wait()

def prepare_arguments(parser):
    add_context_args(parser)
    clang_binary = parser.add_argument
    clang_binary('-c', '--clang-tidy', nargs="?", default="clang-tidy-8", help="Name of clang-tidy binary, e.g. 'clang-tidy-8'")
    fix = parser.add_argument
    fix('-f', '--fix', action='store_true', default=False, help="Apply fixes")
    pkg = parser.add_argument
    pkg('package', help="Package to run for")
    src = parser.add_argument
    src('src_file', nargs='+', help="Source files to run for")
    return parser

def main(opts):
    opts = sys.argv[1:] if opts is None else opts
    print(opts)

    workspace = os.getcwd() if opts.workspace is None else opts.workspace
    workspace = find_enclosing_workspace(workspace)

    if not workspace:
        print("No workspace found")
        sys.exit(1)

    ctx = Context.load(workspace, opts.profile, opts, load_env=False)
    packages = find_packages(ctx.source_space_abs)
    pkg_path = [pkg_path for pkg_path, p in packages.items() if p.name == opts.package]
    pkg_path = None if not pkg_path else pkg_path[0]
    if not pkg_path:
        print("Package '{}' not found!".format(opts.package))
        sys.exit(2)

    pkg_name = packages[pkg_path].name
    build_space = ctx.build_space_abs + os.path.sep + pkg_name
    compile_db = build_space + os.path.sep + "compile_commands.json"
    if not os.path.isfile(compile_db):
        print("No compile_commands.json in {}".format(build_space))
        sys.exit(3)

    runClangTidy(clang_binary=opts.clang_tidy, pkg_root=ctx.source_space_abs + os.path.sep + pkg_path, filenames=opts.src_file, cfg=None, compile_db=build_space, fix=opts.fix, dry_run = False)
    return 0

description = dict(
        verb='tidy',
        description='Runs clang-tidy on a file',
        main=main,
        prepare_arguments=prepare_arguments,
        )
