import os
from subprocess import PIPE, Popen


def cmd(cmd, shell=True):
    """Execute command @cmd and return output using Popen()."""
    print(cmd)
    os.chdir('../exe')
    process = Popen(
        args=cmd,
        stdout=PIPE,
        shell=shell
    )
    return process.communicate()[0].decode("ISO-8859-1")