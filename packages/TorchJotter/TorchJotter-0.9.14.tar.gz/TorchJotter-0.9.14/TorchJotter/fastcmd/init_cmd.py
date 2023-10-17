"""
Usage:
    TorchJotter init [<name>] [--hide] [--with-git]
    TorchJotter -h | --help

Arguments:
    name                    Name of the TorchJotter project

Options:
    -h --help               This is a command to initialize a TorchJotter project
    --hide                  Hide .fitconfig inside .TorchJotter folder
    --with-git              Initialize TorchJotter with a standard git

Examples:
    TorchJotter init project     Create a your project named project
    TorchJotter init             Init the current directory with TorchJotter
"""
from docopt import docopt
from TorchJotter.fastgit import committer


def init_cmd(argv=None):
    args = docopt(__doc__, argv=argv)

    name = args['<name>'] if args['<name>'] else '.'
    committer.init_project(name, hide=args["--hide"], git=args["--with-git"])
