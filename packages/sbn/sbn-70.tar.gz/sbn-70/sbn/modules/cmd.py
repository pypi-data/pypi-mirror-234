# This file is placed in the Public Domain.
#
# pylint: disable=C0116,E0402


"list of commands"


from ..handler import Handler


def cmd(event):
    event.reply(",".join(sorted(Handler.cmds)))
