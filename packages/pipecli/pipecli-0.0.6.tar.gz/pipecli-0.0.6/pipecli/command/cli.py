#!/usr/bin/env python
# encoding: utf-8
import click
import os
import sys
from pipecli.command.beiguo import find_container

__version__ = "0.1"
pgk_dir = os.path.join(os.path.dirname(os.path.abspath('__file__')))


# 主组命令 CSP
# 在setup的entry_points字段中指定
@click.group(context_settings={'help_option_names': ['-h', '--help']}, invoke_without_command=True)
@click.version_option('{0} from {1} (Python {2})'.format(__version__, pgk_dir, sys.version[:3]))
def pipecli():
    """
    PIPE Command line tools
    """ 
 
@pipecli.command()
@click.option("-p","--pid", type=click.STRING, required=True, default=None) 
def docker(pid):
    """
    docker tools 
    """
    print("query container with pid: {}".format(pid))
    find_container(pid)

if __name__ == '__main__':
    pipecli()



