#!/usr/bin/env python

import os
import sys
from subprocess import Popen
import click

def getWSRoot():
    return os.path.expandvars('$ROS_WORKSPACE')

def getPkgRoot(filename):
    pkg_name = getPkgName(filename)
    if not pkg_name:
        return ''
    try:
        from rospkg import RosPack
    except ImportError:
        return ''
    try:
        p = RosPack()
        path = p.get_path(pkg_name)
        return path
    except ResourceNotFound:
        return ''

def getGitRoot(filename):
    try:
        import git
    except ImportError:
        return ''
    try:
        r = git.Repo(filename, search_parent_directories=True)
    except git.exc.InvalidGitRepositoryError:
        return ''
    return r.working_dir

def getPkgName(filename):
    try:
        import rospkg
    except ImportError:
        return ''
    return rospkg.get_package_name(filename)


def getCompileDB(filename):
    pkg_name = getPkgName(filename)
    if not pkg_name:
        return ''
    dir = getWSRoot() + os.path.sep + 'build' + os.path.sep + pkg_name
    return dir

def getConfigFile(candidates, verbose = False):
    for candidate in candidates:
        if not candidate:
            continue
        try:
            with open(candidate + os.path.sep + '.clang-tidy') as f:
                config_yaml = f.read()
                if config_yaml:
                    print("Using .clang-tidy in {}".format(candidate))
                    return config_yaml
        except IOError:
            if verbose: print("Couldn't read .clang-tidy in {}".format(candidate))
    return ''


def getConfig(candidates, verbose = False):
    config_yaml = getConfigFile(candidates, verbose)
    if not config_yaml:
        print("No config file found, running checks with default config and formatting options!")
        return'--checks=clang-diagnostic-*,clang-analyzer-*,*,-abseil*,-fuchsia*,-android*,-zircon*,-hicpp*,-objc*,-readability-braces-around-statements,-google-readability-braces-around-statements,-google-readability-todo,-readability-uppercase-literal-suffix'
    return '-config={}'.format(config_yaml)

def runClangTidy(filename, fix = False, dry_run = False):
    cmd = ['clang-tidy-8']
    cd = getCompileDB(filename)
    if cd:
        cmd += ['-p={}'.format(cd)]
    else:
        print("No compile database found, checks might not work correctly!")
    candidates = ['.', getPkgRoot(filename), getGitRoot(filename), getWSRoot()]
    cmd += [getConfig(candidates, dry_run)]
    if fix:
        cmd += ['--fix']
    cmd += [filename]
    if dry_run:
        print(" ".join(cmd))
    else:
        s = Popen(cmd)
        s.wait()

@click.command()
@click.option('--fix', default=False, is_flag=True, help='apply fixits')
@click.option('--dry-run', default=False, is_flag=True, help='don\'t run, show commands and configs only')
@click.argument('files', nargs=-1, required=True, type=click.Path(exists=True, file_okay=True, dir_okay=False,readable=True))
def main(fix, dry_run, files = None):
    if not files:
        print("Need at least one file!")
        sys.exit(1)
    for f in files:
        print(">>>> {}".format(f))
        runClangTidy(f, fix, dry_run)

if __name__ == '__main__':
    main()
