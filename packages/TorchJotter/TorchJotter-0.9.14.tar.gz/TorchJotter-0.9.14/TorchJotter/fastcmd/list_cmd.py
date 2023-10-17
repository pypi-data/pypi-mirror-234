"""
Usage:
    TorchJotter list [<num>] [--show-now]
    TorchJotter -h | --help

Arguments:
    num                     The number of recent commits you want to list

Options:
    -h --help               This is a command to list committed versions
    --show-now              Show the current version

Examples:
    TorchJotter list 10          List recent 10 commits
    TorchJotter list --show-now  List all commits with the current one marked
"""
from docopt import docopt
from TorchJotter.fastgit import committer


def list_cmd(argv=None):
    args = docopt(__doc__, argv=argv)

    committer.short_logs(args["--show-now"], args["<num>"])
