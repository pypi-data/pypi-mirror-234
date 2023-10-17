"""
Usage:
    TorchJotter <command> [<args>...]
    TorchJotter help <command>
    TorchJotter -h | --help
    TorchJotter --version

Supported commands
    init            Initialize a TorchJotter project
    list            List committed versions
    revert          Revert to a specific version
    log             Visualize logs by a server
    
See "TorchJotter help <command>" for more information on a specific command
"""
import sys
from docopt import docopt
from TorchJotter.fastcmd.init_cmd import init_cmd
from TorchJotter.fastcmd.list_cmd import list_cmd
from TorchJotter.fastcmd.revert_cmd import revert_cmd
from TorchJotter.fastcmd.log_cmd import log_cmd
from TorchJotter import __version__ as version

cmd_map = {
    "init": init_cmd,
    "list": list_cmd,
    "revert": revert_cmd,
    "log": log_cmd
}


def main_cmd():
    argv = sys.argv[1:2] if len(sys.argv) > 2 else sys.argv[1:]
    args = docopt(__doc__, version='TorchJotter ' + version, argv=argv)
    argv = sys.argv[1:]

    cmd = args['<command>']
    if cmd in ['help', None]:
        if len(argv) > 1:
            if argv[1] in cmd_map:
                cmd_map[argv[1]](['-h'])
            else:
                print("Unknown command `{}`, only support {}.".format(argv[1], list(cmd_map.keys())))
                print(__doc__)
        else:
            print("You have to specify a command, support {}.".format(list(cmd_map.keys())))
            print(__doc__)
    elif cmd in cmd_map:
        cmd_map[cmd](argv)
    else:
        print("Unknown command: {}.".format(cmd))
        print(__doc__)
